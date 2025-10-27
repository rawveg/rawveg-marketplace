#!/usr/bin/env python3
"""
Test Validator

Validates that tests exist, are properly structured, and follow TDD principles.
"""

import os
import re
import sys
import json
from pathlib import Path
from typing import Dict, List, Set


class TestValidator:
    """Validates test files for TDD compliance."""

    def __init__(self, path: str):
        self.path = Path(path)
        self.results = {
            'valid': True,
            'test_files': [],
            'issues': [],
            'stats': {
                'total_tests': 0,
                'test_files_found': 0,
                'well_structured': 0
            }
        }

    def validate(self) -> Dict:
        """Run full test validation."""
        test_files = self._find_test_files()

        if not test_files:
            self.results['valid'] = False
            self.results['issues'].append({
                'type': 'no_tests',
                'severity': 'critical',
                'message': 'No test files found. TDD requires writing tests first.'
            })
            return self.results

        for test_file in test_files:
            self._validate_test_file(test_file)

        return self.results

    def _find_test_files(self) -> List[Path]:
        """Find all test files in the path."""
        test_files = []

        if self.path.is_file():
            if self._is_test_file(self.path):
                test_files.append(self.path)
        else:
            for file_path in self.path.rglob('*'):
                if file_path.is_file() and self._is_test_file(file_path):
                    test_files.append(file_path)

        return test_files

    def _is_test_file(self, file_path: Path) -> bool:
        """Check if a file is a test file."""
        name = file_path.name.lower()
        return any([
            name.startswith('test_'),
            name.endswith('_test.py'),
            name.endswith('_test.js'),
            name.endswith('.test.js'),
            name.endswith('.test.ts'),
            name.endswith('.spec.js'),
            name.endswith('.spec.ts'),
            name.endswith('Test.java'),
            name.endswith('_test.go'),
            'test' in file_path.parts,
            'tests' in file_path.parts,
        ])

    def _validate_test_file(self, test_file: Path):
        """Validate a single test file."""
        self.results['stats']['test_files_found'] += 1
        file_result = {
            'file': str(test_file),
            'tests_found': 0,
            'issues': []
        }

        try:
            with open(test_file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Count test cases
            test_count = self._count_tests(content, test_file.suffix)
            file_result['tests_found'] = test_count
            self.results['stats']['total_tests'] += test_count

            if test_count == 0:
                file_result['issues'].append({
                    'type': 'empty_test_file',
                    'severity': 'high',
                    'message': 'Test file contains no test cases'
                })
                self.results['valid'] = False

            # Check test structure
            structure_issues = self._check_test_structure(content, test_file)
            file_result['issues'].extend(structure_issues)

            if not structure_issues:
                self.results['stats']['well_structured'] += 1

            # Check for TDD patterns
            tdd_issues = self._check_tdd_patterns(content, test_file)
            file_result['issues'].extend(tdd_issues)

        except Exception as e:
            file_result['issues'].append({
                'type': 'error',
                'severity': 'high',
                'message': f'Failed to validate test file: {str(e)}'
            })
            self.results['valid'] = False

        self.results['test_files'].append(file_result)

        # Aggregate issues
        for issue in file_result['issues']:
            if issue['severity'] in ['critical', 'high']:
                self.results['valid'] = False
            self.results['issues'].append({
                'file': str(test_file),
                **issue
            })

    def _count_tests(self, content: str, extension: str) -> int:
        """Count the number of test cases in the file."""
        count = 0

        # Language-specific test detection patterns
        patterns = {
            '.py': [r'def test_\w+', r'@pytest\.mark\.'],
            '.js': [r'(test|it)\s*\(', r'describe\s*\('],
            '.ts': [r'(test|it)\s*\(', r'describe\s*\('],
            '.java': [r'@Test', r'public\s+void\s+test\w+'],
            '.go': [r'func\s+Test\w+'],
            '.rb': [r'(it|test)\s+["\']', r'describe\s+["\']'],
            '.php': [r'public\s+function\s+test\w+', r'@test'],
        }

        if extension in patterns:
            for pattern in patterns[extension]:
                count += len(re.findall(pattern, content))

        return count

    def _check_test_structure(self, content: str, test_file: Path) -> List[Dict]:
        """Check if tests follow good structure patterns."""
        issues = []

        # Check for Arrange-Act-Assert pattern (AAA)
        lines = content.split('\n')

        # Look for test functions
        test_functions = self._extract_test_functions(content, test_file.suffix)

        for func_name, func_body in test_functions:
            # Check if test is too long (suggests poor structure)
            func_lines = func_body.split('\n')
            if len(func_lines) > 30:
                issues.append({
                    'type': 'long_test',
                    'severity': 'medium',
                    'test': func_name,
                    'message': f'Test "{func_name}" is {len(func_lines)} lines long. Consider breaking it down.'
                })

            # Check for multiple assertions in one test (might indicate poor isolation)
            assertion_count = len(re.findall(r'assert|expect|should', func_body, re.IGNORECASE))
            if assertion_count > 5:
                issues.append({
                    'type': 'multiple_assertions',
                    'severity': 'low',
                    'test': func_name,
                    'message': f'Test "{func_name}" has {assertion_count} assertions. Consider splitting into focused tests.'
                })

        return issues

    def _extract_test_functions(self, content: str, extension: str) -> List[tuple]:
        """Extract test function names and bodies."""
        functions = []

        # Simple extraction for Python
        if extension == '.py':
            pattern = r'def (test_\w+)\s*\([^)]*\):\s*\n((?:    .*\n)*)'
            matches = re.finditer(pattern, content)
            for match in matches:
                functions.append((match.group(1), match.group(2)))

        # Simple extraction for JavaScript/TypeScript
        elif extension in ['.js', '.ts']:
            pattern = r'(test|it)\s*\([\'"]([^\'"]+)[\'"].*?\{([^}]*)\}'
            matches = re.finditer(pattern, content, re.DOTALL)
            for match in matches:
                functions.append((match.group(2), match.group(3)))

        return functions

    def _check_tdd_patterns(self, content: str, test_file: Path) -> List[Dict]:
        """Check for patterns that indicate TDD was followed."""
        issues = []

        # Check for test-first indicators
        # Red-Green-Refactor should result in:
        # 1. Tests that clearly express intent
        # 2. Minimal production code to make tests pass
        # 3. Clear test names that describe behavior

        test_functions = self._extract_test_functions(content, test_file.suffix)

        for func_name, func_body in test_functions:
            # Check for descriptive test names
            if len(func_name) < 10 or not any(word in func_name.lower() for word in ['should', 'when', 'given', 'test']):
                issues.append({
                    'type': 'poor_test_name',
                    'severity': 'low',
                    'test': func_name,
                    'message': f'Test name "{func_name}" is not descriptive. TDD encourages behavior-focused names.'
                })

            # Check for setup/teardown patterns
            if not any(keyword in content for keyword in ['setUp', 'beforeEach', 'before', 'setup', 'fixture']):
                # Only flag if multiple tests exist
                if len(test_functions) > 3:
                    issues.append({
                        'type': 'missing_setup',
                        'severity': 'low',
                        'message': 'No setup/fixture detected. Consider DRY principle in test arrangement.'
                    })
                    break  # Only report once per file

        return issues


def main():
    """Main entry point for the test validator."""
    if len(sys.argv) < 2:
        print("Usage: validate_tests.py <path>")
        print("  path: File or directory containing tests to validate")
        sys.exit(1)

    path = sys.argv[1]

    if not os.path.exists(path):
        print(f"Error: Path '{path}' does not exist")
        sys.exit(1)

    validator = TestValidator(path)
    results = validator.validate()

    # Output results as JSON
    print(json.dumps(results, indent=2))

    # Exit with appropriate code
    if not results['valid']:
        sys.exit(1)
    else:
        sys.exit(0)


if __name__ == '__main__':
    main()
