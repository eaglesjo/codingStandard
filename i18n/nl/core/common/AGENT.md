# Algemene regels voor AI-agents

1. Lees en volg de repository-instructies.
2. Respecteer de bestaande architectuur en het beleid.
3. Controleer relevante code en tests vóór gedragswijzigingen.
4. Voeg tests toe of werk ze bij bij gedragswijzigingen.
5. Abstracteer platformafhankelijke details.
6. Commit nooit secrets of credentials.
7. Gebruik network access alleen wanneer dit expliciet nodig is.
8. Gebruik de echte execution environment als source of truth.
9. Geef prioriteit aan reproduceerbare validation.
10. Voer validation uit na wijzigingen en rapporteer de resultaten.

## Werkcyclus

```text
Inspect → Plan → Change → Validate → Review → Report
```

Controleer memory en runtime voordat hardware-aannames worden gemaakt. Controleer bij lange workloads early stopping en checkpoint.