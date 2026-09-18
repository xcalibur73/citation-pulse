"""
Schema.org Entity Disambiguation and Knowledge Graph Auditor for GEO.
"""

import json
from typing import Dict, Any, List
from bs4 import BeautifulSoup

def audit_schema_entities(soup: BeautifulSoup) -> Dict[str, Any]:
    schemas = []
    scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
    
    for s in scripts:
        raw = s.string or s.text or ""
        raw = raw.strip()
        if not raw:
            continue
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list):
                schemas.extend(parsed)
            elif isinstance(parsed, dict):
                if "@graph" in parsed and isinstance(parsed["@graph"], list):
                    schemas.extend(parsed["@graph"])
                else:
                    schemas.append(parsed)
        except Exception:
            pass

    types_found = []
    has_org = False
    has_person = False
    has_article = False
    same_as_links = []
    entity_ids = []

    for s in schemas:
        t = s.get("@type", "")
        if isinstance(t, list):
            types_found.extend(t)
        else:
            types_found.append(str(t))

        if "@id" in s:
            entity_ids.append(s["@id"])

        if t in ["Organization", "Corporation", "LocalBusiness"]:
            has_org = True
        if t in ["Person", "Author"]:
            has_person = True
        if t in ["Article", "BlogPosting", "TechArticle", "NewsArticle"]:
            has_article = True

        # Extract sameAs
        same_as = s.get("sameAs", [])
        if isinstance(same_as, str):
            same_as = [same_as]
        if isinstance(same_as, list):
            same_as_links.extend(same_as)

    # Disambiguation score
    score = 30 if schemas else 0
    if has_org:
        score += 20
    if has_person:
        score += 20
    if same_as_links:
        score += 20
    if len(entity_ids) >= 2:
        score += 10

    score = min(100, score)

    # Wikidata / Wikipedia presence
    has_wikidata = any("wikidata.org" in link.lower() for link in same_as_links)
    has_wikipedia = any("wikipedia.org" in link.lower() for link in same_as_links)

    return {
        "score": score,
        "total_schemas": len(schemas),
        "types_found": list(set(types_found)),
        "has_organization": has_org,
        "has_person_author": has_person,
        "has_article": has_article,
        "same_as_links_count": len(same_as_links),
        "same_as_links": same_as_links[:10],
        "has_wikidata_link": has_wikidata,
        "has_wikipedia_link": has_wikipedia
    }
