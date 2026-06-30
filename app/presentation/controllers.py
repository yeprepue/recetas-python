from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List

from app.domain.repositories import MealRepository
from app.application.services import MealService
from app.infrastructure.meal_repository import ApiMealRepository
from app.infrastructure.meal_api_client import MealApiClient

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def get_meal_service() -> MealService:
    api_client = MealApiClient()
    repository = ApiMealRepository(api_client)
    return MealService(repository)


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, service: MealService = Depends(get_meal_service)):
    random_meal = await service.get_random_meal()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "random_meal": random_meal},
    )


@router.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str = "", service: MealService = Depends(get_meal_service)):
    meals = []
    if q:
        meals = await service.search_meals(q)
    return templates.TemplateResponse(
        "search.html",
        {"request": request, "meals": meals, "query": q},
    )


@router.get("/meal/{meal_id}", response_class=HTMLResponse)
async def meal_detail(
    request: Request,
    meal_id: str,
    service: MealService = Depends(get_meal_service),
):
    meal = await service.get_meal_detail(meal_id)
    if not meal:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": "Comida no encontrada"},
        )
    return templates.TemplateResponse(
        "meal_detail.html",
        {"request": request, "meal": meal},
    )


@router.get("/categories", response_class=HTMLResponse)
async def categories(request: Request, service: MealService = Depends(get_meal_service)):
    categories = await service.get_categories()
    return templates.TemplateResponse(
        "categories.html",
        {"request": request, "categories": categories},
    )


@router.get("/category/{category_name}", response_class=HTMLResponse)
async def category_filter(
    request: Request,
    category_name: str,
    service: MealService = Depends(get_meal_service),
):
    meals = await service.filter_by_category(category_name)
    return templates.TemplateResponse(
        "search.html",
        {"request": request, "meals": meals, "query": f"Categoría: {category_name}"},
    )


@router.get("/areas", response_class=HTMLResponse)
async def areas(request: Request, service: MealService = Depends(get_meal_service)):
    areas = await service.get_areas()
    return templates.TemplateResponse(
        "areas.html",
        {"request": request, "areas": areas},
    )


@router.get("/area/{area_name}", response_class=HTMLResponse)
async def area_filter(
    request: Request,
    area_name: str,
    service: MealService = Depends(get_meal_service),
):
    meals = await service.filter_by_area(area_name)
    return templates.TemplateResponse(
        "search.html",
        {"request": request, "meals": meals, "query": f"Área: {area_name}"},
    )


@router.get("/ingredients", response_class=HTMLResponse)
async def ingredients(request: Request, service: MealService = Depends(get_meal_service)):
    ingredients = await service.get_ingredients()
    return templates.TemplateResponse(
        "ingredients.html",
        {"request": request, "ingredients": ingredients},
    )


@router.get("/ingredient/{ingredient_name}", response_class=HTMLResponse)
async def ingredient_filter(
    request: Request,
    ingredient_name: str,
    service: MealService = Depends(get_meal_service),
):
    meals = await service.filter_by_ingredient(ingredient_name)
    return templates.TemplateResponse(
        "search.html",
        {"request": request, "meals": meals, "query": f"Ingrediente: {ingredient_name}"},
    )


@router.get("/letter/{letter}", response_class=HTMLResponse)
async def list_by_letter(
    request: Request,
    letter: str,
    service: MealService = Depends(get_meal_service),
):
    meals = await service.list_all_starting_with(letter)
    return templates.TemplateResponse(
        "search.html",
        {"request": request, "meals": meals, "query": f"Comidas con la letra: {letter}"},
    )
