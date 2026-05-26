# Examen ML - Embeddings et base vectorielle

Ce projet contient une solution permettant de lire un article Word (`.docx`) et de le classer comme article de **sport**, de **cuisine** ou comme article **ambigu** à l'aide d'embeddings et d'une base vectorielle FAISS.

## Contenu du projet

```text
Part4 - BD vectorielle_Embeddings/
├── notebook/
│   └── partie4_embeddings_faiss.ipynb
├── data/
│   ├── train/   # 20 articles d'entraînement : 10 sport + 10 cuisine
│   └── test/    # 10 articles de test : 4 sport + 4 cuisine + 2 ambigus
├── rapport/
│   └── rapport.md
├── requirements.txt
└── README.md
```

## Installation

Installer les dépendances nécessaires avec la commande suivante :

```bash
pip install -r requirements.txt
```

## Exécution

Ouvrir le notebook avec Jupyter :

```bash
jupyter notebook notebook/partie4_embeddings_faiss.ipynb
```

ou avec JupyterLab :

```bash
jupyter lab
```

## Principe général

Le programme suit les étapes suivantes :

1. lecture des articles d'entraînement depuis le dossier `data/train/` ;
2. nettoyage du texte et tokenisation en ignorant la ponctuation ;
3. génération des embeddings avec `sentence-transformers` ;
4. normalisation des vecteurs ;
5. stockage des embeddings dans un index FAISS ;
6. lecture et transformation d'un article de test en embedding ;
7. recherche des documents d'entraînement les plus proches ;
8. prédiction de la catégorie à partir des voisins trouvés ;
9. détection des cas ambigus lorsque la prédiction n'est pas suffisamment fiable.

## Organisation des fichiers

Les documents d'entraînement servent uniquement à construire la base vectorielle. Ils sont nommés avec les préfixes suivants :

- `sport_...docx`
- `cuisine_...docx`

Les documents de test servent à évaluer le programme sur de nouveaux articles. Ils sont nommés avec les préfixes suivants :

- `test_sport_...docx`
- `test_cuisine_...docx`
- `test_ambiguite_...docx`

Les fichiers ambigus sont inclus dans l'évaluation, car le programme peut retourner la catégorie `ambigu`.

## Détection des articles ambigus

Le programme utilise les `k` plus proches voisins pour classer un article. Dans le notebook, la valeur utilisée est `k = 5`.

Une règle de confiance permet de retourner la catégorie `ambigu` dans deux cas :

- lorsque les voisins sont trop partagés entre les catégories sport et cuisine ;
- lorsque la similarité avec le meilleur voisin est trop faible.

Cette règle évite de forcer une prédiction en sport ou en cuisine lorsque le texte mélange plusieurs thèmes ou lorsque le résultat n'est pas suffisamment fiable.

## Résultats affichés dans le notebook

Le notebook permet d'afficher :

- les documents chargés ;
- les textes nettoyés et tokenisés ;
- les embeddings générés ;
- l'index FAISS construit ;
- les voisins les plus proches pour chaque article testé ;
- la prédiction finale ;
- l'accuracy globale sur les catégories sport, cuisine et ambigu ;
- une analyse des cas ambigus ;
- une visualisation 2D des embeddings avec PCA.


