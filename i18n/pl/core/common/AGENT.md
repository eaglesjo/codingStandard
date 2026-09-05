# Ogólne zasady dla agentów AI

1. Przeczytaj i przestrzegaj instrukcji repozytorium.
2. Szanuj istniejącą architekturę i politykę.
3. Przed zmianą zachowania sprawdź odpowiedni kod i tests.
4. Przy zmianach zachowania dodaj lub zaktualizuj tests.
5. Szczegóły zależne od platformy ukrywaj za abstrakcją.
6. Nie commituj secrets ani credentials.
7. Network access stosuj tylko przy wyraźnej potrzebie.
8. Rzeczywiste execution environment traktuj jako source of truth.
9. Preferuj reproducible validation.
10. Po zmianach uruchom validation i zgłoś wyniki.

## Cykl pracy

```text
Inspect → Plan → Change → Validate → Review → Report
```

Sprawdź memory i runtime przed założeniami sprzętowymi. Dla długich zadań zweryfikuj early stopping i checkpoint.