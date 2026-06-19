---
name: notfair-marketing
description: Open-source Claude Code skills for SEO, GEO, Google Ads, and Meta Ads. Connects to live account data via Google Ads MCP, Meta Ads MCP, Google Search Console MCP, and Google Analytics (GA4) MCP to run audits, keyword research, meta tag generation, schema markup, wasted-spend detection, and ad creative analysis directly inside Claude Code.
---

# NotFair Marketing Skills

## Overview

NotFair is a collection of open-source Claude Code skills covering three marketing domains:

- **SEO** — site analysis, keyword research, meta tag optimization, schema markup generation, GEO (generative engine optimization), and content writing.
- **Google Ads** — account audits, wasted-spend detection, search-term cleanup, keyword management, and bid analysis.
- **Meta Ads** — ROAS analysis, creative fatigue detection, audience overlap identification, and campaign health checks.

All skills connect to live data through MCP servers: Google Ads MCP, Meta Ads MCP, Google Search Console MCP, and Google Analytics (GA4) MCP.

Source: [github.com/nowork-studio/NotFair](https://github.com/nowork-studio/NotFair)

## Requirements

- Claude Code with MCP support
- One or more of the following MCP servers configured, depending on which skills you use:
  - [Google Ads MCP](https://github.com/nowork-studio/NotFair) for Google Ads skills
  - [Meta Ads MCP](https://github.com/nowork-studio/NotFair) for Meta Ads skills
  - [Google Search Console MCP](https://github.com/nowork-studio/NotFair) for SEO skills
  - [Google Analytics (GA4) MCP](https://github.com/nowork-studio/NotFair) for analytics-backed SEO skills

## Skill Areas

### SEO (`seo/`)

| Skill | What it does |
|-------|-------------|
| `seo-audit` | Full site SEO audit using Search Console and GA4 data |
| `keyword-research` | Keyword opportunity research with volume and intent analysis |
| `meta-tags-optimizer` | Generate optimized title and description tags |
| `schema-markup-generator` | Create structured data markup for rich results |
| `geo-optimizer` | Optimize content for AI-powered search (GEO) |
| `content-writer` | Write SEO-optimized content briefs and drafts |

### Google Ads (`google-ads/`)

| Skill | What it does |
|-------|-------------|
| `google-ads-audit` | Full account audit: spend, quality scores, and performance trends |
| `google-ads` | General Google Ads management tasks |
| `google-ads-copy` | Generate and review ad copy |
| `google-ads-landing` | Audit landing page relevance vs. ad copy |

### Meta Ads (`meta-ads/`)

| Skill | What it does |
|-------|-------------|
| `meta-ads-audit` | Full Meta Ads account audit: ROAS, creative fatigue, audience overlap |
| `meta-ads` | General Meta Ads management tasks |

## Installation

```bash
# Install from the SkillsForge marketplace
/plugin install notfair-marketing@skillsforge-marketplace
```

Or install directly from the source repository:

```bash
/plugin install github:nowork-studio/NotFair
```

## License

MIT — see [github.com/nowork-studio/NotFair](https://github.com/nowork-studio/NotFair) for details.
