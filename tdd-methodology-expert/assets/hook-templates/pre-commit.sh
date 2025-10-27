#!/bin/bash
#
# Git Pre-Commit Hook for TDD Enforcement
#
# This hook runs before each git commit to ensure TDD principles are followed.
# It validates that tests exist and checks for code smells that indicate
# tests-after-code development.

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🔍 Running TDD compliance check...${NC}"

# Find the skill directory (assuming it's in a standard location)
# You may need to adjust this path based on where the skill is installed
SKILL_SCRIPT=""
if [ -f "$HOME/.claude/skills/tdd-methodology-expert/scripts/check_tdd_compliance.py" ]; then
    SKILL_SCRIPT="$HOME/.claude/skills/tdd-methodology-expert/scripts/check_tdd_compliance.py"
elif [ -f "./.claude/skills/tdd-methodology-expert/scripts/check_tdd_compliance.py" ]; then
    SKILL_SCRIPT="./.claude/skills/tdd-methodology-expert/scripts/check_tdd_compliance.py"
fi

if [ -z "$SKILL_SCRIPT" ]; then
    echo -e "${YELLOW}⚠️  TDD compliance script not found. Skipping check.${NC}"
    exit 0
fi

# Get list of staged files
STAGED_FILES=$(git diff --cached --name-only --diff-filter=ACM)

if [ -z "$STAGED_FILES" ]; then
    echo -e "${GREEN}✅ No files to check${NC}"
    exit 0
fi

# Create temporary directory for checking
TEMP_DIR=$(mktemp -d)
trap "rm -rf $TEMP_DIR" EXIT

# Copy staged files to temp directory
for FILE in $STAGED_FILES; do
    if [ -f "$FILE" ]; then
        mkdir -p "$TEMP_DIR/$(dirname "$FILE")"
        git show ":$FILE" > "$TEMP_DIR/$FILE"
    fi
done

# Run TDD compliance check on staged files
echo -e "${BLUE}Analyzing staged files for TDD compliance...${NC}"
OUTPUT=$(python3 "$SKILL_SCRIPT" "$TEMP_DIR" 2>&1)
EXIT_CODE=$?

# Parse results
COMPLIANCE_LEVEL=$(echo "$OUTPUT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['compliance'])" 2>/dev/null || echo "unknown")
TDD_SCORE=$(echo "$OUTPUT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['metrics']['tdd_score'])" 2>/dev/null || echo "0")
CODE_SMELLS=$(echo "$OUTPUT" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data['metrics']['code_smells'])" 2>/dev/null || echo "0")

echo ""
echo "📊 TDD Compliance Report:"
echo "   Score: $TDD_SCORE/100"
echo "   Level: $COMPLIANCE_LEVEL"
echo "   Code Smells: $CODE_SMELLS"
echo ""

if [ "$EXIT_CODE" -ne 0 ]; then
    echo -e "${RED}❌ TDD compliance check failed!${NC}"
    echo ""
    echo "Issues found:"
    echo "$OUTPUT" | python3 -c "
import sys, json
try:
    data = json.load(sys.stdin)
    for issue in data['issues'][:5]:  # Show first 5 issues
        severity = issue.get('severity', 'unknown')
        msg = issue.get('message', 'Unknown issue')
        file = issue.get('file', '')
        line = issue.get('line', '')

        location = f'{file}:{line}' if line else file
        print(f'  • [{severity.upper()}] {location}')
        print(f'    {msg}')
        print()
except:
    pass
" 2>/dev/null

    echo ""
    echo -e "${YELLOW}💡 TDD Reminder:${NC}"
    echo "   1. 🔴 Write a failing test first"
    echo "   2. 🟢 Write minimal code to pass the test"
    echo "   3. 🔵 Refactor while keeping tests green"
    echo ""
    echo "To commit anyway, use: git commit --no-verify"
    echo ""

    exit 1
fi

echo -e "${GREEN}✅ TDD compliance check passed!${NC}"
echo ""
exit 0
