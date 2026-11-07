# ADR-001: Domain Model como patrón principal de lógica de negocio

## Estado
**Aceptada**

## Contexto
MediNova gestiona las agendas de citas médicas en tres sucursales y requiere aplicar reglas complejas del dominio de salud: prevención de citas duplicadas, registro de cancelaciones con evidencia obligatoria, gestión de estados (No-Show, En Espera, Cancelada) y sobrecupos por médico. Se requiere elegir un patrón arquitectónico para organizar la lógica de negocio en la capa backend.

## Alternativas Consideradas
1. **Transaction Script:** Sencillo de implementar rápidamente, pero duplica reglas de negocio en múltiples procedimientos y complica la mantenibilidad a medida que crecen las 15 Historias de Usuario.
2. **Table Module:** Agrupa operaciones por tablas de datos, pero dificulta expresar transiciones de estado complejas y reglas que involucran la interacción entre Cita, Paciente y Médico.
3. **Domain Model (DDD):** Organiza el dominio mediante entidades, Value Objects, especificaciones y máquinas de estado explícitas.

## Decisión
Adoptar **Domain Model** dentro de una arquitectura en capas basada en Domain-Driven Design (DDD). Las reglas de negocio residen en las entidades (`Cita`) y especificaciones (`SinCitaDuplicadaSpecification`), mientras que los Casos de Uso en la capa de aplicación coordinan la ejecución de los flujos de trabajo.

## Consecuencias
- **Positivas:** Encapsulamiento de reglas de negocio, alta testabilidad (cobertura >90%), desacoplamiento total de la base de datos o interfaz.
- **Negativas:** Mayor complejidad inicial al estructurar la solución en carpetas (`domain`, `application`, `infrastructure`).

## Trazabilidad
- **BRD:** Gestión Centralizada y Concurrencia, Control de Historial y No-Shows.
- **User Stories:** US-01, US-02, US-03, US-05, US-09, US-11.
