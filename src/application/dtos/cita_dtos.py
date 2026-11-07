from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, List

class AgendarCitaDTO(BaseModel):
    paciente_id: str = Field(..., example="PAC-001")
    medico_id: str = Field(..., example="MED-012")
    sucursal_id: str = Field(..., example="SUC-SUR")
    fecha_hora: datetime = Field(..., example="2026-11-10T10:00:00")
    motivo_consulta: str = Field(..., example="Consulta general por migraña")
    es_sobrecupo: bool = Field(default=False)

class CancelarCitaDTO(BaseModel):
    motivo: str = Field(..., example="Paciente presentó justificante de viaje")
    usuario_responsable: str = Field(..., example="recepcion_apodaca")

class RegistrarLlegadaDTO(BaseModel):
    minutos_retraso: int = Field(default=0, example=10)
    forma_pago: str = Field(..., example="PAGO_DIRECTO")  # PAGO_DIRECTO o ASEGURADORA

class OrdenSeguimientoDTO(BaseModel):
    paciente_id: str = Field(..., example="PAC-001")
    medico_id: str = Field(..., example="MED-012")
    motivo_consulta: str = Field(..., example="Estudios de seguimiento")

class CitaResponseDTO(BaseModel):
    cita_id: str
    paciente_id: str
    medico_id: str
    sucursal_id: str
    fecha_hora: datetime
    motivo_consulta: str
    es_sobrecupo: bool
    estado: str
    evidencia_cancelacion: Optional[dict] = None
    
    
class BloquearHorarioDTO(BaseModel):
    medico_id: str = Field(..., example="MED-012")
    fecha_hora: datetime = Field(..., example="2026-11-10T10:00:00")
    usuario_responsable: str = Field(..., example="recepcion_centro")

class CancelarJornadaDTO(BaseModel):
    medico_id: str = Field(..., example="MED-012")
    fecha_jornada: str = Field(..., example="2026-11-10")
    justificante: Optional[str] = Field(default=None, example="Incapacidad médica de empleado")