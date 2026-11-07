from datetime import datetime
from typing import List
from src.domain.specifications.cita_specifications import NoShowAutomatizableSpecification
from src.domain.entities.cita import Cita

class ProcesarNoShowUseCase:
    """
    US-09 / CU-04: Transición automática a No-Show a los 20 min sin llegada registrada.
    """
    def __init__(self, cita_repository):
        self.cita_repository = cita_repository

    def execute(self, hora_actual: datetime) -> List[Cita]:
        citas_programadas = self.cita_repository.obtener_programadas()
        spec = NoShowAutomatizableSpecification(hora_actual)
        
        citas_actualizadas = []
        for cita in citas_programadas:
            if spec.is_satisfied_by(cita):
                cita.marcar_no_show()
                self.cita_repository.guardar(cita)
                citas_actualizadas.append(cita)
                
        return citas_actualizadas