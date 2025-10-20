# Skill Extractor

A comprehensive tool for analyzing Claude Code commands and agents, identifying reusable components, and extracting them into properly structured skills.

## Overview

The Skill Extractor helps you:
- Analyze existing commands/agents for extractable components
- Identify scripts, references, and assets that should be separated
- Create properly structured skills with migration guidance
- Validate skill structure and packaging for distribution
- Refactor monolithic commands into modular, reusable skills

## Quick Start

### 1. Analyze a Command or Agent

```bash
./scripts/skill-extract.sh analyze ~/.claude/commands/mine/novel-planner.md --verbose
```

This will:
- Scan the file for extractable components
- Identify scripts, references, and assets
- Calculate extraction potential
- Save results to `analysis.json`

### 2. Extract Components

```bash
./scripts/skill-extract.sh extract analysis.json --name novel-planning-templates
```

This will:
- Create the skill directory structure
- Extract components to appropriate locations
- Generate SKILL.md
- Create a detailed migration report

### 3. One-Step Process

```bash
./scripts/skill-extract.sh full ~/.claude/agents/mine/article-forge.md \
    --name writing-tools \
    --output ./skills
```

This combines analysis and extraction in one command.

### 4. Package for Distribution

```bash
python3 scripts/package_skill.py ./writing-tools
```

This will:
- Validate the skill structure
- Check YAML frontmatter and naming conventions
- Create a distributable zip package
- Provide installation instructions

## What Gets Extracted?

### Scripts (`scripts/` directory)
- Code blocks with >20 lines
- Reusable processing logic
- Utility functions
- Shell command sequences

**Example**: Data processing pipelines, file manipulation utilities, report generators

### References (`references/` directory)
- Documentation >500 words
- Style guides
- Format specifications
- Comprehensive examples

**Example**: Writing style guides, API documentation, template specifications

### Assets (`assets/` directory)
- Templates and boilerplate
- Configuration examples
- Report structures
- Project scaffolding

**Example**: Report templates, character profile templates, configuration files

## Directory Structure

After extraction:

```
{skill-name}/
├── SKILL.md                    # Main skill definition with frontmatter
├── scripts/                    # Executable scripts (if any)
│   ├── process_data.py
│   └── generate_report.sh
├── references/                 # Reference documentation (if any)
│   ├── style-guide.md
│   └── api-spec.md
├── assets/                     # Templates and resources (if any)
│   ├── report-template.md
│   └── config-example.yaml
└── migration-report.md         # Detailed integration instructions
```

## Usage Examples

### Example 1: Extract Templates from Novel Planner

```bash
# Analyze the novel-planner command
./scripts/skill-extract.sh analyze ~/.claude/commands/mine/novel-planner.md

# Review the analysis
cat analysis.json

# Extract identified components
./scripts/skill-extract.sh extract analysis.json \
    --name novel-planning-templates \
    --output ~/my-skills
```

**Result**: Creates `novel-planning-templates` skill with:
- `assets/character-profile.md`
- `assets/chapter-blueprint.md`
- `assets/scene-card.md`
- Detailed migration report

### Example 2: Extract Analysis Tools from Agent

```bash
# One-step extraction from agent
./scripts/skill-extract.sh full ~/.claude/agents/mine/show-tell-analyzer.md \
    --name narrative-analysis-tools \
    --verbose
```

**Result**: Creates `narrative-analysis-tools` skill with:
- `scripts/analyze_show_tell.py`
- `scripts/generate_heatmap.py`
- `references/analysis-methodology.md`

### Example 3: Batch Analysis

```bash
# Analyze all commands
for file in ~/.claude/commands/mine/*.md; do
    echo "Analyzing: $(basename "$file")"
    ./scripts/skill-extract.sh analyze "$file" > "$(basename "$file" .md)-analysis.json"
done

# Review analyses and extract selectively
```

## Migration Process

After extraction:

1. **Review the Migration Report**
   ```bash
   cat {skill-name}/migration-report.md
   ```

2. **Update Original File**
   - Replace embedded content with skill references
   - Update script execution commands
   - Reference documentation locations
   - Point to template assets

3. **Test Functionality**
   - Verify all scripts execute
   - Confirm references load correctly
   - Test template usage
   - Ensure original functionality preserved

4. **Update Documentation**
   - Document skill dependency
   - Update usage instructions
   - Note new file locations

## Packaging and Distribution

After creating and validating a skill, you can package it for distribution:

### Validate Skill Structure

```bash
python3 scripts/package_skill.py ./my-extracted-skill --validate-only
```

This checks:
- SKILL.md exists with valid YAML frontmatter
- Required fields: `name` and `description`
- Proper directory structure
- Script executability and naming conventions
- Bundled resources (scripts/, references/, assets/)

### Create Distribution Package

```bash
python3 scripts/package_skill.py ./my-extracted-skill --output ./packages
```

Creates a `.zip` file containing:
- Complete skill directory structure
- All bundled resources
- Proper permissions preserved
- Installation instructions

### Install Packaged Skill

```bash
# Extract to Claude Code skills directory
unzip my-extracted-skill.zip -d ~/.claude/skills/

# Or create development symlink
ln -s /path/to/my-extracted-skill ~/.claude/skills/my-extracted-skill
```

## Command Reference

### Analyze Command

```bash
./scripts/skill-extract.sh analyze <input-file> [options]
```

Options:
- `-v, --verbose` - Show detailed analysis output
- `-o, --output FILE` - Save analysis to specific file (default: analysis.json)

### Extract Command

```bash
./scripts/skill-extract.sh extract <analysis-file> [options]
```

Required:
- `--name <skill-name>` - Name for the extracted skill

Options:
- `-o, --output DIR` - Output directory (default: current directory)

### Full Command

```bash
./scripts/skill-extract.sh full <input-file> [options]
```

Required:
- `--name <skill-name>` - Name for the extracted skill

Options:
- `-o, --output DIR` - Output directory (default: current directory)
- `-v, --verbose` - Show detailed progress

## Python Scripts

### analyze_command.py

Direct usage:

```bash
python3 scripts/analyze_command.py ~/.claude/commands/mine/example.md \
    --output analysis.json \
    --verbose
```

### extract_components.py

Direct usage:

```bash
python3 scripts/extract_components.py analysis.json \
    --name my-skill \
    --output ./skills
```

### package_skill.py

Validates skill structure and creates distributable zip packages:

```bash
python3 scripts/package_skill.py path/to/skill-directory [options]
```

Options:
- `-o, --output DIR` - Output directory for package (default: current directory)
- `--validate-only` - Only validate, don't create package
- `--skip-validation` - Skip validation and create package directly

Example:

```bash
# Validate and package a skill
python3 scripts/package_skill.py ./novel-planning-templates

# Validate only (no package creation)
python3 scripts/package_skill.py ./my-skill --validate-only

# Package without validation
python3 scripts/package_skill.py ./my-skill --skip-validation --output ./packages
```

The script performs comprehensive validation:
- Checks for required SKILL.md file
- Validates YAML frontmatter (name and description fields)
- Verifies directory structure
- Checks script permissions and naming conventions
- Creates a zip package with proper structure

## Configuration

### Size Thresholds

Edit `scripts/analyze_command.py` to adjust:

```python
MIN_SCRIPT_LINES = 20      # Minimum lines for script extraction
MIN_REFERENCE_WORDS = 500  # Minimum words for reference extraction
MIN_ASSET_SIZE = 100       # Minimum characters for asset extraction
```

### Confidence Scoring

Extracted components receive confidence scores (0.0-1.0):
- **0.8-1.0**: High confidence - clearly extractable
- **0.6-0.8**: Medium confidence - likely extractable
- **0.4-0.6**: Low confidence - borderline
- **<0.4**: Don't extract

## Best Practices

### When to Extract

✅ **DO Extract**:
- Large reference documentation (>1000 words)
- Reusable scripts (>50 lines)
- Standard templates
- Stable, well-defined components

❌ **DON'T Extract**:
- Core workflow logic
- Small snippets (<20 lines)
- Tightly coupled code
- Volatile/experimental code

### Naming Conventions

**Skills**: Use kebab-case
- `novel-planning-templates`
- `data-processing-utils`
- `narrative-analysis-tools`

**Scripts**: Use snake_case
- `process_data.py`
- `generate_report.py`
- `analyze_text.py`

**References**: Use kebab-case
- `style-guide.md`
- `api-specification.md`
- `best-practices.md`

**Assets**: Use descriptive names
- `report-template.md`
- `character-profile.md`
- `config-example.yaml`

## Troubleshooting

### Analysis finds nothing

**Cause**: File might be too small or well-structured already
**Solution**: Check size thresholds; review with `--verbose`

### Extraction fails

**Cause**: Invalid analysis file or permission issues
**Solution**: Verify analysis.json is valid; check write permissions

### Components not working after extraction

**Cause**: Dependencies not properly resolved
**Solution**: Review migration report; check file paths

### Original file breaks after migration

**Cause**: Incomplete migration or incorrect references
**Solution**: Follow migration report exactly; test incrementally

### Package validation fails

**Cause**: Missing SKILL.md, invalid frontmatter, or incorrect structure
**Solution**: Ensure SKILL.md exists with required `name` and `description` fields; check directory structure matches skill standards

### Packaged skill won't install

**Cause**: Incorrect zip structure or missing files
**Solution**: Verify zip contains skill directory with all components; check SKILL.md frontmatter is valid YAML

## Reference Documentation

- **Skill Patterns**: `references/skill-patterns.md` - Pattern recognition guide
- **Extraction Criteria**: `references/extraction-criteria.md` - When and how to extract

## Contributing

To improve the skill extractor:

1. **Enhance Pattern Matching**: Update patterns in `analyze_command.py`
2. **Refine Criteria**: Adjust thresholds and scoring
3. **Add Templates**: Create additional asset templates
4. **Improve Reports**: Enhance migration report generation

## Integration with Skill Creator

This skill works alongside the `skill-creator` skill:

- **skill-extractor**: Refactors existing commands/agents
- **skill-creator**: Creates new skills from scratch
- **Together**: Build a comprehensive skill ecosystem

## License

Part of the Claude Code skills ecosystem.

## Support

For issues or questions:
1. Review the migration report
2. Check reference documentation
3. Examine example extractions
4. Validate analysis output

---

**Remember**: The Skill Extractor is non-destructive. Your original files remain unchanged. Always test extracted skills before removing original content.
