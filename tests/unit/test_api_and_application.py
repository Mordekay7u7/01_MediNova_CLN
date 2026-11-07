import pytest
from datetime import datetime
from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)

def test_health_check_endpoint():
    """Verifica el endpoint raíz de health check."""
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"status": "ok", "message": "MediNova API en funcionamiento"}

def test_agendar_cita_exitoso_y_duplicado():
    """Valida la respuesta HTTP 201 en agendamiento exitoso y 409 en duplicados."""
    payload = {
        "paciente_id": "PAC-TEST-001",
        "medico_id": "MED-001",
        "sucursal_id": "SUC-SUR",
        "fecha_hora": "2026-11-20T10:00:00",
        "motivo_consulta": "Consulta de prueba API",
        "es_sobrecupo": False
    }

    # Primer agendamiento -> Debe retornar 201 Created
    res1 = client.post("/api/v1/citas/", json=payload)
    assert res1.status_code == 201
    data = res1.json()
    assert data["paciente_id"] == "PAC-TEST-001"
    assert data["estado"] == "PROGRAMADA"

    # Segundo agendamiento con mismo paciente y hora -> Debe retornar 409 Conflict (US-03)
    res2 = client.post("/api/v1/citas/", json=payload)
    assert res2.status_code == 409
    assert "ya cuenta con una cita activa" in res2.json()["detail"]

def test_procesar_no_shows_endpoint():
    """Valida el endpoint de procesamiento de No-Shows."""
    response = client.post("/api/v1/citas/procesar-no-shows")
    assert response.status_code == 200
    assert isinstance(response.json(), list)