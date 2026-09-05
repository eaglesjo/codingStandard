# Regole comuni per agenti IA

Queste regole valgono per ogni dominio supportato.

1. Ispeziona repository, ambiente di esecuzione, dipendenze, test e vincoli di sicurezza prima di modificare il codice.
2. Rileva e misura l'ambiente reale prima di scegliere impostazioni sensibili alle risorse.
3. Non imporre come prerequisito una macchina, un sistema operativo, CPU, RAM, GPU, acceleratore o IDE specifici.
4. Mantieni la logica di dominio riutilizzabile nei moduli e usa notebook/script per l'orchestrazione.
5. Usa configurazione esplicita, metadati di riproducibilità e percorsi deterministici.
6. Mantieni i segreti fuori dal controllo del codice sorgente.
7. Valida prima con il test minimo significativo, poi con la suite più ampia.
8. Dopo la validazione dell'ambiente, rimuovi rami inutilizzati e codice obsoleto salvo supporto multipiattaforma intenzionale.
9. I carichi lunghi dovrebbero usare validazione, Early Stopping, il miglior Checkpoint e Resume quando appropriato.
10. Gli esperimenti devono definire baseline, varianti controllate, seed, metriche e tracciamento delle risorse.

## Ciclo standard

```text
Scopri → Rileva → Misura → Risolvi → Smoke Test → Blocca → Implementa → Valida → Registra
```
