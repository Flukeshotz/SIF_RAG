import unittest
from retrieval.citations import generate_citations
from generation.prompts import format_user_prompt
from retrieval.engine import answer_query

class TestGenerationPipeline(unittest.TestCase):
    def test_citation_generation(self):
        mock_included = [
            {
                "document_id": "Doc A",
                "document_type": "KIM",
                "organization": "Quant"
            }
        ]
        citations = generate_citations(mock_included)
        self.assertIn("[Source 1]", citations)
        self.assertIn("Doc A", citations)
        self.assertIn("Quant", citations)
        
    def test_format_user_prompt(self):
        formatted = format_user_prompt("CONTEXT", "QUERY")
        self.assertIn("CONTEXT", formatted)
        self.assertIn("USER QUESTION: QUERY", formatted)

if __name__ == "__main__":
    unittest.main()
