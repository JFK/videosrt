---
description: Audit and maintain .claude/ configuration
             (commands, agents, rules, hooks, settings)
---

Perform a full audit of the `.claude/` directory against
the current codebase state. Report all findings, then ask
which fixes to apply.

## Audit Steps

### 1. Rules Audit (.claude/rules/)
- Verify referenced imports, packages, patterns still exist
- Check if new patterns have emerged that rules don't cover
- Verify forbidden patterns are not present in the code

### 2. Commands Audit (.claude/commands/)
- Verify CLI commands work (make targets, npm scripts)
- Check MCP tools and parameters match current API
- Verify file paths and tool references are valid

### 3. Agents Audit (.claude/agents/)
- Verify file paths, test patterns, tech stack descriptions
- Check consistency with current project structure

### 4. Hooks Audit (settings.json)
- Verify hook scripts exist and are executable
- Check file pattern matchers cover current file types
- Check secret detection patterns are comprehensive

### 5. Permissions Audit (settings.json)
- Check if allowed commands reference installed tools
- Check if needed commands are missing from allowlist

### 6. CLAUDE.md Consistency Check
- Verify CLAUDE.md references match .claude/ contents
- Flag drift between documentation and configuration

## Output Format

| # | Severity | File | Issue | Proposed Fix |
|---|----------|------|-------|-------------|

After presenting findings, ask which fixes to apply.
Do not modify settings.local.json (user-specific).
