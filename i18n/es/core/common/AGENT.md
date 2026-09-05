# Reglas comunes para agentes de IA

Estas reglas se aplican a todos los dominios compatibles.

1. Inspecciona el repositorio, el entorno de ejecución, las dependencias, las pruebas y los requisitos de seguridad antes de modificar código.
2. Detecta y mide el entorno real antes de elegir configuraciones sensibles a los recursos.
3. No supongas como requisito una máquina, sistema operativo, CPU, RAM, GPU, acelerador o IDE concreto.
4. Mantén la lógica de dominio reutilizable en módulos y limita notebooks/scripts a la orquestación.
5. Usa configuración explícita, metadatos de reproducibilidad y rutas deterministas.
6. Mantén los secretos fuera del control de versiones.
7. Valida primero con la prueba significativa más pequeña y después ejecuta la suite más amplia.
8. Tras validar el entorno, elimina rutas de ejecución sin uso y código obsoleto salvo que el soporte multiplataforma sea intencional.
9. Las cargas largas deberían usar validación, Early Stopping, el mejor Checkpoint y Resume cuando corresponda.
10. Los experimentos deben definir baseline, variantes controladas, seeds, métricas y seguimiento de recursos.

## Ciclo estándar

```text
Explorar → Detectar → Medir → Resolver → Smoke Test → Fijar → Implementar → Validar → Documentar
```
