from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from app.presentation.controllers import router

app = FastAPI(title="Recetario Python", description="App de recetas con arquitectura hexagonal")

app.mount("/static", StaticFiles(directory="static"), name="static")

app.include_router(router)


@app.get("/health")
async def health():
    return {"status": "ok"}
