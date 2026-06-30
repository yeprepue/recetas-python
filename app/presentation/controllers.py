from fastapi import APIRouter, Request, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from typing import Optional

from app.domain.repositories import MealRepository
from app.application.services import MealService
from app.infrastructure.meal_repository import ApiMealRepository
from app.infrastructure.meal_api_client import MealApiClient
from app.i18n.translator import Translator

router = APIRouter()
templates = Jinja2Templates(directory="templates")


def get_language(request: Request) -> str:
    return request.cookies.get("language", "es")


def get_translator(request: Request) -> Translator:
    lang = get_language(request)
    return Translator(language=lang)


def get_meal_service_from_request(request: Request) -> MealService:
    lang = request.cookies.get("language", "es")
    api_client = MealApiClient(target_language=lang)
    repository = ApiMealRepository(api_client)
    return MealService(repository)


@router.get("/", response_class=HTMLResponse)
async def index(request: Request, service: MealService = Depends(get_meal_service_from_request), translator: Translator = Depends(get_translator)):
    random_meal = await service.get_random_meal()
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "random_meal": random_meal, "t": translator},
    )


@router.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str = "", service: MealService = Depends(get_meal_service_from_request), translator: Translator = Depends(get_translator)):
    meals = []
    if q:
        meals = await service.search_meals(q)
    return templates.TemplateResponse(
        "search.html",
        {"request": request, "meals": meals, "query": q, "t": translator},
    )


@router.get("/meal/{meal_id}", response_class=HTMLResponse)
async def meal_detail(
    request: Request,
    meal_id: str,
    service: MealService = Depends(get_meal_service_from_request),
    translator: Translator = Depends(get_translator),
):
    meal = await service.get_meal_detail(meal_id)
    if not meal:
        return templates.TemplateResponse(
            "not_found.html",
            {"request": request, "message": translator.t("meal_not_found"), "t": translator},
        )
    return templates.TemplateResponse(
        "meal_detail.html",
        {"request": request, "meal": meal, "t": translator},
    )


@router.get("/categories", response_class=HTMLResponse)
async def categories(request: Request, service: MealService = Depends(get_meal_service_from_request), translator: Translator = Depends(get_translator)):
    categories = await service.get_categories()
    return templates.TemplateResponse(
        "categories.html",
        {"request": request, "categories": categories, "t": translator},
    )


@router.get("/category/{category_name}", response_class=HTMLResponse)
async def category_filter(
    request: Request,
    category_name: str,
    service: MealService = Depends(get_meal_service_from_request),
    translator: Translator = Depends(get_translator),
):
    meals = await service.filter_by_category(category_name)
    return templates.TemplateResponse(
        "search.html",
        {"request": request, "meals": meals, "query": f"{translator.t('category')}: {category_name}", "t": translator},
    )


@router.get("/areas", response_class=HTMLResponse)
async def areas(request: Request, service: MealService = Depends(get_meal_service_from_request), translator: Translator = Depends(get_translator)):
    areas = await service.get_areas()
    return templates.TemplateResponse(
        "areas.html",
        {"request": request, "areas": areas, "t": translator},
    )


@router.get("/area/{area_name}", response_class=HTMLResponse)
async def area_filter(
    request: Request,
    area_name: str,
    service: MealService = Depends(get_meal_service_from_request),
    translator: Translator = Depends(get_translator),
):
    meals = await service.filter_by_area(area_name)
    return templates.TemplateResponse(
        "search.html",
        {"request": request, "meals": meals, "query": f"{translator.t('area')}: {area_name}", "t": translator},
    )


@router.get("/ingredients", response_class=HTMLResponse)
async def ingredients(request: Request, service: MealService = Depends(get_meal_service_from_request), translator: Translator = Depends(get_translator)):
    ingredients = await service.get_ingredients()
    return templates.TemplateResponse(
        "ingredients.html",
        {"request": request, "ingredients": ingredients, "t": translator},
    )


@router.get("/ingredient/{ingredient_name}", response_class=HTMLResponse)
async def ingredient_filter(
    request: Request,
    ingredient_name: str,
    service: MealService = Depends(get_meal_service_from_request),
    translator: Translator = Depends(get_translator),
):
    meals = await service.filter_by_ingredient(ingredient_name)
    return templates.TemplateResponse(
        "search.html",
        {"request": request, "meals": meals, "query": f"{translator.t('ingredients_title')}: {ingredient_name}", "t": translator},
    )


@router.get("/letter/{letter}", response_class=HTMLResponse)
async def list_by_letter(
    request: Request,
    letter: str,
    service: MealService = Depends(get_meal_service_from_request),
    translator: Translator = Depends(get_translator),
):
    meals = await service.list_all_starting_with(letter)
    return templates.TemplateResponse(
        "search.html",
        {"request": request, "meals": meals, "query": f"{translator.t('search')} {letter}", "t": translator},
    )


@router.get("/set-language/{lang}", response_class=RedirectResponse)
async def set_language(request: Request, lang: str):
    supported = ["es", "en", "fr", "zh"]
    if lang not in supported:
        lang = "es"
    response = RedirectResponse(url=request.headers.get("referer", "/"))
    response.set_cookie(key="language", value=lang, max_age=365 * 24 * 60 * 60, httponly=False)
    return response
