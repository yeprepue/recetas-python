# Recetario Python

Aplicación web para buscar y explorar recetas de comida consumiendo [TheMealDB API](https://www.themealdb.com/api.php).

---

## Tabla de contenidos
- [Qué es Recetario Python](#qué-es-recetario-python)
- [Características](#características)
- [Casos de uso](#casos-de-uso)
- [Arquitectura](#arquitectura)
- [Requisitos previos](#requisitos-previos)
- [Instalación](#instalación)
- [Configuración](#configuración)
- [Ejecución en desarrollo](#ejecución-en-desarrollo)
- [Despliegue en producción](#despliegue-en-producción)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Mantenimiento y contribución](#mantenimiento-y-contribución)
- [URL](#URL)
---

## Qué es Recetario Python

Recetario Python es una app web responsiva que permite:

- Buscar recetas por nombre
- Filtrar por categoría, área geográfica o ingrediente
- Consultar el detalle completo de cualquier receta (ingredientes, medidas, instrucciones y video)
- Navegar por categorías, áreas e ingredientes
- Obtener recetas aleatorias

El frontend usa **Tailwind CSS** para adaptarse a móviles, tablets y escritorio.


##URL
```txt
https://recetas-python.onrender.com/
```

---

## Características

| Característica | Descripción |
|----------------|-------------|
| Búsqueda | Busca por nombre de comida |
| Filtros | Por categoría, área o ingrediente |
| Detalle | Ingredientes, medidas, instrucciones y video de YouTube |
| Responsivo | Diseño adaptable a cualquier dispositivo |
| Arquitectura hexagonal | Separación clara entre dominio, casos de uso y framework |

---

## Casos de uso

### Como usuario
1. **Buscar una receta**: Escribe el nombre (ej. `Arrabiata`, `Chicken`) en la barra de búsqueda.
2. **Explorar categorías**: Entra a `/categories` y elige una categoría para ver sus recetas.
3. **Explorar áreas**: Entra a `/areas` y filtra por país o región.
4. **Explorar ingredientes**: Entra a `/ingredients` y filtra por un ingrediente principal.
5. **Ver receta aleatoria**: En la página inicial (`/`) se muestra una receta aleatoria.
6. **Ver detalle**: En cualquier lista de resultados, haz clic en la tarjeta para ver ingredientes e instrucciones.

### Como desarrollador
1. **Consumir la API interna**: Los endpoints HTML también exponen datos JSON si necesitas integrarlos.
2. **Agregar un endpoint nuevo**: Crea el método en `MealRepository`, implementa la llamada en `MealApiClient`, define el caso de uso en `MealService` y crea la ruta en `controllers.py`.
3. **Cambiar el provedor de datos**: Reemplaza `MealApiClient` por otro adaptador sin tocar el dominio.

---

## Arquitectura

El proyecto sigue **arquitectura hexagonal (puertos y adaptadores)**:

```
app/
├─ domain/                   # Núcleo: entidades y contratos (sin dependencias externas)
│  ├─ entities.py
│  └─ repositories.py
├─ application/              # Casos de uso (lógica de negocio)
│  └─ services.py
├─ infrastructure/           # Adaptadores: APIs externas, persistencia, etc.
│  ├─ meal_api_client.py
│  └─ meal_repository.py
├─ presentation/             # Controladores y rutas (FastAPI + Jinja2)
│  └─ controllers.py
└─ main.py                   # Punto de entrada
```

- **Dominio**: Define `Meal`, `Category`, etc. y la interfaz `MealRepository`.
- **Aplicación**: Orquesta las operaciones sin saber de HTTP.
- **Infraestructura**: Implementa `MealRepository` consumiendo TheMealDB.
- **Presentación**: Recibe la petición HTTP y devuelve la respuesta.

---

## Requisitos previos

- Python 3.11 o superior
- Conda o Pipenv para entornos virtuales
- Navegador web moderno

---

## Instalación

### Opción 1: Conda (recomendado)

```bash
conda create -n recetario python=3.11 -y
conda activate recetario
```

### Opción 2: Venv con Pip

```bash
python -m venv venv
source venv/bin/activate   # En Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Instala las dependencias:

```bash
pip install -r requirements.txt
```

---

## Configuración

No requiere variables de entorno. La URL base de TheMealDB está definida en:

```python
# app/infrastructure/meal_api_client.py
BASE_URL = "https://www.themealdb.com/api/json/v1/1"
```

Si necesitas cambiar el puerto o el host, modifica `run.py`:

```python
uvicorn.run("app.main:app", host="0.0.0.0", port=8000)
```

---

## Ejecución en desarrollo

```bash
conda activate recetario
python run.py
```

Abre tu navegador en `http://localhost:8000`.

### Pruebas rápidas

| Acción | URL |
|--------|-----|
| Inicio | `/` |
| Buscar Arrabiata | `/search?q=Arrabiata` |
| Categorías | `/categories` |
| Áreas | `/areas` |
| Ingredientes | `/ingredients` |
| Health check | `/health` |

---

## Despliegue en producción

### Opción 1: Uvicorn + Nginx (recomendado)

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

Configura Nginx como proxy reverso apuntando a `http://127.0.0.1:8000` y sirve los archivos estáticos.

### Opción 2: Docker

Crea un `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Construye y ejecuta:

```bash
docker build -t recetario .
docker run -p 8000:8000 recetario
```

### Opción 3: Servidor HTML + FastAPI separado

Ejecuta la app en el puerto 8000 y sirve el frontend con Nginx o un CDN.

---

## Estructura del proyecto

```
recetas-python/
├─ app/
│  ├─ domain/
│  │  ├─ entities.py           # Dataclasses: Meal, Category, Area, Ingredient
│  │  └─ repositories.py       # Contratos abstractos
│  ├─ application/
│  │  └─ services.py           # Lógica de aplicación
│  ├─ infrastructure/
│  │  ├─ meal_api_client.py    # Cliente HTTP a TheMealDB
│  │  └─ meal_repository.py    # Implementación del repositorio
│  ├─ presentation/
│  │  └─ controllers.py        # Rutas FastAPI
│  └─ main.py                  # App FastAPI
├─ templates/                  # Vistas HTML (Jinja2)
├─ static/                     # CSS y JS
├─ requirements.txt
├─ run.py
└─ README.md
```

---

## Endpoints disponibles

| Ruta | Descripción |
|------|-------------|
| `GET /` | Inicio con receta aleatoria |
| `GET /search?q=` | Buscar por nombre |
| `GET /meal/{id}` | Detalle de receta |
| `GET /categories` | Listar categorías |
| `GET /category/{nombre}` | Filtrar por categoría |
| `GET /areas` | Listar áreas |
| `GET /area/{nombre}` | Filtrar por área |
| `GET /ingredients` | Listar ingredientes |
| `GET /ingredient/{nombre}` | Filtrar por ingrediente |
| `GET /health` | Estado del servicio |

---

## Mantenimiento y contribución

### Agregar un endpoint nuevo (pasos)

1. Definir el método en `app/domain/repositories.py`
2. Implementar la llamada en `app/infrastructure/meal_api_client.py`
3. Delegar en `app/infrastructure/meal_repository.py`
4. Crear el caso de uso en `app/application/services.py`
5. Exponer la ruta en `app/presentation/controllers.py`
6. Crear el template HTML en `templates/`

### Reportar problemas

Abre un issue en el repositorio describiendo:
- Pasos para reproducir
- Resultado esperado vs obtenido
- Versión de Python y SO

---
##Imagenes

<img width="1282" height="955" alt="image" src="https://github.com/user-attachments/assets/acd66c13-1069-4647-8b37-dc39580cf1aa" />
<img width="389" height="871" alt="image" src="https://github.com/user-attachments/assets/33a3f338-301a-4463-a797-0d64ad6d243e" />
<img width="1904" height="921" alt="image" src="https://github.com/user-attachments/assets/e40e9d78-fbaa-43b4-bd8b-794ed9506aa4" />
<img width="1895" height="946" alt="image" src="https://github.com/user-attachments/assets/86befe54-3bbc-4b2d-b2ff-8a100b5e9b43" />
<img width="1901" height="950" alt="image" src="https://github.com/user-attachments/assets/b9b8eabd-0661-4fc6-8d7f-d9caec0ff680" />
<img width="1284" height="952" alt="image" src="https://github.com/user-attachments/assets/040db57a-9932-420c-8265-5466877a1beb" />




##Licencia

Proyecto educativo. Consume la API pública de TheMealDB bajo sus términos de uso.
