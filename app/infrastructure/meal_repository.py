from typing import List, Optional

from app.domain.entities import Meal, Category, Area, Ingredient
from app.domain.repositories import MealRepository
from app.infrastructure.meal_api_client import MealApiClient


class ApiMealRepository(MealRepository):
    def __init__(self, api_client: MealApiClient):
        self.api_client = api_client

    async def search_by_name(self, name: str) -> List[Meal]:
        return await self.api_client.search_by_name(name)

    async def search_by_first_letter(self, letter: str) -> List[Meal]:
        return await self.api_client.search_by_first_letter(letter)

    async def get_by_id(self, meal_id: str) -> Optional[Meal]:
        return await self.api_client.get_by_id(meal_id)

    async def get_random(self) -> Optional[Meal]:
        return await self.api_client.get_random()

    async def get_categories(self) -> List[Category]:
        return await self.api_client.get_categories()

    async def get_areas(self) -> List[Area]:
        return await self.api_client.get_areas()

    async def get_ingredients(self) -> List[Ingredient]:
        return await self.api_client.get_ingredients()

    async def filter_by_ingredient(self, ingredient: str) -> List[Meal]:
        return await self.api_client.filter_by_ingredient(ingredient)

    async def filter_by_category(self, category: str) -> List[Meal]:
        return await self.api_client.filter_by_category(category)

    async def filter_by_area(self, area: str) -> List[Meal]:
        return await self.api_client.filter_by_area(area)

    async def list_by_letter(self, letter: str) -> List[Meal]:
        return await self.api_client.search_by_first_letter(letter)
