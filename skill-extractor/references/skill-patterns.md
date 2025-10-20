# Skill Pattern Recognition Guide

This document defines the patterns used to identify extractable components in Claude Code commands and agents.

## Component Types

### 1. Scripts (scripts/ directory)

**Definition**: Executable code that performs deterministic operations, suitable for standalone execution.

**Recognition Patterns**:

- Code blocks with significant logic (>20 lines)
- Repeated operations across multiple sections
- File processing or data transformation logic
- Utility functions that could be reused
- Shell command sequences that form complete workflows

**Code Block Markers**:
```
```bash
```python
```javascript
```ruby
```perl
<script>...</script>
```

**Quality Indicators**:
- Clear input/output interface
- Minimal dependencies on surrounding context
- Reusable across different scenarios
- Well-defined purpose
- Could run independently

**Examples**:
```python
# GOOD: Clear, reusable script
def process_data(input_file, output_file):
    # 50+ lines of processing logic
    # Clear parameters
    # Returns useful results
```

```bash
# GOOD: Complete workflow
#!/bin/bash
# Create directory structure
# Process files
# Generate output
# Cleanup
```

### 2. References (references/ directory)

**Definition**: Documentation, guides, specifications, or reference material intended to be consulted rather than executed.

**Recognition Patterns**:

- Large documentation blocks (>500 words)
- Style guides and conventions
- Format specifications
- Template documentation
- Best practices lists
- API documentation
- Schema definitions
- Comprehensive examples

**Section Markers**:
- Headers containing: "Reference", "Guide", "Manual", "Documentation", "Specification", "Format", "Template", "Style", "Convention", "Standard"
- Structured lists and tables
- Detailed explanations
- Example collections

**Quality Indicators**:
- Reference material, not procedural instructions
- Rarely changes
- Large enough to warrant separation (>500 words)
- Self-contained documentation
- Useful across multiple contexts

**Examples**:
```markdown
## Style Guide Reference

### Writing Standards
- Comprehensive list of rules
- Detailed explanations
- Many examples
- Cross-references to other standards

### Format Specifications
- Complete structure definitions
- Field descriptions
- Validation rules
- Example documents
```

### 3. Assets (assets/ directory)

**Definition**: Template files, boilerplate code, or resource files used in output generation.

**Recognition Patterns**:

- Template structures (HTML, Markdown, JSON, YAML, XML)
- Boilerplate project files
- Starter kits or scaffolding
- Report templates
- Configuration file templates
- Design resources (if text-based)

**Template Markers**:
```
```markdown
```html
```json
```yaml
```xml
<template>...</template>
```

**Quality Indicators**:
- Intended to be copied and populated
- Consistent structure
- Placeholder values or variables
- Reusable across instances
- Not documentation (that's references/)

**Examples**:
```markdown
# Report Template

## Title: {TITLE}
**Date**: {DATE}
**Author**: {AUTHOR}

## Summary
{SUMMARY_CONTENT}

## Details
{DETAILED_CONTENT}
```

```json
{
  "project": "{PROJECT_NAME}",
  "version": "{VERSION}",
  "dependencies": []
}
```

## Core Workflow (stays in SKILL.md)

**Definition**: The procedural logic, orchestration steps, and user interaction that defines how the skill works.

**Characteristics**:
- Decision trees and conditional logic
- User interaction flows
- Orchestration of scripts/references/assets
- Step-by-step procedures
- When/how to use components
- Integration instructions

**Keep in SKILL.md**:
```markdown
## Workflow

1. Ask user for preferences
2. IF choice A: execute script_a.py
3. ELSE: execute script_b.py
4. Load reference from references/guide.md
5. Populate template from assets/template.md
6. Generate output
```

## Size Thresholds

### Scripts
- **Minimum**: 20 lines of code
- **Optimal**: 50+ lines
- **Rationale**: Smaller scripts not worth extracting; better inline

### References
- **Minimum**: 500 words
- **Optimal**: 1000+ words
- **Rationale**: Small reference material is better in SKILL.md for quick access

### Assets
- **Minimum**: 100 characters
- **Optimal**: 200+ characters
- **Rationale**: Tiny templates can stay inline; only extract substantial ones

## Anti-Patterns: What NOT to Extract

### Don't Extract:
1. **Tightly Coupled Logic**: Code that depends heavily on surrounding context
2. **Configuration**: Settings that customize the skill behavior
3. **Small Snippets**: Code blocks <20 lines
4. **Brief Documentation**: Explanations <500 words
5. **Inline Examples**: Small illustrative code samples
6. **Metadata**: YAML frontmatter and skill metadata
7. **Usage Instructions**: How to use the skill itself

### Keep These in SKILL.md:
```markdown
---
name: example-skill
description: This stays in SKILL.md
---

# Skill Title

Brief overview stays here.

## When to Use
User guidance stays here.

## Quick Examples
Short examples stay here:
```bash
# 5-line example - keep inline
do_thing()
```

## Integration
How components work together - stays here.
```

## Confidence Scoring

Each identified component receives a confidence score (0.0-1.0):

### High Confidence (0.8-1.0)
- Meets all size thresholds
- Clear reusability
- Well-defined boundaries
- Standard format
- Common pattern

### Medium Confidence (0.6-0.8)
- Meets size thresholds
- Some reusability
- Moderately defined boundaries
- Custom format
- Less common pattern

### Low Confidence (0.4-0.6)
- Borderline size
- Questionable reusability
- Unclear boundaries
- Non-standard format
- Rare pattern

### Very Low (<0.4)
- Don't extract
- Keep in SKILL.md

## Decision Tree

```
Is it code?
├─ Yes: Is it >20 lines?
│  ├─ Yes: Does it have clear I/O?
│  │  ├─ Yes: Extract to scripts/ [confidence: 0.8]
│  │  └─ No: Keep in SKILL.md
│  └─ No: Keep in SKILL.md
└─ No: Is it documentation?
   ├─ Yes: Is it >500 words?
   │  ├─ Yes: Is it reference material?
   │  │  ├─ Yes: Extract to references/ [confidence: 0.9]
   │  │  └─ No: Is it a template?
   │  │     ├─ Yes: Extract to assets/ [confidence: 0.85]
   │  │     └─ No: Keep in SKILL.md
   │  └─ No: Keep in SKILL.md
   └─ No: Keep in SKILL.md
```

## Special Cases

### Multi-File Assets
If a template requires multiple related files:
```
assets/
├── project-template/
│   ├── index.html
│   ├── styles.css
│   └── script.js
```

### Versioned References
If reference material has versions:
```
references/
├── api-v1.md
├── api-v2.md
└── migration-guide.md
```

### Shared Scripts
If multiple skills could use the same script:
- Extract to shared location
- Document in both skill references
- Consider creating a "utils" skill

## Validation Checklist

Before extracting a component, verify:

- [ ] Meets minimum size threshold
- [ ] Has clear purpose/use case
- [ ] Is actually reusable
- [ ] Can function independently
- [ ] Is appropriately categorized
- [ ] Has reasonable confidence score
- [ ] Won't break original functionality
- [ ] Improves overall clarity

## Examples from Real Commands

### Good Extraction: Novel Planner Templates

**Original** (in command file):
```markdown
## Character Profile Template
[50 lines of template structure]

## Chapter Blueprint Template
[100 lines of template structure]

## Scene Card Template
[30 lines of template structure]
```

**After Extraction**:
```
Skill: novel-planning-templates/
├── SKILL.md (references templates)
├── assets/
│   ├── character-profile.md
│   ├── chapter-blueprint.md
│   └── scene-card.md
```

### Good Extraction: Analysis Scripts

**Original** (in agent file):
```python
# Show/Tell Analysis Algorithm
def analyze_show_tell_ratio(text):
    # 150 lines of analysis logic
    # Pattern matching
    # Statistical calculations
    # Report generation
```

**After Extraction**:
```
Skill: narrative-analysis/
├── SKILL.md
├── scripts/
│   ├── analyze_show_tell.py
│   └── generate_report.py
```

### Bad Extraction: Small Snippet

**Don't Extract This**:
```python
# Too small, keep inline
def format_date(date):
    return date.strftime("%Y-%m-%d")
```

**Don't Extract This**:
```markdown
## Quick Tips
- Tip 1
- Tip 2
- Tip 3
```
(Too small, keep in SKILL.md)
