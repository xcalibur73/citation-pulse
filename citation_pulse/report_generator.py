"""
Report Generator & Formatter for CitationPulse GEO Audits.
"""

from typing import Dict, Any

try:
    from rich.console import Console
    from rich.table import Table
    from rich.panel import Panel
    from rich.text import Text
    HAS_RICH = True
except ImportError:
    HAS_RICH = False

def calculate_composite_geo_score(passage_data: Dict[str, Any], crawler_data: Dict[str, Any], schema_data: Dict[str, Any], llms_data: Dict[str, Any]) -> Dict[str, Any]:
    # Weights:
    # 1. Passage Citability (35%)
    # 2. Search Crawler Access (25%)
    # 3. Schema Entity Disambiguation (25%)
    # 4. Technical / llms.txt readiness (15%)

    p_score = passage_data.get("average_citability", 50.0)
    c_score = crawler_data.get("search_bots_score", 100.0)
    s_score = schema_data.get("score", 0.0)
    l_score = llms_data.get("score", 0.0)

    overall = round((p_score * 0.35) + (c_score * 0.25) + (s_score * 0.25) + (l_score * 0.15), 1)

    # Platform specific sub-scores
    # Google AI Overviews: High correlation with Schema + Passage citability + Googlebot
    google_aio = round((p_score * 0.45) + (s_score * 0.35) + (c_score * 0.20), 1)
    
    # ChatGPT Search: Strong correlation with OAI-SearchBot + Entities + Citability
    chatgpt = round((c_score * 0.40) + (p_score * 0.35) + (s_score * 0.25), 1)
    
    # Perplexity: High correlation with Citability + Factual density + PerplexityBot
    perplexity = round((p_score * 0.50) + (c_score * 0.30) + (s_score * 0.20), 1)

    # Top recommendations
    recommendations = []
    if c_score < 100:
        recommendations.append("Ensure 'OAI-SearchBot', 'Claude-SearchBot', and 'PerplexityBot' are explicitly allowed in robots.txt.")
    if p_score < 70:
        recommendations.append("Front-load factual definitions in the first 40-60 words of each section and format key answers into 134-167 word blocks.")
    if not schema_data.get("same_as_links"):
        recommendations.append("Add 'sameAs' entity links in JSON-LD (Wikidata, Wikipedia, LinkedIn, YouTube) to establish authoritative entity graph connections.")
    if not schema_data.get("has_person_author"):
        recommendations.append("Implement 'Person' author schema with explicit credentials and publication dates to boost E-E-A-T citation confidence.")
    if not llms_data.get("present"):
        recommendations.append("Deploy a structured '/llms.txt' file at the domain root with clean Markdown links and core factual claims.")

    if len(recommendations) < 3:
        recommendations.append("Incorporate specific statistical figures with publication dates (+37% citation boost per Princeton KDD 2024 study).")
        recommendations.append("Structure comparison queries with HTML tables rather than text paragraphs (+40% extraction rate).")

    return {
        "overall_score": overall,
        "platform_scores": {
            "google_ai_overviews": min(100.0, google_aio),
            "chatgpt_search": min(100.0, chatgpt),
            "perplexity_ai": min(100.0, perplexity)
        },
        "component_scores": {
            "passage_citability": p_score,
            "crawler_access": c_score,
            "schema_entity_graph": s_score,
            "llms_readiness": l_score
        },
        "recommendations": recommendations[:5]
    }

def print_terminal_geo_report(url: str, geo_result: Dict[str, Any], passage_data: Dict[str, Any], crawler_data: Dict[str, Any], schema_data: Dict[str, Any], llms_data: Dict[str, Any]):
    if not HAS_RICH:
        print(f"\n=== CitationPulse GEO Audit: {url} ===")
        print(f"Overall GEO Readiness Score: {geo_result['overall_score']}/100")
        for plat, sc in geo_result['platform_scores'].items():
            print(f"- {plat}: {sc}/100")
        print("\nTop Recommendations:")
        for r in geo_result['recommendations']:
            print(f"- {r}")
        return

    console = Console()

    score = geo_result["overall_score"]
    score_color = "green" if score >= 80 else ("yellow" if score >= 55 else "red")
    
    header = Text()
    header.append("CitationPulse: Generative Engine Optimization (GEO) Auditor\n", style="bold magenta")
    header.append(f"Target: {url}\n", style="bold white")
    header.append(f"GEO Readiness Score: {score}/100\n", style=f"bold {score_color}")
    header.append(f"Analyzed Passages: {passage_data.get('total_analyzed_passages')} | High-Probability Snippets: {passage_data.get('high_potential_citable_blocks')}", style="dim")

    console.print(Panel(header, border_style="magenta"))

    # Platform Scores Table
    plat_table = Table(title="AI Search Engine Readiness Breakdown", show_header=True, header_style="bold cyan")
    plat_table.add_column("AI Search Surface", style="white")
    plat_table.add_column("Score", style="bold")
    plat_table.add_column("Primary Selection Logic", style="dim")

    plat_table.add_row("Google AI Overviews & AI Mode", f"{geo_result['platform_scores']['google_ai_overviews']}/100", "Top 10 classic rankings + Schema.org + citable answer blocks")
    plat_table.add_row("ChatGPT Search (GPT-4o)", f"{geo_result['platform_scores']['chatgpt_search']}/100", "OAI-SearchBot access + entity authority + factual claims")
    plat_table.add_row("Perplexity AI Search", f"{geo_result['platform_scores']['perplexity_ai']}/100", "Freshness + 134-167 word passages + cited statistics (+37%)")

    console.print(plat_table)

    # AI Crawler Table
    crawl_table = Table(title="2026 AI Search Crawler Access (robots.txt)", show_header=True, header_style="bold blue")
    crawl_table.add_column("Crawler Name", style="cyan")
    crawl_table.add_column("Category", style="dim")
    crawl_table.add_column("Governs", style="white")
    crawl_table.add_column("Status", style="bold")

    for c in crawler_data.get("results", []):
        st_color = "green" if c["status"] == "ALLOWED" else "red"
        crawl_table.add_row(c["name"], c["type"], c["governs"], f"[{st_color}]{c['status']}[/{st_color}]")

    console.print(crawl_table)

    # Top Citability Candidates
    if passage_data.get("top_candidates"):
        cand_table = Table(title="Top Extracted Citable Snippets (High AI Probability)", show_header=True, header_style="bold green")
        cand_table.add_column("Score", style="bold yellow")
        cand_table.add_column("Length", style="dim")
        cand_table.add_column("Candidate Passage Preview", style="white")

        for cand in passage_data["top_candidates"]:
            cand_table.add_row(f"{cand['score']}/100", f"{cand['word_count']} w", cand["preview"])

        console.print(cand_table)

    # Recommendations Panel
    rec_text = Text()
    for i, r in enumerate(geo_result["recommendations"], 1):
        rec_text.append(f"{i}. {r}\n", style="bold white")

    console.print(Panel(rec_text, title="Highest-Impact GEO Recommendations", border_style="yellow"))

def export_geo_markdown(url: str, geo_result: Dict[str, Any], passage_data: Dict[str, Any], crawler_data: Dict[str, Any], schema_data: Dict[str, Any], llms_data: Dict[str, Any]) -> str:
    md = []
    md.append(f"# CitationPulse GEO Forensic Audit: {url}\n")
    md.append(f"**Overall GEO Readiness Score**: {geo_result['overall_score']}/100\n")
    
    md.append("## 1. Platform Citability Breakdown\n")
    md.append("| AI Search Surface | Citability Score | Key Factor |")
    md.append("|:---|:---:|:---|")
    md.append(f"| **Google AI Overviews & Mode** | `{geo_result['platform_scores']['google_ai_overviews']}/100` | Schema parity + first 30% front-loaded answer blocks |")
    md.append(f"| **ChatGPT Search** | `{geo_result['platform_scores']['chatgpt_search']}/100` | OAI-SearchBot crawl access + entity disambiguation |")
    md.append(f"| **Perplexity AI** | `{geo_result['platform_scores']['perplexity_ai']}/100` | 134-167w optimal passage blocks + statistics density |")

    md.append("\n## 2. 2026 AI Crawler Access Matrix\n")
    md.append("| Crawler | Capability Governed | Status |")
    md.append("|:---|:---|:---:|")
    for c in crawler_data.get("results", []):
        md.append(f"| **{c['name']}** ({c['type']}) | {c['governs']} | **{c['status']}** |")

    md.append("\n## 3. Top Citable Content Passages\n")
    for i, cand in enumerate(passage_data.get("top_candidates", []), 1):
        md.append(f"### Candidate {i} (Citability: {cand['score']}/100 | {cand['word_count']} words)\n")
        md.append(f"> {cand['full_text']}\n")

    md.append("## 4. Highest-Impact GEO Recommendations\n")
    for i, r in enumerate(geo_result["recommendations"], 1):
        md.append(f"{i}. **{r}**")

    return "\n".join(md)
