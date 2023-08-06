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
"""Misc. helper functions for DBN models."""

from __future__ import absolute_import
from __future__ import division

from __future__ import print_function

import tensorflow.compat.v1 as tf1
import tensorflow.compat.v2 as tf


def initialize_platform(platform, tpu_bns='local'):
  if platform == 'TPU':
    cluster_resolver = tf.distribute.cluster_resolver.TPUClusterResolver(
        tpu=tpu_bns)
    tf.config.experimental_connect_to_cluster(
        cluster_resolver, protocol='grpc+loas')
    tf.tpu.experimental.initialize_tpu_system(cluster_resolver)
    distribution_strategy = tf.distribute.experimental.TPUStrategy(
        cluster_resolver)
  else:
    distribution_strategy = tf.distribute.MirroredStrategy()
  return distribution_strategy, len(tf.config.list_logical_devices(platform))
