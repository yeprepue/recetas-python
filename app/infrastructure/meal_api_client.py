import httpx
import re
from typing import List, Optional
from app.domain.entities import Meal, Category, Area, Ingredient
from app.i18n.content_translator import ContentTranslator

BASE_URL = "https://www.themealdb.com/api/json/v1/1"


class MealApiClient:
    def __init__(self, base_url: str = BASE_URL, target_language: str = "es"):
        self.base_url = base_url
        self.timeout = 10.0
        self.translator = ContentTranslator(target_language)

    async def _get(self, path: str, params: dict = None) -> dict:
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.get(f"{self.base_url}/{path}", params=params)
            response.raise_for_status()
            return response.json()

    async def search_by_name(self, name: str) -> List[Meal]:
        data = await self._get("search.php", {"s": name})
        meals = data.get("meals")
        if not meals:
            return []
        return [self._map_meal(m) for m in meals]

    async def search_by_first_letter(self, letter: str) -> List[Meal]:
        data = await self._get("search.php", {"f": letter})
        meals = data.get("meals")
        if not meals:
            return []
        return [self._map_meal(m) for m in meals]

    async def get_by_id(self, meal_id: str) -> Optional[Meal]:
        data = await self._get("lookup.php", {"i": meal_id})
        meals = data.get("meals")
        if not meals:
            return None
        return self._map_meal(meals[0])

    async def get_random(self) -> Optional[Meal]:
        data = await self._get("random.php")
        meals = data.get("meals")
        if not meals:
            return None
        return self._map_meal(meals[0])

    async def get_categories(self) -> List[Category]:
        data = await self._get("categories.php")
        categories = data.get("categories")
        if not categories:
            return []
        return [
            Category(
                id=str(c.get("idCategory")),
                name=self.translator.translate(c.get("strCategory")),
                thumbnail_url=c.get("strCategoryThumb"),
                description=self.translator.translate(c.get("strCategoryDescription", "")),
            )
            for c in categories
        ]

    async def get_areas(self) -> List[Area]:
        data = await self._get("list.php", {"a": "list"})
        areas = data.get("meals")
        if not areas:
            return []
        return [Area(name=self.translator.translate(a.get("strArea"))) for a in areas]

    async def get_ingredients(self) -> List[Ingredient]:
        data = await self._get("list.php", {"i": "list"})
        ingredients = data.get("meals")
        if not ingredients:
            return []
        return [
            Ingredient(
                id=str(i.get("idIngredient")),
                name=self.translator.translate(i.get("strIngredient")),
                description=self.translator.translate(i.get("strDescription", "")),
                type=self.translator.translate(i.get("strType", "")),
            )
            for i in ingredients
        ]

    async def filter_by_ingredient(self, ingredient: str) -> List[Meal]:
        data = await self._get("filter.php", {"i": ingredient})
        meals = data.get("meals")
        if not meals:
            return []
        return [self._map_meal_filtered(m) for m in meals]

    async def filter_by_category(self, category: str) -> List[Meal]:
        data = await self._get("filter.php", {"c": category})
        meals = data.get("meals")
        if not meals:
            return []
        return [self._map_meal_filtered(m) for m in meals]

    async def filter_by_area(self, area: str) -> List[Meal]:
        data = await self._get("filter.php", {"a": area})
        meals = data.get("meals")
        if not meals:
            return []
        return [self._map_meal_filtered(m) for m in meals]

    def _map_meal(self, data: dict) -> Meal:
        ingredient_measures = []
        for i in range(1, 21):
            ingredient = data.get(f"strIngredient{i}")
            measure = data.get(f"strMeasure{i}")
            if ingredient:
                translated_ing = self.translator.translate(ingredient)
                translated_measure = self.translator.translate(measure) if measure else ""
                ingredient_measures.append((translated_ing, translated_measure))

        youtube_url = data.get("strYoutube")
        youtube_video_id = None
        if youtube_url:
            match = re.search(r"(?:v=|\/)([0-9A-Za-z_-]{11})", youtube_url)
            if match:
                youtube_video_id = match.group(1)

        return Meal(
            id=str(data.get("idMeal")),
            name=self.translator.translate(data.get("strMeal")),
            alternate_name=self.translator.translate(data.get("strAlternate")),
            category=self.translator.translate(data.get("strCategory")),
            area=self.translator.translate(data.get("strArea")),
            instructions=self.translator.translate(data.get("strInstructions")),
            image_url=data.get("strMealThumb"),
            video_url=data.get("strYoutube"),
            tags=data.get("strTags"),
            youtube_url=youtube_url,
            ingredients=[],
            measures=[],
            source=data.get("strSource"),
            ingredient_measures=ingredient_measures,
            youtube_video_id=youtube_video_id,
        )

    def _map_meal_filtered(self, data: dict) -> Meal:
        return Meal(
            id=str(data.get("idMeal")),
            name=self.translator.translate(data.get("strMeal")),
            image_url=data.get("strMealThumb"),
            category=self.translator.translate(data.get("strCategory")),
            area=self.translator.translate(data.get("strArea")),
        )
