# Partie 4 - Embeddings et base vectorielle

Ce dossier contient la partie du travail consacrée aux embeddings et aux bases vectorielles.

Le projet permet de lire des articles au format Word (`.docx`) et de les classer principalement comme articles de **sport** ou de **cuisine**.  
Une règle de confiance permet aussi de signaler certains textes comme **ambigus** lorsque la prédiction n’est pas suffisamment fiable.

## Contenu du dossier

```txt
part4 - BD vectorielle_Embeddings/
│
├── notebook/
│   └── partie4_embeddings_faiss.ipynb
├── data/
│   ├── train/   # articles utilisés pour construire la base vectorielle
│   └── test/    # articles utilisés pour tester le programme
├── rapport/
│   └── rapport.md
└── README.md
```

## Exécution du notebook

Le notebook peut être ouvert et exécuté avec **VS Code**.

Fichier à ouvrir :

```txt
notebook/partie4_embeddings_faiss.ipynb
```

Il suffit ensuite d’exécuter les cellules dans l’ordre.

## Installation des librairies

Le notebook contient déjà une cellule d’installation au début :

```python
%pip install python-docx sentence-transformers faiss-cpu numpy pandas scikit-learn matplotlib
```

Cette cellule installe les librairies nécessaires à l’exécution du notebook.  
Elle peut être exécutée si les librairies ne sont pas encore installées dans l’environnement Python utilisé par VS Code.

Les principales librairies utilisées sont :

- `python-docx` pour lire les fichiers Word ;
- `sentence-transformers` pour générer les embeddings ;
- `faiss-cpu` pour construire la base vectorielle ;
- `pandas` et `numpy` pour manipuler les données ;
- `scikit-learn` pour la PCA et l’évaluation ;
- `matplotlib` pour les graphiques.

## Principe général

Le programme suit les étapes suivantes :

1. lecture des fichiers Word depuis le dossier `data/train/` ;
2. nettoyage du texte ;
3. tokenisation en ignorant la ponctuation ;
4. génération des embeddings ;
5. normalisation des vecteurs ;
6. stockage des embeddings dans une base vectorielle FAISS ;
7. lecture des fichiers de test ;
8. recherche des articles d’entraînement les plus proches ;
9. prédiction de la catégorie à partir des voisins trouvés ;
10. détection des cas ambigus lorsque la prédiction n’est pas suffisamment fiable ;
11. visualisation des embeddings avec une PCA.

## Organisation des fichiers de données

Les articles d’entraînement sont placés dans :

```txt
data/train/
```

Ils servent à construire la base vectorielle FAISS.

Les articles de test sont placés dans :

```txt
data/test/
```

Ils servent à vérifier les prédictions du programme.

Les noms des fichiers permettent de retrouver leur catégorie attendue :

```txt
sport_...docx
cuisine_...docx
test_sport_...docx
test_cuisine_...docx
test_ambiguite_...docx
```

## Détection des articles ambigus

La classification principale concerne les catégories **sport** et **cuisine**.

La catégorie **ambigu** est une règle de prudence ajoutée après la recherche des plus proches voisins.  
Elle est utilisée lorsque les voisins sont trop partagés entre sport et cuisine, ou lorsque la similarité avec le meilleur voisin est trop faible.

Cela évite de forcer une réponse sport ou cuisine lorsque le texte mélange plusieurs thèmes.

## Résultats affichés dans le notebook

Le notebook affiche notamment :

- les fichiers chargés ;
- les textes nettoyés et tokenisés ;
- les embeddings générés ;
- l’index FAISS construit ;
- les voisins les plus proches pour chaque article testé ;
- la prédiction finale ;
- la matrice de confusion ;
- l’accuracy globale ;
- l’analyse des cas ambigus ;
- la visualisation PCA des embeddings.

## Rapport

Le rapport de cette partie se trouve dans :

```txt
rapport/rapport.md
```

Il résume l’objectif du travail, la méthode utilisée, l’organisation des tests, l’utilisation de l’IA générative, les limites et les améliorations possibles.
