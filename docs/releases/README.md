# Releases

This directory is the home for human-facing documentation about public releases.

## Release model

- `VERSION` is the single source of truth for the current development version in the private source repository.
- Git tags such as `v1.5.0` identify immutable public releases.
- Release notes are generated and published through GitHub Releases.
- Temporary release-staging files do not belong in the public repository.

The public repository is a distribution target, not the private development source of truth.
