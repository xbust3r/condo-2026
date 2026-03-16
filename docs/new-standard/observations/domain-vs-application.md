# Dominio vs Aplicación vs Infraestructura

Esta es una de las ideas más importantes del proyecto.
Si un developer junior entiende esto, evita la mitad de los errores típicos.

---

## 1. Domain

### ¿Qué es?
La parte del sistema que representa el negocio.

### Debe contener
- entidades,
- invariantes,
- reglas del negocio,
- transiciones válidas,
- semántica real del sistema.

### Ejemplo en este proyecto
Un `Lead` debería saber cosas como:
- en qué estado puede estar,
- cómo pasar de pendiente a éxito o fallo,
- qué significa usar un fallback de `media_code`.

### Qué NO debe conocer
- SQLAlchemy
- `DBLeads`
- `requests.post`
- SQS
- detalles HTTP

### ¿Por qué?
Porque el negocio no debería depender de cómo guardas datos o cómo llamas un API.

---

## 2. Application

### ¿Qué es?
La capa que coordina pasos para cumplir un caso de uso.

### Debe contener
- orquestación,
- secuencia del flujo,
- coordinación entre repositorios,
- llamadas a adapters externos,
- decisiones de proceso.

### Ejemplo en este proyecto
`LeadUseCase` sí debe:
- recibir el lead,
- validar campaña,
- registrar el lead,
- mandar a SQS.

`ExecuteUseCase` sí debe:
- recuperar el lead,
- resolver el routing,
- invocar Leadspedia,
- guardar log,
- actualizar el estado final.

### Qué NO debe hacer idealmente
- cargar detalles de persistencia innecesarios,
- actuar como si fuera el dominio entero,
- contener demasiadas reglas que deberían vivir en la entidad.

---

## 3. Infrastructure

### ¿Qué es?
La capa técnica.

### Debe contener
- SQLAlchemy,
- modelos `DB*`,
- sesiones de DB,
- mappers,
- clientes HTTP,
- adapters externos,
- detalles de transporte o persistencia.

### Ejemplo en este proyecto
Aquí viven correctamente:
- `DBLeads`,
- `DBCampaigns`,
- `DBRouting`,
- repositorios concretos,
- mappers,
- el cliente hacia Leadspedia.

### Qué NO debe hacer
- decidir reglas de negocio,
- definir transiciones válidas del lead,
- seleccionar semánticamente el comportamiento del dominio.

---

## 4. Qué se detectó antes

Antes del refactor, el dominio conocía el ORM.
Eso significaba que la frontera entre `domain` e `infrastructure` estaba rota.

Luego se trabajó para mover el mapeo a infraestructura.
Esa fue una corrección importante.

---

## 5. Ejemplo muy simple

## Mal diseño
```python
class Lead:
    @classmethod
    def from_db(cls, db_lead: DBLeads):
        ...
```

¿Por qué está mal?
Porque el dominio está importando una clase de infraestructura.

## Mejor diseño
```python
class Lead:
    def __init__(self, ...):
        ...
```

Y en infraestructura:
```python
class LeadMapper:
    @staticmethod
    def to_domain(db_lead: DBLeads) -> Lead:
        ...
```

Así:
- infraestructura conoce al dominio,
- pero dominio no conoce infraestructura.

---

## 6. Cómo pensarlo como junior

Hazte siempre estas preguntas:

### Si este código habla de negocio, ¿debería vivir en domain?
Ejemplo:
- transiciones de estado,
- reglas de fallback,
- validaciones semánticas.

### Si este código coordina pasos, ¿debería vivir en application?
Ejemplo:
- guardar,
- consultar,
- enviar a SQS,
- invocar provider,
- combinar resultados.

### Si este código habla de tecnología, ¿debería vivir en infrastructure?
Ejemplo:
- SQLAlchemy,
- HTTP,
- boto3,
- requests,
- refresh/flush.

---

## 7. Regla fácil de recordar

### Domain
"Qué significa esto para el negocio"

### Application
"Qué pasos debo ejecutar para cumplir este caso"

### Infrastructure
"Cómo hago técnicamente que eso ocurra"

Si mezclas esas tres preguntas en el mismo lugar, el proyecto se ensucia rápido.
