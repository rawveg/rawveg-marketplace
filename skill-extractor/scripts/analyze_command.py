#!/usr/bin/env python3
"""
Command/Agent Analyzer for Skill Extraction

This script analyzes Claude Code commands and agents to identify
components that should be extracted into skills (scripts, references, assets).
"""

import re
import os
import json
import argparse
from pathlib import Path
from typing import Dict, List, Tuple, Set
from dataclasses import dataclass, asdict, field


@dataclass
class ExtractableComponent:
    """Represents a component that can be extracted."""
    type: str  # 'script', 'reference', 'asset'
    name: str
    content: str
    line_start: int
    line_end: int
    size: int
    reason: str
    confidence: float  # 0.0 to 1.0
    context_heading: str = ""  # Preceding heading/section title
    context_description: str = ""  # Surrounding explanatory text
    placeholders: List[str] = field(default_factory=list)  # {placeholder} patterns found


@dataclass
class AnalysisResult:
    """Results from analyzing a command/agent file."""
    filename: str
    total_lines: int
    total_size: int
    scripts: List[ExtractableComponent]
    references: List[ExtractableComponent]
    assets: List[ExtractableComponent]
    core_workflow_lines: int
    extraction_potential: float  # Percentage of content that should be extracted
    extraction_recommended: bool  # Whether extraction is actually worthwhile (YAGNI check)
    recommendation_reason: str  # Why extraction is/isn't recommended


class CommandAnalyzer:
    """Analyzes command and agent files for extractable components."""

    # Pattern matching rules
    SCRIPT_PATTERNS = [
        (r'```(?:bash|python|javascript|ruby|perl|sh)\n(.*?)\n```', 'code_block'),
    ]

    TEMPLATE_PATTERNS = [
        (r'```(?:markdown|md|yaml|json|xml|html)\n(.*?)\n```', 'template_block'),
    ]

    # XML-like tags that indicate documentation/examples (NOT extractable)
    DOCUMENTATION_TAGS = [
        'task', 'context', 'restrictions', 'agent_categories', 'interactive_process',
        'research_strategy', 'generation_template', 'output_style_check',
        'execution_flow', 'quality_criteria', 'examples', 'deployment_options',
        'final_output', 'continuous_improvement', 'template', 'example'
    ]

    REFERENCE_MARKERS = [
        'reference', 'documentation', 'guide', 'manual', 'specification',
        'format', 'style guide', 'convention', 'standard', 'best practice'
    ]

    # Size thresholds
    MIN_SCRIPT_LINES = 20
    MIN_REFERENCE_WORDS = 500
    MIN_ASSET_SIZE = 200  # Increased to avoid extracting tiny examples

    def __init__(self, filepath: str):
        self.filepath = Path(filepath)
        self.content = self.filepath.read_text(encoding='utf-8')
        self.lines = self.content.split('\n')
        self.used_names: Set[str] = set()  # Track used filenames

    def analyze(self) -> AnalysisResult:
        """Perform comprehensive analysis of the file."""
        # Identify documentation regions first
        doc_regions = self._identify_documentation_regions()

        scripts = self._identify_scripts(doc_regions)
        references = self._identify_references(doc_regions)
        assets = self._identify_assets(doc_regions)

        # Calculate metrics
        total_extractable_lines = sum(
            c.line_end - c.line_start
            for c in scripts + references + assets
        )
        core_workflow_lines = len(self.lines) - total_extractable_lines
        extraction_potential = (total_extractable_lines / len(self.lines)) * 100 if len(self.lines) > 0 else 0

        # Evaluate if extraction is actually worthwhile (YAGNI check)
        is_recommended, reason = self._evaluate_extraction_worthiness(scripts, references, assets)

        return AnalysisResult(
            filename=self.filepath.name,
            total_lines=len(self.lines),
            total_size=len(self.content),
            scripts=scripts,
            references=references,
            assets=assets,
            core_workflow_lines=core_workflow_lines,
            extraction_potential=extraction_potential,
            extraction_recommended=is_recommended,
            recommendation_reason=reason
        )

    def _identify_documentation_regions(self) -> List[Tuple[int, int]]:
        """
        Identify character ranges that are within documentation tags.
        These should NOT be extracted as they're examples/structure.
        """
        regions = []
        for tag in self.DOCUMENTATION_TAGS:
            # Match <tag>...</tag> regions
            pattern = f'<{tag}[^>]*>(.*?)</{tag}>'
            for match in re.finditer(pattern, self.content, re.DOTALL | re.IGNORECASE):
                regions.append((match.start(), match.end()))
        return regions

    def _is_in_documentation_region(self, char_start: int, char_end: int,
                                    doc_regions: List[Tuple[int, int]]) -> bool:
        """Check if a character range overlaps with any documentation region."""
        for doc_start, doc_end in doc_regions:
            # Check for any overlap
            if not (char_end <= doc_start or char_start >= doc_end):
                return True
        return False

    def _capture_context(self, char_start: int) -> Tuple[str, str]:
        """
        Capture context around a code block by looking backwards.

        Returns:
            (heading, description) where:
            - heading is the nearest markdown heading before the block
            - description is explanatory text between heading and block
        """
        # Convert char position to line number
        line_num = self.content[:char_start].count('\n')

        # Look backwards from the current position
        heading = ""
        description_lines = []
        found_heading = False

        # Search backwards through lines
        for i in range(line_num - 1, max(0, line_num - 30), -1):  # Look back up to 30 lines
            line = self.lines[i].strip()

            # Skip empty lines
            if not line:
                if found_heading:
                    # Empty line between heading and current position
                    continue
                else:
                    # Keep searching
                    continue

            # Check if this is a markdown heading
            if line.startswith('#'):
                heading = line.lstrip('#').strip()
                found_heading = True
                break

            # If we haven't found a heading yet, accumulate description
            if not found_heading:
                # Skip code fences and very short lines
                if not line.startswith('```') and len(line) > 3:
                    description_lines.insert(0, line)

        # Clean up description - take only the most recent paragraph
        description = ""
        if description_lines:
            # Take up to 5 lines of description, or until we hit something that looks structural
            relevant_desc = []
            for line in description_lines[-5:]:
                # Skip lines that look like instructions or numbered lists
                if line.startswith(('1.', '2.', '3.', '-', '*', '##')):
                    break
                relevant_desc.append(line)
            description = ' '.join(relevant_desc).strip()

        return heading, description

    def _extract_placeholders(self, content: str) -> List[str]:
        """
        Extract placeholder patterns from template content.
        Looks for both {{placeholder}} (recommended) and {placeholder} (legacy) syntax.

        Returns:
            List of unique placeholder names (without braces)
        """
        # Find all {{placeholder}} patterns (preferred)
        double_brace_placeholders = re.findall(r'\{\{([a-z][a-z0-9_-]*)\}\}', content, re.IGNORECASE)

        # Find all {placeholder} patterns (legacy, but still supported)
        single_brace_placeholders = re.findall(r'\{([a-z][a-z0-9_-]*)\}', content, re.IGNORECASE)

        # Combine both, preferring double-brace if both exist
        all_placeholders = double_brace_placeholders + single_brace_placeholders

        # Return unique placeholders in order of appearance
        seen = set()
        unique_placeholders = []
        for p in all_placeholders:
            if p not in seen:
                seen.add(p)
                unique_placeholders.append(p)

        return unique_placeholders

    def _identify_scripts(self, doc_regions: List[Tuple[int, int]]) -> List[ExtractableComponent]:
        """Identify extractable scripts in the content."""
        scripts = []

        for pattern, pattern_type in self.SCRIPT_PATTERNS:
            for match in re.finditer(pattern, self.content, re.DOTALL):
                # Skip if within documentation region
                if self._is_in_documentation_region(match.start(), match.end(), doc_regions):
                    continue

                script_content = match.group(1)
                line_start, line_end = self._get_line_range(match.start(), match.end())

                # Check if script meets minimum size
                script_lines = len(script_content.split('\n'))
                if script_lines < self.MIN_SCRIPT_LINES:
                    continue

                # Additional validation: ensure it's actual runnable code, not pseudocode
                if self._is_pseudocode(script_content):
                    continue

                # Determine script language and name
                language = self._detect_language(script_content)
                name = self._generate_unique_script_name(script_content, language)

                scripts.append(ExtractableComponent(
                    type='script',
                    name=name,
                    content=script_content,
                    line_start=line_start,
                    line_end=line_end,
                    size=len(script_content),
                    reason=f'{script_lines}-line {language} script - reusable logic',
                    confidence=0.8 if script_lines > 50 else 0.6
                ))

        return scripts

    def _identify_references(self, doc_regions: List[Tuple[int, int]]) -> List[ExtractableComponent]:
        """Identify reference documentation that should be extracted."""
        references = []

        # Look for large documentation blocks
        current_block = []
        current_start = 0
        in_reference_section = False
        section_char_start = 0

        for i, line in enumerate(self.lines):
            # Get character position of this line
            char_pos = sum(len(l) + 1 for l in self.lines[:i])

            # Check if line starts a reference section
            if any(marker in line.lower() for marker in self.REFERENCE_MARKERS):
                if not in_reference_section:
                    in_reference_section = True
                    current_start = i
                    section_char_start = char_pos
                    current_block = [line]
                else:
                    current_block.append(line)
            elif in_reference_section:
                # Check if we've reached the end of reference section
                if line.startswith('#') or line.startswith('##'):
                    # Check if this section is in documentation region
                    section_char_end = char_pos
                    if not self._is_in_documentation_region(section_char_start, section_char_end, doc_regions):
                        # Potential end of section
                        if len(' '.join(current_block).split()) >= self.MIN_REFERENCE_WORDS:
                            content = '\n'.join(current_block)
                            name = self._generate_unique_reference_name(current_block[0])
                            references.append(ExtractableComponent(
                                type='reference',
                                name=name,
                                content=content,
                                line_start=current_start,
                                line_end=i,
                                size=len(content),
                                reason=f'{len(current_block)} lines of reference documentation',
                                confidence=0.9 if len(content) > 2000 else 0.7
                            ))
                    in_reference_section = False
                    current_block = []
                else:
                    current_block.append(line)

        # Check final block
        if in_reference_section and len(' '.join(current_block).split()) >= self.MIN_REFERENCE_WORDS:
            section_char_end = len(self.content)
            if not self._is_in_documentation_region(section_char_start, section_char_end, doc_regions):
                content = '\n'.join(current_block)
                name = self._generate_unique_reference_name(current_block[0])
                references.append(ExtractableComponent(
                    type='reference',
                    name=name,
                    content=content,
                    line_start=current_start,
                    line_end=len(self.lines),
                    size=len(content),
                    reason=f'{len(current_block)} lines of reference documentation',
                    confidence=0.9 if len(content) > 2000 else 0.7
                ))

        return references

    def _identify_assets(self, doc_regions: List[Tuple[int, int]]) -> List[ExtractableComponent]:
        """Identify asset templates that should be extracted."""
        assets = []

        for pattern, pattern_type in self.TEMPLATE_PATTERNS:
            for match in re.finditer(pattern, self.content, re.DOTALL):
                # Skip if within documentation region
                if self._is_in_documentation_region(match.start(), match.end(), doc_regions):
                    continue

                template_content = match.group(1)
                line_start, line_end = self._get_line_range(match.start(), match.end())

                # Check if template meets minimum size
                if len(template_content) < self.MIN_ASSET_SIZE:
                    continue

                # Additional validation: ensure it's an actual template, not documentation
                if not self._is_actual_template(template_content):
                    continue

                # Capture context around this template
                context_heading, context_description = self._capture_context(match.start())

                # Extract placeholders from template
                placeholders = self._extract_placeholders(template_content)

                # Determine template type and name using context
                template_type = self._detect_template_type(template_content)
                name = self._generate_unique_asset_name(template_content, template_type, context_heading)

                assets.append(ExtractableComponent(
                    type='asset',
                    name=name,
                    content=template_content,
                    line_start=line_start,
                    line_end=line_end,
                    size=len(template_content),
                    reason=f'{template_type} template - reusable output format',
                    confidence=0.85,
                    context_heading=context_heading,
                    context_description=context_description,
                    placeholders=placeholders
                ))

        return assets

    def _is_pseudocode(self, code: str) -> bool:
        """Check if code is pseudocode/placeholder rather than actual code."""
        # Look for placeholder patterns
        placeholder_patterns = [
            r'\{[a-z-_]+\}',  # {placeholder}
            r'\[.*?\]',  # [placeholder]
            r'\.\.\..*lines',  # ...lines
        ]

        for pattern in placeholder_patterns:
            if len(re.findall(pattern, code)) > 3:  # More than 3 placeholders = likely example
                return True
        return False

    def _is_actual_template(self, content: str) -> bool:
        """
        Determine if content is an actual reusable template vs documentation/example.

        Actual templates:
        - Have clear placeholder patterns ({{field}}, {field}, etc.)
        - Are meant to be copied and filled in
        - Have consistent structure throughout

        Documentation/examples:
        - Show how to write something
        - Have mixed placeholder and example text
        - Include explanatory comments
        """
        # Count placeholder patterns - look for both {{placeholder}} and {placeholder}
        double_brace_count = len(re.findall(r'\{\{[a-z][a-z0-9_-]*\}\}', content, re.IGNORECASE))
        single_brace_count = len(re.findall(r'\{[a-z][a-z0-9_-]*\}', content, re.IGNORECASE))
        placeholder_count = double_brace_count + single_brace_count

        # Templates should have multiple placeholders
        if placeholder_count < 3:
            return False

        # Check for documentation indicators
        doc_indicators = [
            'for example', 'e.g.', 'i.e.', 'such as', 'like this',
            'you can', 'you should', 'example:', 'note:', 'important:'
        ]

        doc_indicator_count = sum(1 for indicator in doc_indicators if indicator in content.lower())

        # If too many documentation indicators, it's probably not a template
        if doc_indicator_count > 2:
            return False

        # Placeholder density should be reasonable
        placeholder_density = placeholder_count / len(content.split())
        if placeholder_density < 0.05:  # Less than 5% placeholders
            return False

        return True

    def _get_line_range(self, char_start: int, char_end: int) -> Tuple[int, int]:
        """Convert character positions to line numbers."""
        line_start = self.content[:char_start].count('\n') + 1
        line_end = self.content[:char_end].count('\n') + 1
        return line_start, line_end

    def _detect_language(self, code: str) -> str:
        """Detect programming language from code content."""
        if 'def ' in code or 'import ' in code or 'from ' in code:
            return 'python'
        elif 'function' in code or 'const ' in code or 'let ' in code or 'var ' in code:
            return 'javascript'
        elif '#!/bin/bash' in code or '#!/bin/sh' in code or 'echo ' in code:
            return 'bash'
        else:
            return 'script'

    def _detect_template_type(self, template: str) -> str:
        """Detect template format from content."""
        stripped = template.strip()

        # Check for explicit format markers
        if stripped.startswith('{') and stripped.endswith('}'):
            return 'json'
        elif stripped.startswith('<') and stripped.endswith('>'):
            return 'html'

        # Check for markdown indicators (most common for templates)
        md_indicators = ['##', '###', '**', '`', '- ', '* ', '1. ', '> ']
        if any(indicator in template for indicator in md_indicators):
            return 'md'

        # YAML has key: value pairs but markdown can too, so be more strict
        # Only consider YAML if it starts with common YAML patterns
        yaml_starts = ['---\n', 'name:', 'title:', 'description:', 'version:']
        if any(stripped.startswith(pattern) for pattern in yaml_starts):
            # Additional check: does it have YAML structure throughout?
            lines = template.split('\n')
            yaml_lines = sum(1 for line in lines if ':' in line and not line.strip().startswith('#'))
            if yaml_lines > len(lines) * 0.6:  # More than 60% are key:value
                return 'yaml'

        # Default to markdown for text-based templates
        return 'md'

    def _generate_unique_script_name(self, content: str, language: str) -> str:
        """Generate unique script filename."""
        base_name = self._generate_script_name(content, language)
        return self._ensure_unique_name(base_name)

    def _generate_script_name(self, content: str, language: str) -> str:
        """Generate appropriate script filename."""
        # Try to extract a function name or purpose from code
        lines = content.split('\n')
        for line in lines[:10]:
            if 'def ' in line:
                match = re.search(r'def\s+(\w+)', line)
                if match:
                    return f"{match.group(1)}.py"
            elif 'function ' in line:
                match = re.search(r'function\s+(\w+)', line)
                if match:
                    return f"{match.group(1)}.js"
            elif line.strip().startswith('#') and len(line) > 3:
                # Extract from comment
                comment = line.strip('# ').strip().lower()
                if len(comment) > 5 and len(comment.split()) <= 4:
                    clean = re.sub(r'[^\w\s-]', '', comment)
                    clean = re.sub(r'[-\s]+', '_', clean)
                    ext_map = {'python': 'py', 'javascript': 'js', 'bash': 'sh', 'script': 'sh'}
                    ext = ext_map.get(language, 'txt')
                    return f"{clean}.{ext}"

        # Default based on language
        ext_map = {'python': 'py', 'javascript': 'js', 'bash': 'sh', 'script': 'sh'}
        ext = ext_map.get(language, 'txt')
        return f"script.{ext}"

    def _generate_unique_reference_name(self, header: str) -> str:
        """Generate unique reference filename from section header."""
        base_name = self._generate_reference_name(header)
        return self._ensure_unique_name(base_name)

    def _generate_reference_name(self, header: str) -> str:
        """Generate appropriate reference filename from section header."""
        # Remove markdown formatting
        clean = re.sub(r'[#*`<>]', '', header).strip()
        # Convert to kebab-case
        name = re.sub(r'[^\w\s-]', '', clean.lower())
        name = re.sub(r'[-\s]+', '-', name)
        name = name[:50]  # Limit length
        return f"{name}.md" if name else "reference.md"

    def _generate_unique_asset_name(self, content: str, template_type: str, context_heading: str = "") -> str:
        """Generate unique asset filename."""
        base_name = self._generate_asset_name(content, template_type, context_heading)
        return self._ensure_unique_name(base_name)

    def _generate_asset_name(self, content: str, template_type: str, context_heading: str = "") -> str:
        """
        Generate appropriate asset filename using context and content.

        Priority:
        1. Context heading (from surrounding markdown)
        2. Title/name in template content
        3. Generic fallback
        """
        ext_map = {'json': 'json', 'html': 'html', 'yaml': 'yaml', 'md': 'md'}
        ext = ext_map.get(template_type, 'txt')

        # First, try to use context heading if available
        if context_heading:
            # Clean up heading
            name = context_heading.lower()
            # Remove common prefixes
            name = re.sub(r'^(step \d+:\s*|task \d+:\s*|\d+\.\s*)', '', name)
            # Remove placeholders
            name = re.sub(r'\{.*?\}', '', name)
            # Remove special characters
            name = re.sub(r'[^\w\s-]', '', name)
            # Convert to kebab-case
            name = re.sub(r'[-\s]+', '-', name).strip('-')

            if len(name) > 3:
                return f"{name}.{ext}"

        # Fallback: Try to find a title or name in the template content
        lines = content.split('\n')
        for line in lines[:10]:
            line = line.strip()
            # Look for common title patterns
            if line.startswith('# '):
                title = line[2:].strip().lower()
                title = re.sub(r'\{.*?\}', '', title)  # Remove placeholders
                title = re.sub(r'[^\w\s-]', '', title)
                title = re.sub(r'[-\s]+', '-', title)
                if len(title) > 3:
                    return f"{title}.{ext}"
            elif line.startswith('name:') or line.startswith('title:'):
                # YAML front matter
                name = line.split(':', 1)[1].strip().lower()
                name = re.sub(r'\{.*?\}', '', name)
                name = re.sub(r'[^\w\s-]', '', name)
                name = re.sub(r'[-\s]+', '-', name)
                if len(name) > 3:
                    return f"{name}.{ext}"

        # Last resort: generic name
        return f"template.{ext}"

    def _ensure_unique_name(self, name: str) -> str:
        """Ensure filename is unique by appending number if needed."""
        if name not in self.used_names:
            self.used_names.add(name)
            return name

        # Extract base and extension
        parts = name.rsplit('.', 1)
        if len(parts) == 2:
            base, ext = parts
        else:
            base, ext = name, ''

        # Try appending numbers
        counter = 2
        while True:
            new_name = f"{base}-{counter}.{ext}" if ext else f"{base}-{counter}"
            if new_name not in self.used_names:
                self.used_names.add(new_name)
                return new_name
            counter += 1

    def _evaluate_extraction_worthiness(self,
                                       scripts: List[ExtractableComponent],
                                       references: List[ExtractableComponent],
                                       assets: List[ExtractableComponent]) -> Tuple[bool, str]:
        """
        Evaluate if extraction is worthwhile using YAGNI principles.

        Returns:
            (is_recommended, reason)
        """
        total_components = len(scripts) + len(references) + len(assets)

        # No components = not worth it
        if total_components == 0:
            return False, "No extractable components found"

        # Calculate total size and diversity
        total_size = sum(c.size for c in scripts + references + assets)
        component_types = sum([
            1 if scripts else 0,
            1 if references else 0,
            1 if assets else 0
        ])

        # Single component checks
        if total_components == 1:
            component = (scripts + references + assets)[0]

            # Single script: must be very substantial (>100 lines) and high confidence
            if scripts:
                script_lines = len(component.content.split('\n'))
                if script_lines >= 100 and component.confidence >= 0.8:
                    return True, f"Large, reusable script ({script_lines} lines) worth extracting"
                return False, f"Single script too small ({script_lines} lines) - keep inline (YAGNI)"

            # Single reference: must be very large (>3000 chars)
            if references:
                if component.size >= 3000:
                    return True, f"Large reference documentation ({component.size} chars) worth extracting"
                return False, f"Single reference too small ({component.size} chars) - keep inline (YAGNI)"

            # Single asset: not worth it unless very large
            if assets:
                if component.size >= 1000:
                    return True, f"Large template ({component.size} chars) worth extracting"
                return False, f"Single small asset ({component.size} chars) - keep inline (YAGNI)"

        # Assets-only checks (most problematic case)
        if assets and not scripts and not references:
            # Need either many assets or large total size
            if len(assets) >= 3 and total_size >= 1000:
                return True, f"{len(assets)} related templates form a useful collection"
            elif len(assets) >= 5:
                return True, f"{len(assets)} templates - worthwhile collection"
            elif total_size >= 2000:
                return True, f"Substantial template content ({total_size} chars)"
            else:
                return False, f"Only {len(assets)} small asset(s) ({total_size} chars total) - not worth overhead (YAGNI)"

        # Scripts-only checks
        if scripts and not references and not assets:
            if len(scripts) >= 2:
                return True, f"{len(scripts)} reusable scripts worth extracting"
            # Single script already handled above
            return False, "Insufficient script content - keep inline (YAGNI)"

        # References-only checks
        if references and not scripts and not assets:
            if len(references) >= 2:
                return True, f"{len(references)} reference documents worth extracting"
            # Single reference already handled above
            return False, "Single small reference - keep inline (YAGNI)"

        # Mixed component types (multiple types is a good sign)
        if component_types >= 2:
            # Diverse types with reasonable size
            if total_size >= 1000:
                return True, f"Diverse components ({component_types} types, {total_size} chars) worth extracting"
            elif total_components >= 3:
                return True, f"Multiple diverse components ({total_components} items) worth extracting"
            else:
                return False, f"Mixed types but too small ({total_size} chars) - keep inline (YAGNI)"

        # 2-3 components of same type
        if 2 <= total_components <= 3:
            if total_size >= 1500:
                return True, f"{total_components} components with substantial content ({total_size} chars)"
            else:
                return False, f"Only {total_components} small components ({total_size} chars) - overhead not justified (YAGNI)"

        # 4+ components
        if total_components >= 4:
            return True, f"{total_components} components - worthwhile to organize as skill"

        # Default: not recommended
        return False, f"{total_components} component(s), {total_size} chars - extraction overhead not justified (YAGNI)"


def main():
    """Main entry point for the analyzer."""
    parser = argparse.ArgumentParser(
        description='Analyze Claude Code commands/agents for skill extraction'
    )
    parser.add_argument(
        'input',
        type=str,
        help='Path to command or agent file to analyze'
    )
    parser.add_argument(
        '--output',
        '-o',
        type=str,
        default='analysis.json',
        help='Path to save analysis results (default: analysis.json)'
    )
    parser.add_argument(
        '--verbose',
        '-v',
        action='store_true',
        help='Show detailed analysis output'
    )

    args = parser.parse_args()

    # Run analysis
    analyzer = CommandAnalyzer(args.input)
    result = analyzer.analyze()

    # Save results
    output_path = Path(args.output)
    with open(output_path, 'w') as f:
        json.dump(asdict(result), f, indent=2, default=lambda o: o.__dict__)

    # Print summary
    print(f"\n{'='*60}")
    print(f"Analysis Complete: {result.filename}")
    print(f"{'='*60}\n")
    print(f"Total Lines: {result.total_lines}")
    print(f"Total Size: {result.total_size} bytes")
    print(f"Extraction Potential: {result.extraction_potential:.1f}%\n")

    print(f"Components Found:")
    print(f"  Scripts:    {len(result.scripts)}")
    print(f"  References: {len(result.references)}")
    print(f"  Assets:     {len(result.assets)}\n")

    # Show recommendation
    if result.extraction_recommended:
        print(f"✅ RECOMMENDED: {result.recommendation_reason}\n")
    else:
        print(f"❌ NOT RECOMMENDED: {result.recommendation_reason}\n")

    if args.verbose:
        if result.scripts:
            print("Scripts:")
            for script in result.scripts:
                print(f"  - {script.name} (lines {script.line_start}-{script.line_end}, "
                      f"confidence: {script.confidence:.2f})")
                print(f"    {script.reason}\n")

        if result.references:
            print("References:")
            for ref in result.references:
                print(f"  - {ref.name} (lines {ref.line_start}-{ref.line_end}, "
                      f"confidence: {ref.confidence:.2f})")
                print(f"    {ref.reason}\n")

        if result.assets:
            print("Assets:")
            for asset in result.assets:
                print(f"  - {asset.name} (lines {asset.line_start}-{asset.line_end}, "
                      f"confidence: {asset.confidence:.2f})")
                print(f"    {asset.reason}\n")

    print(f"Results saved to: {output_path}")
    print(f"{'='*60}\n")


if __name__ == '__main__':
    main()
