# Releases

This directory is the human-readable history and planning area for releases.

## Rules

- `VERSION` at the repository root contains only the current development version.
- Git tags such as `v1.5.0` are the immutable release identifiers.
- Release-specific notes belong here, using one Markdown file per release when notes are needed (for example `1.5.0.md`).
- Temporary release staging files do not belong in the repository.
- `FINAL_VERSION.txt`, `VERSION.next`, `VERSION.tmp`, and version-specific staging files are obsolete and must not be recreated.

## Release boundary

The private repository is the development source. The public repository is the distribution target. The `Publish public release` workflow is responsible for exporting the validated source, creating/updating the public tag, and creating the GitHub Release.
