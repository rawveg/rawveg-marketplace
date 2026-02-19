# Agent Role Patterns by Task Category

Read this file when designing the team in Phase 2 to select appropriate roles and workflow shapes.

## Contents
1. [Content & Writing](#content--writing)
2. [Software Development](#software-development)
3. [Research & Analysis](#research--analysis)
4. [Marketing & Strategy](#marketing--strategy)
5. [Design & Creative](#design--creative)
6. [Data & Reporting](#data--reporting)
7. [Universal Support Roles](#universal-support-roles)

---

## Content & Writing

**Example tasks:** Article, blog post, white paper, report, book chapter, documentation, newsletter

### Roles
| Role | Responsibility |
|------|---------------|
| Researcher | Gather facts, sources, statistics, and background context |
| Outline Architect | Structure the piece: sections, argument flow, key points per section |
| Drafter | Write full draft from outline and research notes |
| Content Editor | Improve clarity, flow, structure, transitions, and argument coherence |
| Style Editor | Apply tone/voice/style guidelines; remove passive voice, jargon, clichés |
| Fact Checker | Verify all claims against research sources; flag unsupported assertions |
| Proofreader | Final grammar, spelling, punctuation pass |

### Workflow
```
Researcher → Outline Architect → [GATE 1] → Drafter → [GATE 2] → Content Editor → Style Editor → [GATE 3] → Fact Checker → Proofreader
```

### Common Gates
- Gate 1 (post-outline): Human — does the structure match the goal?
- Gate 2 (post-draft): Human or automated — does it cover all sections, meet word count?
- Gate 3 (post-edit): Automated critic — readability score, style compliance

### Lean Version (4 agents)
Researcher → Drafter → Editor → Fact Checker

---

## Software Development

**Example tasks:** New feature, bug fix, refactor, API design, system design

### Roles
| Role | Responsibility |
|------|---------------|
| Requirements Analyst | Clarify and formalise requirements; produce acceptance criteria |
| Architect | Design the approach: components, interfaces, data flows, tech choices |
| Implementer | Write the code |
| Test Writer | Write unit/integration tests |
| Code Reviewer | Review for correctness, security, style, edge cases |
| Documentation Writer | Update or write docs, docstrings, README |

### Workflow
```
Requirements Analyst → Architect → [GATE 1] → Implementer + Test Writer (parallel) → [GATE 2] → Code Reviewer → [GATE 3] → Documentation Writer
```

### Common Gates
- Gate 1 (post-architecture): Human — approve design before coding
- Gate 2 (post-implementation): Automated — do tests pass? Are all acceptance criteria met?
- Gate 3 (post-review): Automated critic — does reviewer approve? Are all review comments addressed?

---

## Research & Analysis

**Example tasks:** Market research, competitive analysis, literature review, feasibility study, due diligence

### Roles
| Role | Responsibility |
|------|---------------|
| Scoper | Define research questions, scope, and methodology |
| Primary Researcher | Gather raw data, sources, case studies |
| Secondary Researcher | Cross-reference and expand with additional sources |
| Synthesiser | Identify patterns, themes, and key insights across all sources |
| Critic | Challenge findings: what's missing? What's weak? What contradicts? |
| Report Writer | Structure and write the final deliverable |

### Workflow
```
Scoper → [GATE 1] → Primary Researcher + Secondary Researcher (parallel) → Synthesiser → Critic → [GATE 2] → Report Writer
```

### Common Gates
- Gate 1 (post-scope): Human — validate research questions before starting
- Gate 2 (post-synthesis + critique): Human or automated — are findings substantiated and complete?

---

## Marketing & Strategy

**Example tasks:** Campaign plan, brand strategy, product launch plan, messaging framework, content calendar

### Roles
| Role | Responsibility |
|------|---------------|
| Market Analyst | Research audience, competitors, trends, positioning landscape |
| Strategist | Define positioning, goals, channels, and high-level approach |
| Messaging Copywriter | Develop core messages, taglines, value propositions |
| Campaign Planner | Translate strategy into concrete tactics, timeline, channels |
| Brand Reviewer | Ensure consistency with brand voice, guidelines, and values |
| Critic | Challenge strategy: what could fail? What's missing? |

### Workflow
```
Market Analyst → Strategist → [GATE 1] → Messaging Copywriter + Campaign Planner (parallel) → Brand Reviewer → Critic → [GATE 2]
```

### Common Gates
- Gate 1 (post-strategy): Human — approve strategic direction before tactical work
- Gate 2 (post-review + critique): Human — final approval before delivery

---

## Design & Creative

**Example tasks:** Product concept, UX flow, visual brief, creative brief, storyboard, naming

### Roles
| Role | Responsibility |
|------|---------------|
| Creative Researcher | Gather inspiration, references, analogues, trends |
| Concept Generator | Produce multiple distinct conceptual directions (typically 3) |
| Concept Developer | Develop the chosen direction in depth |
| Critic | Stress-test the concept: originality, feasibility, audience fit |
| Refiner | Incorporate critique, polish the concept |
| Brief Writer | Document the final concept as a deliverable brief |

### Workflow
```
Creative Researcher → Concept Generator → [GATE 1] → Concept Developer → Critic → [GATE 2] → Refiner → Brief Writer
```

### Common Gates
- Gate 1 (post-concepts): Human — choose which concept direction to develop
- Gate 2 (post-critique): Human or automated — does the developed concept pass the critique?

---

## Data & Reporting

**Example tasks:** Data analysis, dashboard design, metrics report, KPI summary, forecasting

### Roles
| Role | Responsibility |
|------|---------------|
| Data Scoper | Define questions, metrics, data sources, and output format |
| Data Gatherer | Collect and structure relevant data |
| Analyst | Perform analysis: calculations, trends, anomalies, correlations |
| Visualisation Designer | Design charts, tables, and visual presentation |
| Interpreter | Write narrative: what does the data mean? What actions does it suggest? |
| Reviewer | Sanity-check numbers, flag inconsistencies, verify conclusions |

### Workflow
```
Data Scoper → [GATE 1] → Data Gatherer → Analyst → Visualisation Designer + Interpreter (parallel) → Reviewer → [GATE 2]
```

### Common Gates
- Gate 1 (post-scope): Human — validate questions and data sources
- Gate 2 (post-review): Human — approve findings before distribution

---

## Universal Support Roles

These roles can be added to any team regardless of category:

| Role | When to add |
|------|-------------|
| **Orchestrator** | Always — manages the team, gates, and loops (this is the lead agent) |
| **Quality Critic** | Any automated gate — reviews output against defined criteria, returns pass/fail + notes |
| **Consolidator** | When parallel agents produce outputs that need merging into one coherent document |
| **Stakeholder Proxy** | When user needs are complex — simulates the target audience to stress-test output |

---

## Workflow Shape Reference

| Shape | When to use |
|-------|------------|
| **Linear pipeline** | Tasks are strictly sequential; each depends on prior output |
| **Parallel branches** | Independent subtasks can run simultaneously; consolidate before next gate |
| **Iterative loop** | Output must meet a quality bar; critic → revise → re-check |
| **Hybrid** | Most real tasks: linear at top level, parallel within stages, loops at gates |
