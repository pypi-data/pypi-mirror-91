from enum import Enum
from math import sin, cos

import torch
from torch import nn

__all__ = [
    "PositionalEmbeddingType",
    "PositionalEmbedding",
    "MiniBertEmbedding",
]


class PositionalEmbeddingType(Enum):
    TRAINED = 1
    FIXED = 2
    NONE = 3


class PositionalEmbedding(nn.Module):
    def __init__(self, embedding_dim, max_seq_len, ptype=PositionalEmbeddingType.TRAINED):
        super().__init__()

        self.embedding_dim = embedding_dim
        self.max_seq_len = max_seq_len

        if ptype == PositionalEmbeddingType.TRAINED:
            self.embeddings = nn.Embedding(max_seq_len, embedding_dim)
        elif ptype == PositionalEmbeddingType.FIXED:
            # See Attention is all you need, section 3.5 (https://arxiv.org/pdf/1706.03762.pdf)
            positions = torch.zeros(
                (max_seq_len, embedding_dim), dtype=torch.float)
            for pos in range(max_seq_len):
                for i in range(embedding_dim):
                    if i % 2 == 0:
                        positions[pos, i] = sin(
                            pos / pow(10000, 2 * i / embedding_dim))
                    else:
                        positions[pos, i] = cos(
                            pos / pow(10000, 2 * i / embedding_dim))
            self.embeddings = nn.Embedding.from_pretrained(
                positions, freeze=True)
        elif ptype == PositionalEmbeddingType.NONE:
            positions = torch.zeros(
                (max_seq_len, embedding_dim), dtype=torch.float)
            self.embeddings = nn.Embedding.from_pretrained(
                positions, freeze=True)
        else:
            raise Exception("Invalid position type")

        self.register_buffer(
            "position_ids", torch.arange(max_seq_len).expand((1, -1)))

    def forward(self, input):
        seq_len = input.shape[-1]
        return self.embeddings(self.position_ids[:, :seq_len])


class MiniBertEmbedding(nn.Module):
    def __init__(self, voc_size, embedding_dim, max_seq_len, position_type, normalize_embeddings):
        super().__init__()

        self.max_seq_len = max_seq_len
        self.position_type = position_type
        self.normalize_embeddings = normalize_embeddings

        self.word_embeddings = nn.Embedding(voc_size, embedding_dim)
        self.position_embeddings = PositionalEmbedding(
            embedding_dim, max_seq_len, ptype=position_type)

        self.norm = None
        if normalize_embeddings:
            self.norm = nn.LayerNorm(embedding_dim)

    def forward(self, input):
        word_emb = self.word_embeddings(input)
        pos_emb = self.position_embeddings(input)
        emb = word_emb + pos_emb

        if self.normalize_embeddings:
            return self.norm(emb)
        else:
            return emb
