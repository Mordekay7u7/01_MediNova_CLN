from typing import Dict, Optional, List
from src.domain.entities.cita import Cita
from src.infrastructure.persistence.csv_parser import CSVDataLoader

class InMemoryCitaRepository:
    def __init__(self):
        self._citas: Dict[str, Cita] = {}

    def guardar(self, cita: Cita) -> None:
        self._citas[cita.cita_id] = cita

    def obtener_por_id(self, cita_id: str) -> Optional[Cita]:
        return self._citas.get(cita_id)

    def obtener_por_paciente(self, paciente_id: str) -> List[Cita]:
        return [c for c in self._citas.values() if c.paciente_id == paciente_id]

    def obtener_programadas(self) -> List[Cita]:
        return [c for c in self._citas.values() if c.estado == "PROGRAMADA"]

    def seed_desde_csv(self, loader: CSVDataLoader) -> None:
        """Hidrata el repositorio a partir de los CSV del profesor"""
        operaciones = loader.cargar_operaciones()
        for op in operaciones:
            nueva_cita = Cita(
                cita_id=op["operacion_id"],
                paciente_id=op["actor_id"],
                medico_id="MED-DEFAULT",
                sucursal_id="SUC-CENTRO",
                fecha_hora=op["fecha_hora"],
                motivo_consulta="Consulta desde CSV",
                estado=op["estado_inicial"]
            )
            self.guardar(nueva_cita)