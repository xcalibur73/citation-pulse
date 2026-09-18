"""
Passage Citability Scorer based on Princeton KDD 2024 GEO Research
and empirical AI search extraction models.
"""

import re
from typing import Dict, Any, List

# Princeton KDD 2024 GEO Weights & Boosts
CITATION_BOOST = 0.40      # +40%
STATISTICS_BOOST = 0.37    # +37%
QUOTATION_BOOST = 0.30     # +30%
TECHNICAL_BOOST = 0.18     # +18%
VOCAB_BOOST = 0.15         # +15%
KEYWORD_STUFFING_PENALTY = -0.15 # -10% to -15%

# Regex patterns for empirical extraction
STAT_PATTERN = re.compile(r"(\b\d+(\.\d+)?%|\$\d+(\.\d+)?|\b\d{1,3}(,\d{3})+|\b(19|20)\d{2}\b)", re.IGNORECASE)
QUOTE_PATTERN = re.compile(r'["“][^"”]{10,200}["”]', re.UNICODE)
ATTRIBUTION_PATTERN = re.compile(
    r"\b(according to|reported by|study by|source:|data from|research by|cited by|published in|as noted by|found that)\b",
    re.IGNORECASE
)
DEFINITION_PATTERN = re.compile(r"\b([A-Z][a-zA-Z0-9\s]{2,30})\s+(is|refers to|denotes|represents|is defined as)\s+", re.IGNORECASE)

def score_passage(text: str) -> Dict[str, Any]:
    words = text.split()
    word_count = len(words)
    if word_count == 0:
        return {"score": 0, "length_verdict": "EMPTY", "word_count": 0}

    # 1. Optimal Length Score (Optimal: 134-167 words, Acceptable: 60-220 words)
    if 134 <= word_count <= 167:
        length_score = 100
        length_verdict = "OPTIMAL (134-167 words)"
    elif 90 <= word_count <= 210:
        length_score = 80
        length_verdict = "GOOD (90-210 words)"
    elif 40 <= word_count <= 260:
        length_score = 55
        length_verdict = "MARGINAL (40-260 words)"
    else:
        length_score = 25
        length_verdict = "POOR (Too short or too long for concise citation)"

    # 2. Evidence Signals
    stats_matches = STAT_PATTERN.findall(text)
    quotes_matches = QUOTE_PATTERN.findall(text)
    attr_matches = ATTRIBUTION_PATTERN.findall(text)
    def_matches = DEFINITION_PATTERN.findall(text)

    has_stats = len(stats_matches) > 0
    has_quotes = len(quotes_matches) > 0
    has_attr = len(attr_matches) > 0
    has_def = len(def_matches) > 0

    # 3. Vocabulary Richness (Type-Token Ratio)
    unique_words = set(w.lower().strip('.,!?"\'') for w in words)
    ttr = len(unique_words) / word_count if word_count > 0 else 0

    # 4. Keyword Stuffing Detection
    word_counts = {}
    for w in words:
        wl = w.lower().strip('.,!?"\'')
        if len(wl) > 3:
            word_counts[wl] = word_counts.get(wl, 0) + 1
    
    max_freq = max(word_counts.values()) if word_counts else 0
    is_stuffed = (max_freq / word_count) > 0.08 if word_count >= 50 else False

    # Weighted composite score
    base_score = length_score * 0.35
    evidence_score = 0.0
    if has_attr:
        evidence_score += CITATION_BOOST * 100
    if has_stats:
        evidence_score += STATISTICS_BOOST * 100
    if has_quotes:
        evidence_score += QUOTATION_BOOST * 100
    if has_def:
        evidence_score += TECHNICAL_BOOST * 100
    if ttr >= 0.65:
        evidence_score += VOCAB_BOOST * 100

    evidence_score = min(65.0, evidence_score)
    final_score = base_score + evidence_score

    if is_stuffed:
        final_score *= (1.0 + KEYWORD_STUFFING_PENALTY)

    final_score = round(min(100.0, max(0.0, final_score)), 1)

    return {
        "score": final_score,
        "word_count": word_count,
        "length_verdict": length_verdict,
        "signals": {
            "has_definition": has_def,
            "has_statistics": has_stats,
            "has_attributions": has_attr,
            "has_quotes": has_quotes,
            "unique_vocab_ratio": round(ttr, 2),
            "keyword_stuffed": is_stuffed
        },
        "stats_count": len(stats_matches),
        "quotes_count": len(quotes_matches)
    }

def analyze_document_passages(paragraphs: List[str]) -> Dict[str, Any]:
    scored_passages = []
    total_words = 0
    high_potential_count = 0

    for i, p in enumerate(paragraphs):
        p_clean = " ".join(p.split()).strip()
        if len(p_clean.split()) < 20:
            continue

        scored = score_passage(p_clean)
        scored["index"] = i
        scored["preview"] = p_clean[:140] + ("..." if len(p_clean) > 140 else "")
        scored["full_text"] = p_clean
        
        # Position bonus (first 30% of page has 44% citation probability)
        is_frontloaded = (i <= max(2, int(len(paragraphs) * 0.30)))
        scored["is_frontloaded"] = is_frontloaded
        if is_frontloaded and scored["score"] >= 60:
            scored["score"] = min(100.0, round(scored["score"] * 1.15, 1))

        if scored["score"] >= 75:
            high_potential_count += 1

        total_words += scored["word_count"]
        scored_passages.append(scored)

    # Sort to identify top citable snippets
    scored_passages.sort(key=lambda x: x["score"], reverse=True)

    avg_score = round(sum(p["score"] for p in scored_passages) / max(1, len(scored_passages)), 1)
    top_candidates = scored_passages[:3]

    return {
        "average_citability": avg_score,
        "total_analyzed_passages": len(scored_passages),
        "high_potential_citable_blocks": high_potential_count,
        "top_candidates": top_candidates,
        "all_passages": scored_passages
    }
