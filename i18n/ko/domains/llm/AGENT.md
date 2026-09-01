# LLM Domain Agent 규칙

`domains/ml/` 위에 적용하는 LLM/NLP/RAG/fine-tuning 전용 규칙입니다.

## LLM 고유 규칙

1. base model identifier/revision과 tokenizer revision을 기록합니다.
2. prompt/template, preprocessing, context length, generation configuration을 명시하고 versioned 상태로 유지합니다.
3. Fine-Tuning은 측정된 resource와 task 요구사항을 기준으로 full fine-tuning 또는 parameter-efficient 방법을 선택합니다.
4. PEFT를 사용하면 adapter method, target modules, trainable parameter count와 adapter configuration을 기록합니다.
5. Quantization을 사용하면 bit width, backend, compute dtype와 관련 configuration revision을 기록합니다.
6. RAG에서는 corpus/document revision, chunking, embedding model, index, retrieval, reranking, generation model revision을 추적합니다.
7. retrieval과 generation 오류를 구분하여 평가/분석합니다.
8. model/tokenizer/adapter 저장 및 로딩을 비용 큰 학습 전에 검증합니다.

## 공통 정책

Data Validation, Experiment Design, Evaluation, Training, Inference, Distributed Training, HPO, MLOps, Environment, Smoke Test, Checkpoint/Resume, Reproducibility는 `domains/ml/` 공통 정책과 Skill을 사용합니다.

Colab 또는 다른 ephemeral hosted notebook이면 `platform/colab/` 정책도 적용합니다.