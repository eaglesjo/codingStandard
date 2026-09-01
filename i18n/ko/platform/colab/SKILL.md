# Google Colab Skill

Google Colab과 ephemeral hosted notebook runtime에 사용합니다.

```text
active kernel 확인
→ Colab 감지
→ accelerator/RAM/disk 측정
→ active kernel dependency 검증
→ runtime resolve
→ smoke test
→ lock
```

Session reset/interruption을 전제로 checkpoint, model artifact, experiment metadata와 recovery에 필요한 log를 durable storage에 저장합니다.

Long-running run은 충분히 잦은 checkpoint, restore 검증, runtime profile 기록을 사용합니다. 특정 Colab GPU tier를 prerequisite로 가정하지 않습니다.

Notebook은 fresh runtime에서 top-to-bottom 실행 가능해야 하며 중복 설치, hidden state, 무제한 출력과 duplicate environment detection을 줄입니다.