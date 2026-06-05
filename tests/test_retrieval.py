import unittest
from unittest.mock import patch, MagicMock
from retrieval.embed_query import embed_query
from retrieval.search import search_chunks
from retrieval.context_builder import build_context

class TestRetrievalPipeline(unittest.TestCase):
    def test_query_embedding(self):
        vec = embed_query("What is SIF?")
        self.assertEqual(len(vec), 384)
        
    @patch('retrieval.search.get_qdrant')
    def test_search_chunks(self, mock_get_qdrant):
        # Mock the Qdrant client and response so CI doesn't need a real database
        mock_client = MagicMock()
        mock_response = MagicMock()
        
        mock_point = MagicMock()
        mock_point.payload = {
            "chunk_id": "test_chunk_1",
            "text": "Minimum investment amount is 1 crore.",
            "priority_tier": 1
        }
        mock_point.score = 0.8
        
        mock_response.points = [mock_point]
        mock_client.query_points.return_value = mock_response
        mock_get_qdrant.return_value = mock_client
        
        # Don't need real embedding for mock search, just passing a mock vector
        vec = [0.1] * 384
        chunks = search_chunks(vec, top_k=5)
        
        self.assertTrue(len(chunks) > 0)
        self.assertTrue(len(chunks) <= 5)
        # Verify payload has required fields
        self.assertIn("chunk_id", chunks[0])
        self.assertIn("text", chunks[0])
        # Verify priority tier multiplier was applied (Tier 1 = 1.5x)
        self.assertAlmostEqual(chunks[0]["_score"], 0.8 * 1.50)
        
    def test_context_builder(self):
        mock_chunks = [
            {
                "document_id": "Doc A",
                "document_type": "KIM",
                "organization": "Quant",
                "fund_name": "Quant SIF",
                "text": "This is a test chunk."
            }
        ]
        context, included = build_context(mock_chunks, max_tokens=100)
        self.assertIn("=== RETRIEVED CONTEXT ===", context)
        self.assertIn("Doc A", context)
        self.assertIn("This is a test chunk.", context)
        self.assertEqual(len(included), 1)

if __name__ == "__main__":
    unittest.main()

