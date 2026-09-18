"""
Unit tests for CitationPulse GEO & AI Citability modules.
"""

import unittest
from bs4 import BeautifulSoup
from citation_pulse.passage_scorer import score_passage, analyze_document_passages
from citation_pulse.crawler_inspector import test_crawler_access, parse_robots_rules
from citation_pulse.schema_auditor import audit_schema_entities
from citation_pulse.report_generator import calculate_composite_geo_score

class TestCitationPulse(unittest.TestCase):

    def test_passage_citability_boosts(self):
        # Passage with optimal length (140 words), statistics, quotation, and attribution
        optimal_text = (
            "According to a study by Princeton researchers in 2024, Generative Engine Optimization requires specific "
            "structural adaptations to improve search extraction. The research reported by AI experts demonstrated that adding "
            "specific statistical data increased citation rates by 37% across leading answer engines. Furthermore, direct "
            "authoritative quotations such as \"structured data and factual clarity are non-negotiable foundations for modern discovery\" "
            "provided an additional 30% boost in source attribution frequency. When technical documents provide clear, unambiguous "
            "definitions in the opening 40 words, language models can reliably extract and synthesize answers without hallucination. "
            "The benchmark examined 10,000 queries across Google AI Overviews, ChatGPT Search, and Perplexity AI, confirming that "
            "concise blocks between 134 and 167 words outperformed lengthy, conversational narratives by 42% in total attribution frequency. "
            "Maintaining clean entity disambiguation ensures long-term indexing stability. "
            "Rigorous passage engineering directly empowers search engines to index verified content accurately and consistently."
        )
        result = score_passage(optimal_text)
        self.assertGreaterEqual(result["score"], 85)
        self.assertEqual(result["length_verdict"], "OPTIMAL (134-167 words)")
        self.assertTrue(result["signals"]["has_statistics"])
        self.assertTrue(result["signals"]["has_attributions"])
        self.assertTrue(result["signals"]["has_quotes"])

    def test_crawler_access_distinction(self):
        robots_sample = """
User-agent: *
Disallow: /admin/

User-agent: GPTBot
Disallow: /

User-agent: OAI-SearchBot
Allow: /
"""
        test_res = test_crawler_access("https://example.com", robots_sample)
        results = {c["name"]: c["status"] for c in test_res["results"]}

        # OAI-SearchBot (Search citability) should be ALLOWED
        self.assertEqual(results.get("OAI-SearchBot"), "ALLOWED")
        # GPTBot (Model training) should be BLOCKED
        self.assertEqual(results.get("GPTBot"), "BLOCKED")
        # PerplexityBot should be ALLOWED (inherits from wildcard without root block)
        self.assertEqual(results.get("PerplexityBot"), "ALLOWED")

    def test_schema_entity_auditor(self):
        html = """
        <html>
        <head>
            <script type="application/ld+json">
            {
                "@context": "https://schema.org",
                "@graph": [
                    {
                        "@type": "Organization",
                        "@id": "https://example.com/#org",
                        "name": "Acme Metrics",
                        "sameAs": [
                            "https://www.wikidata.org/wiki/Q123456",
                            "https://en.wikipedia.org/wiki/Acme_Corp"
                        ]
                    },
                    {
                        "@type": "Person",
                        "@id": "https://example.com/#author",
                        "name": "Jane Doe",
                        "jobTitle": "Lead Performance Engineer"
                    }
                ]
            }
            </script>
        </head>
        <body>
            <p>Content goes here.</p>
        </body>
        </html>
        """
        soup = BeautifulSoup(html, "html.parser")
        audit = audit_schema_entities(soup)
        self.assertTrue(audit["has_organization"])
        self.assertTrue(audit["has_person_author"])
        self.assertTrue(audit["has_wikidata_link"])
        self.assertTrue(audit["has_wikipedia_link"])
        self.assertGreaterEqual(audit["score"], 80)

    def test_composite_geo_calculation(self):
        passage_data = {"average_citability": 85.0}
        crawler_data = {"search_bots_score": 100.0}
        schema_data = {"score": 90.0, "same_as_links": ["https://wikidata.org"], "has_person_author": True}
        llms_data = {"score": 80.0, "present": True}

        geo = calculate_composite_geo_score(passage_data, crawler_data, schema_data, llms_data)
        self.assertGreaterEqual(geo["overall_score"], 85.0)
        self.assertIn("google_ai_overviews", geo["platform_scores"])
        self.assertIn("chatgpt_search", geo["platform_scores"])
        self.assertIn("perplexity_ai", geo["platform_scores"])

if __name__ == "__main__":
    unittest.main()
