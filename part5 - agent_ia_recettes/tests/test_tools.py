import json
import os

import pytest

from recipe_agent.tools import (
    add_recipe,
    delete_recipe,
    generate_shopping_list,
    list_recipes,
    search_recipes_by_ingredient,
    suggest_recipe,
)


@pytest.fixture(autouse=True)
def temporary_recipes_file(tmp_path, monkeypatch):
    """Utilise un fichier JSON temporaire pour chaque test."""
    recipes_file = tmp_path / "recipes_test.json"
    monkeypatch.setenv("RECIPES_FILE", str(recipes_file))
    recipes_file.write_text("[]", encoding="utf-8")
    yield recipes_file


def test_add_recipe_creates_recipe(temporary_recipes_file):
    result = add_recipe(
        name="Soupe de légumes",
        ingredients=["carotte", "poireau", "pomme de terre"],
        instructions="Cuire les légumes puis mixer.",
        difficulty="facile",
        time_minutes=35,
        category="plat",
    )

    assert "Recette ajoutée" in result
    data = json.loads(temporary_recipes_file.read_text(encoding="utf-8"))
    assert len(data) == 1
    assert data[0]["name"] == "Soupe de légumes"


def test_add_recipe_rejects_invalid_difficulty():
    result = add_recipe(
        name="Recette test",
        ingredients=["test"],
        instructions="Tester.",
        difficulty="impossible",
        time_minutes=10,
        category="plat",
    )
    assert "Erreur" in result


def test_add_recipe_rejects_duplicate_name():
    add_recipe("Omelette", ["oeufs"], "Cuire.", "facile", 10, "plat")
    result = add_recipe("Omelette", ["oeufs"], "Cuire.", "facile", 10, "plat")
    assert "existe déjà" in result


def test_list_recipes_with_filters():
    add_recipe("Omelette", ["oeufs"], "Cuire.", "facile", 10, "plat")
    add_recipe("Crêpes", ["farine", "lait"], "Mélanger.", "facile", 30, "dessert")

    result = list_recipes(category="dessert")
    assert "Crêpes" in result
    assert "Omelette" not in result


def test_search_recipes_by_ingredient():
    add_recipe("Pâtes tomate", ["pâtes", "tomate"], "Cuire.", "facile", 20, "plat")
    add_recipe("Omelette", ["oeufs", "fromage"], "Cuire.", "facile", 10, "plat")

    result = search_recipes_by_ingredient("tomate")
    assert "Pâtes tomate" in result
    assert "Omelette" not in result


def test_suggest_recipe_uses_available_ingredients():
    add_recipe("Omelette", ["oeufs", "fromage", "beurre"], "Cuire.", "facile", 10, "plat")
    add_recipe("Pâtes tomate", ["pâtes", "tomate", "ail"], "Cuire.", "facile", 25, "plat")

    result = suggest_recipe(["oeufs", "fromage"], max_time_minutes=15)
    assert "Omelette" in result


def test_generate_shopping_list_returns_missing_items():
    add_recipe("Pâtes tomate", ["pâtes", "tomate", "ail"], "Cuire.", "facile", 25, "plat")

    result = generate_shopping_list(1, ["pâtes"])
    assert "tomate" in result
    assert "ail" in result
    assert all("pâtes" not in line for line in result.splitlines()[1:])


def test_delete_recipe_removes_recipe():
    add_recipe("Omelette", ["oeufs"], "Cuire.", "facile", 10, "plat")
    result = delete_recipe(1)

    assert "supprimée" in result
    assert "Aucune recette" in list_recipes()


def test_delete_recipe_unknown_id():
    result = delete_recipe(999)
    assert "Erreur" in result
