from abc import ABC, abstractmethod
from datetime import datetime, timedelta
from typing import List
from src.domain.entities.cita import Cita
from src.domain.value_objects import EstadoCitaEnum

class Specification(ABC):
    @abstractmethod
    def is_satisfied_by(self, candidate: Cita) -> bool:
        pass

class SinCitaDuplicadaSpecification(Specification):
    """
    US-03: Impide registrar una segunda cita activa para el mismo paciente
    en la misma fecha y hora, independientemente de la sucursal.
    """
    def __init__(self, citas_existentes_paciente: List[Cita], fecha_hora_propuesta: datetime):
        self.citas_existentes = citas_existentes_paciente
        self.fecha_hora_propuesta = fecha_hora_propuesta

    def is_satisfied_by(self, candidate: Cita) -> bool:
        citas_activas = [
            c for c in self.citas_existentes
            if c.estado in {EstadoCitaEnum.PROGRAMADA, EstadoCitaEnum.EN_ESPERA, EstadoCitaEnum.BLOQUEADA_TEMPORAL}
        ]
        for cita in citas_activas:
            if cita.fecha_hora == self.fecha_hora_propuesta:
                return False  # Violación: Hay colisión de horario
        return True

class NoShowAutomatizableSpecification(Specification):
    """
    US-09: Evalúa si han transcurrido 20 minutos desde la hora programada
    sin que el paciente haya registrado su llegada.
    """
    def __init__(self, hora_actual: datetime):
        self.hora_actual = hora_actual

    def is_satisfied_by(self, cita: Cita) -> bool:
        if cita.estado != EstadoCitaEnum.PROGRAMADA:
            return False
        
        tiempo_transcurrido = self.hora_actual - cita.fecha_hora
        return tiempo_transcurrido >= timedelta(minutes=20)