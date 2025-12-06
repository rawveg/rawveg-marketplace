# Presumption Guard

A Claude Code plugin that detects and flags presumptive actions after they occur.

## What It Does

This plugin adds a Stop hook that reviews every completed response for **presumptive behavior**. It doesn't prevent the action - it makes it absolutely clear when one has taken place.

The hook distinguishes between:

- **Presumption to ask** (acceptable): Asking clarifying questions, seeking input, discussing options
- **Presumption to act** (violation): Taking actions or making decisions without explicit permission

## How It Works

When Claude's response completes, the Stop hook triggers a review that evaluates:

1. **Unrequested actions** - Did it perform edits, writes, or executions that were NOT explicitly requested?
2. **Unverified certainty** - Did it claim certainty about facts without verifying first?
3. **Stolen decisions** - Did it make decisions that belong to the user without asking first?
4. **Workflow deviation** - Did it deviate from explicit workflow instructions?

## What's NOT a Violation

- Asking questions
- Seeking clarification
- Discussing options when no specific workflow was given
- Following explicit instructions

## Installation

Enable the plugin in your Claude Code settings:

```json
{
  "enabledPlugins": {
    "presumption-guard@skillsforge-marketplace": true
  }
}
```

## Origin

This plugin emerged from a direct lesson about agency and accountability: taking choices that belong to others is theft. The pause to ask is not inefficiency - it prevents compounding harm.

## License

MIT
