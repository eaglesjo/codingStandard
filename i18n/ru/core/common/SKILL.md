# Общий AI Development Skill

Этот Skill используется для исследования репозитория, проверки среды, реализации, тестирования, безопасности и воспроизводимости.

## Рабочий процесс

```text
Discover repository
→ Read project instructions
→ Detect runtime
→ Measure available resources
→ Resolve configuration
→ Run smallest meaningful smoke test
→ Lock validated configuration
→ Implement
→ Test
→ Record reproducibility/resource metadata
```

## Правила

- Предпочитайте измеренные возможности предположениям.
- Сохраняйте существующие соглашения проекта, если изменение намеренно их не обновляет.
- Явно отмечайте разрушительные изменения.
- Централизуйте конфигурацию и делайте её воспроизводимой.
- Никогда не раскрывайте секреты.
- Используйте поэтапную проверку и не повторяйте заведомо неработающие конфигурации.
