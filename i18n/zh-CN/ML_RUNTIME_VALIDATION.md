# ML/DL 运行时验证

本指南用于验证安装 `codingStandard` 后的实际执行契约。

## Agent 路由

在仓库根目录运行：

```bash
python scripts/validation/validate_agent_routing.py
```

测试覆盖四个代表性请求：

- 通用 PyTorch 训练 → common + ML 生命周期
- LLM QLoRA → common + ML + LLM 微调/PEFT/量化
- Vision 检测 → common + ML + Vision 检测/评估
- Colab LLM 训练 → common + ML + LLM + Colab checkpoint/恢复策略

测试还会检查这些最小场景不会意外加载无关的领域路由。

## Colab 运行时

在全新的 Colab runtime 中打开 `examples/colab/clean_runtime_validation.ipynb`，从上到下运行所有单元格。

Notebook 必须：

1. 识别当前 Python kernel 和执行环境；
2. 在可用时报告 accelerator、RAM 和 disk 特征；
3. 运行 agent-routing 契约测试；
4. 在可用 PyTorch 时执行小型 forward/backward smoke test；
5. 在选定的持久化目录中写入并恢复 checkpoint；
6. 生成机器可读的 runtime report。

需要在 Colab 重置后保留 checkpoint 时，应使用已挂载的持久化位置。Notebook VM 文件系统必须视为临时资源。

## 结果解释

验证成功表示已安装策略可以被发现、所选 runtime 可以被测量、代表性 workload 可以安全启动，并且恢复 artifact 可以还原。它不表示所有 Colab accelerator 类型或所有模型规模都已经测试。
