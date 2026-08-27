# Common AI Development Skill

Use this skill for repository discovery, environment validation, implementation, testing, security, and reproducibility.

## Workflow

```text
Discover repository
→ Read project instructions
→ Detect runtime
→ Measure available resources
→ Resolve configuration
→ Run smallest meaningful smoke test
→ Lock validated configuration
→ Implement
→ Test
→ Record reproducibility/resource metadata
```

## Rules

- Prefer measured capability over assumptions.
- Preserve existing project conventions unless the change intentionally updates them.
- Make destructive changes explicit.
- Keep configuration centralized and reproducible.
- Never expose secrets.
- Use staged validation and avoid repeating known failing configurations.
