# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.2.1] - 2026-09-24

### Fixed
- Sanitized XML CDATA wrappers (`<![CDATA[...]]>`) and HTML comment blocks in JSON-LD script tags before parsing to prevent extraction errors on WordPress and legacy CMS pages.

### Added
- Linked documentation and quickstart instructions to the interactive web tool on [webaudits.pro/tools/geo-audit](https://webaudits.pro/tools/geo-audit).

## [1.2.0] - 2026-09-20

### Added
- Crawl4AI PruningContentFilter multi-level heuristic alignment:
  - Added `min_words` threshold filtering to discard shallow text fragments (< 8 words) from passage candidate sets.
  - Enhanced legal disclaimer and platform boilerplate filtering for copyright tokens.

## [1.1.0] - 2026-09-20

### Added
- Crawl4AI-inspired text-to-tag density pruning in `passage_scorer.py` and `cli.py`:
  - `compute_text_density()` calculating substantive text ratio vs link anchor text.
  - Automatic filtering of high-link-density elements (e.g. sidebar navigation, breadcrumbs, social share lists).
  - `prune_low_density_passages()` filtering out cookie notices and platform boilerplate prior to passage citability scoring.

## [1.0.0] - 2026-09-19

### Added
- Initial release of citation-pulse: Generative Engine Optimization (GEO) and AI citability auditor implementing Princeton KDD 2024 passage analysis.
- CLI entry point with `--output` (terminal, markdown, json) and `--version` flags.
- Standard PEP 621 packaging via `pyproject.toml`.
- GitHub Actions CI matrix workflow for Python 3.10, 3.11, and 3.12.
- Comprehensive automated unit test suite.
- Integration endpoints for the WebAudits.pro technical audit platform.

### Hardened
- Cross-platform Windows terminal encoding safety (`_safe_str` Unicode sanitization).
- Universal test discovery path resilience.
