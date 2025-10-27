#!/usr/bin/env python3
"""
TDD Compliance Checker

Analyzes code to detect if Test-Driven Development was followed.
Identifies code smells and patterns that indicate tests-after-code.
"""

import os
import re
import sys
import json
from pathlib import Path
from typing import Dict, List, Tuple


class TDDComplianceChecker:
    """Checks code for TDD compliance indicators."""

    # Code smell patterns that suggest tests-after-code
    CODE_SMELLS = {
        'nested_conditionals': r'if\s+.*:\s*\n\s+if\s+.*:|if\s+.*:\s*\n\s+elif\s+',
        'long_methods': None,  # Checked by line count
        'complex_conditions': r'if\s+.*\s+(and|or)\s+.*\s+(and|or)\s+',
        'multiple_responsibilities': None,  # Checked by method analysis
        'missing_abstractions': r'if\s+isinstance\(',
        'god_class': None,  # Checked by class analysis
    }

    def __init__(self, path: str):
        self.path = Path(path)
        self.issues = []
        self.metrics = {
            'files_analyzed': 0,
            'test_files_found': 0,
            'code_smells': 0,
            'tdd_score': 0.0
        }

    def analyze(self) -> Dict:
        """Run full TDD compliance analysis."""
        if self.path.is_file():
            self._analyze_file(self.path)
        else:
            self._analyze_directory(self.path)

        self._calculate_tdd_score()
        return {
            'issues': self.issues,
            'metrics': self.metrics,
            'compliance': self._get_compliance_level()
        }

    def _analyze_directory(self, directory: Path):
        """Recursively analyze all source files in directory."""
        # Common source file extensions
        extensions = {'.py', '.js', '.ts', '.java', '.go', '.rb', '.php', '.c', '.cpp', '.cs'}

        for file_path in directory.rglob('*'):
            if file_path.suffix in extensions and file_path.is_file():
                # Skip test files in analysis (we'll check they exist separately)
                if not self._is_test_file(file_path):
                    self._analyze_file(file_path)

    def _analyze_file(self, file_path: Path):
        """Analyze a single source file for TDD compliance."""
        self.metrics['files_analyzed'] += 1

        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
                lines = content.split('\n')

            # Check for code smells
            self._check_nested_conditionals(file_path, content)
            self._check_long_methods(file_path, lines)
            self._check_complex_conditions(file_path, content)
            self._check_missing_abstractions(file_path, content)

            # Check if corresponding test file exists
            self._check_test_coverage(file_path)

        except Exception as e:
            self.issues.append({
                'file': str(file_path),
                'type': 'error',
                'message': f'Failed to analyze file: {str(e)}'
            })

    def _check_nested_conditionals(self, file_path: Path, content: str):
        """Detect deeply nested conditional statements."""
        pattern = self.CODE_SMELLS['nested_conditionals']
        matches = re.finditer(pattern, content)

        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            self.issues.append({
                'file': str(file_path),
                'line': line_num,
                'type': 'code_smell',
                'severity': 'high',
                'smell': 'nested_conditionals',
                'message': 'Nested conditional statements detected. TDD typically produces flatter, more testable code structures.'
            })
            self.metrics['code_smells'] += 1

    def _check_long_methods(self, file_path: Path, lines: List[str]):
        """Detect methods/functions that are too long."""
        # Simple heuristic: methods longer than 20 lines
        in_method = False
        method_start = 0
        method_name = ''
        indent_level = 0

        for i, line in enumerate(lines):
            stripped = line.lstrip()

            # Detect method/function definitions (language-agnostic patterns)
            if any(keyword in stripped for keyword in ['def ', 'function ', 'func ', 'public ', 'private ', 'protected ']):
                if '{' in stripped or ':' in stripped:
                    in_method = True
                    method_start = i + 1
                    method_name = stripped.split('(')[0].split()[-1]
                    indent_level = len(line) - len(stripped)

            # Check if method ended
            elif in_method:
                current_indent = len(line) - len(line.lstrip())
                if stripped and current_indent <= indent_level and stripped not in ['}', 'end']:
                    method_length = i - method_start
                    if method_length > 20:
                        self.issues.append({
                            'file': str(file_path),
                            'line': method_start,
                            'type': 'code_smell',
                            'severity': 'medium',
                            'smell': 'long_method',
                            'message': f'Method "{method_name}" is {method_length} lines long. TDD encourages smaller, focused methods.'
                        })
                        self.metrics['code_smells'] += 1
                    in_method = False

    def _check_complex_conditions(self, file_path: Path, content: str):
        """Detect overly complex conditional expressions."""
        pattern = self.CODE_SMELLS['complex_conditions']
        matches = re.finditer(pattern, content)

        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            self.issues.append({
                'file': str(file_path),
                'line': line_num,
                'type': 'code_smell',
                'severity': 'medium',
                'smell': 'complex_conditions',
                'message': 'Complex boolean conditions detected. TDD promotes simpler, more testable conditions.'
            })
            self.metrics['code_smells'] += 1

    def _check_missing_abstractions(self, file_path: Path, content: str):
        """Detect type checking that suggests missing abstractions."""
        pattern = self.CODE_SMELLS['missing_abstractions']
        matches = re.finditer(pattern, content)

        for match in matches:
            line_num = content[:match.start()].count('\n') + 1
            self.issues.append({
                'file': str(file_path),
                'line': line_num,
                'type': 'code_smell',
                'severity': 'medium',
                'smell': 'missing_abstractions',
                'message': 'Type checking detected. TDD encourages polymorphism over type checking.'
            })
            self.metrics['code_smells'] += 1

    def _check_test_coverage(self, file_path: Path):
        """Check if a corresponding test file exists."""
        test_file = self._find_test_file(file_path)

        if test_file and test_file.exists():
            self.metrics['test_files_found'] += 1
        else:
            self.issues.append({
                'file': str(file_path),
                'type': 'missing_test',
                'severity': 'critical',
                'message': f'No corresponding test file found. Expected: {test_file}'
            })

    def _find_test_file(self, source_file: Path) -> Path:
        """Find the expected test file location for a source file."""
        # Common test file patterns
        test_patterns = [
            lambda p: p.parent / f'test_{p.name}',
            lambda p: p.parent / f'{p.stem}_test{p.suffix}',
            lambda p: p.parent / 'tests' / f'test_{p.name}',
            lambda p: p.parent.parent / 'tests' / p.parent.name / f'test_{p.name}',
            lambda p: p.parent.parent / 'test' / p.parent.name / f'test_{p.name}',
        ]

        for pattern in test_patterns:
            test_file = pattern(source_file)
            if test_file.exists():
                return test_file

        # Return the most common pattern as expected location
        return source_file.parent / f'test_{source_file.name}'

    def _is_test_file(self, file_path: Path) -> bool:
        """Check if a file is a test file."""
        name = file_path.name.lower()
        return any([
            name.startswith('test_'),
            name.endswith('_test.py'),
            name.endswith('_test.js'),
            name.endswith('.test.js'),
            name.endswith('.spec.js'),
            'test' in file_path.parts,
            'tests' in file_path.parts,
        ])

    def _calculate_tdd_score(self):
        """Calculate an overall TDD compliance score (0-100)."""
        if self.metrics['files_analyzed'] == 0:
            self.metrics['tdd_score'] = 0.0
            return

        # Factors that contribute to score
        test_coverage_ratio = self.metrics['test_files_found'] / self.metrics['files_analyzed']
        smell_penalty = min(self.metrics['code_smells'] * 5, 50)  # Max 50 point penalty

        # Score calculation
        score = (test_coverage_ratio * 100) - smell_penalty
        self.metrics['tdd_score'] = max(0.0, min(100.0, score))

    def _get_compliance_level(self) -> str:
        """Get human-readable compliance level."""
        score = self.metrics['tdd_score']

        if score >= 90:
            return 'excellent'
        elif score >= 75:
            return 'good'
        elif score >= 50:
            return 'fair'
        elif score >= 25:
            return 'poor'
        else:
            return 'critical'


def main():
    """Main entry point for the TDD compliance checker."""
    if len(sys.argv) < 2:
        print("Usage: check_tdd_compliance.py <path>")
        print("  path: File or directory to analyze")
        sys.exit(1)

    path = sys.argv[1]

    if not os.path.exists(path):
        print(f"Error: Path '{path}' does not exist")
        sys.exit(1)

    checker = TDDComplianceChecker(path)
    results = checker.analyze()

    # Output results as JSON
    print(json.dumps(results, indent=2))

    # Exit with appropriate code
    if results['compliance'] in ['critical', 'poor']:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
