# Cómo agregar nuevos Providers de Routing

## Visión general

El sistema soporta múltiples providers de routing (Leadspedia, LeadForce, etc.) mediante una arquitectura basada en herencia.

```
chalicelib/dddpy/
├── routing/
│   └── __init__.py           ← Clase base RoutingProvider
├── routing_leadspedia/        ← Provider existente
│   └── usecase/
│       └── leadspedia_usecase.py
├── routing_leadforce/        ← Ejemplo: nuevo provider
│   └── usecase/
│       └── leadforce_usecase.py
└── ...
```

---

## La clase base: RoutingProvider

**Ubicación:** `chalicelib/dddpy/routing/__init__.py`

```python
from abc import ABC, abstractmethod
from typing import Any, Dict

class RoutingProvider(ABC):
    """Contrato que todo módulo de routing debe implementar."""

    @property
    @abstractmethod
    def name(self) -> str:
        """Nombre del provider."""
        pass

    @abstractmethod
    def transform(self, lead_data: Dict[str, Any]) -> Any:
        """Transforma datos al formato del provider."""
        pass

    @abstractmethod
    def send(self, payload: Any) -> Dict[str, Any]:
        """Envía al provider y retorna respuesta."""
        pass

    def process(self, lead_data: Dict[str, Any]) -> Dict[str, Any]:
        """Conveniencia: transform + send en una llamada."""
        payload = self.transform(lead_data)
        return self.send(payload)
```

---

## Ejemplo: Agregar LeadForce

### Paso 1: Crear estructura

```
routing_leadforce/
├── __init__.py
└── usecase/
    ├── __init__.py
    └── leadforce_usecase.py
```

### Paso 2: Implementar la clase

```python
# routing_leadforce/usecase/leadforce_usecase.py
from chalicelib.dddpy.routing import RoutingProvider
from chalicelib.dddpy.leads.infrastructure.leads_cmd_repository import LeadCmdRepositoryImpl

class LeadForceUsecase(RoutingProvider):
    """Implementación concreta para LeadForce."""

    def __init__(self):
        self.leads_repo = LeadCmdRepositoryImpl()

    @property
    def name(self) -> str:
        return "leadforce"

    def transform(self, lead_data: dict) -> str:
        """
        Transforma datos a XML para LeadForce.
        
        LeadForce usa XML en lugar de JSON.
        """
        # Transformación específica a XML
        xml_template = f"""
        <lead>
            <first_name>{lead_data.get('client', {}).get('first_name')}</first_name>
            <last_name>{lead_data.get('client', {}).get('last_name')}</last_name>
            <phone>{lead_data.get('client', {}).get('phone')}</phone>
            <!-- más campos -->
        </lead>
        """
        return xml_template

    def send(self, payload: str) -> dict:
        """
        Envía via SOAP/XML.
        
        LeadForce usa SOAP en lugar de REST.
        """
        # Ejemplo de envío SOAP
        import requests
        
        response = requests.post(
            "https://api.leadforce.com/submit",
            data={"xml": payload},
            headers={"Content-Type": "application/xml"}
        )
        
        # Convertir respuesta XML a dict
        return {"result": "success", "raw_response": response.text}
```

### Paso 3: (Opcional) Schema si necesitas validación

```python
# routing_leadforce/usecase/leadforce_schema.py
from pydantic import BaseModel

class LeadForceSchema(BaseModel):
    first_name: str
    last_name: str
    phone: str
    # ... campos específicos
```

---

## Uso en ExecuteUseCase

### Opción 1: Inyección de dependencia

```python
# ExecuteUseCase
def __init__(self, routing_provider: RoutingProvider = None):
    self.routing_provider = routing_provider or LeadspediaUsecase()

def execute(self, lead_id: int):
    # ...
    # Usar el provider configurado
    response = self.routing_provider.process(lead_data)
```

### Opción 2: Selección por configuración

```python
# Factory simple
def get_routing_provider(media_code: str) -> RoutingProvider:
    """Selecciona provider según media code."""
    
    # Leer configuración de BD o environment
    routing = get_routing_by_media_code(media_code)
    
    if routing.provider == "leadspedia":
        return LeadspediaUsecase()
    elif routing.provider == "leadforce":
        return LeadForceUsecase()
    else:
        raise ValueError(f"Unknown provider: {routing.provider}")
```

---

## Cuándo crear vs reusing

| Provider | Transform | Send | ¿Reusar? |
|----------|-----------|------|----------|
| Leadspedia | JSON schema | REST HTTP | - |
| LeadForce | XML | SOAP | Diferente |
| ProviderC | JSON | REST | Similar a Leadspedia |

**Regla:** Si el envío es muy diferente (SOAP vs REST), crea clase nueva. Si es similar, puedes heredar y sobreescribir lo necesario.

---

## Testing

```python
# tests/routing_leadforce/test_leadforce_usecase.py
from unittest.mock import Mock
from routing_leadforce.usecase.leadforce_usecase import LeadForceUsecase

def test_transform_to_xml():
    provider = LeadForceUsecase()
    
    lead_data = {
        "client": {
            "first_name": "John",
            "last_name": "Doe",
            "phone": "1234567890"
        }
    }
    
    result = provider.transform(lead_data)
    
    assert "<first_name>John</first_name>" in result
    assert "<last_name>Doe</last_name>" in result

def test_process_full_flow():
    """Test del flujo completo con mock"""
    provider = LeadForceUsecase()
    provider.send = Mock(return_value={"result": "success"})
    
    lead_data = {"client": {"first_name": "Test"}}
    
    result = provider.process(lead_data)
    
    assert result == {"result": "success"}
    provider.send.assert_called_once()
```

---

## Checklist para nuevo provider

- [ ] Crear módulo en `chalicelib/dddpy/routing_<nombre>/`
- [ ] Crear clase que herede de `RoutingProvider`
- [ ] Implementar `name`, `transform()`, `send()`
- [ ] Crear schema si es necesario
- [ ] Agregar tests en `tests/routing_<nombre>/`
- [ ] Documentar en este archivo

---

## Notas

- La clase base está en `routing/__init__.py` - es el contrato común
- Cada provider es un módulo independiente
- El ExecuteUseCase puede iterar sobre múltiples routings
- La relación MediaCode → Routings permite múltiples destinos por lead
