# Travail Machine Learning - Parties 3, 4 et 5

Ce dépôt contient les parties finales du travail de Machine Learning.

Toutes les commandes ci-dessous sont prévues pour être lancées **depuis la racine du dépôt**, c’est-à-dire depuis le dossier qui contient les dossiers `part3 - Titanic_pipeline`, `part4 - BD vectorielle_Embeddings` et `part5 - agent_ia_recettes`.

---

## Structure du dépôt

```txt
Travail Machine Learning Part2/
│
├── part3 - Titanic_pipeline/
├── part4 - BD vectorielle_Embeddings/
├── part5 - agent_ia_recettes/
├── .gitignore
└── README.md
```

---

## Partie 3 - Pipeline Titanic

### Objectif

Cette partie présente la conception complète d’un modèle de prédiction appliqué au dataset Titanic.

Le notebook regroupe les étapes principales :

- chargement des données ;
- préparation des variables ;
- prétraitement ;
- sélection des variables ;
- entraînement du modèle final ;
- évaluation des performances.

### Emplacement

```txt
part3 - Titanic_pipeline/
```

### Exécution

Ouvrir le notebook présent dans le dossier `part3 - Titanic_pipeline/` avec Jupyter Notebook ou VS Code, puis exécuter les cellules dans l’ordre.

Le fichier CSV du dataset Titanic doit rester dans le même dossier que le notebook.

---

## Partie 4 - BD vectorielle et embeddings

### Objectif

Cette partie contient un programme permettant de lire des articles au format Word (`.docx`) et de les classer principalement comme articles de sport ou de cuisine.

Le programme utilise :

- une lecture de fichiers Word ;
- une tokenisation en ignorant la ponctuation ;
- des embeddings ;
- une base vectorielle FAISS ;
- une recherche des voisins les plus proches ;
- une règle de confiance permettant de signaler certains articles comme ambigus.

### Emplacement

```txt
part4 - BD vectorielle_Embeddings/
```

### Structure

```txt
part4 - BD vectorielle_Embeddings/
│
├── notebook/
│   └── partie4_embeddings_faiss.ipynb
├── data/
│   ├── train/
│   └── test/
├── rapport/
│   └── rapport.md
└── requirements.txt
```

### Installation

Depuis la racine du dépôt :

```bash
python -m pip install -r "part4 - BD vectorielle_Embeddings/requirements.txt"
```

### Exécution

Ouvrir le notebook suivant avec Jupyter Notebook ou VS Code :

```txt
part4 - BD vectorielle_Embeddings/notebook/partie4_embeddings_faiss.ipynb
```

puis exécuter les cellules dans l’ordre.

La première exécution peut nécessiter une connexion Internet afin de télécharger le modèle d’embeddings utilisé par `sentence-transformers`.

---

## Partie 5 - Agent IA recettes

### Objectif

Cette partie présente un agent IA basique sous forme d’assistant de recettes.

L’agent permet notamment de :

- consulter des recettes ;
- rechercher des recettes selon des ingrédients ;
- ajouter une recette ;
- supprimer une recette ;
- proposer une liste de courses ;
- interagir avec l’utilisateur via l’interface ADK.

Les données sont stockées dans un fichier JSON.

### Emplacement

```txt
part5 - agent_ia_recettes/
```

### Structure

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

### Prérequis

Pour lancer l’agent, il faut avoir installé :

- Python ;
- uv ;
- Ollama ;
- le modèle Ollama utilisé par l’agent.

Installer le modèle Ollama :

```bash
ollama pull qwen3:4b
```

### Installation de la partie 5

Depuis la racine du dépôt :

```bash
uv --directory "part5 - agent_ia_recettes" sync
```

### Lancer les tests

Depuis la racine du dépôt :

```bash
uv --directory "part5 - agent_ia_recettes" run pytest
```

### Lancer l’agent

Depuis la racine du dépôt :

```bash
uv --directory "part5 - agent_ia_recettes" run adk web
```

Une interface web ADK s’ouvre ensuite dans le navigateur.


## Remarque finale

Les notebooks constituent les livrables principaux pour les parties 3 et 4.

Pour la partie 5, le projet contient :

- le code de l’agent ;
- un notebook de présentation ;
- des tests ;
- un rapport ;
- un diagramme de cas d’utilisation.
