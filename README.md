# CitationPulse

Generative Engine Optimization (GEO) and AI citability auditor.

Part of the [WebAudits.pro](https://webaudits.pro) technical intelligence platform.

---

## What it does

CitationPulse audits content formatting, robots.txt crawl access, and semantic entities to assess how readily AI search engines (Google AI Overviews, ChatGPT Search, Perplexity AI) can ingest and cite a web page. It evaluates:
- Passage citability: scans prose for 134-167 word atomic passages, front-loaded definitions, empirical statistics, and named attribution markers based on Princeton University KDD 2024 GEO research.
- 2026 AI search crawler access: verifies explicit `robots.txt` permissions for search retrieval bots (`OAI-SearchBot`, `Claude-SearchBot`, `PerplexityBot`) versus training scrapers (`GPTBot`, `CCBot`).
- Schema.org entity disambiguation: audits `sameAs` authority links to Wikidata and Wikipedia.
- `/llms.txt` validation: verifies the presence and formatting of markdown documentation for language models.

---

## Why it exists

Search behavior is shifting from ten blue SERP links to synthesized answer overviews. Standard keyword-density optimization fails in generative search engines:
- Large language models select citations based on factual density, concise answering passages, and entity verification.
- Many websites unintentionally block search retrieval bots (`OAI-SearchBot`) in blanket `robots.txt` rules intended to stop model training scrapers.

CitationPulse provides an empirical audit of the technical and syntactic factors governing AI search citation eligibility.

---

## Key features

- **Passage Extraction & Scoring:** Splits body copy into semantic blocks, ranking passages by factual density, word count optimization, and attribution signals.
- **Search Retrieval Bot Permissions Audit:** Tests origin `robots.txt` against both search retrieval bots and training crawlers.
- **Schema Entity Disambiguation:** Checks structured data for explicit `sameAs` canonical references that confirm organization and author identity.
- **LLMS.txt Generator:** Generates a compliant `/llms.txt` template tailored to the audited domain.
- **Platform Sub-Scores:** Models platform-specific citation preferences across Google AI Overviews, ChatGPT Search, and Perplexity.

---

## Architecture

```text
[Input Target URL]
        |
        +---> [HTML Content Fetcher]
        |           |
        |           +---> Passage Segmentation (15+ words, main content)
        |           +---> Citability Scorer (Word count, stats, attributions)
        |           +---> Schema.org JSON-LD Disambiguation Auditor
        |
        +---> [Robots.txt Evaluator]
        |           |
        |           +---> RFC 9309 Rules Matcher (OAI-SearchBot, PerplexityBot)
        |
        +---> [LLMS.txt Checker]
        |
        v
[GEO Scoring Engine]
        |
        +---> Composite GEO Readiness Score
        +---> Platform Sub-Scores (AI Overviews, ChatGPT, Perplexity)
        +---> Terminal Report / Markdown / JSON Pipeline Output
```

CitationPulse executes four diagnostic components:
1. `cli.py`: Orchestrates HTTP fetching, passage segmentation from `<main>` and `<article>` tags, and output formatting.
2. `evaluator.py`: Audits robots.txt permissions for modern AI search bots and checks `/llms.txt` availability.
3. `scorer.py`: Evaluates passage citability using length targets (134-167 words), statistical patterns, and attribution keywords.
4. `report_generator.py`: Generates Rich terminal tables, Markdown documentation, and JSON structures.

---

## Installation

### Prerequisites
- Python 3.10 or higher

### Install from Source
```bash
git clone https://github.com/xcalibur73/citation-pulse.git
cd citation-pulse
pip install -r requirements.txt
pip install -e .
```

---

## Usage

### Basic CLI Invocation
```bash
# Audit a target URL for AI search citability
citation-pulse https://webaudits.pro

# Generate a recommended /llms.txt template for the domain
citation-pulse https://example.com --generate-llms

# Export machine-readable JSON report for CI pipelines
citation-pulse https://example.com --output json --save geo-audit.json

# Check installed version
citation-pulse --version
```

---

## Example output

```text
+-------------------------------------------------------------------------------+
| CitationPulse: Generative Engine Optimization (GEO) Auditor                   |
| Target: https://webaudits.pro                                                 |
| GEO Readiness Score: 80.1/100                                                 |
| Analyzed Passages: 8 | High-Probability Snippets: 4                           |
+-------------------------------------------------------------------------------+

AI Search Engine Readiness Breakdown:
+-------------------------------+-----------+-----------------------------------------+
| AI Search Surface             | Score     | Primary Selection Logic                 |
+-------------------------------+-----------+-----------------------------------------+
| Google AI Overviews & AI Mode | 74.4/100  | Classic rankings + Schema + answer block|
| ChatGPT Search (GPT-4o)       | 80.1/100  | OAI-SearchBot access + entity authority |
| Perplexity AI Search          | 71.6/100  | Freshness + 134-167 word passages + stats|
+-------------------------------+-----------+-----------------------------------------+

2026 AI Search Crawler Access (robots.txt):
- OAI-SearchBot: ALLOWED (Search retrieval bot)
- Claude-SearchBot: ALLOWED (Search retrieval bot)
- PerplexityBot: ALLOWED (Search retrieval bot)
- GPTBot: ALLOWED (Model training scraper)
```

---

## Benchmark / methodology

### Empirical 12-Site GEO Index
- **Dataset:** 12 production web properties across news media, developer documentation, and SaaS blogs.
- **Command Used:** `python run.py <url> --output json`
- **Tool Version:** CitationPulse v1.0.0
- **Environment:** Windows 11 / Ubuntu 22.04, Python 3.12, unthrottled fiber network.
- **Scoring Weights:**
  - Passage Citability: 35% (optimal word count, statistics presence, attribution density)
  - Search Crawler Access: 25% (OAI-SearchBot, PerplexityBot, Claude-SearchBot)
  - Schema Entity Disambiguation: 25% (`sameAs` links, Organization/Person completeness)
  - Technical / llms.txt Readiness: 15%
- **Results:**
  - 41.7% of surveyed production websites blocked training scrapers while permitting search retrieval bots.
  - Complete study dataset: [BENCHMARKS.md](BENCHMARKS.md).

---

## Limitations

- **Diagnostic Heuristic:** The GEO Readiness Score and platform sub-scores are project-derived heuristics based on published research (Princeton University KDD 2024). They do not represent proprietary algorithms of OpenAI, Google, or Perplexity, nor do they guarantee inclusion or citation in any AI search engine.
- **Query Context Independence:** CitationPulse audits static content characteristics. In live systems, AI models select sources dynamically based on the exact user prompt, conversation history, and real-time retrieval rankings.
- **Paywalls & Gated Content:** Analyzes publicly accessible HTML; it does not audit content hidden behind client logins or subscription walls.

---

## Accuracy / standards

CitationPulse categorizes its diagnostic metrics as follows:

| Metric / Check | Classification | Authority / Standard |
|:---|:---|:---|
| Robots.txt Crawler Evaluation | Google / Web Standard | IETF RFC 9309 |
| Schema.org Entity Verification | Web Standard | Schema.org Community Specifications |
| /llms.txt Syntax & Availability | Emerging Community Standard | llmstxt.org Specification |
| Passage Citability Score | Project-Derived Heuristic | Implementation of Princeton KDD 2024 factors |
| Platform Readiness Sub-Scores | Experimental Metric | Weighted projection model |

---

## Testing

CitationPulse includes automated unit tests covering passage extraction, citability scoring, robots.txt evaluation, and report formatters:

```bash
# Run unit test suite
python -m unittest discover -s tests

# Test execution output
# Ran 4 tests in 0.001s
# OK
```

Continuous integration runs automatically on every commit and pull request via GitHub Actions across Linux and Windows runners.

---

## Roadmap

- [x] Initial release with Princeton KDD scoring rules and robots.txt bot checks.
- [x] PEP 621 packaging, CLI `--version`, and Windows cp1252 encoding hardening.
- [ ] Embedding similarity evaluation using local sentence-transformers.
- [ ] Real-time SERP verification via Perplexity and ChatGPT Search APIs.
- [ ] WebAudits.pro continuous AI crawler monitoring integration.

---

## License

MIT License. See [LICENSE](LICENSE) for full details.
