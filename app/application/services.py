from typing import List, Optional

from app.domain.entities import Meal, Category, Area, Ingredient
from app.domain.repositories import MealRepository


class MealService:
    def __init__(self, meal_repository: MealRepository):
        self.meal_repository = meal_repository

    def search_meals(self, query: str) -> List[Meal]:
        return self.meal_repository.search_by_name(query)

    def list_by_letter(self, letter: str) -> List[Meal]:
        return self.meal_repository.list_by_letter(letter)

    def get_meal_detail(self, meal_id: str) -> Optional[Meal]:
        return self.meal_repository.get_by_id(meal_id)

    def get_random_meal(self) -> Optional[Meal]:
        return self.meal_repository.get_random()

    def get_categories(self) -> List[Category]:
        return self.meal_repository.get_categories()

    def get_areas(self) -> List[Area]:
        return self.meal_repository.get_areas()

    def get_ingredients(self) -> List[Ingredient]:
        return self.meal_repository.get_ingredients()

    def filter_by_ingredient(self, ingredient: str) -> List[Meal]:
        return self.meal_repository.filter_by_ingredient(ingredient)

    def filter_by_category(self, category: str) -> List[Meal]:
        return self.meal_repository.filter_by_category(category)

    def filter_by_area(self, area: str) -> List[Meal]:
        return self.meal_repository.filter_by_area(area)

    def list_all_starting_with(self, letter: str) -> List[Meal]:
        return self.meal_repository.list_by_letter(letter)
