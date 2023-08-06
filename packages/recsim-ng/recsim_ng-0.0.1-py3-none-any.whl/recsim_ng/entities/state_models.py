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
"""TODO."""

import abc
import edward2 as ed  # type: ignore
from gym import spaces
import numpy as np

from recsim_ng.core import value
import tensorflow.compat.v2 as tf
import tensorflow_probability as tfp

tfd = tfp.distributions

Value = value.Value
ValueSpec = value.ValueSpec
Space = value.Space


class StaticStateModel(tf.Module, metaclass=abc.ABCMeta):
  """A state sampled at the beginning of the session and held fixed."""

  def __init__(self, batch_shape=None, name='StaticStateModel'):
    super(StaticStateModel, self).__init__(name=name)
    self._batch_shape = batch_shape

  @abc.abstractmethod
  def initial_state(self):
    """Samples the state at the first time step."""

  def next_state(self, old_state):
    """A fixed deterministic state transition."""
    return old_state.map(ed.Deterministic)

  @abc.abstractmethod
  def _specs(self):
    """State space definition."""


class DiscreteEmbedding(StaticStateModel):
  """Picks from the outermost dimension of a tensor of features.

  This class implements a state space representation in terms of a static
  N-dimensional embedding in real space sampled from a finite set of predefined
  possible embeddings according to fixed logits. It supports, for example, the
  implementation, of choice scenarios in which an agent has a fixed goal,
  in terms of an item embedding in Euclidean space.

  This entity ingests a tensor of item features with shape (n_items,
  n_features), where rows are items and columns are real space coordinates.
  The .intent method outputs a target row from that tensor, sampled from a
  categorical distribution with logits provided as arguments to the intent
  method. The entity supports batch execution in the following way: if a logits
  tensor with shape [b1, ..., bk, n_items] is provided, intent will output a
  tensor with shape [b1,..., bk, n_features].
  """

  def __init__(self, target_features, parameters, batch_shape=None):
    """Constructs a DiscreteEmbedding entity.

    Args:
      target_features: a real tensor with shape [n_items, n_features]
        representing the set of potential target points to be used as a goal.
      parameters: a dictionary containing the 'item_logits' key; 'item_logits'
        must be a real tensor of shape [b1, ..., bk, n_items] specifying the
        logits (target item preferences) for each of the b1 x ... x bk targets
        to be sampled.
    """
    super().__init__(batch_shape)
    self._num_items = tf.shape(target_features)[0]
    # TODO(mmladenov, cwhsu):  make target_features batchable too as the set of
    # available targets might be different for every agent
    self._target_features = target_features
    self._parameters = parameters

  def initial_state(self):
    """Samples an intent tensor for a batch of agents.

    Returns:
      a dictionary containing the 'target_point' key, holding a tensor of shape
      [b1, ..., bk, n_features] which contains the target choices for the batch,
      sampled according to the categorical distribution induced by the item
      logits.
    """
    item_logits = self._parameters['item_logits']
    # TODO(mmladenov, cwhsu): consider using a choice model entity instead here
    target_choice = ed.Categorical(logits=item_logits, name='element_pick')
    target_features = tf.gather(self._target_features, target_choice)
    return Value(target_features=ed.Deterministic(target_features))

  def _specs(self):
    if self._batch_shape is None:
      raise RuntimeError(
          'batch_shape must be supplied in the config if this entity is bound'
          'to a random variable.')
    output_shape = tf.concat(
        (tf.constant(self._batch_shape), tf.shape(self._target_features)[1:]),
        axis=0)
    return ValueSpec(
        state=Space(spaces.Box(-np.Inf, np.Inf, shape=output_shape.numpy())))


class ClusteredDiscreteEmbedding(DiscreteEmbedding):
  """Picks a cluster according to logits, then uniformly picks a member item.

  This entity provides a hierarchical model for embedding point generation.
  Similarly to its base class DiscreteEmbedding, it picks among a set
  of predefined embedding points. However, the choice process is hierarchical --
  first, a cluster is chosen according to provided logits, then, an item from
  that cluster is chosen uniformly.
  """

  def __init__(self, target_features, cluster_assignments, parameters,
               batch_shape):
    """Constructs a ClusterTargetPoint entity.

    Args:
      config: a possibly empty dictionary of configuration options. If the
        execution of .spaces is required, config must contain a 'batch_shape'
        key so that output dimensions are known in advance.
      target_features: a real tensor with shape [n_items, n_features]
        representing the set of potential target points to be used as a goal.
      cluster_assignments: a tensor of shape [n_items,] containing the cluster
        assignments of the points in target_features as non-negative integers.
        cluster_assignments must contain one instance of every cluster.
    """
    super(ClusteredDiscreteEmbedding, self).__init__(target_features, None,
                                                     batch_shape)
    # count cluster sizes, sort target embedding rows in order of increasing
    # cluster id;
    # see ClusterTargetPoint.intent for an explanation of why this is necessary
    sorted_assignment_indices = tf.argsort(cluster_assignments)
    self._parameters = parameters
    self._cluster_assignments = tf.gather(cluster_assignments,
                                          sorted_assignment_indices)
    self._target_features = tf.gather(self._target_features,
                                      sorted_assignment_indices)

    unique_clusters, _, self._cluster_sizes = tf.unique_with_counts(
        self._cluster_assignments)
    tf.debugging.assert_equal(
        unique_clusters,
        tf.range(tf.size(unique_clusters), dtype=unique_clusters.dtype),
        message='cluster_assignments must be 0-based, and contain every cluster'
        ' id up to the total number of clusters minus one.')
    # items are now sorted in a way that all members of the same cluster
    # are next to each-other
    self._cluster_boundaries = tf.concat(
        (tf.constant([0]), tf.cumsum(self._cluster_sizes)), axis=0)

  def initial_state(self):
    """Samples an intent tensor for a batch of agents.

    Args:
      parameters: a dictionary containing the 'cluster_logits' key;
        'cluster_logits' must be a real tensor of shape [b1, ..., bk,
        max(cluster_assignments)] specifying the logits (the propensity of an
        agent to select a particular cluster  for each of the b1 x ... x bk
        targets to be sampled.

    Returns:
      a dictionary containing the 'target_point' key, holding a tensor of shape
      [b1, ..., bk, n_features] which contains the target choices for the batch,
      sampled according to the categorical distribution induced by the item
      logits.
    """
    # TODO(mmladenov, ccolby): consider pushing more code in the parent class
    cluster_logits = self._parameters['cluster_logits']
    # clusters may have different numbers of elements, so to enable batch
    # sampling, we will not sample items with a categorical distribution;
    # instead, for each picked cluster, we will sample an integer from 0 to
    # cluster_size by rounding a uniform distribution and then locate the item
    # in the target_features tensor
    # TODO(mmladenov, cwhsu): consider using a choice model entity instead here
    cluster_picks = ed.Categorical(
        logits=cluster_logits, dtype=tf.int32, name='cluster_pick')
    picked_cluster_boundaries = tf.gather(self._cluster_boundaries,
                                          cluster_picks)
    picked_cluster_sizes = tf.gather(self._cluster_sizes, cluster_picks)
    item_picks = tf.math.floor(
        ed.Uniform(
            high=tf.cast(picked_cluster_sizes - 1, dtype=tf.float32),
            name='cluster_element'))
    item_picks = tf.cast(item_picks, dtype=tf.int32)
    target_choices = item_picks + picked_cluster_boundaries
    target_features = tf.gather(self._target_features, target_choices)
    return Value(state=ed.Deterministic(target_features))


class GMMStaticPoint(StaticStateModel):
  """Picks a cluster according to logits, then uniformly picks a member item.

  This entity provides a hierarchical model for target point generation.
  Similarly to its base class TargetPointInFeatureSpace, it picks among a set
  of predefined embedding points. However, the choice process is hierarchical --
  first, a cluster is chosen according to provided logits, then, an item from
  that cluster is chosen uniformly.
  """

  def __init__(self, parameters, batch_shape=None):
    """Constructs a GMMStaticPoint entity.

    Args:
      config: a possibly empty dictionary of configuration options. If the
        execution of .spaces is required, config must contain a 'batch_shape'
        key so that output dimensions are known in advance.
      target_features: a real tensor with shape [n_items, n_features]
        representing the set of potential target points to be used as a goal.
      cluster_assignments: a tensor of shape [n_items,] containing the cluster
        assignments of the points in target_features as non-negative integers.
        cluster_assignments must contain one instance of every cluster.
    """
    super(GMMStaticPoint, self).__init__(batch_shape)
    self._component_means = parameters['component_means']
    self._component_covariances = tf.linalg.cholesky(
        parameters['component_covariances'])
    self._component_logits = parameters['component_logits']

  def initial_state(self):
    """Samples an intent tensor for a batch of agents.

    Args:
      parameters: a dictionary containing the 'cluster_logits' key;
        'cluster_logits' must be a real tensor of shape [b1, ..., bk,
        max(cluster_assignments)] specifying the logits (the propensity of an
        agent to select a particular cluster  for each of the b1 x ... x bk
        targets to be sampled.

    Returns:
      a dictionary containing the 'target_point' key, holding a tensor of shape
      [b1, ..., bk, n_features] which contains the target choices for the batch,
      sampled according to the categorical distribution induced by the item
      logits.
    """
    # TODO(mmladenov, ccolby): consider pushing more code in the parent class
    batch_shape = tf.shape(self._component_logits)[:-1]
    # batch x number of components x dim
    expand_mean_shape = tf.concat((tf.ones(
        tf.size(batch_shape), dtype=tf.int32), tf.shape(self._component_means)),
                                  axis=0)
    broadcast_mean_shape = tf.concat(
        (batch_shape, tf.shape(self._component_means)), axis=0)
    batch_component_means = tf.broadcast_to(
        tf.reshape(self._component_means, expand_mean_shape),
        broadcast_mean_shape)
    expand_cov_shape = tf.concat(
        (tf.ones(tf.size(batch_shape),
                 dtype=tf.int32), tf.shape(self._component_covariances)),
        axis=0)
    batch_component_covariances = tf.reshape(self._component_covariances,
                                             expand_cov_shape)
    # we won't broadcast batch_component_covariances explicitly
    component_dist = tfd.MultivariateNormalTriL(
        loc=batch_component_means, scale_tril=batch_component_covariances)
    mixture_dist = tfd.Categorical(logits=self._component_logits)

    return Value(state=ed.MixtureSameFamily(mixture_dist, component_dist))

  def _specs(self):
    junk_space = spaces.Dict({
        'target_features': spaces.Box(
            low=np.array([0.0]), high=np.array([1.0]))
    })
    return junk_space
