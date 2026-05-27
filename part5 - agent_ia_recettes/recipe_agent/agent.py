from __future__ import annotations

import os

from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

from .tools import (
    add_recipe,
    delete_recipe,
    delete_recipe_by_name,
    generate_shopping_list,
    list_recipes,
    search_recipes_by_ingredient,
    suggest_recipe,
)

MODEL_ID = os.environ.get("MODEL_ID", "ollama_chat/qwen3:4b")

SYSTEM_PROMPT = """Tu es un assistant de gestion de recettes.

Règles :
- Utilise toujours les outils disponibles pour ajouter, rechercher, lister ou supprimer des recettes.
- Lorsque l'utilisateur demande une recette existante, utilise les outils pour consulter les données disponibles au lieu d'inventer une réponse.
- Avant d'ajouter une recette, vérifie avec les outils qu'une recette portant le même nom n'existe pas déjà.
- Après l'ajout réussi d'une recette avec add_recipe, confirme brièvement l'ajout.
- Après cette confirmation, propose 1 ou 2 idées de recettes similaires, variantes ou accompagnements que l'utilisateur pourrait vouloir ajouter.
- Ces suggestions doivent être générées par le LLM à partir du contexte.
- N'ajoute jamais automatiquement les suggestions : demande toujours confirmation à l'utilisateur.
- Si la demande ne concerne pas les recettes, indique poliment que tu ne peux pas aider.
"""

root_agent = Agent(
    name="recipe_agent",
    model=LiteLlm(model=MODEL_ID),
    description="Agent IA basique pour gérer et proposer des recettes",
    instruction=SYSTEM_PROMPT,
    tools=[
        add_recipe,
        list_recipes,
        search_recipes_by_ingredient,
        suggest_recipe,
        generate_shopping_list,
        delete_recipe,
        delete_recipe_by_name,
    ],
)
