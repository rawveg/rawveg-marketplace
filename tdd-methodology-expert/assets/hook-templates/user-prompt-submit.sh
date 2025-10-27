#!/bin/bash
#
# Claude Code User-Prompt-Submit Hook for TDD Reinforcement
#
# This hook runs before every user prompt is submitted to Claude,
# injecting TDD methodology reminders and context into the conversation.

# Colors for output (for debugging)
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get the user's original prompt from stdin
USER_PROMPT=$(cat)

# Build TDD reinforcement message
TDD_REMINDER="

🔴🟢🔵 TDD Methodology Reminder:

This project follows Test-Driven Development (TDD). Every code change must follow the Red-Green-Refactor cycle:

1. 🔴 RED Phase: Write a failing test first
   - Write the test before any production code
   - Test should fail because the feature doesn't exist yet
   - Test should clearly express the desired behavior

2. 🟢 GREEN Phase: Make the test pass
   - Write the minimal code needed to pass the test
   - Don't add extra features or abstractions yet
   - Focus on making the test pass as quickly as possible

3. 🔵 REFACTOR Phase: Improve the code
   - Clean up the code while keeping tests green
   - Remove duplication
   - Improve names and structure
   - Ensure code is maintainable and readable

Code developed with TDD exhibits these characteristics:
✅ Small, focused functions/methods (typically <20 lines)
✅ Flat control flow (minimal nesting, no deep if/elif/else chains)
✅ Clear separation of concerns
✅ High testability and mockability
✅ Simple, straightforward logic

Code developed test-after (NOT TDD) often shows:
❌ Long, complex methods
❌ Deeply nested conditionals
❌ Complex boolean expressions
❌ Type checking instead of polymorphism
❌ Tight coupling and poor abstractions

When responding to this request:
• Explicitly state which TDD phase you're in (Red, Green, or Refactor)
• Write tests BEFORE any production code
• Verify tests fail before implementing features (Red phase)
• Implement minimal code to pass tests (Green phase)
• Refactor only after tests are passing (Refactor phase)
• Validate TDD compliance using the check_tdd_compliance.py script when appropriate
• Reassure the user that TDD principles are being followed

User's original request:
$USER_PROMPT
"

# Output the augmented prompt
echo "$TDD_REMINDER"

# Exit successfully
exit 0
