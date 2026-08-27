# Ablation Study Skill

Use for controlled component and configuration experiments.

Define a baseline and explicit variants in `LLM/config/ablation.yaml` or an equivalent configuration file.

Keep train/validation split, test set, metric definition, Early Stopping policy, maximum budget, checkpoint policy, and evaluation procedure consistent across variants whenever possible.

Repeat important variants across a declared seed set. Record experiment ID, changed parameters, seed, Git commit, model/dataset revision, best metric, early-stopped state, peak VRAM/RAM, runtime, checkpoint path, and resolved environment profile.

Do not change multiple unexplained factors in a single ablation unless the study is explicitly factorial or designed for interactions.
