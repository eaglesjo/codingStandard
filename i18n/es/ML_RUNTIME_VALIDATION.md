# Validación del runtime ML/DL

Esta guía valida el contrato de ejecución real después de instalar `codingStandard`.

## Enrutamiento de agentes

Ejecuta desde la raíz del repositorio:

```bash
python scripts/validation/validate_agent_routing.py
```

La prueba cubre cuatro solicitudes representativas:

- entrenamiento PyTorch genérico → common + ciclo de vida ML
- LLM QLoRA → common + ML + fine-tuning/PEFT/cuantización LLM
- detección Vision → common + ML + detección/evaluación Vision
- entrenamiento LLM en Colab → common + ML + LLM + política de checkpoint/reanudación de Colab

La prueba también verifica que ningún dominio no relacionado se incluya accidentalmente en estos escenarios mínimos.

## Runtime de Colab

Abre `examples/colab/clean_runtime_validation.ipynb` en un runtime de Colab nuevo. Ejecuta todas las celdas de principio a fin.

El notebook debe:

1. identificar el kernel de Python activo y el entorno de ejecución;
2. informar de las características del acelerador, RAM y disco cuando estén disponibles;
3. ejecutar la prueba del contrato de enrutamiento de agentes;
4. ejecutar un pequeño smoke test forward/backward de PyTorch cuando PyTorch esté disponible;
5. guardar y restaurar un checkpoint en el directorio persistente seleccionado;
6. generar un informe del runtime legible por máquinas.

Usa una ubicación persistente montada para los checkpoints que deban sobrevivir a un reinicio de Colab. El sistema de archivos de la VM del notebook debe tratarse como desechable.

## Interpretación

Una validación correcta significa que la política instalada puede descubrirse, que el runtime seleccionado puede medirse, que una carga representativa puede iniciarse de forma segura y que los artefactos de recuperación pueden restaurarse. No significa que se hayan probado todos los tipos de aceleradores de Colab ni todos los tamaños de modelo.
