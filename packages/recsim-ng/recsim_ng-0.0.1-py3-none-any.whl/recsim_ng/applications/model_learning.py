# coding=utf-8
# Copyright 2021 The RecSim Authors.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Lint as: python3
"""Tests for recsim_ng.stories.recs.interest_evolution_simulation."""
import edward2 as ed
from gym import spaces
import numpy as np
from recsim_ng.core import network as network_lib
from recsim_ng.core import value
from recsim_ng.core import variable
from recsim_ng.lib import util
from recsim_ng.lib import log_probability

from recsim_ng.entities import choice_models as choice_lib
from recsim_ng.entities import state_models as state_lib
from recsim_ng.entities import utility_models as utility_lib
from recsim_ng.entities.recs import clustered_user
import tensorflow.compat.v2 as tf

Variable = variable.Variable
ValueDef = variable.ValueDef
Value = value.Value
ValueSpec = value.ValueSpec
Space = value.Space


def make_config(num_users=2000, num_creator_clusters=40):
  """Returns a network for the viable creator simulation."""
  # TODO(cwhsu): Pass more common parameters.
  creator_disp = 64.0
  creator_fan_out = 2
  num_topics = 3
  num_creators = creator_fan_out * num_creator_clusters
  num_docs = num_creators * 5
  creator_means = clustered_user.init_random_creator_clusters(
      creator_disp, creator_fan_out, num_creator_clusters, num_topics)
  config = {
      # Common parameters
      'num_topics': num_topics,
      'num_features': num_topics,
      'num_users': num_users,
      'num_docs': num_docs,
      'slate_size': 4,
      'num_creators': num_creators,
      'creator_means': creator_means,
  }
  return config


def simple_recs_story(user_ctor, recommender_ctor, config):
  ########
  # INIT #
  ########
  user = user_ctor(config)
  recommender = recommender_ctor(config)

  user_response = Variable(name='user response', spec=user.response_spec)
  user_state = Variable(name='user state', spec=user.state_spec)
  slate_docs = Variable(name='slate docs', spec=recommender.slate_docs_spec)

  # 0. Initial state.

  user_state.initial_value = variable.value(user.initial_state)
  slate_docs.initial_value = variable.value(recommender.slate_docs)
  user_response.initial_value = variable.value(user.response,
                                               (user_state, slate_docs))

  user_state.value = variable.value(
      user.next_state,
      (user_state.previous, user_response.previous, slate_docs.previous))
  slate_docs.value = variable.value(recommender.slate_docs)
  user_response.value = variable.value(user.response, (user_state, slate_docs))

  return [
      slate_docs,
      user_state,
      user_response,
  ]


class SimpleNormalRecommender(tf.Module):

  def __init__(self, normal_loc, normal_scale):
    self._normal_loc = normal_loc
    self._normal_scale = normal_scale
    self.slate_docs_spec = self._specs()

  def slate_docs(self):
    slate_doc_features = ed.Normal(
        loc=self._normal_loc, scale=self._normal_scale)
    return Value(features=slate_doc_features)

  def _specs(self):
    output_bcast = self._normal_loc + self._normal_scale
    output_shape = tf.shape(output_bcast)
    return ValueSpec(
        features=Space(
            spaces.Box(low=-np.Inf, high=np.Inf, shape=output_shape)))


class ModelLearningDemoUser(tf.Module):
  """User model with embedding target intent, satisfaction, and curiosity.

  This entity models a user which interacts with a recommender system by
  repeatedly selecting items among slates of items. The user's action
  space consists of:
    * selecting one of k presented items for consumption
    * selecting one of k presented items for exploration
    * terminating the session.
  The user's state consists of:
    * a curiosity parameter c
    * an intent realized by a target item
    * a dynamic satisfaction s, which reflects the user's impression of whether
      the recommender makes progress towards the target
    * an acceptance threshold t.
  The user's choice process proceeds as follows:
    1. the user tries to select a document for consumption, using the item
       utilities as logits. The possibility of not consuming is also added with
       logit equal to t. If a document is selected for consumption, the session
       ends.
    2. Users who do not pick an item for consumption decide whether to explore
       further. The exploration decision is made with probability sigmoid(c * s)
       that is, more satisfied users are likely to explore further.
    3. If the user decides to explore, a document from the slate is selected for
       exploration, this time without the no-choice option. Otherwise the
       session terminates.
  The user state updates as follows:
    * if the decision to end the session has been made during the choice
      process, all state variables are redrawn from their initial distributions.
    * The target, threshold, and curiosity remain fixed over time.
    * The satisfaction s evolves as:
                        s_t = 0.8 * s_{t-1} + delta_t + eps,
      where delta_t is difference between the maximum utility of the items from
      the t-slate and that of the (t-1)-slate, and eps is zero-mean Gaussian
      noise with std=0.3.
  TODO(mmladenov): get rid of the 0.8 magic number.
  """

  def __init__(self, intent_ctor, config, satisfaction_sensitivity=None):

    self._num_users = config.get('num_users')
    self._slate_size = config.get('slate_size')
    self._num_clusters = config.get('num_clusters')
    self._num_features = config.get('num_features')
    if satisfaction_sensitivity is None:
      self._sat_sensitivity = 0.8 * tf.ones(self._num_users)
    else:
      self._sat_sensitivity = satisfaction_sensitivity
    self._intent_model = intent_ctor(config)
    self._choice_model = choice_lib.MultinormialLogitChoiceModel(
        self._num_users, -np.Inf * tf.ones(self._num_users))
    self._affinity_model = utility_lib.TargetPointSimilarity((self._num_users,),
                                                             self._slate_size)
    self.response_spec, self.state_spec = self._specs()

  def initial_state(self):
    intent = self._intent_model.initial_state()
    state = Value(
        satisfaction=ed.Deterministic(loc=5.0 * tf.ones(self._num_users)),
        intent=intent.as_dict['state'],
        max_slate_utility=ed.Deterministic(loc=tf.zeros(self._num_users)))
    return state

  def next_state(self, old_state, choice, slate):
    # compute the improvement of slate scores
    slate_doc_features = slate.as_dict['features']
    slate_doc_affinities = self._affinity_model.utilities(
        old_state.as_dict['intent'], slate_doc_features)
    max_slate_utility = tf.reduce_max(slate_doc_affinities, axis=-1)
    improvement = (max_slate_utility - old_state.as_dict['max_slate_utility'])
    next_satisfaction = self._sat_sensitivity * old_state.as_dict[
        'satisfaction'] + improvement
    return Value(
        satisfaction=ed.Deterministic(next_satisfaction),
        intent=self._intent_model.next_state(
            Value(state=old_state.as_dict['intent'])).as_dict['state'],
        max_slate_utility=ed.Deterministic(max_slate_utility))

  def response(self, state, slate):
    slate_doc_features = slate.as_dict['features']
    slate_doc_scores = self._affinity_model.utilities(state.as_dict['intent'],
                                                      slate_doc_features)
    adjusted_scores = (
        slate_doc_scores +
        tf.expand_dims(state.as_dict['satisfaction'], axis=-1))
    doc_choice = self._choice_model.choice(adjusted_scores)

    return Value(doc_choice=doc_choice)

  def _specs(self):
    # TODO(mmladenov): make this more elegant
    state_spec = ValueSpec(
        intent=Space(
            spaces.Box(
                low=-np.Inf,
                high=np.Inf,
                shape=(self._num_users, self._num_features))),
        satisfaction=Space(
            spaces.Box(low=-np.Inf, high=np.Inf, shape=(self._num_users,))),
        max_slate_utility=Space(
            spaces.Box(low=-np.Inf, high=np.Inf, shape=(self._num_users,))))
    response_spec = ValueSpec(
        doc_choice=Space(
            spaces.MultiDiscrete([self._slate_size] * self._num_users)),)
    return response_spec, state_spec

  def observation(self, _):
    pass


sim_config = make_config(5, 2)
gmm_parameters = {
    'component_means': np.eye(3),
    'component_covariances': 0.1 * np.stack((np.eye(3), np.eye(3), np.eye(3))),
    'component_logits': np.zeros((5, 3))
}
gmm_parameters = {
    k: tf.constant(v, dtype=tf.float32) for k, v in gmm_parameters.items()
}
trainable_user_generator = lambda _: state_lib.GMMStaticPoint(gmm_parameters)
usr = ModelLearningDemoUser(trainable_user_generator, sim_config)
in_state = usr.initial_state()
print(in_state)
recs_agent = SimpleNormalRecommender(tf.zeros((5, 4, 3), dtype=tf.float32), 0.5)
recs = recs_agent.slate_docs()
print(recs)
usr_choice = usr.response(in_state, recs)
print(usr_choice)
nxt_state = usr.next_state(in_state, usr_choice, recs)
print(nxt_state)
variables = simple_recs_story(
    lambda config: ModelLearningDemoUser(trainable_user_generator, config),
    lambda _: SimpleNormalRecommender(
        tf.zeros((5, 4, 3), dtype=tf.float32), 0.5), sim_config)
tf.random.set_seed(0)
horizon = 2
network = network_lib.Network(variables=variables)
trajectory = network.sample_trajectory(num_steps=horizon)

observations = []


def make_f(data):

  def f(time, observation=data):
    return Value(
        **{field: value[time, Ellipsis] for field, value in observation.items()})

  return f


for var, var_trajectory in zip(variables, trajectory):
  print(var, var_trajectory)

  obs = util.time_variable(
      name=var.name + ' obs', spec=var.spec, f=make_f(var_trajectory))
  print(obs.spec)
  observations.append(obs)

for o in observations:
  print(o)
  print(o.initial_value.fn())
  print(o.value.fn(Value(__time_step=0)))
t = log_probability.log_probability(variables, observations, horizon)
