# Skill Extractor

---
name: skill-extractor
description: Analyzes Claude Code commands and agents to identify and extract reusable components into properly structured skills with migration reports
---

## Purpose

This skill analyzes existing Claude Code commands and agents to identify reusable components that should be extracted into standalone skills. It creates properly structured skills following Claude Code conventions while preserving the original files and providing detailed migration guidance.

## When to Use

Use this skill when you:
- Have commands or agents with embedded templates, reference materials, or reusable scripts
- Want to modularize large, complex commands/agents
- Need to identify opportunities for code reuse across your Claude Code ecosystem
- Want to refactor commands/agents to follow skill-based architecture

## How It Works

The skill performs comprehensive analysis to identify extractable components:

### 1. Component Analysis

The analyzer scans for:

**Scripts Candidates (`scripts/` directory)**:
- Repeated code blocks that execute deterministic operations
- Shell scripts, Python scripts, or other executables
- File manipulation utilities
- Processing pipelines

**Reference Material (`references/` directory)**:
- Templates and format specifications
- Style guides and writing standards
- Documentation that should be loaded on-demand
- Large reference tables or datasets
- API specifications

**Assets (`assets/` directory)**:
- Template files used in output generation
- Boilerplate code or project structures
- Images, fonts, or design resources
- Example files or starter kits

**Core Workflow (stays in SKILL.md)**:
- Primary procedural instructions
- Workflow orchestration
- Decision trees and logic
- User interaction patterns

### 2. Extraction Process

When you invoke the skill with a command or agent file path:

```bash
# Analyze and extract from a command
@skill-extractor analyze --input ~/.claude/commands/mine/agent-forge.md

# Analyze and extract from an agent
@skill-extractor analyze --input ~/.claude/agents/mine/novel-chapter-writer.md

# Batch analyze multiple files
@skill-extractor analyze --input ~/.claude/commands/mine/*.md
```

The skill will:

1. **Parse** the input file to understand structure and content
2. **Identify** extractable components using pattern matching
3. **Extract** components into appropriate directories
4. **Generate** the skill structure with proper SKILL.md
5. **Create** migration report detailing required changes

### 3. Output Structure

All extracted skills are created in the current working directory:

```
{current_working_directory}/
└── {extracted-skill-name}/
    ├── SKILL.md                    # Main skill definition
    ├── scripts/                    # Executable scripts (if applicable)
    │   └── example_script.py
    ├── references/                 # Reference documentation (if applicable)
    │   ├── templates.md
    │   └── style-guide.md
    ├── assets/                     # Output resources (if applicable)
    │   └── template.txt
    └── migration-report.md         # Detailed migration instructions
```

## Analysis Methodology

### Pattern Recognition

The analyzer uses sophisticated pattern matching to identify:

**Template Patterns**:
- Markdown code blocks with repeated structure
- YAML/JSON configuration templates
- Format specifications and examples
- Document structure definitions

**Reference Documentation**:
- Large explanatory blocks (>1000 words)
- Style guides and conventions
- Comprehensive lists and tables
- API documentation sections

**Script Candidates**:
- Bash command sequences
- Python code blocks
- File processing operations
- Deterministic workflows

**Workflow Logic** (remains in SKILL.md):
- Conditional decision points
- User interaction flows
- Orchestration steps
- High-level procedures

### Extraction Criteria

Components are extracted when they meet these criteria:

1. **Reusability**: Used or could be used in multiple contexts
2. **Size**: Large enough to warrant separation (scripts >50 lines, references >500 words)
3. **Independence**: Can function standalone without core workflow context
4. **Stability**: Unlikely to change with each workflow execution

## Migration Report

The migration report provides step-by-step guidance for updating the original command/agent:

```markdown
# Migration Report: {Original File Name}

## Executive Summary
- **Extraction Date**: [timestamp]
- **Components Extracted**: [count]
- **Original File Size**: [size]
- **New Skill Size**: [size]
- **Reduction**: [percentage]

## Extracted Components

### 1. Scripts Extracted
- **Location**: `scripts/process_data.py`
- **Original Lines**: 145-298
- **Purpose**: Data processing pipeline
- **Usage**: Execute via `python scripts/process_data.py [args]`

### 2. References Extracted
- **Location**: `references/template-guide.md`
- **Original Lines**: 50-430
- **Purpose**: Template formatting specifications
- **Usage**: Read when formatting templates

### 3. Assets Extracted
- **Location**: `assets/report-template.md`
- **Original Lines**: 500-650
- **Purpose**: Report output template
- **Usage**: Copy and populate for report generation

## Required Changes to Original File

### Update SKILL.md References

Replace embedded content with skill references:

**Before**:
```markdown
<large template section>
```

**After**:
```markdown
For template specifications, refer to `references/template-guide.md` in this skill directory.
```

### Update Script Execution

**Before**:
```bash
# Inline bash commands
mkdir -p output/
python << EOF
[large Python script]
EOF
```

**After**:
```bash
# Execute extracted script
python scripts/process_data.py --output output/
```

### Update Asset References

**Before**:
```markdown
## Report Template
[entire template embedded]
```

**After**:
```markdown
## Report Template
Use template from `assets/report-template.md`, customize as needed.
```

## Testing Checklist

After migration, verify:
- [ ] All script executions work correctly
- [ ] Reference materials are accessible when needed
- [ ] Asset files are properly utilized
- [ ] Original functionality is preserved
- [ ] Skill can be reused in other contexts
```

## Integration with Skill Creation Workflow

This skill works in conjunction with `skill-creator`:

1. **skill-extractor**: Analyzes existing commands/agents, extracts components
2. **skill-creator**: Creates new skills from scratch with user requirements
3. **Together**: Refactor existing code into modular, reusable skills

## Advanced Features

### Dependency Detection

Identifies dependencies between extracted components:
- Scripts that reference assets
- References that link to other references
- Cross-component relationships

### Size Optimization

Recommends which components to extract based on:
- Token usage reduction
- Loading time optimization
- Memory footprint
- Reusability potential

### Conflict Detection

Flags potential issues:
- Name conflicts with existing skills
- Circular dependencies
- Missing file references
- Broken paths after extraction

## Best Practices

### When to Extract

**DO extract** when:
- Component is reused in multiple places
- Content is large and rarely changes
- Material is reference-only (not procedural)
- Script can run independently

**DON'T extract** when:
- Content is core to workflow logic
- Extraction would reduce clarity
- Component is tightly coupled to parent
- Size is minimal (<100 words for references, <20 lines for scripts)

### Naming Conventions

**Skill Names**:
- Use kebab-case: `template-processor`, `style-validator`
- Be descriptive: `novel-writing-templates` not `templates`
- Indicate domain: `publishing-formats`, `data-processing-utils`

**File Names**:
- Scripts: `action_noun.py` (e.g., `generate_report.py`)
- References: `topic-name.md` (e.g., `style-guide.md`)
- Assets: `purpose.extension` (e.g., `report-template.md`)

## Error Handling

The skill handles common issues:

**Invalid Input**:
- Missing files: Reports error with path
- Unsupported format: Lists supported formats
- Access denied: Requests permission

**Extraction Conflicts**:
- Existing skill directory: Offers to append timestamp or skip
- Partial extraction: Saves progress, reports issues
- Invalid component: Skips with warning

**Output Issues**:
- Insufficient space: Checks before creation
- Permission denied: Reports specific location
- Path too long: Suggests shorter names

## Usage Examples

### Example 1: Extract Templates from Novel Planner

```bash
# Input: ~/.claude/commands/mine/novel-planner.md
# Contains: Multiple large templates for character profiles, chapter blueprints

# Run extraction
@skill-extractor analyze --input ~/.claude/commands/mine/novel-planner.md

# Output: novel-planning-templates/
#   ├── SKILL.md (references templates)
#   ├── references/
#   │   ├── character-profile.md
#   │   ├── chapter-blueprint.md
#   │   └── scene-card.md
#   └── migration-report.md
```

### Example 2: Extract Analysis Scripts from Agent

```bash
# Input: ~/.claude/agents/mine/show-tell-analyzer.md
# Contains: Python analysis algorithms

# Run extraction
@skill-extractor analyze --input ~/.claude/agents/mine/show-tell-analyzer.md

# Output: narrative-analysis-tools/
#   ├── SKILL.md
#   ├── scripts/
#   │   ├── analyze_show_tell.py
#   │   └── generate_heatmap.py
#   └── migration-report.md
```

### Example 3: Batch Extract from Multiple Commands

```bash
# Analyze entire commands directory
@skill-extractor analyze --input ~/.claude/commands/mine/*.md --batch

# Creates multiple skills, consolidated report
# Output: batch-extraction-report.md + individual skills
```

## Validation and Quality Assurance

After extraction, the skill validates:

1. **Completeness**: All referenced files exist
2. **Syntax**: SKILL.md frontmatter is valid YAML
3. **Structure**: Follows skill conventions
4. **Documentation**: Migration report is comprehensive
5. **Testing**: Provides verification checklist

## Execution

To use this skill:

1. **Invoke** with target command or agent file path
2. **Review** analysis and proposed extractions
3. **Confirm** or adjust extraction plan
4. **Execute** extraction
5. **Review** migration report
6. **Update** original file following migration guide
7. **Test** to ensure functionality preserved
8. **Package** new skill for distribution if desired

The skill leverages:
- `scripts/analyze_command.py` - Analyzes command/agent structure
- `scripts/extract_components.py` - Extracts identified components
- `scripts/generate_skill.py` - Creates SKILL.md structure
- `references/skill-patterns.md` - Pattern matching rules
- `references/extraction-criteria.md` - Component extraction guidelines

This systematic approach ensures clean extraction, preservation of functionality, and clear migration paths for modernizing your Claude Code ecosystem.
