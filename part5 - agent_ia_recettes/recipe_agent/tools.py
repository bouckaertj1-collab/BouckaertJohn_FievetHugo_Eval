from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any

VALID_DIFFICULTIES = {"facile", "moyen", "difficile"}
VALID_CATEGORIES = {"entree", "plat", "dessert", "autre"}


def _recipes_file() -> Path:
    """Retourne le fichier JSON utilisé pour stocker les recettes."""
    return Path(os.environ.get("RECIPES_FILE", "recipes.json"))


def _load_recipes() -> list[dict[str, Any]]:
    """Charge les recettes depuis le fichier JSON."""
    path = _recipes_file()
    if not path.exists():
        return []
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def _save_recipes(recipes: list[dict[str, Any]]) -> None:
    """Sauvegarde les recettes dans le fichier JSON."""
    path = _recipes_file()
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as f:
        json.dump(recipes, f, indent=2, ensure_ascii=False)


def _next_id(recipes: list[dict[str, Any]]) -> int:
    """Calcule le prochain identifiant disponible."""
    if not recipes:
        return 1
    return max(recipe.get("id", 0) for recipe in recipes) + 1


def _normalise_text(value: str) -> str:
    """Normalise un texte pour les comparaisons simples."""
    return value.strip().lower()


def add_recipe(
    name: str,
    ingredients: list[str],
    instructions: str,
    difficulty: str = "facile",
    time_minutes: int = 30,
    category: str = "plat",
) -> str:
    """Ajoute une recette dans la base locale.

    Args:
        name: Nom de la recette.
        ingredients: Liste des ingrédients nécessaires.
        instructions: Étapes de préparation.
        difficulty: Difficulté de la recette : facile, moyen ou difficile.
        time_minutes: Temps de préparation estimé en minutes.
        category: Catégorie : entree, plat, dessert ou autre.

    Returns:
        Message de confirmation ou message d'erreur.
    """
    name = name.strip()
    difficulty = _normalise_text(difficulty)
    category = _normalise_text(category)

    if not name:
        return "Erreur : le nom de la recette est obligatoire."
    if difficulty not in VALID_DIFFICULTIES:
        return "Erreur : difficulté invalide. Valeurs acceptées : facile, moyen, difficile."
    if category not in VALID_CATEGORIES:
        return "Erreur : catégorie invalide. Valeurs acceptées : entree, plat, dessert, autre."
    if time_minutes <= 0:
        return "Erreur : le temps de préparation doit être positif."
    if not ingredients:
        return "Erreur : au moins un ingrédient est nécessaire."

    cleaned_ingredients = [_normalise_text(i) for i in ingredients if i.strip()]
    if not cleaned_ingredients:
        return "Erreur : au moins un ingrédient valide est nécessaire."

    recipes = _load_recipes()
    if any(_normalise_text(recipe.get("name", "")) == _normalise_text(name) for recipe in recipes):
        return f"Erreur : la recette '{name}' existe déjà."

    recipe = {
        "id": _next_id(recipes),
        "name": name,
        "category": category,
        "difficulty": difficulty,
        "time_minutes": int(time_minutes),
        "ingredients": cleaned_ingredients,
        "instructions": instructions.strip(),
    }
    recipes.append(recipe)
    _save_recipes(recipes)
    return f"Recette ajoutée : '{name}' (id: {recipe['id']}, {category}, {difficulty}, {time_minutes} min)."


def list_recipes(category: str = "all", difficulty: str = "all") -> str:
    """Liste les recettes enregistrées, avec filtres optionnels.

    Args:
        category: Catégorie à filtrer ou all.
        difficulty: Difficulté à filtrer ou all.

    Returns:
        Liste formatée des recettes.
    """
    recipes = _load_recipes()
    if not recipes:
        return "Aucune recette enregistrée."

    category = _normalise_text(category)
    difficulty = _normalise_text(difficulty)

    if category != "all":
        recipes = [r for r in recipes if _normalise_text(r.get("category", "")) == category]
    if difficulty != "all":
        recipes = [r for r in recipes if _normalise_text(r.get("difficulty", "")) == difficulty]

    if not recipes:
        return "Aucune recette ne correspond aux filtres demandés."

    lines = []
    for recipe in recipes:
        ingredients = ", ".join(recipe.get("ingredients", []))
        lines.append(
            f"[{recipe['id']}] {recipe['name']} - {recipe.get('category', 'autre')} - "
            f"{recipe.get('difficulty', 'n/a')} - {recipe.get('time_minutes', '?')} min | ingrédients : {ingredients}"
        )
    return "\n".join(lines)


def search_recipes_by_ingredient(ingredient: str) -> str:
    """Recherche les recettes qui contiennent un ingrédient.

    Args:
        ingredient: Ingrédient recherché.

    Returns:
        Recettes correspondantes ou message si aucune recette ne correspond.
    """
    ingredient = _normalise_text(ingredient)
    recipes = _load_recipes()
    matches = []

    for recipe in recipes:
        recipe_ingredients = [_normalise_text(i) for i in recipe.get("ingredients", [])]
        if any(ingredient in i or i in ingredient for i in recipe_ingredients):
            matches.append(recipe)

    if not matches:
        return f"Aucune recette contenant '{ingredient}' n'a été trouvée."

    lines = [f"Recettes contenant '{ingredient}' :"]
    for recipe in matches:
        lines.append(f"- [{recipe['id']}] {recipe['name']} ({recipe['time_minutes']} min, {recipe['difficulty']})")
    return "\n".join(lines)


def suggest_recipe(available_ingredients: list[str], max_time_minutes: int = 60) -> str:
    """Suggère une recette selon les ingrédients disponibles et le temps maximum.

    Args:
        available_ingredients: Ingrédients disponibles chez l'utilisateur.
        max_time_minutes: Temps maximum de préparation souhaité.

    Returns:
        Suggestion de recette ou message si aucune recette n'est adaptée.
    """
    available = {_normalise_text(i) for i in available_ingredients if i.strip()}
    recipes = [r for r in _load_recipes() if r.get("time_minutes", 9999) <= max_time_minutes]

    if not available:
        return "Erreur : indique au moins un ingrédient disponible."
    if not recipes:
        return "Aucune recette ne respecte le temps maximum indiqué."

    best_recipe = None
    best_score = -1
    best_used: set[str] = set()
    best_missing: set[str] = set()

    for recipe in recipes:
        required = {_normalise_text(i) for i in recipe.get("ingredients", [])}
        used = required & available
        missing = required - available
        score = len(used) * 2 - len(missing)
        if score > best_score:
            best_recipe = recipe
            best_score = score
            best_used = used
            best_missing = missing

    if best_recipe is None or not best_used:
        return "Aucune recette pertinente trouvée avec les ingrédients disponibles."

    used_text = ", ".join(sorted(best_used)) if best_used else "aucun"
    missing_text = ", ".join(sorted(best_missing)) if best_missing else "aucun"
    return (
        f"Suggestion : {best_recipe['name']} (id: {best_recipe['id']}).\n"
        f"Ingrédients disponibles utilisés : {used_text}.\n"
        f"Ingrédients manquants : {missing_text}.\n"
        f"Temps estimé : {best_recipe['time_minutes']} min. Difficulté : {best_recipe['difficulty']}."
    )


def generate_shopping_list(
    recipe_id: int | None = None,
    available_ingredients: list[str] | None = None,
    recipe_name: str | None = None
) -> str:
    """Génère la liste de courses pour une recette.

    Args:
        recipe_id: Identifiant de la recette. Optionnel si recipe_name est fourni.
        available_ingredients: Ingrédients déjà disponibles chez l'utilisateur.
        recipe_name: Nom de la recette. Optionnel si recipe_id est fourni.

    Returns:
        Liste des ingrédients manquants pour préparer la recette.
    """
    available_ingredients = available_ingredients or []
    available = {_normalise_text(i) for i in available_ingredients if i.strip()}

    recipes = _load_recipes()
    recipe = None

    if recipe_id is not None:
        recipe = next((r for r in recipes if r.get("id") == recipe_id), None)

    elif recipe_name is not None:
        normalized_name = _normalise_text(recipe_name)
        recipe = next(
            (
                r for r in recipes
                if _normalise_text(r.get("name", "")) == normalized_name
            ),
            None
        )

    else:
        return "Erreur : veuillez fournir l'id ou le nom de la recette."

    if recipe is None:
        return "Erreur : aucune recette correspondante trouvée."

    required = {_normalise_text(i) for i in recipe.get("ingredients", [])}
    missing = sorted(required - available)

    if not missing:
        return f"Aucun achat nécessaire pour '{recipe['name']}'."

    lines = [f"Liste de courses pour '{recipe['name']}' :"]
    lines.extend(f"- {ingredient}" for ingredient in missing)
    return "\n".join(lines)

def delete_recipe(recipe_id: int) -> str:
    """Supprime une recette à partir de son identifiant.

    Args:
        recipe_id: Identifiant de la recette à supprimer.

    Returns:
        Message de confirmation ou message d'erreur.
    """
    recipes = _load_recipes()
    for index, recipe in enumerate(recipes):
        if recipe.get("id") == recipe_id:
            removed = recipes.pop(index)
            _save_recipes(recipes)
            return f"Recette supprimée : '{removed['name']}' (id: {recipe_id})."
    return f"Erreur : aucune recette trouvée avec l'id {recipe_id}."

def delete_recipe_by_name(recipe_name: str) -> str:
    """Supprime une recette à partir de son nom.

    Args:
        recipe_name: Nom de la recette à supprimer.

    Returns:
        Message de confirmation ou message d'erreur.
    """
    recipes = _load_recipes()
    recipe_name_clean = recipe_name.strip().lower()

    for index, recipe in enumerate(recipes):
        current_name = recipe.get("name", "").strip().lower()

        if current_name == recipe_name_clean:
            removed = recipes.pop(index)
            _save_recipes(recipes)
            return f"Recette supprimée : '{removed['name']}'."

    return f"Erreur : aucune recette trouvée avec le nom '{recipe_name}'."