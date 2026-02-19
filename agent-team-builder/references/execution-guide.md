# Agent Team Execution Guide

How to spawn and run a multi-agent team using Claude Code's built-in tools. Read this during Phase 4 execution.

## Contents
1. [Tool Overview](#tool-overview)
2. [Step-by-Step Execution](#step-by-step-execution)
3. [Implementing Quality Gates](#implementing-quality-gates)
4. [Orchestrator Prompt Template](#orchestrator-prompt-template)
5. [Shutdown & Cleanup](#shutdown--cleanup)
6. [Common Pitfalls](#common-pitfalls)

---

## Tool Overview

| Tool | Purpose |
|------|---------|
| `TeamCreate` | Creates the team namespace and task list |
| `TaskCreate` | Adds a task to the shared task list |
| `TaskUpdate` | Updates task status (pending → in_progress → completed) |
| `TaskList` | Lists all tasks and their current state |
| `Task` | Spawns a sub-agent (worker or orchestrator) |
| `SendMessage` | Sends a message to a named teammate |
| `AskUserQuestion` | Prompts the user (used for human quality gates) |

---

## Step-by-Step Execution

### 1. Create the Team

```
TeamCreate(
  team_name="article-team",
  description="Write a comprehensive article about X"
)
```

### 2. Create Tasks

Create one task per major pipeline stage. Use `addBlockedBy` to enforce sequencing.

```
t1 = TaskCreate(subject="Research phase", description="...")
t2 = TaskCreate(subject="Draft outline", description="...")
TaskUpdate(taskId=t2.id, addBlockedBy=[t1.id])
t3 = TaskCreate(subject="Write first draft", description="...")
TaskUpdate(taskId=t3.id, addBlockedBy=[t2.id])
...
```

For parallel stages, create sibling tasks with the same `addBlockedBy`:
```
t3a = TaskCreate(subject="Write introduction", ...)
t3b = TaskCreate(subject="Write body sections", ...)
TaskUpdate(taskId=t3a.id, addBlockedBy=[t2.id])
TaskUpdate(taskId=t3b.id, addBlockedBy=[t2.id])
```

### 3. Spawn the Orchestrator

The orchestrator is the most important agent — it manages everything. Spawn it with the Task tool using `subagent_type="general-purpose"` and provide a detailed prompt (see template below).

```
Task(
  subagent_type="general-purpose",
  description="Orchestrate article-team",
  prompt="[full orchestrator prompt - see template]",
  team_name="article-team",
  name="orchestrator"
)
```

### 4. Spawn Worker Agents (from the Orchestrator)

The orchestrator spawns each worker when its predecessor task is complete:

```
Task(
  subagent_type="general-purpose",
  description="Research agent",
  prompt="You are the Researcher for article-team. [task-specific instructions]",
  team_name="article-team",
  name="researcher"
)
```

Workers should:
- Mark their task in_progress when starting: `TaskUpdate(taskId=X, status="in_progress")`
- Mark their task completed when done: `TaskUpdate(taskId=X, status="completed")`
- Send their output to the orchestrator via `SendMessage`

---

## Implementing Quality Gates

### Human Gates

Use `AskUserQuestion` within the orchestrator (or a gate-checking agent) to pause and get user sign-off:

```python
# Example: human gate after outline
AskUserQuestion(questions=[{
  "question": "Does this outline look good to proceed with drafting?",
  "header": "Outline review",
  "options": [
    {"label": "Approved", "description": "Proceed to drafting"},
    {"label": "Revise", "description": "Send back for changes"}
  ]
}])
```

If the user selects "Revise", send specific revision instructions to the relevant agent via `SendMessage` and loop.

### Automated Gates

Spawn a dedicated critic agent to review and return a pass/fail verdict:

```
Task(
  subagent_type="general-purpose",
  name="quality-critic",
  description="Review draft quality",
  prompt="""
  You are a quality critic. Review the following draft against these criteria:
  - Covers all outline sections: [list them]
  - Word count between 1200-1500 words
  - No unsupported factual claims
  - Matches tone: [description]

  Return ONLY:
  VERDICT: PASS or FAIL
  NOTES: [specific issues if FAIL, or 'None' if PASS]

  Draft to review:
  [draft content]
  """
)
```

The orchestrator reads the critic's verdict from the task output and branches accordingly.

### Loop Logic

```
loop_count = 0
MAX_LOOPS = 3

while loop_count < MAX_LOOPS:
    run_stage()
    verdict = run_gate()
    if verdict == "PASS":
        break
    else:
        send_revision_instructions_to_agent(verdict.notes)
        loop_count += 1

if loop_count == MAX_LOOPS:
    # Escalate to user
    AskUserQuestion: "We've hit the max revision limit. Here's the current output. How would you like to proceed?"
```

---

## Orchestrator Prompt Template

Use this template when spawning the orchestrator. Fill in the bracketed sections.

```
You are the orchestrator for [team-name].

## Goal
[One sentence goal]

## Team
[List each agent name and their role]

## Workflow
[Stage 1] → [GATE 1] → [Stage 2] → [GATE 2] → [Stage 3]

## Your Responsibilities
1. Spawn each worker agent using the Task tool when their preceding task is complete
2. Pass outputs between agents via SendMessage
3. Enforce quality gates as described below
4. Loop on gate failure (max [N] iterations per gate)
5. Escalate to the user if max iterations are exceeded
6. Compile the final output and deliver it to the user
7. Shut down the team when complete

## Quality Gates
[Gate 1]
- After: [stage name]
- Type: [human/automated]
- Criteria: [specific measurable criteria]
- On fail: [specific revision instruction]

[Gate 2]
...

## Agent Spawning Instructions
For each agent, use the Task tool with:
- subagent_type: "general-purpose"
- team_name: "[team-name]"
- name: "[agent-name]"
- prompt: [detailed role instructions]

Each worker agent should:
- Receive their inputs via SendMessage from you
- Mark their TaskCreate task as in_progress when starting
- Send their completed output back to you via SendMessage
- Mark their task as completed when done

## Final Delivery
When all gates have passed and the final agent completes:
1. Compile the full output
2. Present it to the user directly in the conversation
3. Send a shutdown_request to all active agents
4. Call TeamDelete to clean up

Begin by spawning the first agent: [agent-name].
```

---

## Shutdown & Cleanup

When all work is complete:

1. Send `shutdown_request` to each active agent:
```
SendMessage(type="shutdown_request", recipient="researcher", content="Work complete, shutting down.")
```

2. Wait for `shutdown_response` from each agent.

3. Delete the team:
```
TeamDelete()
```

---

## Common Pitfalls

| Pitfall | Fix |
|---------|-----|
| Agents going idle without completing tasks | Ensure each agent prompt includes explicit instruction to mark task completed and send output via SendMessage |
| Orchestrator losing track of loop count | Use TaskCreate to track loop counts as metadata, not in-memory |
| Human gate never resolving | Set a timeout or default action if user doesn't respond within N minutes |
| Critic agent returning ambiguous verdicts | Require strict format: `VERDICT: PASS` or `VERDICT: FAIL` — anything else is treated as FAIL |
| Parallel agents producing incompatible outputs | Add a Consolidator agent after parallel stages to merge and harmonise output before the next gate |
| Team not shutting down | Always include TeamDelete in the orchestrator's final step |
