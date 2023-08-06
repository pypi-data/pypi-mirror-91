import torch
from torch import nn
from torch.nn import functional as F
from math import sqrt, sin, cos, pow
from enum import Enum

from .activations import parse_activation_function
from .attention import Attention, AttentionType, AttentionEmbedding, NonTransformingAttention
from .embeddings import MiniBertEmbedding

__all__ = [
    "MiniBert",
    "MiniBertForMLM",
    "MiniBertForRegression",
    "MiniBertForMLMAndRegression",
]


class MiniBert(nn.Module):
    def __init__(self, configuration):
        super(MiniBert, self).__init__()

        self.configuration = configuration

        self._voc_size = len(configuration.vocabulary)
        self._embedding_dim = configuration.embedding_dim

        if configuration.attention_type == AttentionType.AttentionEmbedding:
            self.attention_embedding = AttentionEmbedding(
                self._embedding_dim,
                self._voc_size,
                position_type=configuration.position_type,
                normalize_embeddings=configuration.normalize_embeddings
            )
        else:
            self.embedding = MiniBertEmbedding(
                self._voc_size,
                self._embedding_dim,
                max_seq_len=configuration.position_embeddings_count,
                position_type=configuration.position_type,
                normalize_embeddings=configuration.normalize_embeddings
            )

            if configuration.attention_type == AttentionType.SelfAttention:
                self.attention = Attention(
                    self._embedding_dim,
                    self._embedding_dim,
                    hidden_dim=configuration.hidden_dim,
                    key_is_query=configuration.key_is_query
                )
            elif configuration.attention_type == AttentionType.NonTransformingAttention:
                self.attention = NonTransformingAttention(
                    self._embedding_dim
                )
            else:
                raise Exception("Invalid attention type")

    def forward(self, input):
        if self.configuration.attention_type == AttentionType.AttentionEmbedding:
            x = self.attention_embedding(input)
        else:
            x = self.embedding(input)
            x = self.attention(x)
        return x


class MiniBertForMLM(nn.Module):
    def __init__(self, configuration):
        super().__init__()
        self.minibert = MiniBert(configuration)
        self.configuration = configuration

        self._voc_size = len(configuration.vocabulary)
        self._embedding_dim = configuration.embedding_dim

        self.l1 = nn.Linear(self._embedding_dim,
                            configuration.first_layer_output_size, bias=False)
        self.l2 = nn.Linear(
            configuration.first_layer_output_size, self._voc_size, bias=True)

        self.mask_idx = configuration.mask_idx

        self.activation_fun = parse_activation_function(
            configuration.activation_fun)

        self._mask_prob = configuration.mask_prob
        self._keep_mask_prob = configuration.keep_mask_prob
        self._inv_corrupt_mask_prob = 1 - configuration.corrupt_mask_prob

    def forward(self, input):
        if self.training:
            masked_input = input.detach().clone()
            masked = torch.rand_like(
                input, dtype=torch.float) <= self._mask_prob

            masking_strategy = torch.rand_like(input, dtype=torch.float)
            masking = masked & (masking_strategy <=
                                self._keep_mask_prob)  # Keep masks
            corrupt = masked & (self._inv_corrupt_mask_prob <
                                masking_strategy)  # Corrupt masks

            replacements = torch.randint(
                self._voc_size, (torch.sum(corrupt), ), device=input.device)

            masked_input[masking] = self.mask_idx
            masked_input[corrupt] = replacements
            x = self.minibert(masked_input)
        else:
            x = self.minibert(input)

        x = self.l1(x)
        x = self.activation_fun(x)
        x = self.l2(x)

        if self.training:
            labels = input.detach().clone()
            labels[~masked] = -1

            loss_fn = nn.CrossEntropyLoss(ignore_index=-1)
            loss = loss_fn(x.view(-1, self._voc_size), labels.view(-1))
            return (x, loss)
        else:
            return x


class MiniBertForRegression(nn.Module):
    def __init__(self, configuration):
        super().__init__()
        self.minibert = MiniBert(configuration)
        self.configuration = configuration

        self._voc_size = len(configuration.vocabulary)
        self._embedding_dim = configuration.embedding_dim

        self.l1 = nn.Linear(self._embedding_dim,
                            configuration.first_layer_output_size, bias=False)
        self.activation_fun = parse_activation_function(
            configuration.activation_fun)
        self.l2 = nn.Linear(
            configuration.first_layer_output_size, configuration.output_size, bias=True)

    def forward(self, input):
        x = self.minibert(input)

        x = self.l1(x)
        x = self.activation_fun(x)
        x = self.l2(x)
        return x


class MiniBertForMLMAndRegression(nn.Module):
    def __init__(self, configuration):
        super().__init__()
        self.minibert = MiniBert(configuration)
        self.configuration = configuration

        self._voc_size = len(configuration.vocabulary)
        self._embedding_dim = configuration.embedding_dim

        self.mlm_l1 = nn.Linear(self._embedding_dim,
                                configuration.mlm_first_layer_output_size, bias=False)
        self.mlm_l2 = nn.Linear(
            configuration.mlm_first_layer_output_size, self._voc_size, bias=True)

        self.reg_l1 = nn.Linear(self._embedding_dim,
                                configuration.reg_first_layer_output_size, bias=False)
        self.reg_l2 = nn.Linear(
            configuration.reg_first_layer_output_size, configuration.reg_output_size, bias=True)

        self.mask_idx = configuration.mask_idx

        self.mlm_activation_fun = parse_activation_function(
            configuration.mlm_activation_fun)
        self.reg_activation_fun = parse_activation_function(
            configuration.reg_activation_fun)

        self._mask_prob = configuration.mask_prob
        self._keep_mask_prob = configuration.keep_mask_prob
        self._inv_corrupt_mask_prob = 1 - configuration.corrupt_mask_prob

    # task == 0 -> MLM
    # task == 1 -> Regression
    def forward(self, input, task):
        if task == 0:
            return self.forward_mlm(input)
        elif task == 1:
            return self.forward_reg(input)
        else:
            raise Exception(
                f"`task` parameter must be either 0 or 1, not {task}.")

    def forward_mlm(self, input):
        if self.training:
            masked_input = input.clone().detach()
            masked = torch.rand_like(
                input, dtype=torch.float) <= self._mask_prob

            masking_strategy = torch.rand_like(input, dtype=torch.float)
            masking = masked & (masking_strategy <=
                                self._keep_mask_prob)  # Keep masks
            corrupt = masked & (self._inv_corrupt_mask_prob <
                                masking_strategy)  # Corrupt masks

            replacements = torch.randint(
                self._voc_size, (torch.sum(corrupt), ), device=input.device)

            masked_input[masking] = self.mask_idx
            masked_input[corrupt] = replacements
            x = self.minibert(masked_input)
        else:
            x = self.minibert(input)

        x = self.mlm_l1(x)
        x = self.mlm_activation_fun(x)
        x = self.mlm_l2(x)

        if self.training:
            labels = input.clone().detach()
            labels[~masked] = -1

            loss_fn = nn.CrossEntropyLoss(ignore_index=-1)
            loss = loss_fn(x.view(-1, self._voc_size), labels.view(-1))
            return (x, loss)
        else:
            return x

    def forward_reg(self, input):
        x = self.minibert(input)
        x = self.reg_l1(x)
        x = self.reg_activation_fun(x)
        x = self.reg_l2(x)
        return x
