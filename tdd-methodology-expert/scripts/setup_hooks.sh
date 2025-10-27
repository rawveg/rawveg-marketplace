#!/bin/bash
#
# Setup TDD Hooks
#
# Installs git hooks and Claude Code hooks for TDD enforcement.
# This script should be run once per project to enable TDD reinforcement.

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SKILL_DIR="$(dirname "$SCRIPT_DIR")"
PROJECT_ROOT="${1:-.}"

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "🔧 Setting up TDD hooks for project: $PROJECT_ROOT"

# Check if git repository
if [ ! -d "$PROJECT_ROOT/.git" ]; then
    echo -e "${YELLOW}Warning: Not a git repository. Skipping git hooks.${NC}"
    GIT_HOOKS=false
else
    GIT_HOOKS=true
fi

# Check if Claude Code project
if [ ! -d "$PROJECT_ROOT/.claude" ]; then
    echo -e "${YELLOW}Warning: Not a Claude Code project. Creating .claude directory.${NC}"
    mkdir -p "$PROJECT_ROOT/.claude"
fi

# Install git pre-commit hook
if [ "$GIT_HOOKS" = true ]; then
    echo "📝 Installing git pre-commit hook..."
    HOOKS_DIR="$PROJECT_ROOT/.git/hooks"
    mkdir -p "$HOOKS_DIR"

    # Copy pre-commit hook template
    cp "$SKILL_DIR/assets/hook-templates/pre-commit.sh" "$HOOKS_DIR/pre-commit"
    chmod +x "$HOOKS_DIR/pre-commit"

    echo -e "${GREEN}✅ Git pre-commit hook installed${NC}"
fi

# Install Claude Code user-prompt-submit hook
echo "📝 Installing Claude Code user-prompt-submit hook..."
CLAUDE_HOOKS_DIR="$PROJECT_ROOT/.claude/hooks"
mkdir -p "$CLAUDE_HOOKS_DIR"

# Copy user-prompt-submit hook template
cp "$SKILL_DIR/assets/hook-templates/user-prompt-submit.sh" "$CLAUDE_HOOKS_DIR/user-prompt-submit"
chmod +x "$CLAUDE_HOOKS_DIR/user-prompt-submit"

echo -e "${GREEN}✅ Claude Code user-prompt-submit hook installed${NC}"

# Create or update CLAUDE.md to mention TDD
CLAUDE_MD="$PROJECT_ROOT/.claude/CLAUDE.md"
if [ ! -f "$CLAUDE_MD" ]; then
    echo "📝 Creating CLAUDE.md with TDD requirement..."
    cat > "$CLAUDE_MD" << 'EOF'
# Project Guidelines

## Development Methodology

**This project uses Test-Driven Development (TDD).**

All code must be developed following the Red-Green-Refactor cycle:
1. 🔴 Red: Write a failing test first
2. 🟢 Green: Write minimal code to make the test pass
3. 🔵 Refactor: Improve code while keeping tests green

The `tdd-methodology-expert` skill is automatically loaded for this project.
EOF
    echo -e "${GREEN}✅ CLAUDE.md created with TDD requirement${NC}"
else
    # Check if TDD is already mentioned
    if ! grep -q "TDD\|Test-Driven Development" "$CLAUDE_MD"; then
        echo "📝 Updating CLAUDE.md with TDD requirement..."
        echo "" >> "$CLAUDE_MD"
        echo "## Development Methodology" >> "$CLAUDE_MD"
        echo "" >> "$CLAUDE_MD"
        echo "**This project uses Test-Driven Development (TDD).**" >> "$CLAUDE_MD"
        echo "" >> "$CLAUDE_MD"
        echo "All code must be developed following the Red-Green-Refactor cycle." >> "$CLAUDE_MD"
        echo "The \`tdd-methodology-expert\` skill is automatically loaded for this project." >> "$CLAUDE_MD"
        echo -e "${GREEN}✅ CLAUDE.md updated with TDD requirement${NC}"
    else
        echo -e "${GREEN}✅ CLAUDE.md already mentions TDD${NC}"
    fi
fi

# Make scripts executable
chmod +x "$SKILL_DIR/scripts/"*.py

echo ""
echo -e "${GREEN}✅ TDD hooks setup complete!${NC}"
echo ""
echo "The following hooks have been installed:"
if [ "$GIT_HOOKS" = true ]; then
    echo "  • Git pre-commit hook: Validates TDD compliance before commits"
fi
echo "  • Claude Code user-prompt-submit hook: Reinforces TDD in every interaction"
echo ""
echo "To verify installation, run:"
if [ "$GIT_HOOKS" = true ]; then
    echo "  git hook run pre-commit"
fi
echo "  cat $PROJECT_ROOT/.claude/hooks/user-prompt-submit"
