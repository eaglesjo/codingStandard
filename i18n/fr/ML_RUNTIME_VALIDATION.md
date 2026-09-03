# Validation du runtime ML/DL

Ce guide valide le contrat d’exécution réel après l’installation de `codingStandard`.

## Routage des agents

Depuis la racine du dépôt :

```bash
python scripts/validation/validate_agent_routing.py
```

Le test couvre quatre requêtes représentatives :

- entraînement PyTorch générique → common + cycle de vie ML
- LLM QLoRA → common + ML + fine-tuning/PEFT/quantification LLM
- détection Vision → common + ML + détection/évaluation Vision
- entraînement LLM sur Colab → common + ML + LLM + politique checkpoint/reprise Colab

Le test vérifie également qu’aucun domaine non pertinent n’est ajouté accidentellement à ces scénarios minimaux.

## Runtime Colab

Ouvrez `examples/colab/clean_runtime_validation.ipynb` dans un runtime Colab vierge et exécutez toutes les cellules de haut en bas.

Le notebook doit :

1. identifier le kernel Python actif et l’environnement d’exécution ;
2. signaler les caractéristiques de l’accélérateur, de la RAM et du disque lorsqu’elles sont disponibles ;
3. exécuter le test du contrat de routage des agents ;
4. exécuter un petit smoke test PyTorch forward/backward lorsque PyTorch est disponible ;
5. écrire et restaurer un checkpoint dans le répertoire persistant sélectionné ;
6. produire un rapport runtime lisible par machine.

Utilisez un emplacement persistant monté pour les checkpoints qui doivent survivre à une réinitialisation Colab. Le système de fichiers de la VM Notebook doit être considéré comme jetable.

## Interprétation

Une validation réussie signifie que la politique installée peut être découverte, que le runtime sélectionné est mesurable, qu’une charge représentative peut démarrer en sécurité et que les artefacts de récupération peuvent être restaurés. Elle ne signifie pas que tous les types d’accélérateurs Colab ni toutes les tailles de modèles ont été testés.
