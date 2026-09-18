"""
llms.txt Standard Validator and Generator.
Validates syntax against the emerging machine-readable LLM navigation standard.
"""

import urllib.request
import urllib.parse
from typing import Dict, Any

def fetch_llms_txt(base_url: str) -> Dict[str, Any]:
    parsed = urllib.parse.urlparse(base_url)
    llms_url = f"{parsed.scheme}://{parsed.netloc}/llms.txt"
    llms_full_url = f"{parsed.scheme}://{parsed.netloc}/llms-full.txt"
    
    headers = {"User-Agent": "Mozilla/5.0 CitationPulse/1.0"}
    
    result = {
        "url": llms_url,
        "present": False,
        "full_present": False,
        "content": "",
        "validation_errors": [],
        "score": 0
    }
    
    # Check llms.txt
    try:
        req = urllib.request.Request(llms_url, headers=headers)
        with urllib.request.urlopen(req, timeout=8) as resp:
            if resp.status == 200:
                result["present"] = True
                result["content"] = resp.read().decode("utf-8", errors="replace")
    except Exception:
        pass
        
    # Check llms-full.txt
    try:
        req_full = urllib.request.Request(llms_full_url, headers=headers)
        with urllib.request.urlopen(req_full, timeout=8) as resp:
            if resp.status == 200:
                result["full_present"] = True
    except Exception:
        pass

    if result["present"]:
        # Validate format
        text = result["content"]
        lines = [l.strip() for l in text.splitlines() if l.strip()]
        
        has_h1 = any(l.startswith("# ") for l in lines)
        has_blockquote = any(l.startswith("> ") for l in lines)
        has_links = any("[" in l and "](" in l for l in lines)
        
        score = 40
        if has_h1:
            score += 20
        else:
            result["validation_errors"].append("Missing H1 site title header ('# Site Name')")
            
        if has_blockquote:
            score += 20
        else:
            result["validation_errors"].append("Missing blockquote site description ('> Brief summary')")
            
        if has_links:
            score += 20
        else:
            result["validation_errors"].append("Missing structured markdown links ('- [Title](url): Description')")
            
        result["score"] = score
    else:
        result["score"] = 0
        
    return result

def generate_llms_txt_template(site_title: str, domain: str, description: str) -> str:
    return f"""# {site_title}

> {description}

## Core Documentation & Articles
- [{site_title} Architecture]({domain}/architecture): Technical foundation and performance standards.
- [Case Studies & Benchmarks]({domain}/case-studies): Empirical results and empirical data.
- [Tools & Diagnostics]({domain}/tools): Interactive technical diagnostic utilities.

## Key Factual Entities
- Founded: 2024
- Primary Focus: Core Web Vitals, Technical SEO Architecture, and AI Citability Optimization.
- Verification Platform: {domain}
"""
