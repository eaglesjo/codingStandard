# Règles communes pour les agents IA

Ces règles s’appliquent à tous les domaines pris en charge.

1. Inspectez le dépôt réel, l’environnement d’exécution, les dépendances, les tests et les exigences de sécurité avant toute modification du code.
2. Détectez et mesurez l’environnement réel avant de choisir des paramètres sensibles aux ressources.
3. Ne supposez jamais qu’une machine, un système d’exploitation, un CPU, une RAM, un GPU, un accélérateur ou un IDE particulier est requis.
4. Conservez la logique de domaine réutilisable dans les modules et limitez les notebooks/scripts à l’orchestration.
5. Utilisez une configuration explicite, des métadonnées de reproductibilité et des chemins déterministes.
6. Gardez les secrets hors du contrôle de version.
7. Validez d’abord avec le test significatif le plus petit, puis exécutez la suite de tests plus complète.
8. Après validation de l’environnement, supprimez les chemins d’exécution inutilisés et le code obsolète, sauf si le support multiplateforme est intentionnel.
9. Les charges longues devraient utiliser la validation, l’Early Stopping, le meilleur Checkpoint et le Resume lorsque cela est pertinent.
10. Les expériences doivent définir une baseline, des variantes contrôlées, des seeds, des métriques et un suivi des ressources.

## Cycle d’exécution standard

```text
Explorer → Détecter → Mesurer → Résoudre → Smoke Test → Fixer → Implémenter → Valider → Documenter
```
