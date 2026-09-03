# Google Colab 검증

이 문서는 `codingStandard`의 Google Colab 실행 및 검증 방법을 설명합니다.

## Colab에서 열기

저장소 README의 Colab 링크를 사용하거나 다음 노트북을 직접 엽니다.

`https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/tests/colab/codingstandard_colab_test.ipynb`

Fork 또는 복사본을 사용하는 경우 해당 저장소의 Notebook을 Colab에서 열고, 첫 번째 셀에서 저장소 URL을 입력하거나 `CODINGSTANDARD_REPO_URL` 환경 변수를 설정합니다.

## 저장소 선택

노트북은 특정 저장소 URL에 고정되지 않습니다. 다음 순서로 저장소를 선택합니다.

1. `CODINGSTANDARD_REPO_URL` 환경 변수
2. 대화형 저장소 URL 입력
3. 기본값으로 제공되는 `eaglesjo/codingStandard` URL

입력 프롬프트는 다음 두 줄로 표시됩니다.

```text
GitHub repository, owner/repository, or owner
[https://github.com/your-github-username/codingStandard.git]:
```

## 공개 및 비공개 저장소 인증

노트북은 먼저 인증 없이 clone을 시도합니다.

- **공개 저장소:** 즉시 계속 진행하며 token prompt가 표시되지 않습니다.
- **비공개 저장소:** 인증 없는 clone이 거부된 뒤 안전한 `getpass` 입력을 통해 **GitHub Personal Access Token**을 요청합니다.
- Google Colab Secrets 또는 환경 변수에 `GITHUB_TOKEN`이 있으면 자동으로 사용합니다.

Token은 임시 `GIT_ASKPASS` helper를 통해 Git에 전달됩니다. clone URL, Notebook 소스, 출력 내용 또는 저장된 결과 JSON에는 token을 넣지 않습니다. 테스트가 끝나면 Colab 세션에서 token을 제거합니다.

## 검사 항목

1. 선택한 저장소를 Colab runtime에 clone합니다.
2. Python, PyTorch, CPU, RAM, accelerator, VRAM, CUDA/MPS capability와 runtime 정보를 감지합니다.
3. 공통 LLM environment profiler를 실행합니다.
4. checkpoint 저장/재로드를 포함한 작은 LLM training smoke test를 실행합니다.
5. image tensor를 사용하는 작은 Vision training smoke test를 실행합니다.
6. repository validation을 실행합니다.
7. resource 정보와 pass/fail 상태를 JSON으로 기록합니다.
8. 로컬 개발 머신에 의존하지 않고 clean runtime에서 Notebook을 실행할 수 있는지 확인합니다.

실패했거나 불완전한 clone으로 `/content/codingStandard`가 존재하면 Notebook은 해당 디렉터리를 제거하고 깨끗한 상태로 재시도합니다.

테스트는 의도적으로 작게 구성되어 있습니다. Colab smoke test 통과는 개발 표준과 최소 실행 경로를 검증하지만, 임의의 production model이 현재 Colab runtime의 자원에 적합하다는 것을 보장하지는 않습니다.

## 권장 사용 시점

환경 profiler, memory smoke test, training configuration 또는 Colab 관련 instruction을 변경한 뒤 이 Notebook을 실행합니다.

## 관련 검증

- 종합 검증: [Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/tests/colab/codingstandard_colab_test.ipynb)
- Clean runtime: [Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/examples/colab/clean_runtime_validation.ipynb)
- LLM QLoRA: [Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/examples/colab/llm_qlora_validation.ipynb)
- RAG: [Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/examples/colab/rag_validation.ipynb)
