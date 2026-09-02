# Общий Environment Contract

Все домены используют реальную среду выполнения как источник истины.

```text
Detect → Measure → Resolve → Smoke Test → Lock → Optimize
```

Измеряйте доступные CPU, системную RAM, диск, accelerator/GPU, память accelerator, возможности framework, Python/runtime и, когда доступно, состояние IDE/kernel.

## Политика Linux и Ubuntu

**Linux — поддерживаемое семейство ОС; Ubuntu — reference distribution.**

Это различие намеренно:

- runtime contract должен оставаться переносимым между дистрибутивами Linux.
- Ubuntu LTS является основной development и CI baseline благодаря широкому распространению, предсказуемости и доступности как GitHub-hosted runner.
- CI зафиксирован на **Ubuntu 24.04 LTS**, а не на `ubuntu-latest`, чтобы миграция runner image не меняла validation baseline незаметно.
- Специфичные для Ubuntu package или filesystem предположения не должны попадать в общий Python environment contract, если они явно не являются частью installer/CI implementation.
- Другие Linux distribution, предоставляющие необходимый Python и framework capability, остаются поддерживаемыми на уровне Python/runtime contract. Отдельно добавлять их в стандартную CI matrix не требуется.

```text
Supported platform family: Linux
Reference implementation:  Ubuntu 24.04 LTS
CI baseline:              ubuntu-24.04
```

## Классификация OS и runtime

Отделяйте operating system от execution environment. Поле `os` описывает machine/runtime, фактически исполняющий Python, а не клиентское устройство пользователя.

Поддерживаемые OS families определяются по информации Python runtime, а не по hard-coded machine profiles:

- **Linux**: обычные локальные Linux host и cloud runtime, такие как Google Colab. Ubuntu 24.04 LTS — CI reference distribution.
- **macOS**: Apple Silicon и Intel Mac; используется Apple MPS, если framework его предоставляет и он доступен, иначе CPU fallback.
- **Windows**: локальные Windows host; DirectML используется при доступности, иначе применяется CUDA/CPU resolution.

Google Colab session является Linux-based cloud runtime даже при подключении пользователя с macOS или Windows. Нельзя классифицировать Colab как local macOS или Windows по ОС браузера/клиента.

Профиль сообщает:

- `os`: ОС host/runtime, сообщённая Python
- `architecture`: CPU architecture runtime, например `x86_64` или `arm64`
- `execution_environment`: `local`, `jupyter`, `vscode` или `colab`
- `execution_type`: `local` или `cloud`
- `device`: resolved execution device (`cpu`, `cuda`, `mps`, `directml`)

Это позволяет одному и тому же domain code работать в Linux, macOS, Windows, Jupyter, VS Code и Colab без превращения named hardware profile в runtime requirement.

## Platform-specific accelerator policy

Предпочитайте измеренные возможности framework предположениям об ОС:

1. CUDA, если `torch.cuda.is_available()` равно true.
2. Apple MPS, если framework предоставляет доступный MPS backend.
3. DirectML, если `torch_directml` установлен и доступен runtime.
4. CPU как универсальный fallback.

В Linux ROCm следует показывать отдельно от CUDA, даже если PyTorch предоставляет его через CUDA API surface. В macOS Apple MPS показывается отдельно, а CPU fallback обязателен. В Windows наличие DirectML нельзя предполагать.

Runtime recommendations должны быть консервативными. Оставляйте headroom для OS, IDE/runtime, framework allocations и background processes. Не стремитесь к 100% utilization.

## Validation contract

Repository CI проверяет **Ubuntu 24.04 LTS как Linux reference baseline** и напрямую проверяет macOS. Windows покрывается Windows installer workflow. Runtime classification tests имитируют Linux, macOS, Windows, Jupyter, VS Code и Colab, поэтому platform-specific logic можно проверять без наличия каждого accelerator на каждом CI runner.

CI baseline намеренно уже support contract: напрямую проверяется один стабильный Linux distribution, а общий код остаётся distribution-agnostic. Явная Ubuntu LTS runner label делает baseline воспроизводимым.
