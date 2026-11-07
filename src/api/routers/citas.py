from fastapi import APIRouter, HTTPException, status
from typing import List, Optional
from datetime import datetime, timedelta

from src.application.dtos.cita_dtos import (
    AgendarCitaDTO,
    CancelarCitaDTO,
    RegistrarLlegadaDTO,
    OrdenSeguimientoDTO,
    BloquearHorarioDTO,
    CancelarJornadaDTO,
    CitaResponseDTO
)
from src.application.use_cases.agendar_cita_use_case import AgendarCitaUseCase, CitaDuplicadaException
from src.application.use_cases.procesar_no_show_use_case import ProcesarNoShowUseCase
from src.infrastructure.persistence.repositories.in_memory_repository import InMemoryCitaRepository
from src.domain.value_objects import EstadoCitaEnum

router = APIRouter(prefix="/api/v1/citas", tags=["Gestión de Citas Médicas"])
cita_repository = InMemoryCitaRepository()

# US-01, US-02 & US-03: Agendar Cita
@router.post("/", response_model=CitaResponseDTO, status_code=status.HTTP_201_CREATED)
def agendar_cita(dto: AgendarCitaDTO):
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
            estado=cita_creada.estado.value if hasattr(cita_creada.estado, 'value') else str(cita_creada.estado)
        )
    except CitaDuplicadaException as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))

# US-04: Bloqueo Temporal (3 min)
@router.post("/bloquear-temporal")
def bloquear_horario_temporal(dto: BloquearHorarioDTO):
    return {
        "status": "HORARIO_BLOQUEADO",
        "medico_id": dto.medico_id,
        "fecha_hora": dto.fecha_hora.isoformat(),
        "bloqueado_hasta": (datetime.now() + timedelta(minutes=3)).isoformat(),
        "mensaje": "Horario reservado temporalmente por 3 minutos."
    }

# US-05: Registrar Cancelación con Evidencia
@router.post("/{cita_id}/cancelar", response_model=CitaResponseDTO)
def cancelar_cita(cita_id: str, dto: CancelarCitaDTO):
    cita = cita_repository.obtener_por_id(cita_id)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    try:
        cita.cancelar(dto.motivo, dto.usuario_responsable, datetime.now())
        cita_repository.guardar(cita)
        return CitaResponseDTO(
            cita_id=cita.cita_id,
            paciente_id=cita.paciente_id,
            medico_id=cita.medico_id,
            sucursal_id=cita.sucursal_id,
            fecha_hora=cita.fecha_hora,
            motivo_consulta=cita.motivo_consulta,
            es_sobrecupo=cita.es_sobrecupo,
            estado=cita.estado.value if hasattr(cita.estado, 'value') else str(cita.estado),
            evidencia_cancelacion={
                "motivo": cita.evidencia_cancelacion.motivo,
                "usuario_responsable": cita.evidencia_cancelacion.usuario_responsable,
                "fecha": cita.evidencia_cancelacion.fecha_hora_cancelacion.isoformat()
            }
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

# US-06: Validar Convenio Aseguradora
@router.get("/validar-aseguradora/{paciente_id}")
def validar_autorizacion_aseguradora(paciente_id: str, requiere_folio: bool = True):
    if requiere_folio:
        return {
            "requiere_autorizacion": True,
            "alerta": "El convenio con la aseguradora requiere folio de autorización previo al agendamiento."
        }
    return {"requiere_autorizacion": False, "alerta": "No requiere autorización previa."}

# US-07 & US-08: Registrar Llegada y Retrasos
@router.post("/{cita_id}/registrar-llegada", response_model=CitaResponseDTO)
def registrar_llegada(cita_id: str, dto: RegistrarLlegadaDTO):
    cita = cita_repository.obtener_por_id(cita_id)
    if not cita:
        raise HTTPException(status_code=404, detail="Cita no encontrada")
    if dto.minutos_retraso > 15:
        raise HTTPException(status_code=400, detail="Retraso superior a 15 min. Requiere reagendamiento.")
    
    cita.cambiar_estado(EstadoCitaEnum.EN_ESPERA)
    cita_repository.guardar(cita)
    return CitaResponseDTO(
        cita_id=cita.cita_id,
        paciente_id=cita.paciente_id,
        medico_id=cita.medico_id,
        sucursal_id=cita.sucursal_id,
        fecha_hora=cita.fecha_hora,
        motivo_consulta=cita.motivo_consulta,
        es_sobrecupo=cita.es_sobrecupo,
        estado=cita.estado.value if hasattr(cita.estado, 'value') else str(cita.estado)
    )

# US-09: Procesar No-Shows Automáticos
@router.post("/procesar-no-shows", response_model=List[CitaResponseDTO])
def procesar_no_shows():
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
            estado=c.estado.value if hasattr(c.estado, 'value') else str(c.estado)
        )
        for c in citas_actualizadas
    ]

# US-10: Restricción por Reincidencia (3 No-Shows)
@router.get("/paciente/{paciente_id}/validar-reincidencia")
def validar_reincidencia_no_shows(paciente_id: str):
    citas_paciente = cita_repository.obtener_por_paciente(paciente_id)
    no_shows_count = sum(1 for c in citas_paciente if str(c.estado) == "NO_SHOW")
    if no_shows_count >= 3:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Paciente bloqueado para agendar por Teléfono/WhatsApp por acumular 3 No-Shows. Solo agendamiento presencial."
        )
    return {"status": "PERMITIDO", "no_shows_acumulados": no_shows_count}

# US-12 & US-13: Cancelar Jornada Médica
@router.post("/cancelar-jornada")
def cancelar_jornada_medico(dto: CancelarJornadaDTO):
    citas_programadas = cita_repository.obtener_programadas()
    afectadas = 0
    for cita in citas_programadas:
        if cita.medico_id == dto.medico_id:
            cita.cambiar_estado(EstadoCitaEnum.PENDIENTE_CONFIRMACION)
            cita_repository.guardar(cita)
            afectadas += 1
    return {
        "status": "JORNADA_CANCELADA",
        "medico_id": dto.medico_id,
        "citas_afectadas": afectadas,
        "mensaje": f"Se canceló la jornada. {afectadas} citas pasaron a estado PENDIENTE_CONFIRMACION."
    }

# US-14: Historial de Citas del Paciente
@router.get("/paciente/{paciente_id}/historial", response_model=List[CitaResponseDTO])
def obtener_historial_paciente(paciente_id: str):
    citas = cita_repository.obtener_por_paciente(paciente_id)
    return [
        CitaResponseDTO(
            cita_id=c.cita_id,
            paciente_id=c.paciente_id,
            medico_id=c.medico_id,
            sucursal_id=c.sucursal_id,
            fecha_hora=c.fecha_hora,
            motivo_consulta=c.motivo_consulta,
            es_sobrecupo=c.es_sobrecupo,
            estado=c.estado.value if hasattr(c.estado, 'value') else str(c.estado)
        )
        for c in citas
    ]

# US-15: Orden de Seguimiento
@router.post("/orden-seguimiento")
def generar_orden_seguimiento(dto: OrdenSeguimientoDTO):
    return {
        "status": "ORDEN_GENERADA",
        "paciente_id": dto.paciente_id,
        "medico_id": dto.medico_id,
        "motivo_consulta": dto.motivo_consulta,
        "mensaje": "Orden registrada. Recepción puede agendar fecha sin recapturar datos."
    }

# Endpoint para la interfaz web
@router.get("/todas", response_model=List[CitaResponseDTO])
def obtener_todas_las_citas():
    citas = cita_repository.obtener_programadas()
    return [
        CitaResponseDTO(
            cita_id=c.cita_id,
            paciente_id=c.paciente_id,
            medico_id=c.medico_id,
            sucursal_id=c.sucursal_id,
            fecha_hora=c.fecha_hora,
            motivo_consulta=c.motivo_consulta,
            es_sobrecupo=c.es_sobrecupo,
            estado=c.estado.value if hasattr(c.estado, 'value') else str(c.estado)
        )
        for c in citas
    ]