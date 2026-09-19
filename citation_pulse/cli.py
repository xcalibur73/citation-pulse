"""
CitationPulse CLI: Generative Engine Optimization (GEO) & AI Citability Auditor.
"""

import sys
import os
import json
import argparse
import urllib.request
import urllib.parse
from bs4 import BeautifulSoup

from citation_pulse.passage_scorer import (
    analyze_document_passages,
    compute_text_density,
    prune_low_density_passages
)
from citation_pulse.crawler_inspector import fetch_robots_txt, test_crawler_access
from citation_pulse.schema_auditor import audit_schema_entities
from citation_pulse.llms_validator import fetch_llms_txt, generate_llms_txt_template
from citation_pulse.report_generator import (
    calculate_composite_geo_score,
    print_terminal_geo_report,
    export_geo_markdown
)

def fetch_page_html(url: str, timeout: int = 15) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
    }
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req, timeout=timeout) as resp:
        return resp.read().decode("utf-8", errors="replace")

def extract_content_passages(soup: BeautifulSoup) -> list:
    import copy
    doc_copy = copy.copy(soup)
    # Remove non-content tags from working copy
    for tag in doc_copy(["script", "style", "nav", "footer", "header", "noscript", "svg", "aside"]):
        tag.decompose()

    passages = []
    # Search for main content containers first
    main_el = doc_copy.find("main") or doc_copy.find("article") or doc_copy.find("body")
    if not main_el:
        main_el = doc_copy

    elements = main_el.find_all(["p", "blockquote", "li"])
    for el in elements:
        text = " ".join(el.get_text().split()).strip()
        if len(text.split()) >= 15:
            # Crawl4ai-inspired text-to-link density evaluation
            links = el.find_all("a")
            link_text = " ".join(a.get_text() for a in links).strip()
            density = compute_text_density(text, len(link_text))
            # Filter out link-heavy navigation blocks masquerading as content
            if density >= 0.45:
                passages.append(text)

    return prune_low_density_passages(passages)

def run_audit(url: str) -> dict:
    # 1. Fetch main HTML
    html = fetch_page_html(url)
    soup = BeautifulSoup(html, "html.parser")

    # 2. Audit Schema.org JSON-LD entities
    schema_data = audit_schema_entities(soup)

    # 3. Extract passages and score citability
    paragraphs = extract_content_passages(soup)
    passage_data = analyze_document_passages(paragraphs)

    # 4. Inspect robots.txt for AI search and training crawlers
    robots_res = fetch_robots_txt(url)
    crawler_data = test_crawler_access(url, robots_res.get("content", ""))

    # 5. Check llms.txt validation
    llms_data = fetch_llms_txt(url)

    # 6. Calculate composite GEO score
    geo_result = calculate_composite_geo_score(
        passage_data=passage_data,
        crawler_data=crawler_data,
        schema_data=schema_data,
        llms_data=llms_data
    )

    page_title = soup.title.string.strip() if soup.title and soup.title.string else url

    return {
        "url": url,
        "page_title": page_title,
        "geo_result": geo_result,
        "passage_data": passage_data,
        "crawler_data": crawler_data,
        "schema_data": schema_data,
        "llms_data": llms_data
    }

def main():
    from citation_pulse import __version__
    parser = argparse.ArgumentParser(
        prog="citation-pulse",
        description="CitationPulse: Generative Engine Optimization (GEO) & AI Citability Auditor"
    )
    parser.add_argument("url", nargs="?", help="Target URL to audit for AI search citability")
    parser.add_argument(
        "--version",
        action="version",
        version=f"CitationPulse v{__version__}"
    )
    parser.add_argument(
        "--output", "-o",
        choices=["terminal", "markdown", "json"],
        default="terminal",
        help="Output display format (default: terminal)"
    )
    parser.add_argument(
        "--save", "-s",
        help="Path to save markdown or JSON report"
    )
    parser.add_argument(
        "--generate-llms",
        action="store_true",
        help="Generate an optimized /llms.txt template for the domain"
    )
    parser.add_argument(
        "--cloud",
        action="store_true",
        help="Generate continuous monitoring audit link on WebAudits.pro"
    )

    args = parser.parse_args()
    if not args.url:
        parser.print_help()
        return 0

    target_url = args.url
    if not target_url.startswith("http://") and not target_url.startswith("https://"):
        target_url = "https://" + target_url

    print(f"[*] Auditing GEO Citability signals for: {target_url} ...")

    try:
        data = run_audit(target_url)
    except Exception as e:
        print(f"[!] Error executing audit: {e}", file=sys.stderr)
        sys.exit(1)

    url = data["url"]
    geo_result = data["geo_result"]
    passage_data = data["passage_data"]
    crawler_data = data["crawler_data"]
    schema_data = data["schema_data"]
    llms_data = data["llms_data"]

    # Handle output
    if args.output == "terminal":
        print_terminal_geo_report(
            url=url,
            geo_result=geo_result,
            passage_data=passage_data,
            crawler_data=crawler_data,
            schema_data=schema_data,
            llms_data=llms_data
        )

    if args.output == "markdown" or args.save:
        md_content = export_geo_markdown(
            url=url,
            geo_result=geo_result,
            passage_data=passage_data,
            crawler_data=crawler_data,
            schema_data=schema_data,
            llms_data=llms_data
        )
        if args.output == "markdown" and not args.save:
            print(md_content)
        if args.save:
            with open(args.save, "w", encoding="utf-8") as f:
                if args.save.endswith(".json") or args.output == "json":
                    json.dump(data, f, indent=2)
                else:
                    f.write(md_content)
            print(f"[+] Audit saved successfully to: {args.save}")

    if args.output == "json" and not args.save:
        print(json.dumps(data, indent=2))

    if args.generate_llms:
        parsed = urllib.parse.urlparse(url)
        domain = f"{parsed.scheme}://{parsed.netloc}"
        title = data.get("page_title", parsed.netloc)
        template = generate_llms_txt_template(
            site_title=title,
            domain=domain,
            description=f"Official technical documentation and verification index for {parsed.netloc}."
        )
        print("\n=== Recommended /llms.txt Template ===")
        print(template)

    if args.cloud:
        cloud_url = f"https://webaudits.pro/tools/geo-audit?url={urllib.parse.quote(url)}"
        print(f"\n[+] WebAudits.pro Cloud Audit Link:")
        print(f"    {cloud_url}")
        print(f"    Features: continuous AI crawler monitoring, bulk sitemap scans, scheduled alerts.")
    elif args.output == "terminal":
        print(f"\n[i] WebAudits.pro Cloud Platform: Run with --cloud or visit https://webaudits.pro/tools/geo-audit for continuous monitoring.")

if __name__ == "__main__":
    main()
