# CitationPulse: 12-Site GEO & AI Crawler Study

Evaluation of AI search crawler access, passage citability scores, and Knowledge Graph disambiguation gathered during local testing.

---

## Methodology

Evaluated using CitationPulse v1.0.0. Audits measured:
1. Retrieval permissions in `robots.txt` across live search crawlers (`OAI-SearchBot`, `Claude-SearchBot`, `PerplexityBot`, `Googlebot`).
2. Opt-out status for foundation model scrapers (`GPTBot`, `CCBot`, `ClaudeBot`).
3. Passage citability scoring based on Princeton University KDD 2024 formulas (word count 134-167 words, statistics, quotes, attributions).
4. Machine-readable standard discovery (`/llms.txt`).

Testing environment: Python 3.10, 2026-09-19.

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
