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

## Public release credential

The private repository requires one repository secret for publishing to the public repository:

```text
PUBLIC_REPO_TOKEN
```

Use a GitHub fine-grained personal access token scoped only to `eaglesjo/codingStandard` with repository **Contents: Read and write** permission. Do not place this token in source files, workflow YAML, or local configuration committed to Git.

## Release procedure

1. Keep `VERSION` and `COMMON/environment.py` consistent.
2. Run and pass repository validation, installer tests, Windows PowerShell tests, and LLM/Vision smoke tests.
3. Prepare the release branch `release/<version>` when the candidate is ready.
4. Merge or fast-forward the release commit into private `main` after validation.
5. Create and push the private release tag:

```bash
git tag v1.4.1
git push origin v1.4.1
```

6. The `Publish public release` workflow validates the tag/version pair, runs repository validation, then publishes the commit and tag to the public repository and creates the GitHub Release.

The workflow does not rewrite or move existing public tags.
