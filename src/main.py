import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from src.api.routers import citas
from src.infrastructure.persistence.csv_parser import CSVDataLoader

app = FastAPI(
    title="MediNova API - Sistema de Gestión de Citas",
    description="API REST del Producto Integrador de Aprendizaje (PIA) - Lógica de Negocio",
    version="1.0.0"
)

app.include_router(citas.router)

# Ruta a los archivos estáticos
static_dir = os.path.join(os.path.dirname(__file__), "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

@app.get("/", include_in_schema=False)
def index():
    """Sirve la interfaz web comprensible para el usuario."""
    index_path = os.path.join(static_dir, "index.html")
    if os.path.exists(index_path):
        return FileResponse(index_path)
    return {"message": "MediNova API activa. Visita /docs para la especificación OpenAPI."}

@app.on_event("startup")
def startup_event():
    try:
        loader = CSVDataLoader(data_folder="data")
        citas.cita_repository.seed_desde_csv(loader)
        print("✓ Base de datos hidratada con los CSV exitosamente.")
    except Exception as e:
        print(f"Advertencia al cargar CSVs: {e}")