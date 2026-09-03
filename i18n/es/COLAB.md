# Validación de Google Colab

Este documento describe cómo ejecutar y validar `codingStandard` en Google Colab.

## Abrir en Colab

Usa el enlace de Colab del README del repositorio o abre directamente el siguiente notebook:

`https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/tests/colab/codingstandard_colab_test.ipynb`

Para un fork o una copia movida, abre el notebook de esa copia en Colab e introduce la URL del repositorio en la primera celda o define la variable de entorno `CODINGSTANDARD_REPO_URL`.

## Selección del repositorio

El notebook no está fijado a una única URL. Se utiliza esta prioridad:

1. Variable de entorno `CODINGSTANDARD_REPO_URL`.
2. Solicitud interactiva de la URL del repositorio.
3. La URL original `eaglesjo/codingStandard` como valor predeterminado.

## Autenticación de repositorios públicos y privados

El notebook intenta primero un clone sin autenticación.

- **Repositorio público:** el clone continúa inmediatamente y no se muestra ninguna solicitud de token.
- **Repositorio privado:** después de rechazar el clone sin autenticación, se solicita un **GitHub Personal Access Token** mediante `getpass`.
- Un `GITHUB_TOKEN` almacenado en Google Colab Secrets o en el entorno se utiliza automáticamente cuando está disponible.

El token se pasa a Git mediante un helper temporal `GIT_ASKPASS`. No se coloca en la URL de clone, en el código del notebook, en la salida impresa ni en el JSON de resultados guardado. Elimina el token de la sesión de Colab después de la prueba.

## Qué comprueba

1. Clona el repositorio seleccionado en el runtime de Colab.
2. Detecta Python, PyTorch, CPU, RAM, acelerador, VRAM, capacidades CUDA/MPS e información del runtime.
3. Ejecuta el profiler de entorno LLM compartido.
4. Ejecuta un pequeño smoke test de entrenamiento LLM con guardado y recarga de checkpoint.
5. Ejecuta un pequeño smoke test de entrenamiento Vision con tensores de imagen.
6. Ejecuta la validación del repositorio.
7. Registra información de recursos y estado de éxito/fallo en JSON.
8. Verifica que el notebook funcione desde un runtime limpio sin depender de una máquina de desarrollo local.

Si `/content/codingStandard` existe por un clone fallido o parcial, el notebook elimina el directorio incompleto y vuelve a intentarlo desde cero.

Las pruebas son intencionadamente pequeñas. Un smoke test de Colab correcto valida el estándar de desarrollo y la ruta mínima de ejecución; no garantiza que cualquier modelo de producción quepa en los recursos disponibles del runtime de Colab.

## Uso recomendado

Ejecuta este notebook después de cambios en el profiler de entorno, los memory smoke tests, la configuración de entrenamiento o las instrucciones relacionadas con Colab.

## Validaciones relacionadas

- Validación completa: [Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/tests/colab/codingstandard_colab_test.ipynb)
- Clean runtime: [Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/examples/colab/clean_runtime_validation.ipynb)
- LLM QLoRA: [Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/examples/colab/llm_qlora_validation.ipynb)
- RAG: [Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/examples/colab/rag_validation.ipynb)
