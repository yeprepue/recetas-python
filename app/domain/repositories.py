from abc import ABC, abstractmethod
from typing import List, Optional

from app.domain.entities import Meal, Category, Area, Ingredient


class MealRepository(ABC):
    @abstractmethod
    def search_by_name(self, name: str) -> List[Meal]:
        pass

    @abstractmethod
    def search_by_first_letter(self, letter: str) -> List[Meal]:
        pass

    @abstractmethod
    def get_by_id(self, meal_id: str) -> Optional[Meal]:
        pass

    @abstractmethod
    def get_random(self) -> Optional[Meal]:
        pass

    @abstractmethod
    def get_categories(self) -> List[Category]:
        pass

    @abstractmethod
    def get_areas(self) -> List[Area]:
        pass

    @abstractmethod
    def get_ingredients(self) -> List[Ingredient]:
        pass

    @abstractmethod
    def filter_by_ingredient(self, ingredient: str) -> List[Meal]:
        pass

    @abstractmethod
    def filter_by_category(self, category: str) -> List[Meal]:
        pass

    @abstractmethod
    def filter_by_area(self, area: str) -> List[Meal]:
        pass

    @abstractmethod
    def list_by_letter(self, letter: str) -> List[Meal]:
        pass
