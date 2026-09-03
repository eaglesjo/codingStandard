# Проверка ML/DL runtime

Это руководство проверяет реальный контракт выполнения после установки `codingStandard`.

## Маршрутизация Agent

Запустите из корня репозитория:

```bash
python scripts/validation/validate_agent_routing.py
```

Тест охватывает четыре типичных запроса:

- обычное обучение PyTorch → common + жизненный цикл ML
- LLM QLoRA → common + ML + fine-tuning/PEFT/quantization LLM
- Vision detection → common + ML + detection/evaluation Vision
- Colab LLM training → common + ML + LLM + политика checkpoint/resume для Colab

Тест также проверяет, что в этих минимальных сценариях случайно не подключаются нерелевантные домены.

## Colab runtime

Откройте `examples/colab/clean_runtime_validation.ipynb` в новом Colab runtime. Выполните все ячейки сверху вниз.

Notebook должен:

1. определить активный Python kernel и среду выполнения;
2. сообщить характеристики accelerator, RAM и disk, если они доступны;
3. выполнить проверку контракта agent-routing;
4. выполнить небольшой PyTorch forward/backward smoke test, если PyTorch доступен;
5. сохранить и восстановить checkpoint в выбранном постоянном каталоге;
6. сформировать машиночитаемый runtime report.

Для checkpoint, которые должны пережить сброс Colab, используйте подключённое постоянное хранилище. Файловую систему Notebook VM следует считать временной.

## Интерпретация

Успешная проверка означает, что установленную политику можно обнаружить, выбранный runtime можно измерить, типичную нагрузку можно безопасно запустить, а артефакты восстановления можно восстановить. Это не означает, что протестированы все типы Colab accelerator или все размеры моделей.
