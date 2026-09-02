# codingStandard Private Development Repository

This repository is the private development source for the public `eaglesjo/codingStandard` distribution repository.

## Repository roles

- `codingStandard-private` — development, testing, release preparation, and internal changes.
- `codingStandard` — public distribution, tags, and GitHub Releases.

Do not develop directly in the public repository unless a release hotfix is required.

## Development flow

```text
main
  ↓
feature work / fixes
  ↓
CI GREEN
  ↓
release/<version>
  ↓
final validation
  ↓
tag v<version>
  ↓
Publish public release workflow
  ↓
public codingStandard main + tag + GitHub Release
```

## Canonical repository structure

Shared resources live under `core/common/`, domain resources live under `domains/`, human-facing documentation lives under `docs/`, and executable tooling lives under `scripts/`. The complete path and compatibility contract is defined in `docs/development/REPOSITORY_STRUCTURE.md`.

Do not recreate legacy top-level domain directories such as `COMMON/`, `LLM/`, `VISION/`, or `MANUS/`. Do not recreate temporary release/version files such as `FINAL_VERSION.txt` or `VERSION-*`.

## Public release credential

The private repository requires one repository secret for publishing to the public repository:

```text
PUBLIC_REPO_TOKEN
```

Use a GitHub fine-grained personal access token scoped only to `eaglesjo/codingStandard` with repository **Contents: Read and write** permission. Do not place this token in source files, workflow YAML, or local configuration committed to Git.

## Release procedure

1. Keep `VERSION` and the shared environment implementation under `core/common/` consistent.
2. Run and pass repository validation, installer tests, Windows PowerShell tests, and LLM/Vision smoke tests.
3. Prepare the release branch `release/<version>` when the candidate is ready.
4. Merge or fast-forward the release commit into private `main` after validation.
5. Trigger the `Publish public release` workflow with the release tag, for example:

```bash
gh workflow run "Publish public release" --repo eaglesjo/codingStandard-private -f tag=v1.5.0
```

6. The workflow validates the tag/version pair, runs repository validation, then publishes the commit and tag to the public repository and creates the GitHub Release.

`VERSION` is the single source of truth for the current development version. Historical release state belongs under `docs/releases/` and Git tags, not in root-level temporary version files.

The workflow does not rewrite or move existing public tags.
