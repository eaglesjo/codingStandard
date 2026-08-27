# Google Colab Validation

This directory contains a Colab-runnable validation set for the coding standard.

## Open in Colab

Open `codingstandard_colab_test.ipynb` from GitHub in Google Colab, or use the notebook's `Open in Colab` badge/link from the repository README.

## What it checks

1. Clones the current repository into the Colab runtime.
2. Detects Python, PyTorch, CPU, RAM, accelerator, VRAM, CUDA/MPS capability, and runtime information.
3. Runs the shared LLM environment profiler.
4. Runs a small LLM training smoke test with checkpoint save/reload.
5. Runs a small Vision training smoke test with image tensors.
6. Records resource information and pass/fail status as JSON.
7. Verifies that the notebook can run from a clean runtime without relying on a local developer machine.

The tests are intentionally small. A passing Colab smoke test validates the development standard and minimal execution path; it does not prove that an arbitrary production model will fit in the available Colab runtime.

## Expected use

Run this notebook after changes to the environment profiler, memory smoke tests, training configuration, or Colab-related instructions.
