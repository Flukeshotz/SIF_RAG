import unittest
from retrieval.embed_query import embed_query
from retrieval.search import search_chunks
from retrieval.context_builder import build_context

class TestRetrievalPipeline(unittest.TestCase):
    def test_query_embedding(self):
        vec = embed_query("What is SIF?")
        self.assertEqual(len(vec), 384)
        
    def test_search_chunks(self):
        vec = embed_query("Minimum investment amount")
        chunks = search_chunks(vec, top_k=5)
        self.assertTrue(len(chunks) > 0)
        self.assertTrue(len(chunks) <= 5)
        # Verify payload has required fields
        self.assertIn("chunk_id", chunks[0])
        self.assertIn("text", chunks[0])
        
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
