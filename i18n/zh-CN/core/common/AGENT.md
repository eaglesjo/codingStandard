# 通用 AI Agent 规则

这些规则适用于所有受支持的项目领域。

1. 修改代码前，检查实际仓库、运行时、依赖、测试以及安全约束。
2. 在选择依赖资源的设置前，先检测并测量真实运行环境。
3. 不要把特定机器、操作系统、CPU、RAM、GPU、加速器或 IDE 硬编码为项目前提条件。
4. 可复用的领域逻辑应放在模块中，Notebook 和脚本应专注于编排。
5. 使用显式配置、可复现元数据和确定性的路径。
6. 将密钥保存在源代码管理之外。
7. 先用最小且有意义的测试验证变更，再运行更广泛的测试套件。
8. 完成环境验证后，除非明确需要多平台支持，否则删除未使用的执行分支和过时代码。
9. 长时间运行的工作负载应在有意义时使用验证、Early Stopping、最佳 Checkpoint 和 Resume。
10. 实验应定义 baseline、受控 variant、seed、metric 和 resource tracking。

## 标准执行生命周期

```text
Discover → Detect → Measure → Resolve → Smoke Test → Lock → Implement → Validate → Record
```
