#!/usr/bin/env python3
"""
Component Extractor for Skill Creation

This script extracts identified components from commands/agents
and creates the skill directory structure.
"""

import os
import json
import argparse
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class SkillExtractor:
    """Extracts components and creates skill structure."""

    def __init__(self, analysis_file: str, output_dir: str, skill_name: str):
        self.analysis_file = Path(analysis_file)
        self.output_dir = Path(output_dir)
        self.skill_name = skill_name
        self.skill_dir = self.output_dir / skill_name

        # Load analysis results
        with open(self.analysis_file) as f:
            self.analysis = json.load(f)

        # Load original file
        self.original_file = self._find_original_file()
        with open(self.original_file) as f:
            self.original_content = f.read()
            self.original_lines = self.original_content.split('\n')

    def _find_original_file(self) -> Path:
        """Find the original file that was analyzed."""
        filename = self.analysis['filename']
        # Try common locations
        locations = [
            Path(f"~/.claude/commands/mine/{filename}").expanduser(),
            Path(f"~/.claude/agents/mine/{filename}").expanduser(),
            Path(filename)
        ]

        for loc in locations:
            if loc.exists():
                return loc

        raise FileNotFoundError(f"Could not find original file: {filename}")

    def _describe_placeholder(self, placeholder: str) -> str:
        """
        Generate a human-readable description for a placeholder based on its name.
        Uses common naming patterns to infer purpose.
        """
        # Common placeholder patterns and their descriptions
        descriptions = {
            # Counts and numbers
            'count': 'Total count or number',
            'num': 'Number or index',
            'total': 'Total amount or count',
            'index': 'Index position',
            'sequential_number': 'Sequential number in series',

            # Identifiers
            'id': 'Unique identifier',
            'name': 'Name or title',
            'title': 'Title or heading',
            'type': 'Type or category',

            # Line and position info
            'line_num': 'Line number',
            'line_start': 'Starting line number',
            'line_end': 'Ending line number',
            'para_num': 'Paragraph number',

            # Text content
            'content': 'Main content or text',
            'description': 'Description or explanation',
            'text': 'Text content',
            'message': 'Message or note',

            # File and path
            'file': 'File name or path',
            'path': 'File or directory path',
            'filename': 'Name of file',

            # Time and date
            'date': 'Date value',
            'time': 'Time value',
            'timestamp': 'Timestamp',
            'hours': 'Number of hours',

            # Size and metrics
            'size': 'Size measurement',
            'percent': 'Percentage value',
            'score': 'Score or rating',

            # Context-specific
            'chapter': 'Chapter number or name',
            'issue': 'Issue number or description',
            'category': 'Category name',
            'priority': 'Priority level',
            'severity': 'Severity level',
        }

        # Direct match
        if placeholder.lower() in descriptions:
            return descriptions[placeholder.lower()]

        # Pattern matching for common suffixes
        lower_ph = placeholder.lower()
        if lower_ph.endswith('_count'):
            base = lower_ph.replace('_count', '').replace('_', ' ')
            return f"Count of {base}"
        elif lower_ph.endswith('_percent'):
            base = lower_ph.replace('_percent', '').replace('_', ' ')
            return f"Percentage of {base}"
        elif lower_ph.endswith('_hours'):
            base = lower_ph.replace('_hours', '').replace('_', ' ')
            return f"Number of {base} hours"
        elif lower_ph.endswith('_score'):
            base = lower_ph.replace('_score', '').replace('_', ' ')
            return f"Score for {base}"
        elif lower_ph.endswith('_num'):
            base = lower_ph.replace('_num', '').replace('_', ' ')
            return f"{base.title()} number"

        # Fallback: convert snake_case to readable text
        readable = placeholder.replace('_', ' ').title()
        return f"{readable} value"

    def _generate_purpose_detail(self, extracted: Dict) -> str:
        """Generate detailed purpose description based on extracted components."""
        details = []

        # Add asset-specific purposes
        if extracted['assets']:
            asset_purposes = []
            for asset in extracted['assets']:
                if asset.get('context_description'):
                    # Use existing description if available
                    desc = asset['context_description'].strip()
                    if desc and not desc.endswith('.'):
                        desc += '.'
                    asset_purposes.append(f"- {desc}")
                elif asset.get('context_heading'):
                    # Fall back to heading-based description
                    heading = asset['context_heading']
                    asset_purposes.append(f"- {heading} template for consistent formatting.")

            if asset_purposes:
                details.append("The templates include:\n" + "\n".join(asset_purposes))

        # Add script-specific purposes
        if extracted['scripts']:
            details.append(f"Contains {len(extracted['scripts'])} executable script(s) for automation.")

        # Add reference-specific purposes
        if extracted['references']:
            details.append(f"Includes {len(extracted['references'])} reference document(s) for standardization.")

        return "\n\n".join(details) if details else "Extracted components provide standardized, reusable functionality."

    def _generate_when_to_use(self, extracted: Dict) -> str:
        """Generate 'When to Use' bullet points based on extracted components."""
        use_cases = []

        # Asset-based use cases
        if extracted['assets']:
            for asset in extracted['assets']:
                heading = asset.get('context_heading', asset['name'].replace('-', ' ').replace('.md', ''))
                placeholders = asset.get('placeholders', [])

                if placeholders:
                    use_cases.append(f"- Consistent {heading.lower()} formatting with {len(placeholders)} customizable field(s)")
                else:
                    use_cases.append(f"- Standard {heading.lower()} structure")

        # Script-based use cases
        if extracted['scripts']:
            use_cases.append("- Automated processing tasks that can be reused across projects")

        # Reference-based use cases
        if extracted['references']:
            use_cases.append("- Projects requiring standardized guidelines and reference material")

        # General use case
        use_cases.append("- Maintaining consistency across multiple commands or projects")

        return "\n".join(use_cases)

    def extract(self):
        """Perform extraction and create skill structure."""
        # Check if extraction is recommended (YAGNI check)
        if not self.analysis.get('extraction_recommended', True):
            reason = self.analysis.get('recommendation_reason', 'Extraction not worthwhile')
            print(f"\n{'='*60}")
            print(f"❌ EXTRACTION NOT RECOMMENDED")
            print(f"{'='*60}\n")
            print(f"Reason: {reason}")
            print(f"\nYAGNI Principle: Don't break up commands/agents unless there's")
            print(f"clear value in extraction. Keep components inline to avoid")
            print(f"unnecessary overhead and complexity.\n")
            print(f"{'='*60}\n")
            import sys
            sys.exit(2)  # Exit with code 2 to indicate "not recommended"

        print(f"Creating skill: {self.skill_name}")
        print(f"Output directory: {self.skill_dir}")

        # Create skill directory structure
        self.skill_dir.mkdir(parents=True, exist_ok=True)

        # Extract components
        extracted = {
            'scripts': self._extract_scripts(),
            'references': self._extract_references(),
            'assets': self._extract_assets()
        }

        # Generate SKILL.md
        self._generate_skill_md(extracted)

        # Generate README.md
        self._generate_readme(extracted)

        # Generate migration report
        self._generate_migration_report(extracted)

        print(f"\n✅ Skill extraction complete!")
        print(f"   Location: {self.skill_dir}")
        print(f"   Review: {self.skill_dir / 'README.md'}")
        print(f"   Migration: {self.skill_dir / 'migration-report.md'}")

    def _extract_scripts(self) -> List[Dict]:
        """Extract scripts to scripts/ directory."""
        scripts = self.analysis['scripts']
        if not scripts:
            return []

        scripts_dir = self.skill_dir / 'scripts'
        scripts_dir.mkdir(exist_ok=True)

        extracted = []
        for script in scripts:
            # Write script file
            script_path = scripts_dir / script['name']
            script_path.write_text(script['content'])

            # Make executable if it's a shell script
            if script_path.suffix in ['.sh', '.bash']:
                os.chmod(script_path, 0o755)

            extracted.append({
                'name': script['name'],
                'path': str(script_path.relative_to(self.skill_dir)),
                'original_lines': f"{script['line_start']}-{script['line_end']}",
                'size': script['size']
            })

            print(f"  📄 Extracted script: {script['name']}")

        return extracted

    def _extract_references(self) -> List[Dict]:
        """Extract reference documentation to references/ directory."""
        references = self.analysis['references']
        if not references:
            return []

        refs_dir = self.skill_dir / 'references'
        refs_dir.mkdir(exist_ok=True)

        extracted = []
        for ref in references:
            # Write reference file
            ref_path = refs_dir / ref['name']
            ref_path.write_text(ref['content'])

            extracted.append({
                'name': ref['name'],
                'path': str(ref_path.relative_to(self.skill_dir)),
                'original_lines': f"{ref['line_start']}-{ref['line_end']}",
                'size': ref['size']
            })

            print(f"  📚 Extracted reference: {ref['name']}")

        return extracted

    def _extract_assets(self) -> List[Dict]:
        """Extract asset templates to assets/ directory."""
        assets = self.analysis['assets']
        if not assets:
            return []

        assets_dir = self.skill_dir / 'assets'
        assets_dir.mkdir(exist_ok=True)

        extracted = []
        for asset in assets:
            # Write asset file
            asset_path = assets_dir / asset['name']
            asset_path.write_text(asset['content'])

            extracted.append({
                'name': asset['name'],
                'path': str(asset_path.relative_to(self.skill_dir)),
                'original_lines': f"{asset['line_start']}-{asset['line_end']}",
                'size': asset['size'],
                'context_heading': asset.get('context_heading', ''),
                'context_description': asset.get('context_description', ''),
                'placeholders': asset.get('placeholders', [])
            })

            print(f"  🎨 Extracted asset: {asset['name']}")

        return extracted

    def _generate_skill_md(self, extracted: Dict):
        """Generate SKILL.md file with proper frontmatter."""
        has_scripts = bool(extracted['scripts'])
        has_references = bool(extracted['references'])
        has_assets = bool(extracted['assets'])

        # Build description based on what's included
        component_types = []
        if has_scripts:
            component_types.append('scripts')
        if has_references:
            component_types.append('reference documentation')
        if has_assets:
            component_types.append('templates')

        description_parts = ' and '.join(component_types) if component_types else 'components'

        # Generate SKILL.md content
        content = f"""---
name: {self.skill_name}
description: {description_parts.capitalize()} for reusable functionality
---

# {self.skill_name.replace('-', ' ').title()}

## Purpose

This skill provides {description_parts} extracted from a command for reusable functionality across projects.

{self._generate_purpose_detail(extracted)}

## When to Use

Use this skill when you need:
{self._generate_when_to_use(extracted)}

## Components

"""

        if has_scripts:
            content += "### Scripts\n\n"
            for script in extracted['scripts']:
                content += f"- **{script['name']}**: Execute via `python {script['path']}` or similar\n"
            content += "\n"

        if has_references:
            content += "### Reference Documentation\n\n"
            for ref in extracted['references']:
                content += f"- **{ref['name']}**: Comprehensive reference material\n"
            content += "\n"

        if has_assets:
            content += "### Assets\n\n"
            for asset in extracted['assets']:
                # Use context heading or fall back to filename
                asset_title = asset.get('context_heading', '') or asset['name'].replace('-', ' ').replace('.md', '').title()

                content += f"#### {asset_title}\n\n"
                content += f"**File**: `{asset['path']}`\n\n"

                # Add context description if available
                if asset.get('context_description'):
                    content += f"{asset['context_description']}\n\n"

                # Document placeholders if present
                if asset.get('placeholders'):
                    content += "**Placeholders**:\n"
                    for placeholder in asset['placeholders']:
                        content += f"- `{{{{{placeholder}}}}}`: {self._describe_placeholder(placeholder)}\n"
                    content += "\n"

            content += "\n"

        content += """## Usage

This skill provides reusable components that can be referenced in commands and agents:

"""

        if has_scripts:
            content += """### Using Scripts

Execute scripts from your command/agent:
```bash
python scripts/[script-name].py [arguments]
```

"""

        if has_references:
            content += """### Accessing References

Load reference documentation when needed:
- Read files from `references/` directory
- Use content to inform your process
- Update references as standards evolve

"""

        if has_assets:
            content += "### Utilizing Assets\n\n"
            content += "Reference templates directly using `@` syntax:\n\n"

            for asset in extracted['assets']:
                asset_title = asset.get('context_heading', '') or asset['name']
                content += f"**{asset_title}**:\n"
                content += f"```markdown\n"
                content += f"@SKILL_PATH/{asset['path']}\n"
                content += f"```\n"
                content += f"_Replace `SKILL_PATH` with `./.claude/skills/{self.skill_name}` (project) or `~/.claude/skills/{self.skill_name}` (user)_\n\n"

                if asset.get('placeholders'):
                    content += "Placeholders: "
                    placeholder_list = ["`{{" + ph + "}}`" for ph in asset['placeholders']]
                    content += ", ".join(placeholder_list)
                    content += "\n\n"

        # Write SKILL.md
        skill_md_path = self.skill_dir / 'SKILL.md'
        skill_md_path.write_text(content)
        print(f"  📝 Generated SKILL.md")

    def _generate_readme(self, extracted: Dict):
        """Generate developer-focused README.md."""
        has_scripts = bool(extracted['scripts'])
        has_references = bool(extracted['references'])
        has_assets = bool(extracted['assets'])

        # Build overview
        component_list = []
        if has_scripts:
            component_list.append(f"{len(extracted['scripts'])} script(s)")
        if has_references:
            component_list.append(f"{len(extracted['references'])} reference document(s)")
        if has_assets:
            component_list.append(f"{len(extracted['assets'])} template(s)")

        components_summary = ", ".join(component_list) if component_list else "components"

        content = f"""# {self.skill_name.replace('-', ' ').title()}

A Claude Code skill providing {components_summary} for reusable functionality.

## Overview

This skill contains:
"""

        if has_scripts:
            content += f"- **{len(extracted['scripts'])} Script(s)**: Executable utilities\n"
        if has_references:
            content += f"- **{len(extracted['references'])} Reference(s)**: Documentation and guidelines\n"
        if has_assets:
            content += f"- **{len(extracted['assets'])} Template(s)**: Reusable output formats\n"

        content += f"""
## Installation

### Project-level Installation (Recommended for project-specific use)

Install to `.claude/skills/` in your project:

```bash
cp -r {self.skill_name} .claude/skills/
```

### User-level Installation (Global, available in all projects)

Install to `~/.claude/skills/`:

```bash
cp -r {self.skill_name} ~/.claude/skills/
```

## Usage

Reference skill components directly in your commands/agents using `@` syntax.

The path depends on your installation location:
- **Project-level**: `@./.claude/skills/{self.skill_name}/...`
- **User-level**: `@~/.claude/skills/{self.skill_name}/...`

"""

        # Scripts section
        if has_scripts:
            content += "### Scripts\n\n"
            for script in extracted['scripts']:
                content += f"#### {script['name']}\n\n"
                content += f"Execute from your command or agent:\n\n"
                content += f"```bash\n"
                content += f"python {self.skill_name}/scripts/{script['name']}\n"
                content += f"```\n\n"

        # References section
        if has_references:
            content += "### Reference Documentation\n\n"
            for ref in extracted['references']:
                content += f"#### {ref['name']}\n\n"
                content += f"Load this reference when needed:\n\n"
                content += f"```python\n"
                content += f"with open('{self.skill_name}/references/{ref['name']}', 'r') as f:\n"
                content += f"    reference_content = f.read()\n"
                content += f"```\n\n"

        # Assets section with detailed examples
        if has_assets:
            content += "### Templates\n\n"
            for asset in extracted['assets']:
                asset_title = asset.get('context_heading', '') or asset['name'].replace('-', ' ').replace('.md', '').replace('.yaml', '').title()

                content += f"#### {asset_title}\n\n"

                # Add context description if available
                if asset.get('context_description'):
                    content += f"**Purpose**: {asset['context_description']}\n\n"

                content += f"**File**: `{asset['path']}`\n\n"

                # Document placeholders
                if asset.get('placeholders'):
                    content += f"**Placeholders** ({len(asset['placeholders'])} total):\n\n"
                    for placeholder in asset['placeholders']:
                        desc = self._describe_placeholder(placeholder)
                        content += f"- `{{{{{placeholder}}}}}` - {desc}\n"
                    content += "\n"

                # Usage example using @ syntax
                content += "**Usage in Commands/Agents**:\n\n"
                content += "```markdown\n"
                content += f"<!-- For project-level installation -->\n"
                content += f"@./.claude/skills/{self.skill_name}/{asset['path']}\n\n"
                content += f"<!-- For user-level installation -->\n"
                content += f"@~/.claude/skills/{self.skill_name}/{asset['path']}\n"
                content += "```\n\n"

                if asset.get('placeholders'):
                    content += f"Define variables before the template reference:\n\n"
                    content += "```markdown\n"
                    # Show variable assignment syntax
                    for placeholder in asset['placeholders']:
                        content += f"{{{{{placeholder}=\"your_value_here\"}}}}\n"
                    content += f"\n@./.claude/skills/{self.skill_name}/{asset['path']}\n"
                    content += "```\n\n"
                    content += "Claude Code will automatically substitute the variables in the template.\n\n"

        # Integration example
        content += f"""## Integration in Commands/Agents

To use this skill in your Claude Code command or agent, simply reference the files using `@` syntax.

### Example Command Integration

```markdown
---
name: my-command
---

# My Command

<!-- Define variables first -->
{{{{field1="value1"}}}}
{{{{field2="value2"}}}}

<!-- Then load template - choose based on installation location -->
@~/.claude/skills/{self.skill_name}/assets/template-name.md

<!-- Or for project-level -->
@./.claude/skills/{self.skill_name}/assets/template-name.md
```

Claude Code automatically loads the template and substitutes your variables.

## Development

To modify or extend this skill:

1. Edit files in the appropriate directory (`scripts/`, `references/`, or `assets/`)
2. Update this README if you add new components
3. Test your changes before committing

## License

This skill was extracted from an existing command/agent for reusability.
"""

        # Write README.md
        readme_path = self.skill_dir / 'README.md'
        readme_path.write_text(content)
        print(f"  📖 Generated README.md")

    def _generate_migration_report(self, extracted: Dict):
        """Generate detailed migration report."""
        components_count = len(extracted['scripts']) + len(extracted['references']) + len(extracted['assets'])
        file_size = self.analysis['total_size']
        file_lines = self.analysis['total_lines']
        extraction_pct = f"{self.analysis['extraction_potential']:.1f}%"

        content = f"""# Migration Report

**Original File**: `{self.original_file}`
**Skill Created**: `{self.skill_name}`
**Extraction Date**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## Executive Summary

- **Components Extracted**: {components_count}
- **Original File Size**: {file_size} bytes ({file_lines} lines)
- **Extraction Potential**: {extraction_pct}

## Extracted Components

"""

        if extracted['scripts']:
            content += "### Scripts Extracted\n\n"
            for script in extracted['scripts']:
                content += f"""#### {script['name']}
- **New Location**: `{script['path']}`
- **Original Lines**: {script['original_lines']}
- **Size**: {script['size']} bytes

**Usage**: Execute this script via command line or integrate into workflows.

"""

        if extracted['references']:
            content += "### References Extracted\n\n"
            for ref in extracted['references']:
                content += f"""#### {ref['name']}
- **New Location**: `{ref['path']}`
- **Original Lines**: {ref['original_lines']}
- **Size**: {ref['size']} bytes

**Usage**: Read and reference this documentation when needed.

"""

        if extracted['assets']:
            content += "### Assets Extracted\n\n"
            for asset in extracted['assets']:
                asset_title = asset.get('context_heading', '') or asset['name']

                content += f"""#### {asset_title}

**File**: `{asset['path']}`
**Original Lines**: {asset['original_lines']}
**Size**: {asset['size']} bytes

"""
                if asset.get('context_description'):
                    content += f"**Purpose**: {asset['context_description']}\n\n"

                if asset.get('placeholders'):
                    content += f"**Placeholders** ({len(asset['placeholders'])} total):\n"
                    for ph in asset['placeholders'][:10]:  # Show first 10
                        content += f"- `{{{ph}}}`\n"
                    if len(asset['placeholders']) > 10:
                        content += f"- _(and {len(asset['placeholders']) - 10} more...)_\n"
                    content += "\n"

                content += "**Usage**: Load this template and populate placeholders with actual values.\n\n"


        content += """## Required Changes to Original File

### Step 1: Update References

Replace embedded content with skill references:

**For Scripts**:
```markdown
Before: [embedded script code]
After: Execute using: python path/to/{skill_name}/scripts/[script-name].py
```

**For References**:
```markdown
Before: [large reference section]
After: See references/[reference-name].md in {skill_name} skill for details.
```

**For Assets**:
```markdown
Before: [embedded template]
After: Use template from assets/[asset-name] in {skill_name} skill.
```

### Step 2: Verify Functionality

After updating references:
1. Test all script executions work correctly
2. Verify reference materials are accessible
3. Confirm assets are properly utilized
4. Ensure original functionality preserved

### Step 3: Clean Up

Remove the now-redundant embedded content from the original file while preserving:
- Core workflow logic
- User interaction flows
- Orchestration steps
- Decision trees

## Next Steps

1. Review this migration report
2. Update original file with new references
3. Test thoroughly to ensure functionality preserved
4. Consider packaging skill for distribution
5. Update any documentation referencing the original structure

## Notes

- Original file is UNCHANGED by this extraction process
- All extracted components are in the `{self.skill_name}` directory
- Migration can be done incrementally
- Keep both versions until migration is complete and tested

## Validation Checklist

- [ ] All extracted components accessible from original file location
- [ ] Scripts execute successfully
- [ ] References load correctly
- [ ] Assets can be utilized
- [ ] Original functionality works as before
- [ ] No broken references in original file
- [ ] Documentation updated to reflect new structure
"""

        # Write migration report
        report_path = self.skill_dir / 'migration-report.md'
        report_path.write_text(content)
        print(f"  📋 Generated migration report")


def main():
    """Main entry point for the extractor."""
    parser = argparse.ArgumentParser(
        description='Extract components and create skill structure'
    )
    parser.add_argument(
        'analysis',
        type=str,
        help='Path to analysis JSON file from analyze_command.py'
    )
    parser.add_argument(
        '--output',
        type=str,
        default='.',
        help='Output directory for skill creation (default: current directory)'
    )
    parser.add_argument(
        '--name',
        type=str,
        required=True,
        help='Name for the extracted skill (kebab-case recommended)'
    )

    args = parser.parse_args()

    # Perform extraction
    extractor = SkillExtractor(args.analysis, args.output, args.name)
    extractor.extract()


if __name__ == '__main__':
    main()
