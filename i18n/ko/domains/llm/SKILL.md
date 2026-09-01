# LLM Domain Skill

`domains/ml/`과 함께 사용하며 LLM, NLP, RAG, fine-tuning, text-model workflow에 적용합니다.

## 공통 lifecycle

다음 공통 ML Skill 중 필요한 것만 사용합니다.

```text
Data Validation
Experiment Design
Evaluation
Training
Inference
Distributed Training
HPO
MLOps
```

## LLM task routing

필요한 task Skill을 추가합니다.

```text
Fine-Tuning
PEFT
Quantization
RAG
Ablation
Debugging
Notebook
Release
```

비용이 큰 실행 전 model/tokenizer/configuration 경로와 대표 load/forward/training smoke test를 검증합니다. Base model revision, tokenizer/preprocessing, context length, generation settings, adapter/quantization configuration, dataset/index revision을 추적합니다.

## Resource / Memory

VRAM/RAM 사용량과 context length, batch size, precision, KV/cache, gradient checkpointing, quantization/offload를 실제 runtime 기준으로 결정합니다. Memory Smoke Test 통과 후 resolved configuration을 고정합니다.
