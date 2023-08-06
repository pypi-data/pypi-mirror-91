from enum import Enum
from math import sqrt

from .embeddings import PositionalEmbeddingType, PositionalEmbedding

import torch
from torch import nn
from torch.nn import functional as F

__all__ = [
    "AttentionType",
    "AttentionEmbedding",
    "Attention",
    "NonTransformingAttention",
]


class AttentionType(Enum):
    SelfAttention = 1
    AttentionEmbedding = 2
    NonTransformingAttention = 3


class AttentionEmbedding(nn.Module):
    def __init__(self, embedding_dim, voc_size, out_dim=None, max_seq_len=1024, position_type=PositionalEmbeddingType.TRAINED, normalize_embeddings=True):
        super(AttentionEmbedding, self).__init__()
        if out_dim is None:
            out_dim = embedding_dim

        self.embedding_dim = embedding_dim
        self.voc_size = voc_size
        self.out_dim = out_dim
        self.max_seq_len = max_seq_len

        self.key = nn.Embedding(voc_size, embedding_dim)
        self.query = nn.Embedding(voc_size, embedding_dim)
        self.value = nn.Embedding(voc_size, out_dim)
        self._sqrt_embedding = sqrt(embedding_dim)

        self.position_embedding = PositionalEmbedding(
            embedding_dim, max_seq_len, ptype=position_type)

        self.norm = None
        self.normalize_embeddings = normalize_embeddings
        if normalize_embeddings:
            self.norm = nn.LayerNorm(embedding_dim)

    def forward(self, input):
        pos = self.position_embedding(input)
        key = self.key(input) + pos
        query = self.query(input) + pos
        value = self.value(input)

        if self.normalize_embeddings:
            key = self.norm(key)
            query = self.norm(query)
            value = self.norm(value)

        key_t = torch.transpose(key, -2, -1)
        qk = torch.matmul(query, key_t) / self._sqrt_embedding
        attention = F.softmax(qk, dim=-1)
        return torch.matmul(attention, value)


class Attention(nn.Module):
    def __init__(self, in_dim, out_dim, hidden_dim=None, key_is_query=False):
        super(Attention, self).__init__()
        if hidden_dim is None:
            hidden_dim = out_dim

        self.in_dim = in_dim
        self.out_dim = out_dim
        self.key_is_query = key_is_query
        self.hidden_dim = hidden_dim
        self.key = nn.Parameter(torch.rand((in_dim, hidden_dim)))
        if key_is_query:
            self.query = self.key
        else:
            self.query = nn.Parameter(torch.rand((in_dim, hidden_dim)))
        self.value = nn.Parameter(torch.rand((in_dim, out_dim)))
        self._sqrt_hidden = sqrt(hidden_dim)

    @classmethod
    def from_weights(cls, key, query, value):
        in_dim, hidden_dim = key.shape
        out_dim = value.shape[1]
        x = cls(in_dim, out_dim, hidden_dim)
        with torch.no_grad():
            x.key = nn.Parameter(key)
            x.query = nn.Parameter(query)
            x.value = nn.Parameter(value)
        return x

    def forward(self, input):
        key = torch.matmul(input, self.key)
        query = torch.matmul(input, self.query)
        value = torch.matmul(input, self.value)

        key_t = torch.transpose(key, -2, -1)
        qk = torch.matmul(query, key_t) / self._sqrt_hidden
        attention = F.softmax(qk, dim=-1)
        return torch.matmul(attention, value)


class NonTransformingAttention(nn.Module):
    def __init__(self, dim):
        super(NonTransformingAttention, self).__init__()
        self.dim = dim
        self._sqrt_dim = sqrt(dim)

    def forward(self, input):
        query = input
        key = input
        key_t = torch.transpose(key, -2, -1)
        qk = torch.matmul(query, key_t) / self._sqrt_dim
        attention = F.softmax(qk, dim=-1)
        return torch.matmul(attention, input)
