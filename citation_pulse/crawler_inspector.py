"""
AI Crawler Access Inspector.
Tests robots.txt against distinct 2026 AI Search vs Training crawlers.
"""

import urllib.request
import urllib.parse
from typing import Dict, Any, List

CRAWLER_DEFINITIONS = [
    # Search Citability Crawlers (Essential for being cited in answers)
    {"name": "OAI-SearchBot", "type": "Search Citability", "governs": "ChatGPT Search retrieval and answers"},
    {"name": "Claude-SearchBot", "type": "Search Citability", "governs": "Claude.ai web search citations"},
    {"name": "PerplexityBot", "type": "Search Citability", "governs": "Perplexity AI search engine citations"},
    {"name": "Googlebot", "type": "Search Citability", "governs": "Google Search, AI Overviews & AI Mode"},
    
    # Model Training Crawlers (Can be allowed or blocked by business preference)
    {"name": "GPTBot", "type": "Model Training", "governs": "OpenAI foundation model training only"},
    {"name": "ClaudeBot", "type": "Model Training", "governs": "Anthropic foundation model training only"},
    {"name": "Google-Extended", "type": "Model Training", "governs": "Gemini & Vertex AI model training / grounding"},
    {"name": "Applebot-Extended", "type": "Model Training", "governs": "Apple Intelligence training opt-out"},
    {"name": "CCBot", "type": "Model Training", "governs": "Common Crawl dataset scraping"}
]

def parse_robots_rules(robots_txt: str) -> Dict[str, Dict[str, List[str]]]:
    rules = {}
    current_agents = []
    in_directives = False
    
    for line in robots_txt.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
            
        if ":" not in line:
            continue
            
        key, val = line.split(":", 1)
        key = key.strip().lower()
        val = val.strip()
        
        if key == "user-agent":
            if in_directives:
                current_agents = []
                in_directives = False
            current_agents.append(val.lower())
        elif key == "disallow":
            in_directives = True
            for agent in current_agents:
                rules.setdefault(agent, {"disallow": [], "allow": []})["disallow"].append(val)
        elif key == "allow":
            in_directives = True
            for agent in current_agents:
                rules.setdefault(agent, {"disallow": [], "allow": []})["allow"].append(val)
            
    return rules

def test_crawler_access(base_url: str, robots_txt: str) -> Dict[str, Any]:
    rules = parse_robots_rules(robots_txt)
    wildcard_rules = rules.get("*", {"disallow": [], "allow": []})
    
    results = []
    search_allowed = 0
    search_total = 0
    
    for crawler in CRAWLER_DEFINITIONS:
        name = crawler["name"]
        name_lower = name.lower()
        c_type = crawler["type"]
        governs = crawler["governs"]
        
        disallowed = False
        reason = "Explicitly or implicitly allowed"
        
        if name_lower in rules:
            agent_rule = rules[name_lower]
            disallows = agent_rule.get("disallow", [])
            allows = agent_rule.get("allow", [])
            
            has_root_disallow = "/" in disallows or any(d == "/" for d in disallows)
            has_root_allow = "/" in allows or any(a == "/" for a in allows)
            
            if has_root_disallow and not has_root_allow:
                disallowed = True
                reason = f"Explicitly blocked via 'Disallow: /' for User-agent: {name}"
            elif has_root_allow:
                disallowed = False
                reason = f"Explicitly allowed via 'Allow: /' for User-agent: {name}"
        else:
            disallows = wildcard_rules.get("disallow", [])
            allows = wildcard_rules.get("allow", [])
            has_root_disallow = "/" in disallows or any(d == "/" for d in disallows)
            has_root_allow = "/" in allows or any(a == "/" for a in allows)
            
            if has_root_disallow and not has_root_allow:
                disallowed = True
                reason = "Blocked by wildcard 'User-agent: *' directive"
                
        status = "BLOCKED" if disallowed else "ALLOWED"
        
        if c_type == "Search Citability":
            search_total += 1
            if not disallowed:
                search_allowed += 1
                
        results.append({
            "name": name,
            "type": c_type,
            "status": status,
            "governs": governs,
            "reason": reason
        })
        
    search_ratio = round((search_allowed / max(1, search_total)) * 100, 1)
    
    return {
        "search_bots_allowed_percent": search_ratio,
        "search_bots_score": round((search_allowed / max(1, search_total)) * 100),
        "results": results
    }

def fetch_robots_txt(base_url: str) -> Dict[str, Any]:
    parsed = urllib.parse.urlparse(base_url)
    robots_url = f"{parsed.scheme}://{parsed.netloc}/robots.txt"
    
    try:
        req = urllib.request.Request(robots_url, headers={"User-Agent": "Mozilla/5.0 CitationPulse/1.0"})
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read().decode("utf-8", errors="replace")
            return {
                "url": robots_url,
                "found": True,
                "status_code": resp.status,
                "content": content
            }
    except Exception as e:
        return {
            "url": robots_url,
            "found": False,
            "error": str(e),
            "content": ""
        }
