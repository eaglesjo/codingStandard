# 通用 AI 开发 Skill

此 Skill 用于仓库发现、环境验证、实现、测试、安全与可复现性。

## 工作流

```text
Discover repository
→ Read project instructions
→ Detect runtime
→ Measure available resources
→ Resolve configuration
→ Run smallest meaningful smoke test
→ Lock validated configuration
→ Implement
→ Test
→ Record reproducibility/resource metadata
```

## 规则

- 优先使用已测量的能力，而不是主观假设。
- 除非明确更新，否则保持现有项目约定。
- 明确标记破坏性变更。
- 集中管理配置并确保可复现。
- 绝不暴露密钥。
- 使用分阶段验证，避免重复已知失败的配置。
