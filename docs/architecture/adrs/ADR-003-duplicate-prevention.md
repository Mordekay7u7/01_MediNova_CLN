# ADR-003: Prevención de Citas Duplicadas mediante Specification Pattern

## Estado
**Aceptada**

## Contexto
El BRD exige evitar colisiones de agenda cuando un paciente intenta agendar citas en la misma fecha y hora, independientemente de la sucursal (Sur, Centro, Norte) o del canal de atención (recepción, teléfono, WhatsApp).

## Alternativas Consideradas
1. **Validación exclusiva en la interfaz o frontend:** Vulnerable a llamadas concurrentes a la API y fácil de eludir.
2. **Restricción de base de datos (Unique Index):** Difícil de validar dinámicamente cuando se filtran estados no activos (ej. citas en estado `CANCELADA`).
3. **Specification Pattern en la Capa de Dominio:** Implementar `SinCitaDuplicadaSpecification` que valida el historial de citas activas del paciente contra el nuevo horario propuesto antes de persistir.

## Decisión
Utilizar el patrón de diseño **Specification Pattern** (`SinCitaDuplicadaSpecification`) dentro del Caso de Uso `AgendarCitaUseCase`. Toda solicitud de agendamiento evalúa si la especificación se satisface; de lo contrario, se lanza una excepción de negocio `CitaDuplicadaException` que se traduce en un código HTTP `409 Conflict`.

## Consecuencias
- **Positivas:** Garantiza 0% de citas duplicadas en cualquier canal, lógica reutilizable y fácilmente testeable con Pytest.
- **Negativas:** Requiere realizar la lectura previa de las citas activas del paciente antes de realizar la inserción.

## Trazabilidad
- **BRD:** Gestión Centralizada y Concurrencia (Objetivo 0% duplicados).
- **User Stories:** US-03 (Validación de cita duplicada entre sucursales).
