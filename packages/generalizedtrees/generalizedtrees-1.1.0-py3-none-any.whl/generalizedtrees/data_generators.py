# Data generators (used in oracle-based explainers)
#
# Copyright 2020 Yuriy Sverchkov
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

from generalizedtrees.features import FeatureSpec
import numpy as np


#####################
# Trepan's approach #
#####################


def trepan_generator_n(tree_model, training_data: np.ndarray):
    """
    The data generation scheme used in Trepan

    n-sample version
    """

    d = training_data.shape[1]

    # The Trepan generator independently generates the individual feature values.
    feature_generators = [
        _n_feature_generator(training_data[:,i], tree_model.feature_spec[i])
        for i in range(d)]

    return lambda n: np.column_stack([f(n) for f in feature_generators])


def _n_feature_generator(data_vector, feature: FeatureSpec, rng=np.random.default_rng()):

    n = len(data_vector)

    if feature is FeatureSpec.CONTINUOUS:
        # Sample from a KDE.
        # We use Generator and not RandomState but KDE implementations use RandomState
        # so it's more reliable to just implement the sampling here. 
        return lambda m: rng.normal(
            loc = rng.choice(data_vector, size=m),
            scale = 1/np.sqrt(n),
            size = m)[0]

    elif feature & FeatureSpec.DISCRETE:
        # Sample from the empirical distribution
        values, counts = np.unique(data_vector, return_counts=True)
        return lambda m: rng.choice(values, p=counts/n, size=m)
    
    else:
        raise ValueError(f"I don't know how to handle feature spec {feature}")


def trepan_generator(tree_model, training_data: np.ndarray):
    """
    The data generation scheme used in Trepan

    1-sample version
    """

    d = training_data.shape[1]

    # The Trepan generator independently generates the individual feature values.
    feature_generators = [
        _feature_generator(training_data[:,i], tree_model.feature_spec[i])
        for i in range(d)]

    return lambda: np.array([f() for f in feature_generators])

def _feature_generator(data_vector, feature: FeatureSpec, rng=np.random.default_rng()):

    n = len(data_vector)

    if feature is FeatureSpec.CONTINUOUS:
        # Sample from a KDE.
        # We use Generator and not RandomState but KDE implementations use RandomState
        # so it's more reliable to just implement the sampling here. 
        return lambda: rng.normal(
            loc = rng.choice(data_vector, size=1),
            scale = 1/np.sqrt(n),
            size = 1)[0]

    elif feature & FeatureSpec.DISCRETE:
        # Sample from the empirical distribution
        values, counts = np.unique(data_vector, return_counts=True)
        return lambda: rng.choice(values, p=counts/n)
    
    else:
        raise ValueError(f"I don't know how to handle feature spec {feature}")


############
# Smearing #
############

def smearing(tree_model, training_data: np.ndarray):
    r"""
    The data generation scheme used in Born Again Trees

    Given a training set $( \mathbf x^{(i)} | i \in 1:n )$ of $d$-dimensional instances,
    to generate a new training sample $\mathbf x^{(+)}$:

    1. Select random $a \in 1:n$
    2. For each $j \in 1:d$,
        with probability $p_\mathrm{alt}$
        let $x^{(+)}_j \leftarrow x^{(a)}_j$, otherwise
        let $x^{(+)}_j \leftarrow x^{(b)}_j$ for random $b \in 1:n$.
    """

    # Ensure p-alt defined
    tree_model.p_alt = getattr(tree_model, "p_alt", 0.5)

    # Ensure rng defined
    tree_model.rng = getattr(tree_model, "rng", np.random.default_rng())

    n, d = training_data.shape

    def gen():
        base_instance = training_data[tree_model.rng.integers(n)].copy()
        for i in range(d):
            if tree_model.rng.random() < tree_model.p_alt:
                base_instance[i] = tree_model.rng.choice(training_data[:, i])

    return gen


