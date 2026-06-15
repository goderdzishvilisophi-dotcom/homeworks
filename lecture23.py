import json
import requests
from pydantic import BaseModel, ValidationError
from requests.exceptions import HTTPError, ConnectTimeout


API_URL = "https://crudcrud.com/api/66f30b5b34f34d9d822f24bd79509aea/recipes"

class Recipe(BaseModel):
    name: str
    cuisine: str
    time_minutes: str
try:
    with open("recipes.json", "r", encoding="utf-8") as file:
        recipes_data = json.load(file)

    for item in recipes_data:
        recipe = Recipe(**item)
        response = requests.post(
            API_URL,
            json=recipe.model_dump(),
            timeout=5
        )
        response.raise_for_status()

    print("All recipes uploaded successfully")
except ValidationError as e:
    print(" Validation Error:", e)
except HTTPError as e:
    print(" HTTP Error:", e)
except ConnectTimeout:
    print("Connection timeout")
try:
    response = requests.get(API_URL, timeout=5)
    response.raise_for_status()

    recipes = response.json()

    print("\nAll Recipes:")
    for recipe in recipes:
        print(f"{recipe['name']} - {recipe['time_minutes']} min")

except HTTPError as e:
    print("HTTP Error:", e)
except ConnectTimeout:
    print("Connection timeout")

try:
    response = requests.get(API_URL, timeout=5)
    response.raise_for_status()
    recipes = response.json()

    if recipes:
        first_id = recipes[0]["_id"]

        response = requests.get(
            f"{API_URL}/{first_id}",
            timeout=5
        )
        response.raise_for_status()

        print("\nSingle Recipe:")
        print(response.json())
except HTTPError as e:
    print("HTTP Error:", e)
except ConnectTimeout:
    print("Connection timeout")

try:
    response = requests.get(API_URL, timeout=5)
    response.raise_for_status()
    recipes = response.json()

    if recipes:
        recipe_id = recipes[0]["_id"]

        updated_recipe = {
            "name": "Updated Khachapuri",
            "cuisine": "Georgian",
            "time_minutes": "40"
        }
        response = requests.put(
            f"{API_URL}/{recipe_id}",
            json=updated_recipe,
            timeout=5
        )
        response.raise_for_status()

        with open("updated_recipe.json", "w", encoding="utf-8") as file:
            json.dump(updated_recipe, file, ensure_ascii=False, indent=4)

        print("\nRecipe updated successfully")

except HTTPError as e:
    print("HTTP Error:", e)

except ConnectTimeout:
    print("Connection timeout")

try:
    response = requests.get(API_URL, timeout=5)
    response.raise_for_status()
    recipes = response.json()

    if recipes:
        last_id = recipes[-1]["_id"]

        response = requests.delete(f"{API_URL}/{last_id}", timeout=5)
        response.raise_for_status()

        print("\nRecipe deleted successfully")

        response = requests.get(API_URL, timeout=5)
        response.raise_for_status()

        print("\nRemaining Recipes:")
        for recipe in response.json():
            print(f"{recipe['name']} - {recipe['time_minutes']} min")

except HTTPError as e:
    print("HTTP Error:", e)
except ConnectTimeout:
    print("Connection timeout")

