# Project Profiles

`profiles/project.json` is the repository-level entry point for architecture, policy, runtime, delivery, and scalability contracts.

## Resolution

1. Load `profiles/project.json`.
2. Resolve `architecture_profile` from `profiles/architecture/<id>.json`.
3. Resolve `policy_profile` from `profiles/policies/<id>.json`.
4. Validate all referenced contracts before implementation or release.

The current project type is `developer-standard`. The supported runtime contract explicitly covers Linux, macOS, and Windows, with Ubuntu 24.04 as the CI reference environment.

The profile is declarative: it constrains engineering behavior without prescribing a single language or framework.
