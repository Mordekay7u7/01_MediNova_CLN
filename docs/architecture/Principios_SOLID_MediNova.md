# 🛡️ Aplicación de Principios SOLID en MediNova

El desarrollo del backend para el sistema de citas médicas **MediNova** fue estructurado bajo una arquitectura **Domain-Driven Design (DDD)**. Para garantizar un código mantenible, escalable y altamente testeable, se aplicaron los 5 principios de diseño **SOLID**.

---

## 1. SRP — Single Responsibility Principle (Principio de Responsabilidad Única)

> *"Una clase debe tener una sola razón para cambiar."*

Cada capa y componente dentro del sistema posee una función delimitada:
* **Entidades (`Cita`):** Mantienen el estado y validan transiciones del ciclo de vida.
* **Casos de Uso (`AgendarCitaUseCase`):** Coordinan el flujo operativo sin acoplarse a frameworks web ni a la base de datos.
* **Repositorios (`InMemoryCitaRepository`):** Encargados únicamente de la persistencia de datos.

```python
# src/application/use_cases/agendar_cita_use_case.py

class AgendarCitaUseCase:
    """
    Responsabilidad Única: Ejecutar el flujo de agendamiento 
    validando reglas del negocio antes de persistir.
    """
    def __init__(self, cita_repository):
        self.cita_repository = cita_repository

    def execute(self, dto: AgendarCitaDTO) -> Cita:
        citas_existentes = self.cita_repository.obtener_por_paciente(dto.paciente_id)
        spec = SinCitaDuplicadaSpecification(citas_existentes, dto.fecha_hora)

        if not spec.is_satisfied_by(None):
            raise CitaDuplicadaException(f"El paciente ya tiene cita el {dto.fecha_hora}")

        nueva_cita = Cita(
            cita_id=str(uuid.uuid4()),
            paciente_id=dto.paciente_id,
            medico_id=dto.medico_id,
            sucursal_id=dto.sucursal_id,
            fecha_hora=dto.fecha_hora,
            motivo_consulta=dto.motivo_consulta,
            es_sobrecupo=dto.es_sobrecupo
        )
        self.cita_repository.guardar(nueva_cita)
        return nueva_cita
```

---

## 2. OCP — Open/Closed Principle (Principio de Abierto/Cerrado)

> *"Las entidades de software deben estar abiertas a la extensión, pero cerradas a la modificación."*

Mediante el **Patrón Especificación (`Specification Pattern`)**, se pueden incorporar nuevas reglas de validación o políticas de agendamiento sin alterar las clases de dominio ni los casos de uso existentes.

```python
# src/domain/specifications/cita_specifications.py

class BaseSpecification:
    def is_satisfied_by(self, candidate) -> bool:
        raise NotImplementedError()

class SinCitaDuplicadaSpecification(BaseSpecification):
    """Extiende BaseSpecification sin modificar la entidad Cita."""
    def __init__(self, citas_existentes: List[Cita], fecha_hora: datetime):
        self.citas_existentes = citas_existentes
        self.fecha_hora = fecha_hora

    def is_satisfied_by(self, candidate: Cita = None) -> bool:
        for c in self.citas_existentes:
            if c.fecha_hora == self.fecha_hora and c.estado != EstadoCitaEnum.CANCELADA:
                return False
        return True
```

---

## 3. LSP — Liskov Substitution Principle (Principio de Sustitución de Liskov)

> *"Las clases derivadas deben ser sustituibles por sus clases base sin alterar el comportamiento del programa."*

El repositorio define un contrato uniforme. Cualquier implementación que cumpla con los métodos de almacenamiento y consulta puede sustituir a la implementación en memoria sin afectar el comportamiento de los casos de uso ni de la API.

```python
# src/domain/interfaces/cita_repository.py

class CitaRepositoryInterface:
    def guardar(self, cita: Cita) -> None:
        pass
    def obtener_por_id(self, cita_id: str) -> Optional[Cita]:
        pass

# src/infrastructure/persistence/repositories/in_memory_repository.py

class InMemoryCitaRepository(CitaRepositoryInterface):
    """Sustituible por SQLiteCitaRepository o PostgresCitaRepository sin modificar el Use Case."""
    def __init__(self):
        self._citas: Dict[str, Cita] = {}

    def guardar(self, cita: Cita) -> None:
        self._citas[cita.cita_id] = cita

    def obtener_por_id(self, cita_id: str) -> Optional[Cita]:
        return self._citas.get(cita_id)
```

---

## 4. ISP — Interface Segregation Principle (Principio de Segregación de Interfaces)

> *"Los clientes no deben verse obligados a depender de interfaces que no utilizan."*

En lugar de modelos monolíticos, se definieron **DTOs de Pydantic** específicos y delgados para cada transacción u operación de negocio (agendar, cancelar con evidencia, registrar llegada, etc.).

```python
# src/application/dtos/cita_dtos.py

class AgendarCitaDTO(BaseModel):
    paciente_id: str
    medico_id: str
    sucursal_id: str
    fecha_hora: datetime
    motivo_consulta: str
    es_sobrecupo: bool = False

class CancelarCitaDTO(BaseModel):
    """DTO específico que solo contiene la evidencia requerida para cancelaciones (US-05)."""
    motivo: str
    usuario_responsable: str
```

---

## 5. DIP — Dependency Inversion Principle (Principio de Inversión de Dependencias)

> *"Los módulos de alto nivel no deben depender de módulos de bajo nivel; ambos deben depender de abstracciones."*

Los casos de uso de la capa de aplicación y la API REST no dependen de una implementación concreta de base de datos ni de infraestructura física, sino que reciben sus dependencias por medio de **Inyección de Dependencias**.

```python
# src/api/routers/citas.py

from fastapi import APIRouter, Depends
from src.infrastructure.persistence.repositories.in_memory_repository import InMemoryCitaRepository

router = APIRouter(prefix="/api/v1/citas")
cita_repository = InMemoryCitaRepository()

@router.post("/", response_model=CitaResponseDTO)
def agendar_cita(dto: AgendarCitaDTO):
    # Inyección del repositorio abstracto en el caso de uso
    use_case = AgendarCitaUseCase(cita_repository=cita_repository)
    cita_creada = use_case.execute(dto)
    return cita_creada
```