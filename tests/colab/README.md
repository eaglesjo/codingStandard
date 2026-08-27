# Google Colab Validation

This directory contains a Colab-runnable validation set for the coding standard.

## Open in Colab

Use the direct Colab URL from the repository README, or open the notebook manually:

`https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/tests/colab/codingstandard_colab_test.ipynb`

For a fork or moved copy, open that copy's notebook in Colab and enter the fork URL when prompted, or set `CODINGSTANDARD_REPO_URL` before running the first cell.

## Repository selection

The notebook does not require the repository URL to stay fixed. It uses this precedence:

1. `CODINGSTANDARD_REPO_URL` environment variable.
2. Interactive repository URL prompt.
3. The original `eaglesjo/codingStandard` URL as the default value.

The repository prompt is displayed as two lines:

```text
GitHub repository, owner/repository, or owner
[https://github.com/your-github-username/codingStandard.git]:
```

## Public and private repository authentication

The notebook first attempts an unauthenticated clone.

- **Public repository:** clone continues immediately; no token prompt is shown.
- **Private repository:** after the unauthenticated clone is rejected, the notebook requests a **GitHub Personal Access Token** through a secure `getpass` prompt.
- A `GITHUB_TOKEN` stored in Google Colab Secrets or the environment is used automatically when available.

The token is passed to Git through a temporary `GIT_ASKPASS` helper. It is not placed in the clone URL, notebook source, printed output, or saved result JSON. Remove the token from the Colab session after testing.

## What it checks

1. Clones the selected repository into the Colab runtime.
2. Detects Python, PyTorch, CPU, RAM, accelerator, VRAM, CUDA/MPS capability, and runtime information.
3. Runs the shared LLM environment profiler.
4. Runs a small LLM training smoke test with checkpoint save/reload.
5. Runs a small Vision training smoke test with image tensors.
6. Runs repository validation.
7. Records resource information and pass/fail status as JSON.
8. Verifies that the notebook can run from a clean runtime without relying on a local developer machine.

If `/content/codingStandard` exists from a failed or partial clone, the notebook removes the incomplete directory and retries cleanly.

The tests are intentionally small. A passing Colab smoke test validates the development standard and minimal execution path; it does not prove that an arbitrary production model will fit in the available Colab runtime.

## Expected use

Run this notebook after changes to the environment profiler, memory smoke tests, training configuration, or Colab-related instructions.
