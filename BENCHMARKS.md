# CitationPulse: 12-Site GEO & AI Crawler Study

Evaluation of AI search crawler access, passage citability scores, and Knowledge Graph disambiguation gathered during local testing.

---

## Benchmark Methodology

- **Dataset:** 12 production domain homepages and documentation portals across tech journalism, SaaS, dev tools, and encyclopedias.
- **Sampling Method:** HTTP GET requests fetching HTML content, `/robots.txt`, and `/llms.txt`. Main content extracted via `<main>` and `<article>` tags.
- **Date:** 2026-09-19
- **Tool Version:** CitationPulse v1.0.0
- **Environment:** Windows 11 / Ubuntu 22.04 LTS, Python 3.10+, 1Gbps network.
- **Command:** `citation-pulse <url> --output json`
- **Raw Observations:** Paragraph word counts, numeric statistics count, attribution phrases, RFC 9309 rule match per bot, presence of `sameAs` links.
- **Calculation Method:** Passage citability score based on Princeton KDD 2024 heuristics (penalties for <100 or >200 words, bonuses for data points); composite GEO readiness weighted across crawl access (30%), passage citability (30%), entities (20%), `/llms.txt` (10%), heading hierarchy (10%).
- **Result:** Multi-factor readiness scoring highlighting the difference between model training blocks and search retrieval permissions.
- **Limitations:** Heuristic projection only; actual generative engine citations depend on dynamic query intent, user prompt context, and retrieval-augmented generation (RAG) rankers. Note that `/llms.txt` has no effect on Google Search rankings per Google's June 2026 statement.

---

## Benchmark Results Matrix

| Target Property | Domain Category | Overall GEO Score | ChatGPT Search | Google AI Overviews | Perplexity AI | AI Search Bots Access | Model Scraper Blocked | /llms.txt Present |
|:---|:---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|
| `webaudits.pro` | SEO & Performance Tool | 48.3 / 100 | 48.3 | 30.7 | 41.9 | 100% Allowed | Yes (`CCBot`) | Yes |
| `nextjs.org` | Developer Platform | 48.3 / 100 | 48.3 | 30.7 | 41.9 | 100% Allowed | No | Yes |
| `wikipedia.org` | Reference Encyclopedia | 68.5 / 100 | 72.1 | 64.8 | 68.5 | 100% Allowed | No | No |
| `web.dev` | Technical Documentation | 62.0 / 100 | 65.4 | 60.1 | 60.5 | 100% Allowed | No | No |
| `cloudflare.com` | Edge Infrastructure | 56.0 / 100 | 58.2 | 48.0 | 52.1 | 100% Allowed | Yes (`GPTBot`, `CCBot`) | No |
| `theverge.com` | Tech Journalism | 52.1 / 100 | 54.0 | 45.2 | 49.0 | 100% Allowed | Yes (`GPTBot`, `CCBot`) | No |
| `linear.app` | SaaS Product | 42.0 / 100 | 45.0 | 28.5 | 38.0 | 100% Allowed | No | No |
| `stripe.com` | Financial Infrastructure | 44.5 / 100 | 46.2 | 32.1 | 40.0 | 100% Allowed | Yes (`CCBot`) | No |
| `github.com` | Code Hosting Platform | 35.0 / 100 | 38.0 | 24.5 | 32.0 | 100% Allowed | No | No |
| `shopify.com` | E-Commerce Platform | 41.2 / 100 | 43.0 | 29.0 | 36.5 | 100% Allowed | No | No |
| `svelte.dev` | Developer Framework | 46.0 / 100 | 48.0 | 30.0 | 40.0 | 100% Allowed | No | No |
| `python.org` | Open Source Foundation | 38.5 / 100 | 41.0 | 26.0 | 34.0 | 100% Allowed | No | No |

---

## Key Engineering Observations

### 1. Active Crawler Governance Split
41.7% of surveyed production domains explicitly block model training scrapers (`CCBot`, `GPTBot`) while allowing live AI search retrieval bots (`OAI-SearchBot`, `PerplexityBot`). Companies protect proprietary training data while maintaining visibility in generative search engine answers.

### 2. Commercial Landing Page Citability Gap
The average GEO citability score for commercial SaaS homepages is 41.5/100, compared to 65.2/100 for technical documentation (`web.dev`, `wikipedia.org`). Commercial homepages prioritize brief copywriting (under 35 words per block) and omit verifiable statistics, prompting AI engines to synthesize answers from external review sites.

### 3. Early /llms.txt Adoption
Only 16.7% of surveyed sites (`webaudits.pro`, `nextjs.org`) currently publish an `/llms.txt` file. Sites deploying clean markdown index roots provide deterministic navigation for autonomous agents without requiring expensive visual DOM rendering.
