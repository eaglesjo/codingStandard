# LLM Domain Skill

Use with `domains/ml/` for language-model, NLP, RAG, fine-tuning, and text-model workflows.

## Shared lifecycle

Load only the relevant shared ML Skills for data validation, experiment design, evaluation, training, inference, distributed training, hyperparameter optimization, and MLOps.

## LLM task routing

Load task-specific Skills when applicable:

```text
fine-tuning
PEFT
quantization
RAG
ablation
debugging
notebook
release
```

## LLM validation

Before expensive execution, validate the model/tokenizer/configuration path and run a representative load/forward/training smoke test. Keep base-model revision, tokenizer/preprocessing, context length, generation settings, adapter/quantization configuration, and dataset/index revision traceable.

For RAG, preserve corpus, chunking, embedding, index, retrieval, and generation revisions. For fine-tuning, record the training strategy and trainable parameter count.
