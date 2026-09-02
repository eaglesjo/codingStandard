# ML/DL Runtime Validation

This guide validates the real execution contract after codingStandard installation.

## Agent routing

Run from the repository root:

```bash
python scripts/validation/validate_agent_routing.py
```

The test covers four representative requests:

- generic PyTorch training → common + ML lifecycle
- LLM QLoRA → common + ML + LLM fine-tuning/PEFT/quantization
- Vision detection → common + ML + Vision detection/evaluation
- Colab LLM training → common + ML + LLM + Colab checkpoint/resume policy

The test also checks that unrelated domain-specific routing is not accidentally pulled into these minimal scenarios.

## Colab runtime

Open `examples/colab/clean_runtime_validation.ipynb` in a fresh Colab runtime. Run every cell from top to bottom.

The notebook must:

1. identify the active Python kernel and execution environment;
2. report accelerator, RAM, and disk characteristics when available;
3. run the agent-routing contract test;
4. execute a tiny PyTorch forward/backward smoke test when PyTorch is available;
5. write and restore a checkpoint in the selected durable directory;
6. emit a machine-readable runtime report.

Use a mounted durable location for checkpoints when the artifacts must survive a Colab reset. The notebook VM filesystem must be treated as disposable.

## Interpretation

A successful validation means the installed policy can be discovered, the selected runtime is measurable, a representative workload can start safely, and recovery artifacts can be restored. It does not imply that every Colab accelerator type or every model size has been tested.
