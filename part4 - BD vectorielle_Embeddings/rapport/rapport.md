# Mini rapport - BD vectorielle et embeddings

## 1. Objectif du travail
L’objectif de ce travail est de réaliser un programme Python, sous forme de notebook, capable de lire un article au format Word (`.docx`) et de déterminer s’il correspond principalement à un article de **sport** ou de **cuisine**.
Une règle de confiance a également été ajoutée afin de signaler certains articles comme **ambigus** lorsque la prédiction n’est pas suffisamment fiable.
Pour cela, le programme utilise une approche basée sur les embeddings et une base vectorielle FAISS. Chaque article est transformé en vecteur numérique représentant le sens général du texte. Le document à classer est ensuite comparé aux articles d’entraînement déjà présents dans la base, afin de retrouver les textes les plus proches et d’en déduire la catégorie la plus probable.

## 2. Méthode utilisée

Le programme suit les étapes suivantes :

1. lecture des fichiers Word avec la bibliothèque `python-docx` ;
2. nettoyage du texte ;
3. tokenisation en ignorant la ponctuation ;
4. génération des embeddings avec `sentence-transformers` ;
5. normalisation des vecteurs ;
6. indexation des embeddings dans FAISS avec `IndexFlatL2` ;
7. recherche des `k` documents les plus proches ;
8. prédiction de la catégorie à partir des voisins trouvés ;
9. détection des cas ambigus lorsque le résultat n’est pas suffisamment fiable.

Cette méthode ne se limite pas à vérifier la présence de mots précis. Elle permet de comparer les textes selon leur sens général, en utilisant leur représentation sous forme de vecteurs numériques.

## 3. Organisation des tests

Les fichiers sont organisés en deux dossiers :

- `data/train/` : articles connus, utilisés pour construire la base vectorielle ;
- `data/test/` : articles inconnus, utilisés pour évaluer les prédictions du programme.

Les fichiers d’entraînement sont nommés avec un préfixe indiquant leur catégorie :

- `sport_...docx` pour les articles de sport ;
- `cuisine_...docx` pour les articles de cuisine.

Les fichiers de test suivent également une convention de nommage :

- `test_sport_...docx` pour les articles de sport ;
- `test_cuisine_...docx` pour les articles de cuisine ;
- `test_ambiguite_...docx` pour les articles mélangeant volontairement les deux thèmes.

Les fichiers de test ne sont pas utilisés pour construire la base vectorielle. Ils servent uniquement à vérifier le comportement du programme sur de nouveaux articles.

## 4. Détection des cas ambigus

En plus des catégories sport et cuisine, le programme peut retourner la catégorie `ambigu`.

Cette détection est ajoutée après la recherche des plus proches voisins. Le modèle d’embeddings permet de transformer le texte en vecteur et FAISS permet de retrouver les documents les plus proches, mais c’est une règle supplémentaire qui décide si le résultat est suffisamment fiable ou non.

Le programme classe un article comme ambigu dans deux situations :

- lorsque les voisins trouvés sont trop partagés entre sport et cuisine ;
- lorsque la similarité avec le meilleur voisin est trop faible.

Dans le notebook, la classification utilise `k = 5`. Par exemple, si les cinq voisins les plus proches sont répartis en trois documents sport et deux documents cuisine, la majorité existe, mais elle reste trop faible pour être totalement fiable. Le programme considère alors que le texte est ambigu.

De la même manière, si le meilleur voisin obtenu a une similarité trop faible, le programme évite de forcer une prédiction en sport ou en cuisine. Cette règle permet de traiter plus prudemment les textes qui mélangent plusieurs thèmes.

## 5. Résultats obtenus

Les résultats obtenus sont satisfaisants dans le cadre de ce travail. Les articles de test clairement liés au sport ou à la cuisine sont correctement classés. Les articles ambigus sont également pris en compte dans l’évaluation, puisque le programme peut maintenant retourner la catégorie `ambigu`.

L’analyse des voisins permet aussi de justifier les prédictions. Pour chaque article testé, le programme affiche les documents d’entraînement les plus proches, leur catégorie et leur similarité avec le texte testé. Cela permet de comprendre pourquoi un article est classé comme sport, cuisine ou ambigu.

Les résultats montrent donc que l’approche fonctionne bien sur les fichiers utilisés pour ce travail. Elle permet non seulement de classer les articles clairement orientés, mais aussi d’éviter une réponse trop catégorique lorsque le texte contient des éléments liés aux deux catégories.

## 6. Utilisation de l’IA générative et analyse réflexive

L’IA générative a été utilisée pour générer les articles utilisés pour les tests, pour formuler certaines explications du notebook. Elle a surtout servi de support de compréhension et de vérification. 


## 7. Limites et améliorations possibles

Le programme donne de bons résultats sur les fichiers de test utilisés, mais il reste limité par le nombre de documents disponibles. Les résultats sont donc valables dans le cadre de cet exercice, mais ils devraient être vérifiés avec davantage d’articles réels.

Les seuils utilisés pour détecter les cas ambigus sont fixés manuellement. Ils fonctionnent pour les tests réalisés, mais ils pourraient être ajustés avec un jeu de test plus large.

Avec de vrais articles plus longs, il faudrait aussi tenir compte de la limite de tokens du modèle d’embeddings. Si un texte est trop long, le modèle peut ne prendre en compte qu’une partie du contenu. Une amélioration possible serait donc de découper les longs articles en plusieurs morceaux, puis de combiner les résultats obtenus.

Pour améliorer le projet, on pourrait également ajouter plus d’articles, tester plusieurs modèles d’embeddings, comparer différentes valeurs de `k`, ou analyser plus précisément l’impact des seuils utilisés pour la catégorie `ambigu`.

## 8. Conclusion

Ce travail montre qu’il est possible de classer automatiquement des articles Word à l’aide d’embeddings et d’une base vectorielle FAISS. Le programme transforme chaque texte en vecteur numérique, recherche les articles d’entraînement les plus proches, puis détermine la catégorie la plus adaptée.

Les résultats montrent que l’approche fonctionne correctement pour distinguer les articles de sport et de cuisine. L’ajout d’une règle de confiance permet aussi de traiter les textes ambigus sans forcer systématiquement une réponse. Le système devient donc plus prudent lorsque le texte testé mélange plusieurs thèmes ou lorsque la proximité avec les documents connus est insuffisante.