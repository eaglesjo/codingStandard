from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

SCENARIOS = {
    "generic-pytorch-training": {
        "files": ["core/common/AGENT.md", "core/common/SKILL.md", "core/common/ENVIRONMENT.md", "domains/ml/AGENT.md", "domains/ml/SKILL.md", "domains/ml/ENVIRONMENT.md"],
        "required": ["data contract", "training", "evaluation", "experiment", "memory smoke"],
    },
    "llm-qlora": {
        "files": ["core/common/AGENT.md", "core/common/SKILL.md", "core/common/ENVIRONMENT.md", "domains/ml/AGENT.md", "domains/ml/SKILL.md", "domains/llm/AGENT.md", "domains/llm/SKILL.md", "domains/llm/ENVIRONMENT.md", "domains/llm/skills/finetuning/SKILL.md", "domains/llm/skills/peft/SKILL.md", "domains/llm/skills/quantization/SKILL.md"],
        "required": ["fine-tuning", "lora", "parameter-efficient", "quantized llm", "memory"],
    },
    "vision-detection": {
        "files": ["core/common/AGENT.md", "core/common/SKILL.md", "core/common/ENVIRONMENT.md", "domains/ml/AGENT.md", "domains/ml/SKILL.md", "domains/vision/AGENT.md", "domains/vision/SKILL.md", "domains/vision/ENVIRONMENT.md", "domains/vision/skills/detection/SKILL.md"],
        "required": ["object detection", "bounding-box", "map", "iou", "checkpoint", "resume"],
    },
    "colab-llm-training": {
        "files": ["core/common/AGENT.md", "core/common/SKILL.md", "core/common/ENVIRONMENT.md", "domains/ml/AGENT.md", "domains/ml/SKILL.md", "domains/llm/AGENT.md", "domains/llm/SKILL.md", "domains/llm/ENVIRONMENT.md", "domains/llm/skills/finetuning/SKILL.md", "platform/colab/AGENT.md", "platform/colab/SKILL.md"],
        "required": ["google colab", "ephemeral", "checkpoint", "resume", "fine-tuning"],
    },
}

for name, case in SCENARIOS.items():
    corpus = "\n".join((ROOT / path).read_text(encoding="utf-8").lower() for path in case["files"])
    missing = [term for term in case["required"] if term.lower() not in corpus]
    if missing:
        raise SystemExit(f"{name}: missing={missing}")
    print(f"routing scenario passed: {name}")

print("agent routing validation passed")
