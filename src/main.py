from fastapi import FastAPI
from src.api.routers import citas
from src.infrastructure.persistence.csv_parser import CSVDataLoader
from src.infrastructure.persistence.repositories.in_memory_repository import InMemoryCitaRepository

app = FastAPI(
    title="MediNova API - Sistema de Gestión de Citas",
    description="API REST del Producto Integrador de Aprendizaje (PIA) - Lógica de Negocios",
    version="1.0.0"
)

# Incluir routers
app.include_router(citas.router)

@app.on_event("startup")
def startup_event():
    """Carga los CSV al iniciar el servidor."""
    try:
        loader = CSVDataLoader(data_folder="data")
        citas.cita_repository.seed_desde_csv(loader)
        print("✓ Base de datos hidratada con los CSV exitosamente.")
    except Exception as e:
        print(f"Advertencia al cargar CSVs: {e}")

@app.get("/", tags=["Health Check"])
def root():
    return {"status": "ok", "message": "MediNova API en funcionamiento"}