# LLM Domain Agent Rules

Apply on top of `domains/ml/` for language-model, NLP, RAG, and LLM-specific work.

## LLM-specific rules

1. Record the base model identifier/revision and tokenizer revision when applicable.
2. Keep prompt/template, preprocessing, context length, and generation configuration explicit and versioned.
3. For fine-tuning, select full fine-tuning or parameter-efficient methods based on measured resources and task requirements.
4. For PEFT, record adapter method, target modules, trainable parameter count, and adapter configuration.
5. For quantized execution/fine-tuning, record bit width, backend, compute dtype, and calibration/configuration revision.
6. For RAG, keep corpus/document revision, chunking, embedding model revision, index revision, retrieval configuration, and generation model revision traceable.
7. Evaluate task quality using an explicit benchmark/evaluation protocol and keep retrieval and generation errors distinguishable where applicable.
8. Validate model/tokenizer/adapter save-load behavior before expensive training or deployment.

## Shared policy

Use the shared ML lifecycle for data validation, experiment design, evaluation, training, inference, distributed execution, HPO, MLOps, environment measurement, smoke tests, checkpoint/resume, and reproducibility.

For notebooks and Colab, also apply the relevant notebook and `platform/colab/` policies.
