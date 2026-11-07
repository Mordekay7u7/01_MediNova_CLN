from fastapi import APIRouter, HTTPException, status
from typing import List
from datetime import datetime
from src.application.dtos.cita_dtos import AgendarCitaDTO, CancelarCitaDTO, CitaResponseDTO
from src.application.use_cases.agendar_cita_use_case import AgendarCitaUseCase, CitaDuplicadaException
from src.application.use_cases.procesar_no_show_use_case import ProcesarNoShowUseCase
from src.infrastructure.persistence.repositories.in_memory_repository import InMemoryCitaRepository

router = APIRouter(prefix="/api/v1/citas", tags=["Gestión de Citas Médicas"])

# Instancia global del repositorio cargado en memoria
cita_repository = InMemoryCitaRepository()

@router.post("/", response_model=CitaResponseDTO, status_code=status.HTTP_201_CREATED)
def agendar_cita(dto: AgendarCitaDTO):
    """US-03 / CU-02: Agenda una cita médica validando la no duplicidad de horarios."""
    use_case = AgendarCitaUseCase(cita_repository)
    try:
        cita_creada = use_case.execute(dto)
        return CitaResponseDTO(
            cita_id=cita_creada.cita_id,
            paciente_id=cita_creada.paciente_id,
            medico_id=cita_creada.medico_id,
            sucursal_id=cita_creada.sucursal_id,
            fecha_hora=cita_creada.fecha_hora,
            motivo_consulta=cita_creada.motivo_consulta,
            es_sobrecupo=cita_creada.es_sobrecupo,
            estado=cita_creada.estado.value
        )
    except CitaDuplicadaException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

@router.post("/procesar-no-shows", response_model=List[CitaResponseDTO])
def procesar_no_shows():
    """US-09 / CU-04: Transición automática a No-Show a los 20 min de inasistencia."""
    use_case = ProcesarNoShowUseCase(cita_repository)
    citas_actualizadas = use_case.execute(hora_actual=datetime.now())
    
    return [
        CitaResponseDTO(
            cita_id=c.cita_id,
            paciente_id=c.paciente_id,
            medico_id=c.medico_id,
            sucursal_id=c.sucursal_id,
            fecha_hora=c.fecha_hora,
            motivo_consulta=c.motivo_consulta,
            es_sobrecupo=c.es_sobrecupo,
            estado=c.estado.value
        )
        for c in citas_actualizadas
    ]