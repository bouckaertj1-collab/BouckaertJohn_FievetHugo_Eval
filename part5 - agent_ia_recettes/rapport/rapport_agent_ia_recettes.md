# Rapport - Agent IA Assistant de Recettes

## 1. Introduction

L'objectif de ce travail est de créer un agent IA basique en s'appuyant sur les principes vus pendant l'atelier de M. Suire.

L'atelier présentait la création d'un agent capable d'utiliser des outils Python pour gérer des données. Pour ce devoir, j'ai choisi de réutiliser cette logique dans un autre contexte : un assistant de recettes.

## 2. Objectif de l'agent

L'agent IA assistant de recettes permet à l'utilisateur de gérer une petite base locale de recettes. Il peut ajouter une recette, afficher les recettes disponibles, rechercher une recette par ingrédient, proposer une recette selon les ingrédients disponibles, générer une liste de courses et supprimer une recette.

L'utilisateur n'a pas besoin d'appeler directement les fonctions Python. Il peut formuler une demande en langage naturel, par exemple : « J'ai des oeufs, du fromage et du beurre. Que peux-tu me proposer ? ». L'agent interprète la demande et appelle l'outil adapté.

## 3. Différence entre un chatbot et un agent IA

Un chatbot classique produit principalement une réponse textuelle. Dans ce projet, l'agent peut agir sur des données locales grâce à des outils Python.

Par exemple, lorsqu'un utilisateur demande d'ajouter une recette, l'agent ne se contente pas de répondre qu'il peut le faire. Il appelle une fonction Python qui enregistre réellement la recette dans le fichier `recipes.json`. Cette capacité à utiliser des outils distingue l'agent d'un simple chatbot.

## 4. Use case

L'acteur principal est l'utilisateur. Il interagit avec l'agent pour gérer ses recettes ou obtenir une proposition de plat.

Les principaux cas d'utilisation sont : enregistrer une nouvelle recette, afficher les recettes disponibles, trouver des recettes avec un ingrédient donné, proposer une recette selon les ingrédients disponibles, préparer une liste d'achats, supprimer une recette et refuser une demande hors périmètre.

Le diagramme use case est fourni dans le dossier `use_case/`. 

## 5. Architecture technique

Le projet est organisé autour de plusieurs éléments :

- `recipe_agent/agent.py` : définition de l'agent, du modèle, du prompt système et des outils disponibles ;
- `recipe_agent/tools.py` : fonctions Python appelables par l'agent ;
- `recipes.json` : fichier de stockage des recettes ;
- `tests/test_tools.py` : tests unitaires des outils.

Le fonctionnement général est le suivant :

```text
Utilisateur -> Agent ADK -> Modèle de langage -> Choix d'un outil Python -> recipes.json -> Réponse finale
```

Le modèle de langage ne modifie pas directement les données. Son rôle est d'interpréter la demande et de choisir l'outil adapté. Les actions réelles sont exécutées par le code Python.

## 6. Technologies utilisées

### Google ADK

Google ADK est utilisé pour définir et exécuter l'agent. Il permet de déclarer un agent, de lui associer un modèle de langage, un prompt système et une liste d'outils Python. Dans ce projet, il joue le rôle d'orchestrateur.

### LiteLLM

LiteLLM sert de connecteur entre Google ADK et le modèle de langage. Il permet d'utiliser un modèle local ou distant avec une interface commune.

### Ollama

Ollama permet de faire tourner un modèle de langage localement. Dans ce projet, il exécute le modèle utilisé par l'agent pour comprendre les demandes de l'utilisateur.

### Fichier JSON

Le fichier `recipes.json` sert de stockage local. Les recettes restent enregistrées après l'arrêt du notebook ou de l'interface ADK Web.

## 7. Outils développés

Les outils sont des fonctions Python classiques rendues accessibles à l'agent.

- `add_recipe` ajoute une recette dans le fichier JSON.
- `list_recipes` affiche les recettes enregistrées.
- `search_recipes_by_ingredient` recherche les recettes contenant un ingrédient.
- `suggest_recipe` propose une recette en fonction des ingrédients disponibles.
- `generate_shopping_list` génère une liste de courses pour une recette.
- `delete_recipe` supprime une recette à partir de son identifiant.

Ces outils sont déterministes : pour une même entrée, ils produisent le même résultat. Cela les rend plus faciles à tester que le comportement global d'un agent basé sur un modèle de langage.


## 7.1 Suggestions automatiques via le LLM

Comme dans l’atelier, les suggestions automatiques ne sont pas implémentées sous forme d’un outil Python déterministe. Elles sont pilotées par le prompt système et générées par le LLM à partir du contexte.

Dans ce projet, après l’ajout réussi d’une recette, l’agent confirme l’ajout puis propose une ou deux idées de recettes similaires, de variantes ou d’accompagnements. Ces propositions ne sont pas ajoutées automatiquement dans le fichier `recipes.json` : l’utilisateur doit confirmer s’il veut réellement les enregistrer. Cette partie illustre la différence entre les outils déterministes, qui donnent toujours le même résultat pour une même entrée, et un comportement génératif du LLM, plus flexible mais moins prévisible.

## 8. Démarche de conception du projet

L'objectif était de conserver la même logique technique vu pendant l'atelier de M. Suire, tout en l'appliquant à un cas d'usage différent de l'exemple de gestion de tâches.

Le choix de l'assistant de recettes répond à plusieurs critères. Le domaine est simple à comprendre, les données peuvent être stockées localement dans un fichier JSON, et les actions possibles sont assez variées pour montrer l'intérêt d'un agent : ajouter, rechercher, proposer, lister ou supprimer une recette.

Le projet a donc été organisé en séparant clairement les rôles. Le fichier `agent.py` définit le comportement général de l'agent et les outils disponibles. Le fichier `tools.py` contient les fonctions Python qui réalisent les actions concrètes. Le fichier `recipes.json` conserve les recettes afin que les données restent disponibles entre deux exécutions.

Cette organisation permet d'avoir un projet simple, lisible et testable. Les fonctions Python peuvent être vérifiées avec des tests unitaires, tandis que le comportement global de l'agent peut être observé dans l'interface ADK Web à travers des scénarios en langage naturel.

## 9. Analyse réflexive 

Ce projet m'a permis de mieux comprendre la différence entre un simple chatbot et un agent IA. L'intérêt principal de l'agent ne vient pas seulement du modèle de langage, mais de sa capacité à utiliser des outils.

Dans ce projet, le modèle sert surtout à comprendre la demande de l'utilisateur. Les actions importantes sont réalisées par les fonctions Python. Cette séparation est importante, car elle permet de garder une partie fiable et testable dans le projet.

Le choix de l'assistant de recettes montre qu'une architecture vue dans l'atelier de Mr Suire peut être adaptée à un autre domaine. Le principe reste le même : un agent, des outils et des données persistantes. Par contre, les outils développés répondent à un nouveau besoin : rechercher des recettes, proposer un plat ou générer une liste de courses.

Ce travail montre aussi certaines limites. Un modèle de langage peut mal interpréter une demande, oublier d'utiliser un outil ou extraire une information de manière incomplète. Pour limiter ces risques, le prompt système doit être précis et les outils Python doivent gérer les erreurs possibles.

Enfin, les tests montrent qu'il faut distinguer les tests du code Python et les tests du comportement de l'agent. Les fonctions Python sont déterministes et peuvent être testées avec `pytest`. Le comportement global de l'agent est plus difficile à valider automatiquement, car il dépend de l'interprétation du modèle.


## 10. Utilisation de l’IA générative

L’IA générative a été utilisée comme support pendant le projet. Elle m’a principalement aidé à reformuler certaines parties du rapport afin de rendre les explications plus claires et mieux structurées.

Elle m’a également permis de mieux comprendre la théorie liée à la conception d’un agent IA, notamment la logique générale d’un agent, le rôle des outils.

## 11. Organisation des tests

Les tests sont organisés à deux niveaux.

### Tests unitaires

Les tests unitaires se trouvent dans `tests/test_tools.py`. Ils vérifient les outils Python indépendamment du modèle de langage. Ils utilisent un fichier JSON temporaire afin de ne pas modifier les vraies données du projet.

La commande utilisée est :

```bash
uv run pytest tests/ -v
```

Les tests vérifient notamment l'ajout d'une recette, le refus d'une difficulté invalide, le refus d'un doublon, l'affichage des recettes, la recherche par ingrédient, la suggestion de recette, la génération d'une liste de courses et la suppression d'une recette.

### Tests manuels dans ADK Web

Les tests manuels consistent à envoyer des messages à l'agent dans l'interface ADK Web. Ils permettent de vérifier que l'agent comprend une demande en langage naturel et choisit le bon outil.

Exemples de messages testés :

| Scénario | Message envoyé | Résultat attendu |
|---|---|---|
| Afficher les recettes | `Liste les recettes disponibles.` | L'agent affiche les recettes enregistrées. |
| Rechercher par ingrédient | `Quelles recettes contiennent de la tomate ?` | L'agent retourne les recettes contenant de la tomate. |
| Suggérer une recette | `J'ai des œufs, du fromage et du beurre. Que peux-tu me proposer ?` | L'agent propose une recette compatible. |
| Générer une liste de courses | `Que dois-je acheter pour faire les pâtes tomate basilic si j'ai déjà des pâtes et de la tomate ?` | L'agent retourne les ingrédients manquants. |
| Ajouter une recette | `Ajoute une recette de soupe de légumes avec carotte, pomme de terre, poireau et oignon.` | L'agent enregistre la recette. |
| Demande hors périmètre | `Quel temps fera-t-il demain ?` | L'agent refuse poliment. |

## 12. Limites et améliorations possibles

L'agent reste volontairement basique. Le stockage dans un fichier JSON est simple, mais il est limité pour une application plus grande. Les ingrédients ne contiennent pas encore de quantités, donc la liste de courses indique seulement les ingrédients manquants.

Le comportement dépend aussi du modèle de langage utilisé. Avec un petit modèle local, certaines réponses peuvent être moins précises.

Des améliorations possibles seraient d'ajouter des quantités, des tags comme végétarien ou économique, une base SQLite, une confirmation avant suppression, des tests comportementaux automatisés ou une connexion à une API de recettes.

## 13. Conclusion

Ce projet montre comment construire un agent IA simple capable d'utiliser des outils Python. L'agent assistant de recettes ne se limite pas à produire une réponse textuelle : il peut consulter et modifier une base locale de recettes.

Le projet reprend les principes vus pendant l'atelier de M. Suire, mais les adapte à un nouveau cas d'usage. Il met en évidence le rôle du modèle de langage, des outils Python, de la persistance des données et des tests.

L'intérêt principal de ce travail est de montrer qu'un agent IA doit être pensé comme un petit système logiciel. Il faut définir son périmètre, ses outils, ses données, ses erreurs possibles et sa manière d'être testé. Même si l'application reste simple, elle permet de comprendre concrètement comment un modèle de langage peut être relié à des fonctions Python pour effectuer des actions réelles.
