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

This allows the same notebook to validate the original repository, a fork, or a relocated copy.

## Private repository authentication

The repository may be private. The notebook supports both public and private repositories.

For a private repository, create a GitHub token with read access to that repository and either:

1. store it in Google Colab Secrets as `GITHUB_TOKEN`, or
2. let the notebook prompt for it securely with `getpass`.

The token is passed to Git through a temporary `GIT_ASKPASS` helper. It is not placed in the clone URL, notebook source, printed output, or saved result JSON. Remove the token from the Colab session after testing.

If the repository is public, leave the token prompt blank.

## What it checks

1. Clones the selected repository into the Colab runtime.
2. Detects Python, PyTorch, CPU, RAM, accelerator, VRAM, CUDA/MPS capability, and runtime information.
3. Runs the shared LLM environment profiler.
4. Runs a small LLM training smoke test with checkpoint save/reload.
5. Runs a small Vision training smoke test with image tensors.
6. Records resource information and pass/fail status as JSON.
7. Verifies that the notebook can run from a clean runtime without relying on a local developer machine.

If `/content/codingStandard` exists from a failed or partial clone and is not a valid Git working tree, the notebook removes the incomplete directory and retries cleanly.

The tests are intentionally small. A passing Colab smoke test validates the development standard and minimal execution path; it does not prove that an arbitrary production model will fit in the available Colab runtime.

## Expected use

Run this notebook after changes to the environment profiler, memory smoke tests, training configuration, or Colab-related instructions.
