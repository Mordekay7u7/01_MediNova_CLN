# ADR-002: Delimitación de Contextos y Separación de Cita y Paciente

## Estado
**Aceptada**

## Contexto
En MediNova, las cancelaciones exigen guardar información de evidencia (motivo, usuario responsable y fecha/hora), mientras que el control de inasistencias (No-Show) requiere actualizar el estado de la cita, registrar el evento en el historial del paciente y liberar el horario ocupado en la agenda médica. Se requirió definir la separación de responsabilidades y límites de contexto (Bounded Contexts).

## Alternativas Consideradas
1. **Modelo Monolítico Integrado (Single Entity):** Combinar la cita, el paciente y la agenda en una única entidad grande. Esto genera alto acoplamiento y dificulta la trazabilidad de cambios individuales.
2. **Separación de Entidades y Contextos Delimitados:** Separar `Cita` (como entidad principal que gestiona su propio estado y evidencia) de `Paciente` (que gestiona su historial y reincidencias) e interactuar a través de servicios de aplicación DTOs.

## Decisión
Separar explícitamente `Cita` y `Paciente` como entidades independientes del dominio con responsabilidades bien delimitadas. `Cita` administra su ciclo de vida y estado (`EstadoCitaEnum`), mientras que los Casos de Uso coordinan la actualización del historial del `Paciente` y las reglas de reincidencia por No-Shows.

## Consecuencias
- **Positivas:** Estructura modular clara, prevención de efectos secundarios no deseados en la base de datos, cumplimiento del Principio de Responsabilidad Única (SRP).
- **Negativas:** Requiere el uso de DTOs y mapeadores para enviar datos entre la capa de API REST y la capa de Dominio.

## Trazabilidad
- **BRD:** Trazabilidad de Cancelaciones, Control de Historial y No-Shows.
- **User Stories:** US-05 (Cancelación con evidencia), US-09 (Proceso No-Show), US-10 (Restricción por reincidencia de ausencias), US-14 (Historial de paciente).
