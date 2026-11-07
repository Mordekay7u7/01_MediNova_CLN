from enum import Enum
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

class EstadoCitaEnum(str, Enum):
    PROGRAMADA = "PROGRAMADA"
    BLOQUEADA_TEMPORAL = "BLOQUEADA_TEMPORAL"
    EN_ESPERA = "EN_ESPERA"
    ATENDIDA = "ATENDIDA"
    NO_SHOW = "NO_SHOW"
    CANCELADA = "CANCELADA"
    PENDIENTE_CONFIRMACION = "PENDIENTE_CONFIRMACION"

class TipoMedicoEnum(str, Enum):
    EMPLEADO = "EMPLEADO"
    HONORARIOS = "HONORARIOS"

class CanalAgendamientoEnum(str, Enum):
    RECEPCION = "RECEPCION"
    TELEFONO = "TELEFONO"
    WHATSAPP = "WHATSAPP"

@dataclass(frozen=True)
class EvidenciaCancelacion:
    motivo: str
    usuario_responsable: str
    fecha_hora_cancelacion: datetime

    def __post_init__(self):
        if not self.motivo or not self.motivo.strip():
            raise ValueError("El motivo de cancelación es obligatorio.")
        if not self.usuario_responsable or not self.usuario_responsable.strip():
            raise ValueError("El usuario responsable de la cancelación es obligatorio.")