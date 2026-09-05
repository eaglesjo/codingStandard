# Gemeinsame Regeln für KI-Agenten

Diese Regeln gelten für alle unterstützten Projektdomänen.

1. Untersuche vor Änderungen am Code das tatsächliche Repository, die Laufzeitumgebung, Abhängigkeiten, Tests und Sicherheitsanforderungen.
2. Erkenne und messe die reale Ausführungsumgebung, bevor ressourcenabhängige Einstellungen gewählt werden.
3. Hardcode niemals eine bestimmte Maschine, ein Betriebssystem, eine CPU, RAM, GPU, einen Beschleuniger oder eine IDE als Projektvoraussetzung.
4. Halte wiederverwendbare Domänenlogik in Modulen und beschränke Notebooks/Skripte auf die Orchestrierung.
5. Verwende explizite Konfiguration, Metadaten zur Reproduzierbarkeit und deterministische Pfade.
6. Bewahre Geheimnisse außerhalb der Quellcodeverwaltung auf.
7. Validiere Änderungen zuerst mit dem kleinsten sinnvollen Test und führe anschließend die umfassendere Testsuite aus.
8. Entferne nach der Umgebungsvalidierung ungenutzte Ausführungspfade und veralteten Code, sofern Mehrplattformunterstützung nicht beabsichtigt ist.
9. Lang laufende Workloads sollten Validierung, Early Stopping, den besten Checkpoint und Resume verwenden, sofern sinnvoll.
10. Experimente sollten eine Baseline, kontrollierte Varianten, Seeds, Metriken und Ressourcenverfolgung definieren.

## Standard-Ausführungszyklus

```text
Entdecken → Erkennen → Messen → Auflösen → Smoke Test → Festlegen → Implementieren → Validieren → Dokumentieren
```
