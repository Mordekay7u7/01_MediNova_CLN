from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

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

class CitaResponseDTO(BaseModel):
    cita_id: str
    paciente_id: str
    medico_id: str
    sucursal_id: str
    fecha_hora: datetime
    motivo_consulta: str
    es_sobrecupo: bool
    estado: str