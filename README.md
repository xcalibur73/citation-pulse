# CitationPulse: Generative Engine Optimization (GEO) & AI Citability Auditor

[![Python Version](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Clean](https://img.shields.io/badge/code%20style-production-000000.svg)](https://github.com/xcalibur73/citation-pulse)

CitationPulse is a command-line diagnostic tool and Python audit engine designed to evaluate web content for Generative Engine Optimization (GEO). It scores how reliably passages, schemas, and technical crawl rules satisfy extraction heuristics used by modern AI answer engines: Google AI Overviews, ChatGPT Search, Perplexity AI, and Claude.

Built on empirical benchmarks from the Princeton University KDD 2024 GEO study, SE Ranking citation studies, and emerging 2026 search crawler protocols, CitationPulse transforms subjective content auditing into deterministic scoring.

---

## Why GEO Auditing Matters

Traditional search engines index documents based on inverted keyword indexes and PageRank link graphs. AI answer engines operate differently:

1. They crawl and retrieve documents via specialized search bots (e.g. `OAI-SearchBot`, `PerplexityBot`, `Claude-SearchBot`).
2. They chunk content into passage embeddings and assess factual density, attribution markers, and sentence conciseness.
3. They synthesize answers using top-scoring passages, citing only sources with high information gain and clear entity credentials.

Blocking search crawlers by mistake in `robots.txt` or formatting critical insights into verbose, unfocused paragraphs causes content to be passed over by AI summaries, even when ranking well in traditional SERPs. CitationPulse isolates these regressions before traffic drops.

---

## Core Capabilities

- **Passage Citability Scoring**: Evaluates content blocks against Princeton KDD 2024 research. Scores optimal passage length (134 to 167 words), front-loaded definitions, statistical density (+37% boost), authoritative quotations (+30% boost), and attribution phrases (+40% boost).
- **2026 AI Search Crawler Inspection**: Audits `robots.txt` rules specifically distinguishing AI Search retrieval bots (`OAI-SearchBot`, `Claude-SearchBot`, `PerplexityBot`, `Googlebot`) from model-training scrapers (`GPTBot`, `ClaudeBot`, `Google-Extended`, `Applebot-Extended`, `CCBot`).
- **Schema.org Knowledge Graph Disambiguation**: Checks JSON-LD entities for `Organization`, `Person`, and `sameAs` entity links pointing to authoritative knowledge repositories (Wikidata, Wikipedia, LinkedIn).
- **Machine-Readable Standard Validation**: Checks root presence and syntax conformity for `/llms.txt` and `/llms-full.txt`, scoring structured markdown navigation readiness.
- **Platform-Specific Readiness Breakdown**: Generates tailored citability scores (0 to 100) for Google AI Overviews, ChatGPT Search, and Perplexity AI.

---

## Installation

CitationPulse runs locally with standard Python 3.10+ and minimal external dependencies:

```bash
git clone https://github.com/xcalibur73/citation-pulse.git
cd citation-pulse
pip install -r requirements.txt
```

---

## Usage

### 1. Terminal Audit (Interactive Rich Tables)
Run a direct audit on any public URL:

```bash
python run.py https://webaudits.pro
```

### 2. Export Markdown Report
Generate a forensic markdown report for sharing with engineering or content teams:

```bash
python run.py https://example.com/guide --output markdown --save GEO-AUDIT.md
```

### 3. Generate Optimized /llms.txt Template
Inspect a domain and generate a standards-compliant `/llms.txt` template:

```bash
python run.py https://example.com --generate-llms
```

### 4. Cloud Integration with WebAudits.pro
Generate an automated monitoring link for continuous crawler checks:

```bash
python run.py https://example.com --cloud
```

### 5. Machine-Readable JSON Pipeline Output
Pipe audit output directly into CI/CD pipelines or automated reporting systems:

```bash
python run.py https://example.com --output json
```

---

## Enterprise Continuous Monitoring (WebAudits.pro)

While CitationPulse CLI provides ad-hoc single-URL audits, enterprise applications frequently require continuous visibility.

Through [WebAudits.pro](https://webaudits.pro/tools/geo-audit), you can access the hosted, hardened cloud engine:
- Continuous 24/7 AI crawler access monitoring with Slack/Discord webhook alerts when robots.txt changes.
- Automated bulk XML sitemap audits evaluating hundreds of URLs in parallel.
- Historical AI citability score tracking across Google AI Overviews, ChatGPT Search, and Perplexity.
- Visual citation extraction diffs showing passage shifts across content revisions.

## Architecture & Scoring Methodology

CitationPulse applies a weighted scoring algorithm across four distinct signal layers:

| Layer | Weight | Evaluated Signals | Primary Impact |
| :--- | :---: | :--- | :--- |
| **Passage Citability** | 35% | Word count (134-167 words), stats density, attributions, quotes, front-loading | Perplexity, ChatGPT citations |
| **Crawler Access** | 25% | `robots.txt` permissions for `OAI-SearchBot`, `PerplexityBot`, `Claude-SearchBot` | Retrieval in live AI search |
| **Entity Graph** | 25% | JSON-LD schema, `sameAs` Wikidata/Wikipedia links, `Person` author credentials | Google AI Overviews grounding |
| **Technical Standards** | 15% | `/llms.txt` file presence, markdown heading structure, blockquote description | Emerging agent indexation |

### Empirical Heuristics Reference:
- **Statistics Addition**: The Princeton KDD 2024 benchmark showed adding verifiable quantitative figures increased source citation rates by up to 37%.
- **Quotation and Attribution**: Explicit source attribution phrases ("according to", "study by") boost model confidence scores by up to 40%.
- **Passage Length**: Passages between 134 and 167 words yield the highest extraction probability across dense neural retrieval models.

---

## Programmatic Python API

CitationPulse modules can be integrated into custom testing harnesses and web scraping pipelines:

```python
from bs4 import BeautifulSoup
from citation_pulse.passage_scorer import score_passage, analyze_document_passages
from citation_pulse.crawler_inspector import test_crawler_access
from citation_pulse.schema_auditor import audit_schema_entities

# Score a single passage block
result = score_passage(
    "According to a study by MIT researchers in 2024, synthetic data pipelines reduced model error rates by 34%."
)
print(f"Citability Score: {result['score']}/100")
print(f"Features: {result['signals']}")

# Audit crawler permissions against raw robots.txt content
crawler_status = test_crawler_access("https://example.com", "User-agent: *\nDisallow: /admin/\n")
print(f"Search Bots Score: {crawler_status['search_bots_score']}/100")
```

---

## Unit Testing

Run the test suite to verify scoring calibration and parser stability:

```bash
python -m unittest discover -s tests -p "test_*.py"
```

---

## Author & Contact

Built by **Sadikeen Firoz** ([@xcalibur73](https://github.com/xcalibur73))  
Platform: [WebAudits.pro](https://webaudits.pro)

## License

This project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
