# LLM Fine-Tuning Skill

Use for adapting pretrained language models to downstream tasks or domain data.

## Strategy selection

Choose the smallest training method that satisfies the quality requirement under the measured resource budget:

```text
model/task/data requirements
→ available VRAM/RAM
→ full fine-tuning candidate
→ parameter-efficient fine-tuning candidate
→ quantized fine-tuning candidate
→ checkpoint/parallelism requirements
```

## Rules

- Record the base model identifier and immutable revision when available.
- Keep tokenizer and preprocessing versions with the experiment.
- Use a validation set and explicit primary metric.
- Record trainable parameter count and effective batch size.
- Do not silently change quantization, precision, context length, or adapter configuration between compared runs.
- Validate save/load of adapters and merged models before expensive training.
- For constrained runtimes, prefer PEFT/quantization when they satisfy the task rather than assuming a larger accelerator is available.