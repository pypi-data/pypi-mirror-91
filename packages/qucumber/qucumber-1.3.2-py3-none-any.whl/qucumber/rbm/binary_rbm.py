# Copyright 2019 PIQuIL - All Rights Reserved.

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#     http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


import numpy as np
import torch
from torch import nn
from torch.nn import functional as F
from torch.nn.utils import parameters_to_vector

from qucumber import _warn_on_missing_gpu
from qucumber.utils import auto_unsqueeze_args


class BinaryRBM(nn.Module):
    def __init__(self, num_visible, num_hidden=None, zero_weights=False, gpu=True):
        super().__init__()
        self.num_visible = int(num_visible)
        self.num_hidden = int(num_hidden) if num_hidden else self.num_visible
        self.num_pars = (
            (self.num_visible * self.num_hidden) + self.num_visible + self.num_hidden
        )

        _warn_on_missing_gpu(gpu)
        self.gpu = gpu and torch.cuda.is_available()

        self.device = torch.device("cuda") if self.gpu else torch.device("cpu")

        self.initialize_parameters(zero_weights=zero_weights)

    def __repr__(self):
        return (
            f"BinaryRBM(num_visible={self.num_visible}, "
            f"num_hidden={self.num_hidden}, gpu={self.gpu})"
        )

    def initialize_parameters(self, zero_weights=False):
        """Randomize the parameters of the RBM"""

        gen_tensor = torch.zeros if zero_weights else torch.randn
        self.weights = nn.Parameter(
            (
                gen_tensor(
                    self.num_hidden,
                    self.num_visible,
                    device=self.device,
                    dtype=torch.double,
                )
                / np.sqrt(self.num_visible)
            ),
            requires_grad=False,
        )

        self.visible_bias = nn.Parameter(
            torch.zeros(self.num_visible, device=self.device, dtype=torch.double),
            requires_grad=False,
        )
        self.hidden_bias = nn.Parameter(
            torch.zeros(self.num_hidden, device=self.device, dtype=torch.double),
            requires_grad=False,
        )

    @auto_unsqueeze_args()
    def effective_energy(self, v):
        r"""The effective energies of the given visible states.

        .. math::

            \mathcal{E}(\bm{v}) &= -\sum_{j}b_j v_j
                        - \sum_{i}\log
                            \left\lbrack 1 +
                                  \exp\left(c_{i} + \sum_{j} W_{ij} v_j\right)
                            \right\rbrack

        :param v: The visible states.
        :type v: torch.Tensor

        :returns: The effective energies of the given visible states.
        :rtype: torch.Tensor
        """
        v = v.to(self.weights)
        visible_bias_term = torch.matmul(v, self.visible_bias)
        hid_bias_term = F.softplus(F.linear(v, self.weights, self.hidden_bias)).sum(-1)

        return -(visible_bias_term + hid_bias_term)

    def effective_energy_gradient(self, v, reduce=True):
        """The gradients of the effective energies for the given visible states.

        :param v: The visible states.
        :type v: torch.Tensor
        :param reduce: If `True`, will sum over the gradients resulting from
                       each visible state. Otherwise will return a batch of
                       gradient vectors.
        :type reduce: bool

        :returns: Will return a vector (or matrix if `reduce=False` and multiple
                  visible states were given as a matrix) containing the gradients
                  for all parameters (computed on the given visible states v).
        :rtype: torch.Tensor
        """
        v = (v.unsqueeze(0) if v.dim() < 2 else v).to(self.weights)
        prob = self.prob_h_given_v(v)

        if reduce:
            W_grad = -torch.matmul(prob.transpose(0, -1), v)
            vb_grad = -torch.sum(v, 0)
            hb_grad = -torch.sum(prob, 0)
            return parameters_to_vector([W_grad, vb_grad, hb_grad])
        else:
            W_grad = -torch.einsum("...j,...k->...jk", prob, v)
            vb_grad = -v
            hb_grad = -prob
            vec = [W_grad.view(*v.shape[:-1], -1), vb_grad, hb_grad]
            return torch.cat(vec, dim=-1)

    @auto_unsqueeze_args()
    def prob_v_given_h(self, h, out=None):
        """Given a hidden unit configuration, compute the probability
        vector of the visible units being on.

        :param h: The hidden unit
        :type h: torch.Tensor
        :param out: The output tensor to write to.
        :type out: torch.Tensor

        :returns: The probability of visible units being active given the
                  hidden state.
        :rtype: torch.Tensor
        """
        return (
            torch.matmul(h, self.weights.data, out=out)
            .add_(self.visible_bias.data)
            .sigmoid_()
            .clamp_(min=0, max=1)
        )

    @auto_unsqueeze_args()
    def prob_h_given_v(self, v, out=None):
        """Given a visible unit configuration, compute the probability
        vector of the hidden units being on.

        :param h: The hidden unit.
        :type h: torch.Tensor
        :param out: The output tensor to write to.
        :type out: torch.Tensor

        :returns: The probability of hidden units being active given the
                  visible state.
        :rtype: torch.Tensor
        """
        return (
            torch.matmul(v, self.weights.data.t(), out=out)
            .add_(self.hidden_bias.data)
            .sigmoid_()
            .clamp_(min=0, max=1)
        )

    def sample_v_given_h(self, h, out=None):
        """Sample/generate a visible state given a hidden state.

        :param h: The hidden state.
        :type h: torch.Tensor
        :param out: The output tensor to write to.
        :type out: torch.Tensor

        :returns: The sampled visible state.
        :rtype: torch.Tensor
        """
        v = self.prob_v_given_h(h, out=out)
        v = torch.bernoulli(v, out=out)  # overwrite v with its sample
        return v

    def sample_h_given_v(self, v, out=None):
        """Sample/generate a hidden state given a visible state.

        :param h: The visible state.
        :type h: torch.Tensor
        :param out: The output tensor to write to.
        :type out: torch.Tensor

        :returns: The sampled hidden state.
        :rtype: torch.Tensor
        """
        h = self.prob_h_given_v(v, out=out)
        h = torch.bernoulli(h, out=out)  # overwrite h with its sample
        return h

    def gibbs_steps(self, k, initial_state, overwrite=False):
        r"""Performs k steps of Block Gibbs sampling. One step consists of sampling
        the hidden state :math:`\bm{h}` from the conditional distribution
        :math:`p(\bm{h}\:|\:\bm{v})`, and sampling the visible
        state :math:`\bm{v}` from the conditional distribution
        :math:`p(\bm{v}\:|\:\bm{h})`.

        :param k: Number of Block Gibbs steps.
        :type k: int
        :param initial_state: The initial state of the Markov Chains.
        :type initial_state: torch.Tensor
        :param overwrite: Whether to overwrite the initial_state tensor.
                          Exception: If initial_state is not on the same device
                          as the RBM, it will NOT be overwritten.
        :type overwrite: bool

        :returns: Returns the visible states after k steps of
                  Block Gibbs sampling
        :rtype: torch.Tensor
        """
        v = (initial_state if overwrite else initial_state.clone()).to(self.weights)

        h = torch.zeros(*v.shape[:-1], self.num_hidden).to(self.weights)

        for _ in range(k):
            self.sample_h_given_v(v, out=h)
            self.sample_v_given_h(h, out=v)

        return v

    def partition(self, space):
        """Compute the partition function of the RBM.

        :param space: A rank 2 tensor of the visible space.
        :type space: torch.Tensor

        :returns: The value of the partition function evaluated at the current
                  state of the RBM.
        :rtype: torch.Tensor
        """
        logZ = (-self.effective_energy(space)).logsumexp(0)
        return logZ.exp()
