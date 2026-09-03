# Проверка Google Colab

Этот документ описывает запуск и проверку `codingStandard` в Google Colab.

## Открытие в Colab

Используйте ссылку Colab из README репозитория или откройте Notebook напрямую:

`https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/tests/colab/codingstandard_colab_test.ipynb`

Для fork или перемещённой копии откройте Notebook этой копии в Colab и укажите URL репозитория в первой ячейке либо задайте переменную окружения `CODINGSTANDARD_REPO_URL`.

## Выбор репозитория

Notebook не привязан к одному URL репозитория. Используется такой порядок приоритета:

1. переменная окружения `CODINGSTANDARD_REPO_URL`;
2. интерактивный ввод URL репозитория;
3. исходный URL `eaglesjo/codingStandard` по умолчанию.

## Аутентификация публичных и приватных репозиториев

Сначала Notebook пытается выполнить clone без аутентификации.

- **Публичный репозиторий:** clone продолжается сразу, запрос token не появляется.
- **Приватный репозиторий:** после отказа неаутентифицированного clone запрашивается **GitHub Personal Access Token** через безопасный `getpass`.
- Если `GITHUB_TOKEN` сохранён в Google Colab Secrets или в окружении, он используется автоматически.

Token передаётся Git через временный helper `GIT_ASKPASS`. Он не помещается в clone URL, исходный код Notebook, вывод или сохранённый JSON результатов. После теста удалите token из сессии Colab.

## Что проверяется

1. Выбранный репозиторий клонируется в Colab runtime.
2. Определяются Python, PyTorch, CPU, RAM, accelerator, VRAM, возможности CUDA/MPS и информация о runtime.
3. Запускается общий LLM environment profiler.
4. Запускается небольшой LLM training smoke test с сохранением и повторной загрузкой checkpoint.
5. Запускается небольшой Vision training smoke test с image tensor.
6. Выполняется repository validation.
7. Информация о ресурсах и статус pass/fail сохраняются в JSON.
8. Проверяется запуск Notebook в чистом runtime без зависимости от локальной машины разработчика.

Если после неудачного или неполного clone существует `/content/codingStandard`, Notebook удаляет незавершённый каталог и выполняет чистую повторную попытку.

Тесты намеренно небольшие. Успешный Colab smoke test подтверждает стандарт разработки и минимальный путь выполнения, но не гарантирует, что произвольная production model поместится в доступные ресурсы Colab runtime.

## Рекомендуемое использование

Запускайте этот Notebook после изменений environment profiler, memory smoke tests, training configuration или Colab instructions.

## Связанные проверки

- Полная проверка: [Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/tests/colab/codingstandard_colab_test.ipynb)
- Clean runtime: [Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/examples/colab/clean_runtime_validation.ipynb)
- LLM QLoRA: [Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/examples/colab/llm_qlora_validation.ipynb)
- RAG: [Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/examples/colab/rag_validation.ipynb)
