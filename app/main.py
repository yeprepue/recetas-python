from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from app.presentation.controllers import router

app = FastAPI(
    title="Recetario Python", 
    description="App de recetas con arquitectura hexagonal"
)

# Configurar CORS (necesario para producción)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Incluir rutas
app.include_router(router)

@app.get("/health")
async def health():
    return {"status": "ok", "version": "1.0.0"}