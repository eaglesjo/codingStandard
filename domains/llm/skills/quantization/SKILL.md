# Quantization Skill

Use for 8-bit, 4-bit, weight-only, activation-aware, or other quantized LLM execution/fine-tuning.

## Strategy

Select quantization based on measured memory pressure, supported hardware/frameworks, target quality, and inference/training requirements.

## Rules

- Record quantization scheme, bit width, backend, compute dtype, and calibration/configuration revision.
- Do not assume a quantization backend is available on every accelerator or operating system.
- Validate model loading and a representative forward pass before long execution.
- For fine-tuning, verify the interaction between quantization and adapters/gradient computation.
- Compare quality against the unquantized or declared baseline using the same evaluation protocol.
- Record memory and latency changes as well as quality changes.
