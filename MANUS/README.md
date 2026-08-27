# Manus Integration

Manus does not currently document a repository-root `AGENTS.md`-style automatic instruction filename. The supported integration path is to use Manus Project Instructions and file-system-based Skills. Manus supports importing Skills from public GitHub repositories and using project-specific Skills. citeturn238096search1turn238096search2

## Project Instructions

Copy the contents of `MANUS/PROJECT_INSTRUCTIONS.md` into the Manus Project Instructions for the project. Project instructions are then applied to tasks in that Manus project.

## Skill

`MANUS/SKILL.md` is a reusable codingStandard Skill. For a public Skill repository, Manus supports importing a GitHub repository through the Skills UI. Review the Skill and bundled resources before importing community-created Skills.

## Local Development

When Manus Desktop App / My Computer is used, commands operate on authorized local folders through the terminal. Grant only the minimum folder access needed and review repository scripts before execution. citeturn154244search7turn154244search6

## Relation to codingStandard Domains

```text
Manus Project Instructions
        ↓
COMMON
        ↓
LLM and/or VISION
        ↓
Task-specific Skill
```

The same environment, memory-safety, Early Stopping, Checkpoint/Resume, Ablation, reproducibility, and security policies used by other supported coding tools should be applied inside Manus.
