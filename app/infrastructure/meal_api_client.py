import httpx
from typing import List, Optional
from app.domain.entities import Meal, Category, Area, Ingredient

BASE_URL = "https://www.themealdb.com/api/json/v1/1"


class MealApiClient:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
        self.timeout = 10.0

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
                name=c.get("strCategory"),
                thumbnail_url=c.get("strCategoryThumb"),
                description=c.get("strCategoryDescription", ""),
            )
            for c in categories
        ]

    async def get_areas(self) -> List[Area]:
        data = await self._get("list.php", {"a": "list"})
        areas = data.get("meals")
        if not areas:
            return []
        return [Area(name=a.get("strArea")) for a in areas]

    async def get_ingredients(self) -> List[Ingredient]:
        data = await self._get("list.php", {"i": "list"})
        ingredients = data.get("meals")
        if not ingredients:
            return []
        return [
            Ingredient(
                id=str(i.get("idIngredient")),
                name=i.get("strIngredient"),
                description=i.get("strDescription", ""),
                type=i.get("strType", ""),
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
        ingredients = []
        measures = []
        for i in range(1, 21):
            ingredient = data.get(f"strIngredient{i}")
            measure = data.get(f"strMeasure{i}")
            if ingredient:
                ingredients.append(ingredient)
            if measure:
                measures.append(measure)

        image_url = data.get("strMealThumb")
        if image_url:
            image_url = image_url + "/preview"

        return Meal(
            id=str(data.get("idMeal")),
            name=data.get("strMeal"),
            alternate_name=data.get("strAlternate"),
            category=data.get("strCategory"),
            area=data.get("strArea"),
            instructions=data.get("strInstructions"),
            image_url=data.get("strMealThumb"),
            video_url=data.get("strYoutube"),
            tags=data.get("strTags"),
            youtube_url=data.get("strYoutube"),
            ingredients=ingredients,
            measures=measures,
            source=data.get("strSource"),
        )

    def _map_meal_filtered(self, data: dict) -> Meal:
        return Meal(
            id=str(data.get("idMeal")),
            name=data.get("strMeal"),
            image_url=data.get("strMealThumb"),
            category=data.get("strCategory"),
            area=data.get("strArea"),
        )
