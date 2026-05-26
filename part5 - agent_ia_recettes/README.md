# Agent IA Assistant de Recettes

Ce projet contient un agent IA basique basé sur Google ADK. L'agent aide à gérer une petite base locale de recettes.

## Fonctionnalités

- Ajouter une recette
- Lister les recettes
- Rechercher par ingrédient
- Suggérer une recette selon les ingrédients disponibles
- Générer une liste de courses
- Supprimer une recette

## Installation

```bash
uv sync
```

Si le projet est placé dans OneDrive et que `uv` signale un problème de hardlink, utiliser :

```bash
uv sync --link-mode=copy
```

## Lancer les tests

```bash
uv run pytest tests/ -v
```

## Lancer l'agent

Ollama doit être installé et lancé, avec un modèle disponible, par exemple :

```bash
ollama pull qwen3:4b
```

Le modèle configuré par défaut dans `recipe_agent/agent.py` est `ollama_chat/qwen3:4b`.

Puis lancer ADK Web :

```bash
uv run adk web
```

Ouvrir ensuite :

```text
http://127.0.0.1:8000
```

et sélectionner l'agent `recipe_agent`.

## Structure du projet

```text
recipe_agent/agent.py                               Définition de l'agent ADK
recipe_agent/tools.py                               Outils Python utilisés par l'agent
agent_ia_assistant_recettes_NOTEBOOK.ipynb          Notebook de présentation du projet
recipes.json                                        Base locale de recettes
tests/test_tools.py                                 Tests unitaires
rapport/                                            Rapport du devoir
use_case/                                           Diagramme de cas d'utilisation
```
