from src.domain.value_objects import EstadoCitaEnum

class TransicionEstadoInvalidaException(Exception):
    """Excepción lanzada al intentar realizar un cambio de estado no permitido."""
    pass

class CitaStateMachine:
    """Maneja las reglas de cambio de estado de una Cita en MediNova."""
    
    TRANSICIONES_PERMITIDAS = {
        EstadoCitaEnum.BLOQUEADA_TEMPORAL: {
            EstadoCitaEnum.PROGRAMADA,
            EstadoCitaEnum.CANCELADA
        },
        EstadoCitaEnum.PROGRAMADA: {
            EstadoCitaEnum.EN_ESPERA,
            EstadoCitaEnum.CANCELADA,
            EstadoCitaEnum.NO_SHOW,
            EstadoCitaEnum.PENDIENTE_CONFIRMACION
        },
        EstadoCitaEnum.EN_ESPERA: {
            EstadoCitaEnum.ATENDIDA,
            EstadoCitaEnum.CANCELADA
        },
        EstadoCitaEnum.PENDIENTE_CONFIRMACION: {
            EstadoCitaEnum.PROGRAMADA,
            EstadoCitaEnum.CANCELADA
        },
        EstadoCitaEnum.ATENDIDA: set(),
        EstadoCitaEnum.NO_SHOW: set(),
        EstadoCitaEnum.CANCELADA: set()
    }

    @classmethod
    def validar_transicion(cls, estado_actual: EstadoCitaEnum, nuevo_estado: EstadoCitaEnum) -> bool:
        if nuevo_estado not in cls.TRANSICIONES_PERMITIDAS.get(estado_actual, set()):
            raise TransicionEstadoInvalidaException(
                f"No se puede cambiar el estado de {estado_actual.value} a {nuevo_estado.value}."
            )
        return True