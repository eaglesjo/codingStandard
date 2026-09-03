# Google Colab 验证

本文档介绍如何在 Google Colab 中运行和验证 `codingStandard`。

## 在 Colab 中打开

使用仓库 README 中的 Colab 链接，或直接打开以下 Notebook：

`https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/tests/colab/codingstandard_colab_test.ipynb`

如果使用 fork 或移动后的副本，请在 Colab 中打开该副本的 Notebook，并在第一个单元格中输入仓库 URL，或设置环境变量 `CODINGSTANDARD_REPO_URL`。

## 仓库选择

Notebook 不要求固定的仓库 URL，优先级如下：

1. `CODINGSTANDARD_REPO_URL` 环境变量；
2. 交互式仓库 URL 输入；
3. 原始 `eaglesjo/codingStandard` URL 作为默认值。

## 公有和私有仓库认证

Notebook 首先尝试不进行身份验证的 clone。

- **公有仓库：** clone 会立即继续，不会显示 token 提示。
- **私有仓库：** 未认证 clone 被拒绝后，通过安全的 `getpass` 提示请求 **GitHub Personal Access Token**。
- 如果 Google Colab Secrets 或环境中存在 `GITHUB_TOKEN`，则会自动使用。

Token 通过临时的 `GIT_ASKPASS` helper 传递给 Git。它不会写入 clone URL、Notebook 源码、打印输出或保存的结果 JSON。测试完成后请从 Colab 会话中移除 token。

## 检查内容

1. 将选定的仓库 clone 到 Colab runtime。
2. 检测 Python、PyTorch、CPU、RAM、accelerator、VRAM、CUDA/MPS capability 和 runtime 信息。
3. 运行共享的 LLM environment profiler。
4. 运行包含 checkpoint 保存/重新加载的小型 LLM training smoke test。
5. 使用图像张量运行小型 Vision training smoke test。
6. 运行 repository validation。
7. 将资源信息和通过/失败状态记录为 JSON。
8. 验证 Notebook 可以在干净 runtime 中运行，而不依赖本地开发机器。

如果 `/content/codingStandard` 因 clone 失败或不完整而存在，Notebook 会删除不完整目录并重新进行干净尝试。

测试规模是有意控制的。Colab smoke test 通过表示开发标准和最小执行路径有效，但不能证明任意生产模型都能适配当前 Colab runtime 的可用资源。

## 推荐使用时机

在修改环境 profiler、memory smoke tests、training configuration 或 Colab 相关 instructions 后运行此 Notebook。

## 相关验证

- 完整验证：[Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/tests/colab/codingstandard_colab_test.ipynb)
- Clean runtime：[Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/examples/colab/clean_runtime_validation.ipynb)
- LLM QLoRA：[Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/examples/colab/llm_qlora_validation.ipynb)
- RAG：[Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/examples/colab/rag_validation.ipynb)
