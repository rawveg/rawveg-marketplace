# Extraction Criteria and Best Practices

This document defines when and how to extract components from Claude Code commands and agents into skills.

## Extraction Philosophy

**Goal**: Transform monolithic commands/agents into modular, reusable skills while preserving functionality and improving maintainability.

**Principles**:
1. **Progressive Disclosure**: Keep frequently needed info in SKILL.md, load details on-demand
2. **Single Responsibility**: Each extracted component serves one clear purpose
3. **Token Efficiency**: Reduce context window usage by loading only what's needed
4. **Reusability**: Extracted components should be useful across multiple contexts
5. **Non-Destructive**: Original files remain unchanged during extraction

## When to Extract

### Extract When:

✅ **Component is Reusable**
- Used in multiple places within the command/agent
- Could be useful in other commands/agents
- Represents a general-purpose utility

✅ **Component is Large**
- Scripts: >20 lines of code
- References: >500 words of documentation
- Assets: >100 characters in templates
- Extraction reduces cognitive load

✅ **Component is Stable**
- Rarely changes
- Well-defined interface
- Mature implementation
- Not experimental

✅ **Component is Independent**
- Can function without surrounding context
- Has clear inputs/outputs
- Doesn't rely on ephemeral state
- Self-contained logic

✅ **Component Improves Clarity**
- Extraction makes main workflow clearer
- Reduces nesting/complexity
- Separates concerns effectively
- Improves readability

### Don't Extract When:

❌ **Component is Tightly Coupled**
- Depends heavily on surrounding code
- Shares state with parent
- Requires deep knowledge of context
- Would need many parameters

❌ **Component is Small**
- <20 lines of code for scripts
- <500 words for documentation
- <100 characters for templates
- Extraction adds overhead

❌ **Component is Volatile**
- Changes frequently
- Still experimental
- Poorly defined interface
- Under active development

❌ **Component is Core Workflow**
- Defines the main skill logic
- Orchestrates other components
- Handles user interaction
- Implements decision trees

❌ **Extraction Reduces Clarity**
- Makes workflow harder to understand
- Adds unnecessary indirection
- Fragments cohesive logic
- Confuses rather than clarifies

## Extraction Priority

### High Priority (Extract First)

1. **Large Reference Documentation** (>1000 words)
   - Style guides
   - Format specifications
   - Comprehensive examples
   - API documentation

2. **Reusable Scripts** (>50 lines)
   - Data processing utilities
   - File manipulation tools
   - Report generators
   - Analysis algorithms

3. **Standard Templates** (>200 chars)
   - Report formats
   - Configuration templates
   - Output structures
   - Boilerplate code

### Medium Priority (Extract If Clear Benefit)

1. **Moderate Documentation** (500-1000 words)
   - Usage guides
   - Best practices
   - Troubleshooting tips
   - FAQ sections

2. **Utility Scripts** (20-50 lines)
   - Helper functions
   - Format converters
   - Validators
   - Simple processors

3. **Custom Templates** (100-200 chars)
   - Specialized formats
   - Domain-specific structures
   - Custom outputs

### Low Priority (Keep Inline)

1. **Brief Documentation** (<500 words)
   - Quick tips
   - Short examples
   - Basic usage
   - Overview text

2. **Code Snippets** (<20 lines)
   - Simple functions
   - One-line utilities
   - Inline examples
   - Configuration code

3. **Mini Templates** (<100 chars)
   - Simple formats
   - Basic structures
   - Placeholder text

## Quality Criteria

### For Scripts

**Must Have**:
- Clear purpose statement
- Defined inputs and outputs
- Error handling
- Usage documentation
- Appropriate shebang line (for scripts)

**Should Have**:
- Command-line argument parsing
- Help/usage message
- Exit codes
- Logging capability
- Type hints (Python)

**Nice to Have**:
- Unit tests
- Configuration file support
- Progress indicators
- Verbose mode

### For References

**Must Have**:
- Clear topic/subject
- Organized structure
- Complete information
- Accurate content

**Should Have**:
- Table of contents (if >2000 words)
- Cross-references
- Examples
- Update date

**Nice to Have**:
- Visual aids
- Comparison tables
- Decision trees
- Quick reference section

### For Assets

**Must Have**:
- Clear purpose
- Consistent format
- Placeholder indicators
- Usage instructions

**Should Have**:
- Validation rules
- Format specification
- Example values
- Field descriptions

**Nice to Have**:
- Multiple variants
- Versioning
- Schema definition
- Automated validation

## Extraction Process

### Phase 1: Analysis

1. **Identify Candidates**
   - Scan for large code blocks
   - Find documentation sections
   - Locate template structures
   - Note repeated patterns

2. **Assess Suitability**
   - Check size thresholds
   - Evaluate reusability
   - Consider independence
   - Estimate impact

3. **Calculate Confidence**
   - Apply scoring rubric
   - Consider special cases
   - Review edge cases
   - Document reasoning

### Phase 2: Extraction

1. **Create Structure**
   - Make skill directory
   - Create subdirectories (scripts/, references/, assets/)
   - Initialize SKILL.md

2. **Extract Components**
   - Copy to appropriate directories
   - Preserve formatting
   - Add metadata
   - Update permissions (scripts)

3. **Generate Documentation**
   - Create SKILL.md content
   - Write migration report
   - Document usage
   - List prerequisites

### Phase 3: Validation

1. **Verify Extraction**
   - Check all files created
   - Validate formats
   - Test scripts
   - Review documentation

2. **Test Functionality**
   - Execute scripts
   - Load references
   - Use templates
   - Verify outputs

3. **Assess Impact**
   - Measure size reduction
   - Calculate token savings
   - Evaluate clarity improvement
   - Document benefits

## Integration Patterns

### Pattern 1: Direct Script Execution

**Before**:
```markdown
Process data using this inline script:
```python
[50 lines of processing code]
```
```

**After**:
```markdown
Process data:
```bash
python scripts/process_data.py input.csv output.csv
```

See `scripts/process_data.py` for processing logic.
```

### Pattern 2: Reference Loading

**Before**:
```markdown
## Style Guide
[1000 lines of style documentation]
```

**After**:
```markdown
## Style Guide

Load style specifications from `references/style-guide.md` when needed.

Quick reference:
- Use active voice
- Prefer showing over telling
- [3-5 key points]

See full guide for details.
```

### Pattern 3: Template Utilization

**Before**:
```markdown
Use this report template:
```markdown
[Large template structure]
```
```

**After**:
```markdown
Generate report:
```bash
cp assets/report-template.md output/report.md
# Populate template with data
```

Template location: `assets/report-template.md`
```

## Common Pitfalls

### Pitfall 1: Over-Extraction

**Problem**: Extracting everything, including tiny snippets
**Solution**: Follow size thresholds; keep small items inline
**Example**: Don't extract 5-line helper functions

### Pitfall 2: Under-Extraction

**Problem**: Not extracting large, clearly reusable components
**Solution**: Be bold with large (>1000 word) reference docs
**Example**: Extract comprehensive style guides

### Pitfall 3: Poor Naming

**Problem**: Generic names like `script.py`, `template.md`
**Solution**: Use descriptive, purpose-driven names
**Example**: `generate_report.py`, `character-profile-template.md`

### Pitfall 4: Breaking Dependencies

**Problem**: Extracted component needs parent context
**Solution**: Make components truly independent or don't extract
**Example**: Add parameters to scripts instead of relying on environment

### Pitfall 5: Incomplete Migration

**Problem**: Original file still has embedded content
**Solution**: Follow migration report completely
**Example**: Remove redundant content after confirming extraction works

## Testing Strategy

### Pre-Extraction Tests

1. **Document Current Behavior**
   - Run original command/agent
   - Capture outputs
   - Note dependencies
   - Record performance

2. **Identify Test Cases**
   - Happy path scenarios
   - Edge cases
   - Error conditions
   - Integration points

### Post-Extraction Tests

1. **Verify Extracted Components**
   - Scripts execute successfully
   - References load correctly
   - Templates are valid
   - All files accessible

2. **Test Integration**
   - Updated command/agent works
   - Outputs match original
   - No broken references
   - Performance acceptable

3. **Validate Functionality**
   - All features work
   - Edge cases handled
   - Errors caught appropriately
   - Dependencies resolved

## Success Metrics

### Quantitative Metrics

- **Size Reduction**: Original size vs new size
- **Token Efficiency**: Tokens used in context
- **Reuse Count**: Times components used elsewhere
- **Load Time**: Time to load when needed

### Qualitative Metrics

- **Clarity**: Easier to understand?
- **Maintainability**: Easier to update?
- **Reusability**: Useful in other contexts?
- **Modularity**: Clean separation of concerns?

## Decision Framework

Use this framework to decide on extraction:

```
1. Is component >minimum size threshold?
   NO → Keep inline
   YES → Continue

2. Is component reusable?
   NO → Keep inline
   YES → Continue

3. Can component function independently?
   NO → Keep inline (or refactor first)
   YES → Continue

4. Does extraction improve clarity?
   NO → Keep inline
   YES → Continue

5. Is component stable (won't change often)?
   NO → Consider keeping inline
   YES → EXTRACT

6. Determine type:
   - Executable code → scripts/
   - Reference docs → references/
   - Templates → assets/
```

## Examples

### Example 1: Novel Planning Templates

**Analysis**:
- Size: 200+ lines of templates
- Reusable: Yes, across different novels
- Independent: Yes, templates are self-contained
- Stable: Yes, templates rarely change
- **Decision**: EXTRACT to assets/

**Extraction**:
```
novel-planning-templates/
├── SKILL.md
├── assets/
│   ├── character-profile.md
│   ├── chapter-blueprint.md
│   └── scene-card.md
└── migration-report.md
```

### Example 2: Data Processing Script

**Analysis**:
- Size: 150 lines of Python
- Reusable: Yes, general-purpose data processing
- Independent: Yes, clear input/output
- Stable: Yes, mature implementation
- **Decision**: EXTRACT to scripts/

**Extraction**:
```
data-processing-utils/
├── SKILL.md
├── scripts/
│   ├── process_csv.py
│   └── generate_report.py
└── migration-report.md
```

### Example 3: Quick Tips (DON'T EXTRACT)

**Analysis**:
- Size: 50 words
- Reusable: Somewhat
- Independent: Yes
- Stable: Yes
- **Decision**: KEEP INLINE (too small)

## Maintenance

### Ongoing Considerations

- **Updates**: When to update extracted components vs original
- **Versioning**: How to handle component versions
- **Dependencies**: Managing component dependencies
- **Documentation**: Keeping migration reports current

### Best Practices

1. **Document Changes**: Log all extractions
2. **Test Thoroughly**: Before and after extraction
3. **Communicate**: If others use the command/agent
4. **Version Control**: Git-track both original and skills
5. **Review Regularly**: Reassess extraction decisions periodically
