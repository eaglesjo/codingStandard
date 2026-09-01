#!/usr/bin/env python3
"""End-to-end ML integration smoke for the codingStandard ML/Vision stack.

The test creates a disposable project, installs the ML and Vision domains, then
runs a deterministic synthetic image-classification workload with validation,
metrics, checkpointing, resume, and final evaluation.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INSTALLER = ROOT / "scripts" / "installers" / "install-domains.sh"

PROJECT_FILES = {
    "train.py": '''
from __future__ import annotations

import json
import random
from pathlib import Path

import torch
from torch import nn

SEED = 1337
random.seed(SEED)
torch.manual_seed(SEED)

CHECKPOINT = Path("artifacts/checkpoint.pt")
METRICS = Path("artifacts/metrics.json")
CHECKPOINT.parent.mkdir(parents=True, exist_ok=True)

# Synthetic 2-class 16x16 images: class 0 has a bright left bar,
# class 1 has a bright right bar. No external dataset is required.
def make_dataset(samples_per_class: int = 64):
    generator = torch.Generator().manual_seed(SEED)
    total = samples_per_class * 2
    x = torch.randn(total, 1, 16, 16, generator=generator) * 0.08
    y = torch.zeros(total, dtype=torch.long)
    y[samples_per_class:] = 1
    x[:samples_per_class, :, :, 2:6] += 1.0
    x[samples_per_class:, :, :, 10:14] += 1.0
    return x, y

x, y = make_dataset()
# Stratified split: 48 train + 16 validation samples per class.
train_idx = torch.cat((torch.arange(0, 48), torch.arange(64, 112)))
val_idx = torch.cat((torch.arange(48, 64), torch.arange(112, 128)))
train_x, val_x = x[train_idx], x[val_idx]
train_y, val_y = y[train_idx], y[val_idx]

model = nn.Sequential(
    nn.Conv2d(1, 8, kernel_size=3, padding=1),
    nn.ReLU(),
    nn.AdaptiveAvgPool2d((4, 4)),
    nn.Flatten(),
    nn.Linear(8 * 4 * 4, 2),
)
optimizer = torch.optim.Adam(model.parameters(), lr=1e-2)
loss_fn = nn.CrossEntropyLoss()

best_val = 0.0
history = []
start_epoch = 0

if CHECKPOINT.exists():
    state = torch.load(CHECKPOINT, map_location="cpu", weights_only=False)
    model.load_state_dict(state["model"])
    optimizer.load_state_dict(state["optimizer"])
    start_epoch = state["epoch"] + 1
    best_val = state["best_val"]

for epoch in range(start_epoch, 4):
    model.train()
    optimizer.zero_grad(set_to_none=True)
    logits = model(train_x)
    loss = loss_fn(logits, train_y)
    loss.backward()
    optimizer.step()

    model.eval()
    with torch.no_grad():
        val_pred = model(val_x).argmax(dim=1)
        val_acc = (val_pred == val_y).float().mean().item()
    best_val = max(best_val, val_acc)
    history.append({"epoch": epoch, "loss": float(loss.item()), "val_accuracy": val_acc})
    torch.save(
        {
            "epoch": epoch,
            "model": model.state_dict(),
            "optimizer": optimizer.state_dict(),
            "best_val": best_val,
            "seed": SEED,
        },
        CHECKPOINT,
    )

METRICS.write_text(
    json.dumps(
        {"seed": SEED, "best_val_accuracy": best_val, "history": history},
        indent=2,
    ) + "\\n",
    encoding="utf-8",
)

# Explicit restore validation: reload into a fresh model and reproduce metrics.
restored = nn.Sequential(
    nn.Conv2d(1, 8, kernel_size=3, padding=1),
    nn.ReLU(),
    nn.AdaptiveAvgPool2d((4, 4)),
    nn.Flatten(),
    nn.Linear(8 * 4 * 4, 2),
)
state = torch.load(CHECKPOINT, map_location="cpu", weights_only=False)
restored.load_state_dict(state["model"])
restored.eval()
with torch.no_grad():
    restored_acc = (restored(val_x).argmax(dim=1) == val_y).float().mean().item()

assert best_val >= 0.95, f"validation accuracy too low: {best_val}"
assert abs(restored_acc - state["best_val"]) < 1e-6
assert METRICS.exists() and CHECKPOINT.exists()

print(json.dumps({
    "status": "passed",
    "seed": SEED,
    "best_val_accuracy": best_val,
    "restored_accuracy": restored_acc,
    "checkpoint": str(CHECKPOINT),
}, indent=2))
''',
}


def run(cmd: list[str], cwd: Path, *, check: bool = True) -> subprocess.CompletedProcess[str]:
    return subprocess.run(cmd, cwd=cwd, check=check, text=True, capture_output=True)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="codingstandard-ml-verify-") as tmp:
        project = Path(tmp) / "ml-project"
        run(["bash", str(INSTALLER), str(project), "en", "ml", "overwrite", "false"], ROOT)
        run(["bash", str(INSTALLER), str(project), "en", "vision", "overwrite", "false"], ROOT)

        for required in (
            "AGENTS.md",
            "core/common/environment.py",
            "domains/ml/AGENT.md",
            "domains/ml/skills/data/SKILL.md",
            "domains/ml/skills/training/SKILL.md",
            "domains/ml/skills/evaluation/SKILL.md",
            "domains/vision/AGENT.md",
        ):
            assert (project / required).is_file(), f"missing installed resource: {required}"

        for rel, content in PROJECT_FILES.items():
            path = project / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content.strip() + "\n", encoding="utf-8")

        result = run([sys.executable, str(project / "train.py")], project, check=False)
        if result.stdout:
            print(result.stdout, end="")
        if result.stderr:
            print(result.stderr, file=sys.stderr, end="")
        if result.returncode != 0:
            raise RuntimeError(f"synthetic training failed with exit code {result.returncode}")
        print("end-to-end ML classification integration passed")
        return 0


if __name__ == "__main__":
    raise SystemExit(main())
