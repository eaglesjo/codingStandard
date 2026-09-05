# Architecture Profiles

Architecture profiles are declarative contracts describing how this repository may evolve. They are consumed by validation tooling and AI coding agents before implementation changes.

## Active profile

`profiles/project.json` selects `repository-standard`.

The profile separates the repository into five layers:

- `interface`: CLI, installer, documentation, and integration adapters.
- `policy`: repository-wide coding and delivery rules.
- `validation`: static checks, tests, and environment validation.
- `domain`: standards, contracts, and reusable engineering rules.
- `infrastructure`: CI runners, platform adapters, and external tooling.

`path_roots` binds these architectural layers to repository paths. The profile validator parses Python imports from those paths and resolves local modules, including namespace-package directories. Forbidden edges therefore become executable CI checks rather than documentation-only rules.

Dependencies must follow the declared direction in `profiles/architecture/repository-standard.json`. Forbidden edges are explicit architectural boundaries.

## AI implementation rule

An AI agent should inspect the active project and architecture profiles before adding modules, dependencies, or integrations. A conflicting change requires an explicit profile change rather than silently weakening the contract.
