# ML / Deep Learning Domain

`domains/ml/` owns cross-domain machine-learning lifecycle policy. It complements, rather than duplicates, the LLM and Vision domains.

## Use this domain for

- classical ML and tabular ML;
- time-series and structured-data workflows;
- generic PyTorch/TensorFlow/JAX training;
- experiment design and evaluation;
- inference and model lifecycle work;
- distributed training and resource-aware optimization.

## Skills

```text
data/                    dataset validation and leakage checks
experiment/               hypothesis, baseline, controlled comparisons
evaluation/               metrics, regression gates, error analysis
training/                 generic training contract
distributed-training/     multi-GPU/multi-node execution
hyperparameter-optimization/
                          systematic tuning under a fixed budget
inference/                reproducible prediction and latency/memory checks
mlops/                    model/artifact lineage and promotion
```

Load only the Skills relevant to the task. LLM and Vision domains inherit this lifecycle policy and add their task-specific rules.
