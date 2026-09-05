# Policy Inheritance

Policies form a deterministic hierarchy:

`repository -> project -> domain -> component -> task`

A child scope may add restrictions, but it may not weaken a parent rule. When rules conflict, the stricter rule wins. Ambiguous conflicts must fail validation rather than being resolved implicitly.

The repository baseline is `profiles/policies/repository-default.json`.

## Baseline principles

- Validation is required.
- Behavior changes require tests.
- Platform-specific paths must be abstracted.
- Secrets must not be committed.
- Network access must be explicit.
- Reproducibility is required.

Policy evaluation should remain deterministic and must not require network access.
