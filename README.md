# CitationPulse

Generative Engine Optimization (GEO) & AI Citability Auditor

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Clean](https://img.shields.io/badge/code%20style-production-000000.svg)](https://github.com/xcalibur73/citation-pulse)

CitationPulse is a command-line utility and Python audit library for Generative Engine Optimization (GEO). It evaluates web pages against the retrieval and citation heuristics used by Google AI Overviews, ChatGPT Search, Perplexity AI, and Claude.

The scoring model implements empirical findings from the Princeton University KDD 2024 GEO benchmark, tracking passage density, factual attributions, crawl permissions, and knowledge graph disambiguation.

---

## The Shift from SERP Ranking to AI Citation

Traditional search engines index documents through inverted term indexes and PageRank graphs. AI answer engines operate on retrieval-augmented generation (RAG):
1. Specialized search bots (OAI-SearchBot, PerplexityBot, Claude-SearchBot) crawl and cache web documents.
2. Dense passage retrieval models segment content into embedding chunks, filtering for concise factual density.
3. Language models synthesize answers from top-ranked passages, citing only sources with clear attribution and unambiguous entity credentials.

If a site blocks AI search bots in `robots.txt` or buries key conclusions in conversational filler, generative engines skip the document entirely, even if it ranks on page one of traditional search results.

---

## Technical Capabilities

- Passage citability scoring: evaluates content blocks against the Princeton KDD 2024 benchmark. Checks for optimal passage length (134 to 167 words), front-loaded definitions, verifiable quantitative figures, direct quotes, and explicit attribution phrasing.
- 2026 search crawler governance: parses `robots.txt` rules to distinguish live AI search bots (OAI-SearchBot, Claude-SearchBot, PerplexityBot, Googlebot) from model-training web scrapers (GPTBot, ClaudeBot, CCBot).
- Entity disambiguation: checks JSON-LD schemas for Organization, Person, and authoritative `sameAs` entity links pointing to Wikidata and Wikipedia.
- Machine-readable discovery: validates the presence, syntax, and section structure of root `/llms.txt` and `/llms-full.txt` files.
- Platform-specific breakdowns: calculates individual readiness scores (0 to 100) calibrated for Google AI Overviews, ChatGPT Search, and Perplexity AI.

---

## Installation

```bash
git clone https://github.com/xcalibur73/citation-pulse.git
cd citation-pulse
pip install -r requirements.txt
```

---

## Quick Start

### Terminal Audit
```bash
python run.py https://webaudits.pro
```

### Export Markdown Report
```bash
python run.py https://example.com/article --output markdown --save GEO-AUDIT.md
```

### Generate Standards-Compliant /llms.txt Template
```bash
python run.py https://example.com --generate-llms
```

### Export JSON for CI/CD Pipelines
```bash
python run.py https://example.com --output json --save audit.json
```

---

## Web Platform Integration (WebAudits.pro)

To run hosted audits without installing local Python dependencies:
- Web tool: [WebAudits.pro/tools/geo-audit](https://webaudits.pro/tools/geo-audit)
- Automated crawler access checks and sitemap scanning.

---

## Scoring Architecture

CitationPulse evaluates content across four signal layers:

| Layer | Weight | Signals Evaluated | Primary Retrieval Target |
|:---|:---:|:---|:---|
| Passage Citability | 35% | Word count (134-167 words), stats density, attributions, quotations | Perplexity, ChatGPT Search |
| Crawler Access | 25% | `robots.txt` access for `OAI-SearchBot`, `PerplexityBot`, `Claude-SearchBot` | Live AI search indexing |
| Entity Graph | 25% | JSON-LD schema, `sameAs` Wikidata/Wikipedia links, author credentials | Google AI Overviews |
| Technical Standards | 15% | `/llms.txt` syntax, markdown heading hierarchy, blockquote descriptions | Agent indexation |

### Empirical Heuristics Reference

- Adding verifiable numerical data increased citation frequency by up to 37% in the Princeton KDD 2024 study.
- Explicit attribution phrases ("according to", "study by") improved passage retrieval confidence by up to 40%.
- Passages between 134 and 167 words showed the highest extraction rate across neural embedding models.

---

## Python API Usage

```python
from citation_pulse.passage_scorer import score_passage
from citation_pulse.crawler_inspector import test_crawler_access

# Score a passage block
passage = "According to a 2024 study by MIT researchers, synthetic data pipelines reduced model error rates by 34%."
result = score_passage(passage)
print(f"Citability Score: {result['score']}/100")
print(f"Signals: {result['signals']}")

# Audit robots.txt permissions
status = test_crawler_access("https://example.com", "User-agent: *\nDisallow: /admin/\n")
print(f"Search Bots Score: {status['search_bots_score']}/100")
```

---

## Running Unit Tests

```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## Author

Developed by **Sadikeen Firoz** ([@xcalibur73](https://github.com/xcalibur73)), creator of [WebAudits.pro](https://webaudits.pro).

Part of a technical SEO engineering tooling trio:
1. [dom-hydrate](https://github.com/xcalibur73/dom-hydrate): Headless Chromium SSR vs CSR DOM diff engine.
2. [citation-pulse](https://github.com/xcalibur73/citation-pulse): GEO and AI search citability benchmark engine.
3. [index-trace](https://github.com/xcalibur73/index-trace): Search Console emergency triage and crawler collision tracer.

---

## License

Licensed under the [MIT License](LICENSE).
