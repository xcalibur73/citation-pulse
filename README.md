# CitationPulse

Generative Engine Optimization (GEO) and AI citability auditor.

Part of the [WebAudits.pro](https://webaudits.pro) technical intelligence platform.

---

## Quickstart

Install in editable mode and audit AI search citability in seconds:

```bash
# Clone and install
git clone https://github.com/xcalibur73/citation-pulse.git
cd citation-pulse
pip install -r requirements.txt
pip install -e .

# Audit target URL for AI search eligibility
citation-pulse https://example.com

# Generate a compliant /llms.txt template
citation-pulse https://example.com --generate-llms
```

---

## What It Does & Why It Matters

CitationPulse audits content formatting, robots.txt crawl permissions, and semantic entities to assess how readily AI search engines (Google AI Overviews, ChatGPT Search, Perplexity AI) can ingest and cite a web page.

Standard keyword-density optimization fails in generative search engines. Large language models prioritize concise answering passages, verified data points, and clear entity attributions. Furthermore, websites frequently block search retrieval crawlers (`OAI-SearchBot`) in blanket `robots.txt` rules intended to stop model training scrapers.

CitationPulse evaluates key factors governing AI search citation readiness:
- **Passage Citability Scoring:** Scans prose for 134-167 word atomic passages, front-loaded definitions, empirical data, and named attribution markers. This is a project-defined heuristic based partly on published GEO research (Aggarwal et al., Princeton / IIT Delhi KDD 2024).
- **AI Search Crawler Access:** Verifies explicit `robots.txt` permissions for search retrieval bots (`OAI-SearchBot`, `Claude-SearchBot`, `PerplexityBot`) versus training scrapers (`GPTBot`, `CCBot`).
- **Schema.org Entity Disambiguation:** Checks structured data for explicit `sameAs` authority links to Wikidata and Wikipedia.
- **`/llms.txt` Format Validation:** Verifies the presence and syntax of markdown documentation for language model scrapers. Note: Google Search Central explicitly clarified in June 2026 that `llms.txt` is not required for Google Search and does not affect Google organic rankings or visibility. CitationPulse evaluates `/llms.txt` strictly as an optional file convention for third-party AI agents.

---

## Visual Diagnostic Workflow

```text
[Input Target URL]
      |
      v
[1. Passage Citability Scan] --------> Finding: Long unbroken paragraphs (320 words) with buried definitions
      |                                Recommendation: Split into 130-160 word atomic answer passages with bold lead-ins
      v
[2. Robots.txt Crawler Audit] -------> Finding: OAI-SearchBot blocked by blanket User-agent: * Disallow rule
      |                                Recommendation: Add explicit "User-agent: OAI-SearchBot Allow: /" exception
      v
[3. Schema Disambiguation Check] ----> Finding: Organization node lacks sameAs entity references
                                       Recommendation: Inject sameAs links to official Wikidata and LinkedIn profiles
```

---

## Usage & CLI Options

```bash
# Audit a target URL
citation-pulse https://webaudits.pro

# Generate a recommended /llms.txt template for the domain
citation-pulse https://example.com --generate-llms

# Export machine-readable JSON report for CI pipelines
citation-pulse https://example.com --output json --save geo-audit.json

# Check installed version
citation-pulse --version
```

---

## Example Output

```text
+-------------------------------------------------------------------------------+
| CitationPulse: Generative Engine Optimization (GEO) Diagnostic                |
| Target URL: https://webaudits.pro                                             |
| Overall GEO Readiness Score: 92.5/100 (Grade: A)                              |
| Crawler Permissions: ALLOWED | Passages Analyzed: 14 | Top Citability: 96%   |
+-------------------------------------------------------------------------------+

Component Score Breakdown:
+-----------------------------------+--------+------------+
| Component Dimension               | Weight | Score      |
+-----------------------------------+--------+------------+
| AI Crawler Access (RFC 9309)      | 30%    | 100.0/100  |
| Atomic Passage Citability         | 30%    | 91.0/100   |
| Entity Disambiguation (sameAs)    | 20%    | 95.0/100   |
| LLMS.txt Standardization          | 10%    | 80.0/100   |
| Structural Heading Hierarchy      | 10%    | 90.0/100   |
+-----------------------------------+--------+------------+

Platform Readiness Indicators:
- Google AI Overviews: High (Structured entity anchors, clean definition passages)
- ChatGPT Search: High (OAI-SearchBot allowed, concise atomic summaries)
- Perplexity AI: High (PerplexityBot allowed, verified data attributions)
```

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

- `cli.py`: Orchestrates HTTP fetching, passage segmentation from `<main>` and `<article>` tags, and output formatting.
- `evaluator.py`: Audits robots.txt permissions for modern AI search bots and checks `/llms.txt` availability.
- `scorer.py`: Evaluates passage citability using length targets (134-167 words), statistical patterns, and attribution keywords.
- `report_generator.py`: Generates Rich terminal tables, Markdown documentation, and JSON structures.

---

## Standards & Heuristics

CitationPulse separates established Internet standards from academic optimization heuristics:

| Metric / Check | Classification | Authority / Basis |
|:---|:---|:---|
| AI Crawler Access | Internet Standard | IETF RFC 9309 (Robots Exclusion Protocol) |
| Passage Citability Modeling | Academic Research Heuristic | Project heuristic based on Princeton / IIT Delhi KDD 2024 GEO Study |
| Entity Disambiguation | Web Standard | Schema.org Community Vocabulary |
| `/llms.txt` Syntax | Emerging File Convention | llmstxt.org proposal (Not required for Google Search) |
| Platform Readiness Scores | Project-Derived Heuristic | Multi-factor weighted eligibility models |

> **Google Search Central Note:** Google clarified in June 2026 that `llms.txt` is not required for Google Search and does not affect Google rankings or indexing. CitationPulse uses it solely as an optional readiness metric for third-party AI agents.

---

## Limitations

- **Heuristic Projection:** Passage citability scores reflect published academic optimization heuristics; they cannot guarantee inclusion in dynamic LLM search answers.
- **Dynamic Retrieval Variations:** Generative engines evaluate real-time query semantics and retrieval context that change per prompt.
- **Paywalled / Gated Content:** Analyzes public crawlable HTML; content protected by client-side authentication or CAPTCHAs requires pre-authenticated sessions.

---

## Testing & CI

```bash
# Run unit tests
python -m unittest discover -s tests

# Output
# Ran 4 tests in 0.001s
# OK
```

Continuous integration runs automatically across Ubuntu and Windows runners on every commit via GitHub Actions.

---

## License

MIT License. See [LICENSE](LICENSE) for details.
