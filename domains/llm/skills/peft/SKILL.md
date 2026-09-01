# PEFT Skill

Use for LoRA, adapters, and other parameter-efficient fine-tuning methods.

## Before training

Record:

```text
base model revision
adapter method
target modules
rank / alpha / dropout when applicable
trainable parameter count
precision / quantization
learning rate
sequence length
effective batch size
seed
```

## Rules

- Keep adapter configuration versioned separately from application code.
- Validate that only intended parameters are trainable.
- Compare against a clearly defined baseline.
- Save adapter-only artifacts when they are the intended deliverable and test loading them onto the declared base-model revision.
- When merging adapters into a base model, validate the merged artifact and preserve the original adapter artifact.