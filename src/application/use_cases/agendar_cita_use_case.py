import uuid
from datetime import datetime
from src.domain.entities.cita import Cita
from src.domain.specifications.cita_specifications import SinCitaDuplicadaSpecification
from src.application.dtos.cita_dtos import AgendarCitaDTO

class CitaDuplicadaException(Exception):
    """Excepción al detectar colisión de horario en cualquier sucursal (US-03)."""
    pass

class AgendarCitaUseCase:
    """
    US-03 / CU-02: Valida duplicados sin importar la sucursal antes de guardar.
    """
    def __init__(self, cita_repository):
        self.cita_repository = cita_repository

    def execute(self, dto: AgendarCitaDTO) -> Cita:
        citas_existentes = self.cita_repository.obtener_por_paciente(dto.paciente_id)
        spec = SinCitaDuplicadaSpecification(citas_existentes, dto.fecha_hora)
        
        nueva_cita = Cita(
            cita_id=str(uuid.uuid4()),
            paciente_id=dto.paciente_id,
            medico_id=dto.medico_id,
            sucursal_id=dto.sucursal_id,
            fecha_hora=dto.fecha_hora,
            motivo_consulta=dto.motivo_consulta,
            es_sobrecupo=dto.es_sobrecupo
        )

        if not spec.is_satisfied_by(nueva_cita):
            raise CitaDuplicadaException(
                f"El paciente {dto.paciente_id} ya cuenta con una cita activa el {dto.fecha_hora}."
            )

        self.cita_repository.guardar(nueva_cita)
        return nueva_cita