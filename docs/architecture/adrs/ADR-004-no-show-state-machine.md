# ADR-004: Máquina de Estados para el Flujo de Citas y Proceso No-Show

## Estado
**Aceptada**

## Contexto
Las citas médicas transitan por diversos estados durante su ciclo de vida (`PROGRAMADA`, `BLOQUEADA_TEMPORAL`, `EN_ESPERA`, `ATENDIDA`, `NO_SHOW`, `CANCELADA`, `PENDIENTE_CONFIRMACION`). En particular, US-09 exige que pasados 20 minutos de la hora programada sin registro de llegada, la cita deba pasar automáticamente a estado `NO_SHOW`.

## Alternativas Consideradas
1. **Modificación directa de strings de estado:** Cambiar arbitrariamente la propiedad `estado` de la cita desde cualquier parte del código, con riesgo de transiciones inválidas (ej. pasar de `CANCELADA` a `ATENDIDA`).
2. **Máquina de Estados explícita (State Pattern):** Definir una matriz de transiciones válidas y encauzar los cambios de estado a través de métodos explícitos en la entidad (`marcar_no_show()`, `cancelar()`, `cambiar_estado()`).

## Decisión
Implementar el patrón **State Machine** en la entidad `Cita` restringido por `EstadoCitaEnum`. Las transiciones solo ocurren mediante reglas explícitas de negocio. El Caso de Uso `ProcesarNoShowUseCase` y la especificación `NoShowAutomatizableSpecification` evalúan la regla de los 20 minutos de tolerancia para aplicar la transición a `NO_SHOW` de manera atómica.

## Consecuencias
- **Positivas:** Previene inconsistencias de estado, facilita la trazabilidad en logs y simplifica las pruebas unitarias parametrizadas.
- **Negativas:** Obliga a rechazar peticiones con excepciones de negocio si la cita se encuentra en un estado terminal.

## Trazabilidad
- **BRD:** Control de Historial y No-shows, Medición de No-Shows.
- **User Stories:** US-07 (Llegada), US-08 (Retrasos), US-09 (No-Show automático de 20 min), US-12 y US-13 (Cancelación de jornada y reagendamiento).
