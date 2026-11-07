import os
from src.infrastructure.persistence.csv_parser import CSVDataLoader
from src.infrastructure.persistence.repositories.in_memory_repository import InMemoryCitaRepository

def ejecutar_seeding():
    print("Iniciando carga masiva de datos desde archivos CSV...")
    loader = CSVDataLoader(data_folder="data")
    
    actores = loader.cargar_actores()
    catalogo = loader.cargar_catalogo()
    operaciones = loader.cargar_operaciones()
    
    repo = InMemoryCitaRepository()
    repo.seed_desde_csv(loader)
    
    print(f"✓ {len(actores)} Actores cargados correctamente.")
    print(f"✓ {len(catalogo)} Servicios del catálogo cargados.")
    print(f"✓ {len(operaciones)} Operaciones/Citas e hidratadas en memoria.")

if __name__ == "__main__":
    ejecutar_seeding()