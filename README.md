# 🏥 MediNova - Sistema de Gestión de Citas Médicas (PIA)

[![MediNova CI/CD Pipeline](https://github.com/CLNEG-EQU-1/01_MediNova_CLN/actions/workflows/ci-cd.yml/badge.svg)](https://github.com/CLNEG-EQU-1/01_MediNova_CLN/actions)
[![Coverage Status](https://img.shields.io/badge/coverage-92.37%25-brightgreen.svg)](https://github.com/CLNEG-EQU-1/01_MediNova_CLN)
[![Python](https://img.shields.io/badge/python-3.11-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100.0-009688.svg)](https://fastapi.tiangolo.com/)

Sistema backend robusto para la gestión y optimización de citas médicas en clínicas multisucursal. Desarrollado con arquitectura **Domain-Driven Design (DDD)**, **FastAPI** y patrones de diseño de dominio (Specification, State Machine, Aggregate Root), cumpliendo estrictamente con los requerimientos del Producto Integrador de Aprendizaje (PIA).

---

## 🌐 Enlaces de Despliegue en Vivo

* **URL Pública (Interfaz Web):** [https://medinova-api.onrender.com](https://medinova-api.onrender.com)
* **Documentación OpenAPI / Swagger UI:** [https://medinova-api.onrender.com/docs](https://medinova-api.onrender.com/docs)

---

## 📌 Arquitectura y Patrones de Diseño

El proyecto sigue una arquitectura en capas limpia basada en **DDD (Domain-Driven Design)**:

```text
src/
├── api/                    # Capa de Presentación (Routers FastAPI y DTOs)
├── application/            # Capa de Aplicación (Casos de Uso y Servicios)
├── domain/                 # Capa de Dominio (Entidades, Objetos de Valor, Especificaciones, Máquina de Estados)
└── infrastructure/         # Capa de Infraestructura (Persistencia, Parsers CSV, Repositorio InMemory)
```

### Patrones Aplicados:
1. **Specification Pattern (`cita_specifications.py`):** Encapsula reglas de negocio complejas como la detección de citas duplicadas multisucursal (`SinCitaDuplicadaSpecification`) y la elegibilidad de No-Show automático (`NoShowAutomatizableSpecification`).
2. **State Machine (`cita_state_machine.py`):** Administra el ciclo de vida de la cita (`PROGRAMADA`, `EN_ESPERA`, `ATENDIDA`, `NO_SHOW`, `CANCELADA`, `PENDIENTE_CONFIRMACION`) impidiendo transiciones inválidas.
3. **Repository Pattern (`in_memory_repository.py`):** Abstrae la persistencia de datos e integra hidratación de datos iniciales a partir de archivos CSV.

---

## 📋 Trazabilidad de Historias de Usuario (US-01 a US-15)

| US | Descripción de la Historia de Usuario | Componente / Endpoint | Estado |
| :--- | :--- | :--- | :---: |
| **US-01** | Agendamiento básico de cita médica | `POST /api/v1/citas/` |  Implementado |
| **US-02** | Validación de horario y médico asignado | `AgendarCitaUseCase` |  Implementado |
| **US-03** | Bloqueo de duplicados en cualquier sucursal | `SinCitaDuplicadaSpecification` |  Implementado |
| **US-04** | Bloqueo temporal por 3 minutos (Concurrencia) | `POST /api/v1/citas/bloquear-temporal` |  Implementado |
| **US-05** | Cancelación con evidencia obligatoria | `POST /api/v1/citas/{id}/cancelar` |  Implementado |
| **US-06** | Validación de autorización con Aseguradora | `GET /api/v1/citas/validar-aseguradora/{id}` |  Implementado |
| **US-07** | Registro de llegada del paciente a recepción | `POST /api/v1/citas/{id}/registrar-llegada` |  Implementado |
| **US-08** | Control de tolerancias y retrasos (>15 min) | `RegistrarLlegadaDTO` |  Implementado |
| **US-09** | Transición automática a No-Show (20 min) | `POST /api/v1/citas/procesar-no-shows` |  Implementado |
| **US-10** | Restricción por 3 No-Shows acumulados | `GET /api/v1/citas/paciente/{id}/validar-reincidencia` |  Implementado |
| **US-11** | Manejo de solicitudes de sobrecupo | `AgendarCitaDTO (es_sobrecupo)` |  Implementado |
| **US-12** | Cancelación de jornada médica completa | `POST /api/v1/citas/cancelar-jornada` |  Implementado |
| **US-13** | Reagendamiento prioritario por cancelación | `EstadoCitaEnum.PENDIENTE_CONFIRMACION` |  Implementado |
| **US-14** | Expediente e historial único del paciente | `GET /api/v1/citas/paciente/{id}/historial` |  Implementado |
| **US-15** | Órdenes de seguimiento post-consulta | `POST /api/v1/citas/orden-seguimiento` |  Implementado |

---

## 🚀 Instalación y Ejecución Local

### Prerrequisitos
* Python 3.11+
* Git

### Pasos de Instalación

1. **Clonar el repositorio:**
   ```bash
   git clone https://github.com/CLNEG-EQU-1/01_MediNova_CLN.git
   cd 01_MediNova_CLN
   ```

2. **Crear y activar un entorno virtual:**
   ```bash
   # En Windows
   python -m venv .venv
   .venv\Scripts\activate

   # En Linux/macOS
   python3 -m venv .venv
   source .venv/bin/activate
   ```

3. **Instalar dependencias:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Ejecutar el servidor local:**
   ```bash
   python -m uvicorn src.main:app --reload --port 8000
   ```

5. **Acceder a la aplicación:**
   * **Vista Web:** [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
   * **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## 🐳 Ejecución con Docker Compose

El proyecto está completamente contenerizado bajo la especificación **12-Factor App**.

```bash
# Levantar el entorno web y ejecutar pruebas automáticamente
docker-compose up --build
```

El servicio expondrá la interfaz en `http://localhost:8000` y ejecutará la suite de pruebas garantizando una cobertura mínima del 80%.

---

## 🧪 Pruebas Automatizadas y Cobertura

La suite de pruebas valida la arquitectura DDD, los endpoints de FastAPI y los **140 casos de prueba parametrizados** provistos en los archivos CSV.

### Ejecutar las pruebas:
```bash
python -m pytest
```

### Reporte de Cobertura Obtenido (92.37%):
```text
REQUIRED COVERAGE: 80%, TOTAL COVERAGE: 92.37%
======================== 140 passed in 2.10s ========================
```

---

## 🛠️ Tecnologías Utilizadas

* **Lenguaje:** Python 3.11
* **Framework Web:** FastAPI / Uvicorn
* **Validación de Datos:** Pydantic v2
* **Testing:** Pytest / Pytest-Cov / HTTPX
* **Despliegue y CI/CD:** Docker / GitHub Actions / Render