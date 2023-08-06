from minibert.embeddings import PositionalEmbeddingType
import unittest
import torch

from minibert import *


class TestMiniBert(unittest.TestCase):
    def test_minibert_not_fail(self):
        vocabulary = ["<mask>", "a", "b", "c", "d", "e"]
        d = 4

        for pos in PositionalEmbeddingType:
            for att in AttentionType:
                config = MiniBertConfiguration(
                    vocabulary=vocabulary,
                    embedding_dim=d,
                    position_embeddings_count=16,
                    mask_idx=0,
                    position_type=pos,
                    attention_type=att
                )
                minibert = MiniBert(config)
                x = torch.tensor([
                    [1, 3, 4, 5],
                    [1, 3, 4, 5],
                    [1, 3, 4, 5]
                ])
                output = minibert(x)
                self.assertEqual(
                    output.size(),
                    torch.Size((x.size(0), x.size(1), d))
                )

    def test_minibert_mlm_and_reggression(self):
        vocabulary = ["<mask>", "a", "b", "c", "d", "e"]
        sentences = torch.tensor([
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5],
            [1, 2, 3, 4, 5],
        ])

        x_acr = torch.tensor([
            [3, 4, 5],
            [1, 4, 2],
        ])
        y_acr = torch.tensor([1, 2])

        for pos in PositionalEmbeddingType:
            for att in AttentionType:
                config = MiniBertForMLMAndRegressionConfiguration(
                    vocabulary=vocabulary,
                    embedding_dim=4,
                    position_embeddings_count=16,
                    mask_idx=0,
                    reg_output_size=len(vocabulary),
                    position_type=pos,
                    attention_type=att
                )
                model = MiniBertForMLMAndRegression(config)

                mlm_output = model.forward(sentences, 0)
                reg_output = model.forward(x_acr, 1)

                self.assertIsInstance(mlm_output, tuple)
                self.assertEqual(
                    mlm_output[0].size(),
                    torch.Size(
                        (sentences.size(0), sentences.size(1), len(vocabulary)))
                )
                self.assertEqual(
                    reg_output.size(),
                    torch.Size((x_acr.size(0), x_acr.size(1), len(vocabulary)))
                )


if __name__ == '__main__':
    unittest.main()
