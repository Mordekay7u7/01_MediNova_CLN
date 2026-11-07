from datetime import datetime
from typing import Optional
from src.domain.value_objects import EstadoCitaEnum, EvidenciaCancelacion
from src.domain.state_machine.cita_state_machine import CitaStateMachine

class Cita:
    def __init__(
        self,
        cita_id: str,
        paciente_id: str,
        medico_id: str,
        sucursal_id: str,
        fecha_hora: datetime,
        motivo_consulta: str,
        es_sobrecupo: bool = False,
        estado: EstadoCitaEnum = EstadoCitaEnum.PROGRAMADA
    ):
        self.cita_id = cita_id
        self.paciente_id = paciente_id
        self.medico_id = medico_id
        self.sucursal_id = sucursal_id
        self.fecha_hora = fecha_hora
        self.motivo_consulta = motivo_consulta
        self.es_sobrecupo = es_sobrecupo
        self.estado = estado
        self.evidencia_cancelacion: Optional[EvidenciaCancelacion] = None

    def cambiar_estado(self, nuevo_estado: EstadoCitaEnum):
        """Aplica la máquina de estados antes de realizar la transición."""
        CitaStateMachine.validar_transicion(self.estado, nuevo_estado)
        self.estado = nuevo_estado

    def cancelar(self, motivo: str, usuario_responsable: str, fecha_hora_cancelacion: datetime):
        """Registra la evidencia obligatoria de cancelación y cambia el estado a CANCELADA."""
        self.cambiar_estado(EstadoCitaEnum.CANCELADA)
        self.evidencia_cancelacion = EvidenciaCancelacion(
            motivo=motivo,
            usuario_responsable=usuario_responsable,
            fecha_hora_cancelacion=fecha_hora_cancelacion
        )

    def marcar_no_show(self):
        """Transición directa a No-Show tras 20 min de inasistencia."""
        self.cambiar_estado(EstadoCitaEnum.NO_SHOW)