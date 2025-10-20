#!/usr/bin/env python
"""
Skill Packaging and Validation Script

Validates skill structure and creates distributable zip packages.
"""

import os
import sys
import yaml
import zipfile
import argparse
from pathlib import Path
from typing import List, Tuple, Dict


class Colors:
    """ANSI color codes for terminal output."""
    RED = '\033[0;31m'
    GREEN = '\033[0;32m'
    YELLOW = '\033[1;33m'
    BLUE = '\033[0;34m'
    NC = '\033[0m'  # No Color


class SkillValidator:
    """Validates skill structure and content."""

    REQUIRED_FILES = ['SKILL.md']
    OPTIONAL_DIRS = ['scripts', 'references', 'assets']

    def __init__(self, skill_path: Path):
        self.skill_path = skill_path
        self.skill_name = skill_path.name
        self.errors = []
        self.warnings = []

    def validate(self) -> bool:
        """Perform comprehensive validation. Returns True if valid."""
        print(f"{Colors.BLUE}Validating skill: {self.skill_name}{Colors.NC}")
        print("=" * 60)

        # Check basic structure
        self._check_directory_structure()
        self._validate_skill_md()
        self._check_bundled_resources()
        self._validate_naming_conventions()

        # Report results
        self._print_results()

        return len(self.errors) == 0

    def _check_directory_structure(self):
        """Validate directory exists and has correct structure."""
        if not self.skill_path.exists():
            self.errors.append(f"Skill directory does not exist: {self.skill_path}")
            return

        if not self.skill_path.is_dir():
            self.errors.append(f"Skill path is not a directory: {self.skill_path}")
            return

        # Check for SKILL.md
        skill_md = self.skill_path / 'SKILL.md'
        if not skill_md.exists():
            self.errors.append("Required file SKILL.md is missing")
        else:
            print(f"{Colors.GREEN}✓{Colors.NC} Found SKILL.md")

    def _validate_skill_md(self):
        """Validate SKILL.md structure and frontmatter."""
        skill_md = self.skill_path / 'SKILL.md'
        if not skill_md.exists():
            return  # Already reported in structure check

        try:
            content = skill_md.read_text(encoding='utf-8')
        except Exception as e:
            self.errors.append(f"Cannot read SKILL.md: {e}")
            return

        # Check for frontmatter
        if not content.startswith('---'):
            self.errors.append("SKILL.md must start with YAML frontmatter (---)")
            return

        # Extract frontmatter
        parts = content.split('---', 2)
        if len(parts) < 3:
            self.errors.append("SKILL.md frontmatter not properly closed with ---")
            return

        frontmatter = parts[1]

        # Parse YAML
        try:
            metadata = yaml.safe_load(frontmatter)
        except yaml.YAMLError as e:
            self.errors.append(f"Invalid YAML in frontmatter: {e}")
            return

        # Validate required fields
        if not isinstance(metadata, dict):
            self.errors.append("Frontmatter must be a YAML dictionary")
            return

        # Check required fields
        if 'name' not in metadata:
            self.errors.append("Frontmatter missing required field: name")
        else:
            skill_name = metadata['name']
            print(f"{Colors.GREEN}✓{Colors.NC} Skill name: {skill_name}")

            # Validate name format (kebab-case)
            if not self._is_kebab_case(skill_name):
                self.warnings.append(
                    f"Skill name '{skill_name}' should use kebab-case (lowercase with hyphens)"
                )

        if 'description' not in metadata:
            self.errors.append("Frontmatter missing required field: description")
        else:
            desc = metadata['description']
            print(f"{Colors.GREEN}✓{Colors.NC} Description: {desc[:60]}...")

            # Check description length
            if len(desc) < 20:
                self.warnings.append("Description is very short (< 20 characters)")
            elif len(desc) > 200:
                self.warnings.append("Description is very long (> 200 characters)")

        # Check body content
        body = parts[2].strip()
        if len(body) < 100:
            self.warnings.append("SKILL.md body is very short (< 100 characters)")

        # Check for common sections
        if '## Purpose' not in body and '## When to Use' not in body:
            self.warnings.append("Consider adding '## Purpose' or '## When to Use' section")

    def _check_bundled_resources(self):
        """Check for and validate bundled resources."""
        found_resources = []

        for dirname in self.OPTIONAL_DIRS:
            dir_path = self.skill_path / dirname
            if dir_path.exists():
                if not dir_path.is_dir():
                    self.errors.append(f"{dirname}/ exists but is not a directory")
                    continue

                # Count files
                files = list(dir_path.glob('**/*'))
                file_count = len([f for f in files if f.is_file()])

                if file_count == 0:
                    self.warnings.append(f"{dirname}/ directory is empty")
                else:
                    found_resources.append(f"{dirname}/ ({file_count} files)")
                    print(f"{Colors.GREEN}✓{Colors.NC} Found {dirname}/ with {file_count} file(s)")

                    # Validate scripts are executable
                    if dirname == 'scripts':
                        self._check_script_permissions(dir_path)

        if not found_resources:
            self.warnings.append("No bundled resources (scripts/, references/, assets/) found")

    def _check_script_permissions(self, scripts_dir: Path):
        """Check if scripts have executable permissions."""
        for script in scripts_dir.glob('*'):
            if script.is_file() and script.suffix in ['.sh', '.py', '.bash']:
                if not os.access(script, os.X_OK):
                    self.warnings.append(
                        f"Script {script.name} is not executable. Run: chmod +x {script}"
                    )

    def _validate_naming_conventions(self):
        """Validate file naming conventions."""
        # Check scripts/
        scripts_dir = self.skill_path / 'scripts'
        if scripts_dir.exists():
            for script in scripts_dir.glob('*'):
                if script.is_file():
                    if not self._is_snake_case(script.stem) and not self._is_kebab_case(script.stem):
                        self.warnings.append(
                            f"Script name '{script.name}' should use snake_case or kebab-case"
                        )

        # Check references/
        refs_dir = self.skill_path / 'references'
        if refs_dir.exists():
            for ref in refs_dir.glob('*.md'):
                if not self._is_kebab_case(ref.stem):
                    self.warnings.append(
                        f"Reference name '{ref.name}' should use kebab-case"
                    )

    def _is_kebab_case(self, name: str) -> bool:
        """Check if string is in kebab-case."""
        return name.islower() and ' ' not in name and '_' not in name

    def _is_snake_case(self, name: str) -> bool:
        """Check if string is in snake_case."""
        return name.islower() and ' ' not in name and '-' not in name

    def _print_results(self):
        """Print validation results."""
        print("\n" + "=" * 60)

        if self.errors:
            print(f"{Colors.RED}✗ Validation Failed{Colors.NC}")
            print(f"\n{Colors.RED}Errors:{Colors.NC}")
            for error in self.errors:
                print(f"  • {error}")
        else:
            print(f"{Colors.GREEN}✓ Validation Passed{Colors.NC}")

        if self.warnings:
            print(f"\n{Colors.YELLOW}Warnings:{Colors.NC}")
            for warning in self.warnings:
                print(f"  • {warning}")

        print("=" * 60 + "\n")


class SkillPackager:
    """Creates distributable skill packages."""

    def __init__(self, skill_path: Path, output_dir: Path = None):
        self.skill_path = skill_path
        self.skill_name = skill_path.name
        self.output_dir = output_dir or Path.cwd()

    def package(self) -> Path:
        """Create a zip package of the skill."""
        output_file = self.output_dir / f"{self.skill_name}.zip"

        print(f"{Colors.BLUE}Packaging skill: {self.skill_name}{Colors.NC}")
        print(f"Output: {output_file}")
        print("=" * 60)

        # Collect files
        files_to_package = self._collect_files()

        if not files_to_package:
            print(f"{Colors.RED}✗ No files found to package{Colors.NC}")
            sys.exit(1)

        # Create zip
        with zipfile.ZipFile(output_file, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for file_path, archive_name in files_to_package:
                zipf.write(file_path, archive_name)
                print(f"{Colors.GREEN}✓{Colors.NC} Added: {archive_name}")

        # Get file size
        size_bytes = output_file.stat().st_size
        size_kb = size_bytes / 1024

        print("=" * 60)
        print(f"{Colors.GREEN}✓ Package created successfully{Colors.NC}")
        print(f"  Location: {output_file}")
        print(f"  Size: {size_kb:.1f} KB")
        print(f"  Files: {len(files_to_package)}")

        return output_file

    def _collect_files(self) -> List[Tuple[Path, str]]:
        """Collect all files to include in package."""
        files = []

        # Always include SKILL.md
        skill_md = self.skill_path / 'SKILL.md'
        if skill_md.exists():
            files.append((skill_md, f"{self.skill_name}/SKILL.md"))

        # Include README.md if it exists
        readme = self.skill_path / 'README.md'
        if readme.exists():
            files.append((readme, f"{self.skill_name}/README.md"))

        # Include all bundled resources
        for dirname in ['scripts', 'references', 'assets']:
            resource_dir = self.skill_path / dirname
            if resource_dir.exists():
                for file_path in resource_dir.rglob('*'):
                    if file_path.is_file():
                        # Preserve directory structure in archive
                        rel_path = file_path.relative_to(self.skill_path)
                        archive_name = f"{self.skill_name}/{rel_path}"
                        files.append((file_path, archive_name))

        return files


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description='Validate and package Claude Code skills'
    )
    parser.add_argument(
        'skill_path',
        type=str,
        help='Path to skill directory to validate/package'
    )
    parser.add_argument(
        '--output',
        '-o',
        type=str,
        default=None,
        help='Output directory for package (default: current directory)'
    )
    parser.add_argument(
        '--validate-only',
        action='store_true',
        help='Only validate, do not create package'
    )
    parser.add_argument(
        '--skip-validation',
        action='store_true',
        help='Skip validation and create package directly'
    )

    args = parser.parse_args()

    # Resolve paths
    skill_path = Path(args.skill_path).resolve()
    output_dir = Path(args.output).resolve() if args.output else Path.cwd()

    # Validate skill
    if not args.skip_validation:
        validator = SkillValidator(skill_path)
        is_valid = validator.validate()

        if not is_valid:
            print(f"{Colors.RED}✗ Validation failed. Fix errors before packaging.{Colors.NC}")
            sys.exit(1)

        if args.validate_only:
            print(f"{Colors.GREEN}✓ Validation complete. Skill is ready for packaging.{Colors.NC}")
            sys.exit(0)

    # Package skill
    packager = SkillPackager(skill_path, output_dir)
    package_path = packager.package()

    # Installation instructions
    print("\n" + "=" * 60)
    print(f"{Colors.BLUE}Installation Instructions:{Colors.NC}")
    print(f"\n  To install this skill:")
    print(f"  1. unzip {package_path.name} -d ~/.claude/skills/")
    print(f"  2. Skill will be available at: ~/.claude/skills/{skill_path.name}/")
    print(f"\n  Or create a symlink for development:")
    print(f"  ln -s {skill_path} ~/.claude/skills/{skill_path.name}")
    print("=" * 60 + "\n")


if __name__ == '__main__':
    main()
