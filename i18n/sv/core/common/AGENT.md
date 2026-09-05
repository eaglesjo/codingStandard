# Allmänna regler för AI-agenter

1. Läs och följ repositoryts instruktioner.
2. Respektera befintlig arkitektur och policy.
3. Kontrollera relevant kod och tests före beteendeförändringar.
4. Lägg till eller uppdatera tests vid beteendeförändringar.
5. Abstrahera plattformsspecifika detaljer.
6. Committa aldrig secrets eller credentials.
7. Använd network access endast när det uttryckligen behövs.
8. Använd den verkliga execution environment som source of truth.
9. Prioritera reproducible validation.
10. Kör validation efter ändringar och rapportera resultatet.

## Arbetscykel

```text
Inspect → Plan → Change → Validate → Review → Report
```

Kontrollera memory och runtime innan hårdvaruantaganden. För långa arbetsflöden, verifiera early stopping och checkpoint.