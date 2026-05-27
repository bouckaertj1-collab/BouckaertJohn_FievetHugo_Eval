# Agent IA - Assistant de Recettes

Ce dossier contient la partie 5 du travail : un agent IA basique réalisé avec Google ADK.

L’agent permet de gérer une petite base locale de recettes stockée dans un fichier JSON.

## Fonctionnalités

L’agent peut notamment :

- ajouter une recette ;
- lister les recettes disponibles ;
- rechercher des recettes par ingrédient ;
- suggérer une recette selon les ingrédients disponibles ;
- générer une liste de courses ;
- supprimer une recette.

## Structure du dossier

```txt
part5 - agent_ia_recettes/
│
├── agent_ia_assistant_recettes_NOTEBOOK.ipynb
├── pyproject.toml
├── uv.lock
├── recipes.json
├── data/
├── recipe_agent/
│   ├── __init__.py
│   ├── agent.py
│   └── tools.py
├── tests/
│   └── test_tools.py
├── rapport/
│   └── rapport_agent_ia_recettes.md
└── use_case/
```

## Prérequis

Pour exécuter cette partie, il faut avoir installé :

- Python ;
- uv ;
- Ollama.

Le modèle utilisé par défaut dans `recipe_agent/agent.py` est :

```txt
ollama_chat/qwen3:4b
```

Il faut donc installer le modèle Ollama correspondant :

```bash
ollama pull qwen3:4b
```

Pour vérifier que le modèle est bien disponible :

```bash
ollama list
```

La liste doit contenir :

```txt
qwen3:4b
```

---

# Exécution depuis la racine du dépôt

Ces commandes sont prévues pour être lancées depuis la racine du dépôt, c’est-à-dire depuis le dossier qui contient `part3 - Titanic_pipeline`, `part4 - BD vectorielle_Embeddings` et `part5 - agent_ia_recettes`.

## Installer les dépendances

```bash
uv --directory "part5 - agent_ia_recettes" sync
```

Si le projet est placé dans OneDrive et que `uv` signale un problème de hardlink, utiliser :

```bash
uv --directory "part5 - agent_ia_recettes" sync --link-mode=copy
```

## Lancer les tests

```bash
uv --directory "part5 - agent_ia_recettes" run pytest
```

ou avec plus de détails :

```bash
uv --directory "part5 - agent_ia_recettes" run pytest tests/ -v
```

## Lancer l’agent

```bash
uv --directory "part5 - agent_ia_recettes" run adk web
```

Ouvrir ensuite l’interface web :

```txt
http://127.0.0.1:8000
```

Puis sélectionner l’agent `recipe_agent`.

---

# Exécution depuis le dossier de la partie 5

Si le terminal est déjà placé dans le dossier `part5 - agent_ia_recettes/`, les commandes sont plus courtes.

## Installer les dépendances

```bash
uv sync
```

En cas de problème de hardlink dans OneDrive :

```bash
uv sync --link-mode=copy
```

## Lancer les tests

```bash
uv run pytest
```

ou :

```bash
uv run pytest tests/ -v
```

## Lancer l’agent

```bash
uv run adk web
```

Ouvrir ensuite :

```txt
http://127.0.0.1:8000
```

et sélectionner l’agent `recipe_agent`.


