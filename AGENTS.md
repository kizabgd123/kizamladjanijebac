# AGENTS.md — Autonomous Agent Guidelines

Guidelines for AI coding agents (Copilot, Antigravity, Hermes, Claude, Codex) working in this workspace.

## Quick Reference Commands

### Bootstrap Entire Environment from Scratch

```bash
cd agy-hermes-kit && ./bootstrap.sh
```

### Sync MCP Servers (Antigravity & Hermes)

```bash
python3 agy-hermes-kit/scripts/sync_mcp.py --write
```

### Diagnostic Verification

```bash
bash agy-hermes-kit/scripts/verify.sh
```

### Pre-Action JudgeGuard Verification

```bash
echo "🟡 Starting [ACTION]" >> WORK_LOG.md
python3 judge_guard.py "Start [ACTION]"
```

### Post-Action JudgeGuard Verification

```bash
echo "✅ Completed [ACTION]" >> WORK_LOG.md
python3 judge_guard.py "Verify [ACTION] Complete"
```

## Mandatory Operating Protocols

1. **Law of Work Log:** Before executing any significant action, append `🟡 Starting [ACTION]` to `WORK_LOG.md`. Upon completion, append `✅ Completed [ACTION]`.
2. **Task Backlog Cap:** Maximum 5 open `🟡 Starting` tasks at any time. Close or abandon open tasks before starting new ones.
3. **Safety & Zero Destruction:** Never execute destructive system commands (`rm -rf /`, `chmod -R 777`). All operations must preserve data integrity.
4. **Configuration Single Source of Truth:** All shared MCP definitions must be modified in `agy-hermes-kit/configs/connections.json`, never manually patched in generated configs.
5. **Skill Standard:** Custom skills belong in `agy-hermes-kit/skills/<skill-name>/SKILL.md` and are symlinked into `~/.agents/skills/` for cross-agent discovery.

## Key Paths & Components

- [agy-hermes-kit/README.md](./agy-hermes-kit/README.md) — Detailed portable kit documentation
- [agy-hermes-kit/configs/connections.json](./agy-hermes-kit/configs/connections.json) — Universal MCP connection registry
- [judge_guard.py](./judge_guard.py) — 3-layer invariant and workflow verification engine
- [WORK_LOG.md](./WORK_LOG.md) — Persistent chronological audit log
