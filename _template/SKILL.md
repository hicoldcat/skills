---
name: {{SKILL_NAME}}
description: {{SKILL_DESCRIPTION}}
---

# {{SKILL_NAME}}

Write concise, procedural instructions for another Claude instance.

## Triggers

- Use when the task involves ...
- Use when the user mentions ...
- Use when the work touches ...

## Workflow

1. Inspect the current context and touched files
2. Read any bundled references only if needed
3. Apply the repository- or domain-specific rules
4. Use bundled scripts or assets when they add reliability
5. Return a concise result with verification steps

## Rules

- Preserve existing conventions unless the task explicitly requires change
- Keep edits local and compatible with current workflows
- Avoid unnecessary refactors or dependency churn
- Add safety notes specific to this skill

## References

- Read `references/...` when you need deeper domain details
- Use `scripts/...` when a deterministic helper is provided
- Use `assets/...` only when the task needs bundled output resources

## Examples

- "Help me ..."
- "Fix ..."
- "Review ..."

## Output

- Summarize what changed or what was found
- Mention affected files or systems
- Include the smallest useful verification steps
