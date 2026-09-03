# Validation Google Colab

Ce document décrit l’exécution et la validation de `codingStandard` dans Google Colab.

## Ouvrir dans Colab

Utilisez le lien Colab du README du dépôt ou ouvrez directement le notebook suivant :

`https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/tests/colab/codingstandard_colab_test.ipynb`

Pour un fork ou une copie déplacée, ouvrez le notebook de cette copie dans Colab, puis saisissez l’URL du dépôt dans la première cellule ou définissez la variable d’environnement `CODINGSTANDARD_REPO_URL`.

## Sélection du dépôt

Le notebook n’est pas lié à une URL de dépôt unique. La priorité est la suivante :

1. variable d’environnement `CODINGSTANDARD_REPO_URL` ;
2. invite interactive pour l’URL du dépôt ;
3. URL `eaglesjo/codingStandard` comme valeur par défaut.

## Authentification des dépôts publics et privés

Le notebook tente d’abord un clone sans authentification.

- **Dépôt public :** le clone continue immédiatement, sans demande de token.
- **Dépôt privé :** après le rejet du clone non authentifié, un **GitHub Personal Access Token** est demandé via `getpass`.
- Un `GITHUB_TOKEN` présent dans Google Colab Secrets ou dans l’environnement est utilisé automatiquement lorsqu’il est disponible.

Le token est transmis à Git via un helper `GIT_ASKPASS` temporaire. Il n’est pas placé dans l’URL de clone, le code du notebook, la sortie affichée ou le JSON de résultat enregistré. Supprimez le token de la session Colab après le test.

## Vérifications effectuées

1. Clone le dépôt sélectionné dans le runtime Colab.
2. Détecte Python, PyTorch, CPU, RAM, accélérateur, VRAM, capacités CUDA/MPS et informations du runtime.
3. Exécute le profiler d’environnement LLM partagé.
4. Exécute un petit smoke test d’entraînement LLM avec sauvegarde/rechargement du checkpoint.
5. Exécute un petit smoke test d’entraînement Vision avec des tenseurs d’image.
6. Exécute la validation du dépôt.
7. Enregistre les ressources et l’état réussite/échec au format JSON.
8. Vérifie que le notebook fonctionne dans un runtime propre sans dépendre d’une machine de développement locale.

Si `/content/codingStandard` existe après un clone échoué ou partiel, le notebook supprime le répertoire incomplet et réessaie proprement.

Les tests sont volontairement petits. Un smoke test Colab réussi valide le standard de développement et le chemin d’exécution minimal ; il ne garantit pas qu’un modèle de production arbitraire tiendra dans les ressources du runtime Colab disponible.

## Utilisation recommandée

Exécutez ce notebook après une modification du profiler d’environnement, des memory smoke tests, de la configuration d’entraînement ou des instructions Colab.

## Validations associées

- Validation complète : [Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/tests/colab/codingstandard_colab_test.ipynb)
- Clean runtime : [Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/examples/colab/clean_runtime_validation.ipynb)
- LLM QLoRA : [Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/examples/colab/llm_qlora_validation.ipynb)
- RAG : [Open in Colab](https://colab.research.google.com/github/eaglesjo/codingStandard/blob/main/examples/colab/rag_validation.ipynb)
