# Guía de Arquitectura DDD + CQRS para Módulos Python (Chalice)

> **Proyecto Base:** `chalice-zatanna.routing` & `chalice-aca_health.insert-python`
> 
> **Framework:** AWS Chalice
> 
> **Fecha:** Marzo 2026
> 
> **Base de Datos:** MySQL / PostgreSQL
> 
> **ORM:** SQLAlchemy

---

## 1. Configuración de Chalice

### 1.1 Estructura de Archivos

```
src/
├── .chalice/
│   ├── config.json          # Configuración principal
│   ├── policy.json         # Policy IAM
│   └── deployments/        # Deployments
├── app.py                  # Entry point de la app
├── chalicelib/
│   ├── api/                # Rutas (Blueprints)
│   │   ├── routing/
│   │   ├── lead/
│   │   └── campaigns/
│   └── dddpy/              # Módulos DDD
│       ├── {modulo}/
│       └── shared/
└── requirements.txt
```

### 1.2 config.json

La configuración se define en `src/.chalice/config.json`:

```json
{
  "version": "2.0",
  "app_name": "condo-api",
  "environment_variables": {
    "DB_USER": "root",
    "DB_PASSWORD": "123456",
    "DB_HOST": "mysql",
    "DB_PORT": "3306",
    "DB_NAME": "condo_db",
    "API_USER": "local",
    "API_KEY": "local123",
    "SQS_QUEUE_NAME": "dev-condo-queue",
    "SQS_REGION": "us-east-1",
    "SQS_URL": "https://sqs.us-east-1.amazonaws.com/123456789012/dev-condo-queue"
  },
  "autogen_policy": true,
  "iam_policy_file": "policy.json",
  "stages": {
    "dev": {
      "api_gateway_stage": "api"
    }
  }
}
```

### 1.3 app.py (Entry Point)

```python
# app.py
from chalice import Chalice, Response
import os

from chalicelib.api.routing.routes_routing import routing_routes
from chalicelib.api.lead.routes_lead import lead_routes
from chalicelib.dddpy.shared.logging.logging import Logger

app = Chalice(app_name='condo-api')
logger = Logger('app')

# Middleware global para autenticación
@app.middleware('http')
def verify_and_add_headers(event, get_response):
    request_headers = event.headers or {}
    api_user = request_headers.get('API_USER')
    api_key = request_headers.get('API_KEY')
    expected_user = os.environ.get('API_USER')
    expected_key = os.environ.get('API_KEY')

    if api_user != expected_user or api_key != expected_key:
        logger.error(f"Unauthorized access attempt")
        return Response(status_code=401, body={"error": "Unauthorized"})

    response = get_response(event)
    return response

# Registrar Blueprints
app.register_blueprint(routing_routes)
app.register_blueprint(lead_routes)

@app.route('/')
def index():
    return {'hello': 'condo'}
```

---

## 2. Visión General de la Arquitectura

### 1.1 Patrones Utilizados

| Patrón | Descripción |
|--------|-------------|
| **DDD (Domain Driven Design)** | Estructura del código basada en el dominio |
| **CQRS** | Separación de comandos (escritura) y queries (lectura) |
| **Factory Pattern** | Creación de casos de uso mediante factories |
| **Repository Pattern** | Abstracción de acceso a datos |

### 1.2 Estructura de un Módulo

```
src/chalicelib/dddpy/
└── {nombre_modulo}/
    ├── domain/                 # Lógica de dominio
    │   ├── {modulo}.py         # Entidad/Dominio model
    │   ├── {modulo}_exception.py  # Excepciones del dominio
    │   ├── {modulo}_success.py    # Mensajes de éxito
    │   ├── {modulo}_repository.py # Interfaces de repositorio
    │   └── {modulo}_validation.py # Validaciones de dominio
    │
    ├── infrastructure/         # Implementación de acceso a datos
    │   ├── {modulo}.py         # Modelos SQLAlchemy (DB)
    │   ├── {modulo}_cmd_repository.py  # Repository write
    │   └── {modulo}_query_repository.py # Repository read
    │
    └── usecase/               # Casos de uso
        ├── {modulo}_cmd_schema.py    # Schemas Pydantic (write)
        ├── {modulo}_query_schema.py   # Schemas Pydantic (read)
        ├── {modulo}_cmd_usecase.py    # Lógica de escritura
        ├── {modulo}_query_usecase.py  # Lógica de lectura
        ├── {modulo}_factory.py        # Factory para crear usecases
        └── {modulo}_usecase.py        # Caso de uso unificado (Factory)
```

---

## 2. Componentes Detallados

### 2.1 Domain Layer (`domain/`)

Contiene la **lógica de negocio pura**, sin dependencias de frameworks.

#### Entidad/Dominio Model
```python
# domain/leads.py
from datetime import datetime
from typing import Optional, Dict, Any
from chalicelib.dddpy.leads.infrastructure.leads import DBLeads

class Lead:
    def __init__(
        self, 
        id: int, 
        code: str, 
        media_code: str,    
        content: Dict[str, Any], 
        google_captcha_score: float,
        # ... otros campos
    ) -> None:
        self.id = id
        self.code = code
        # ...
    
    @classmethod
    def from_db(cls, db_lead: DBLeads) -> 'Lead':
        """Crea dominio desde modelo DB"""
        return cls(
            id=db_lead.id,
            # ...
        )
    
    def to_dict(self) -> Dict[str, Any]:
        """Convierte a diccionario"""
        return {"id": self.id, ...}
```

#### Excepciones del Dominio
```python
# domain/leads_exception.py
from chalicelib.dddpy.shared.decorators.domain_exception import DomainException

class LeadNotFoundException(DomainException):
    message = "Your lead was not found by your ID"
    
    def __init__(self):
        super().__init__(message=self.message, status_code=404)
```

#### Mensajes de Éxito
```python
# domain/leads_success.py
class SuccessMessages:
    LEAD_SUBMITTED = "Lead successfully submitted"
    LEAD_RETRIEVED = "Lead retrieved successfully"
    NOTE_PROCESSED = "Note processed successfully"
```

#### Interfaz de Repositorio
```python
# domain/leads_cmd_repository.py
from abc import ABC, abstractmethod
from typing import Optional
from chalicelib.dddpy.leads.domain.leads import Lead
from chalicelib.dddpy.leads.usecase.leads_cmd_schema import CreateLeadSchema

class LeadCmdRepository(ABC):
    @abstractmethod
    def create(self, lead: CreateLeadSchema) -> Lead:
        pass
    
    @abstractmethod
    def update(self, id: int, data: dict) -> Lead:
        pass
```

---

### 2.2 Infrastructure Layer (`infrastructure/`)

Contiene los **modelos SQLAlchemy** y la **implementación de repositorios**.

#### Modelo SQLAlchemy
```python
# infrastructure/leads.py
from sqlalchemy import Column, Integer, String, JSON, DateTime, func
from chalicelib.dddpy.shared.mysql.base import Base

class DBLeads(Base):
    __tablename__ = "zatanna_data"
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    code = Column(String(50), nullable=False)
    media_code = Column(String(50), nullable=False)
    content = Column(JSON, nullable=False)
    google_captcha_score = Column(String(20), nullable=True)
    external_system = Column(String(60), nullable=True)
    external_id = Column(String(60), nullable=True)
    status_lead = Column(Integer, nullable=False, default=0)
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    updated_at = Column(DateTime, nullable=False, server_default=func.now(), onupdate=func.now())
```

#### Repository de Comandos (Escritura)
```python
# infrastructure/leads_cmd_repository.py
from chalicelib.dddpy.leads.domain.leads import Lead
from chalicelib.dddpy.leads.domain.leads_cmd_repository import LeadCmdRepository
from chalicelib.dddpy.leads.infrastructure.leads import DBLeads
from chalicelib.dddpy.shared.mysql.session_manager import session_scope
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("lead_cmd_repository")

class LeadCmdRepositoryImpl(LeadCmdRepository):
    def __init__(self):
        logging.info("LeadCmdRepositoryImpl initialized")
    
    def create(self, lead: CreateLeadSchema) -> Lead:
        with session_scope() as session:
            db_lead = DBLeads(
                code=lead.code,
                media_code=lead.media_code,
                content=lead.content,
                # ...
            )
            session.add(db_lead)
            session.commit()
            session.refresh(db_lead)
            return Lead.from_db(db_lead)
```

#### Repository de Queries (Lectura)
```python
# infrastructure/leads_query_repository.py
from typing import Optional
from chalicelib.dddpy.leads.domain.leads import Lead
from chalicelib.dddpy.leads.domain.leads_query_repository import LeadQueryRepository
from chalicelib.dddpy.leads.infrastructure.leads import DBLeads
from chalicelib.dddpy.shared.mysql.session_manager import session_scope

class LeadQueryRepositoryImpl(LeadQueryRepository):
    def get_by_id(self, id: int) -> Optional[Lead]:
        with session_scope() as session:
            db_lead = session.query(DBLeads).filter(DBLeads.id == id).first()
            if db_lead:
                return Lead.from_db(db_lead)
            return None
```

---

### 2.3 Usecase Layer (`usecase/`)

Contiene los **schemas Pydantic** y la **lógica de aplicación** (CQRS).

#### Schemas Pydantic (Comandos - Escritura)
```python
# usecase/leads_cmd_schema.py
from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class IncomingLeadSchema(BaseModel):
    payloadId: str
    entityType: str
    agentId: str
    applicationSource: str
    application: 'ApplicationSchema'

class CreateLeadSchema(BaseModel):
    code: str = Field(..., max_length=100)
 Optional[str] =    media_code: None
    content: Dict[str, Any]
    google_captcha_score: float
    external_system: Optional[str] = None
    status_lead: Optional[int] = None
```

#### Usecase de Comandos (Escritura)
```python
# usecase/leads_cmd_usecase.py
from chalicelib.dddpy.leads.domain.leads import Lead
from chalicelib.dddpy.leads.domain.leads_cmd_repository import LeadCmdRepository
from chalicelib.dddpy.leads.usecase.leads_cmd_schema import IncomingLeadSchema
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("lead_cmd_usecase")

class LeadCmdUseCase:
    def __init__(self, repository: LeadCmdRepository):
        self.repository = repository
    
    def create(self, lead_data: IncomingLeadSchema) -> Lead:
        logging.info(f"Creating a new lead: {lead_data}")
        # Lógica de negocio...
        return self.repository.create(lead_data)
```

#### Usecase de Queries (Lectura)
```python
# usecase/leads_query_usecase.py
from typing import Optional
from chalicelib.dddpy.leads.domain.leads import Lead
from chalicelib.dddpy.leads.domain.leads_query_repository import LeadQueryRepository

class LeadQueryUseCase:
    def __init__(self, repository: LeadQueryRepository):
        self.repository = repository
    
    def get_by_id(self, id: int) -> Optional[Lead]:
        return self.repository.get_by_id(id)
```

#### Factory (Patrón Factory)
```python
# usecase/leads_factory.py
from chalicelib.dddpy.leads.usecase.leads_cmd_usecase import LeadCmdUseCase
from chalicelib.dddpy.leads.usecase.leads_query_usecase import LeadQueryUseCase
from chalicelib.dddpy.leads.infrastructure.leads_cmd_repository import LeadCmdRepositoryImpl
from chalicelib.dddpy.leads.infrastructure.leads_query_repository import LeadQueryRepositoryImpl

def lead_cmd_usecase_factory() -> LeadCmdUseCase:
    repository = LeadCmdRepositoryImpl()
    return LeadCmdUseCase(repository)

def lead_query_usecase_factory() -> LeadQueryUseCase:
    repository = LeadQueryRepositoryImpl()
    return LeadQueryUseCase(repository)
```

#### Caso de Uso Unificado (Combina CMD + QUERY)
```python
# usecase/leads_usecase.py
from chalicelib.dddpy.leads.usecase.leads_factory import (
    lead_cmd_usecase_factory,
    lead_query_usecase_factory,
)
from chalicelib.dddpy.leads.domain.leads_success import SuccessMessages
from chalicelib.dddpy.shared.schemas.response_schema import ResponseSuccessSchema
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("lead_usecase")

class LeadUseCase:
    def __init__(self):
        self.cmd = lead_cmd_usecase_factory()
        self.query = lead_query_usecase_factory()
    
    def create(self, lead_data):
        new_lead = self.cmd.create(lead_data)
        return ResponseSuccessSchema(
            success=True,
            message=SuccessMessages.LEAD_SUBMITTED,
            data=new_lead.to_dict(),
        )
    
    def get_by_id(self, id: int):
        return self.query.get_by_id(id)
```

---

## 3. Componentes Compartidos (`shared/`)

### 3.1 Estructura de Shared

```
src/chalicelib/dddpy/shared/
├── decorators/           # Manejo de excepciones y API handler
│   ├── api_handler.py   # Decorador @api_handler para rutas Chalice
│   └── domain_exception.py  # Clase base DomainException
├── logging/             # Sistema de logging
│   └── logging.py       # Logger personalizado
├── mysql/               # Configuración MySQL
│   ├── base.py          # Engine y Base de SQLAlchemy
│   └── session_manager.py  # Context manager para sesiones
├── postgresql/          # Configuración PostgreSQL
│   ├── base.py          # Engine con soporte IAM RDS
│   └── session_manager.py  # Context manager para sesiones
├── schemas/             # Esquemas comunes
│   └── response_schema.py  # ResponseSuccessSchema, ResponseErrorSchema
├── utils/               # Utilidades
│   ├── validate_email.py
│   ├── password.py
│   ├── urls.py
│   └── uploads.py
└── timezone.py          # Utilidades de timezone
```

### 3.2 Logging

```python
# shared/logging/logging.py
import logging

class Logger:
    inside_method = ""
    
    def __init__(self, logger_name):
        self.logger_name = logger_name
        self.logger = logging.getLogger(logger_name)
        self.logger.setLevel(logging.INFO)
    
    def add_inside_method(self, method_name):
        self.inside_method = method_name
    
    def info(self, data):
        message = f"{self.logger_name} - {self.inside_method} - {data}"
        return self.logger.info(message)
    
    def error(self, data):
        return self.logger.error(data)
    
    def warning(self, data):
        return self.logger.warning(data)
    
    def debug(self, data):
        return self.logger.debug(data)
```

**Uso:**
```python
logging = Logger("mi_modulo")

def mi_funcion():
    logging.add_inside_method("mi_funcion")
    logging.info("Iniciando proceso...")
    # lógica...
    logging.error("Algo salió mal")
```

### 3.3 Manejo de Excepciones (API Handler)

```python
# shared/decorators/domain_exception.py
class DomainException(Exception):
    def __init__(self, message: str, status_code: int = 500):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)
```

```python
# shared/decorators/api_handler.py
from functools import wraps
from chalice import Response
from pydantic import ValidationError
import traceback

from chalicelib.dddpy.shared.logging.logging import Logger
from chalicelib.dddpy.shared.schemas.response_schema import ResponseErrorSchema
from chalicelib.dddpy.shared.decorators.domain_exception import DomainException

logger = Logger("Api Handler Decorator")

def api_handler(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        logger.info(f"--- Start Request: {func.__name__} ---")
        
        try:
            return func(*args, **kwargs)
        
        except DomainException as e:
            logger.warning(f"Domain Exception: {str(e)}")
            error_response = ResponseErrorSchema(success=False, message=str(e))
            return Response(body=error_response.dict(), status_code=e.status_code)
        
        except ValidationError as e:
            logger.error(f"Validation Error: {e}")
            return Response(body=ResponseErrorSchema(success=False, message=str(e)).dict(), status_code=400)
        
        except Exception as e:
            logger.error(f"Critical Error: {str(e)}")
            logger.error(traceback.format_exc())
            return Response(body=ResponseErrorSchema(success=False, message="Internal Server Error").dict(), status_code=500)
    
    return wrapper
```

### 3.4 MySQL Configuration

```python
# shared/mysql/base.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST", "mysql")
DB_PORT = os.environ.get("DB_PORT", "3306")
DB_NAME = os.environ.get("DB_NAME")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

```python
# shared/mysql/session_manager.py
from chalicelib.dddpy.shared.mysql.base import SessionLocal
from contextlib import contextmanager

@contextmanager
def session_scope():
    """Provides a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
```

### 3.5 PostgreSQL Configuration (con IAM RDS)

```python
# shared/postgresql/base.py
import os
import boto3
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

Base = declarative_base()

def get_db_engine_and_session():
    DB_USER = os.environ.get("DB_USER")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT", "5432")
    DB_NAME = os.environ.get("DB_NAME")
    IAM_AUTH_RDS = os.environ.get("IAM_AUTH_RDS", "DISABLED")
    
    password = ""
    ssl_args = {}
    
    if IAM_AUTH_RDS.upper() == "ENABLED":
        aws_region = 'us-west-1'
        rds_client = boto3.client('rds', region_name=aws_region)
        password = rds_client.generate_db_auth_token(
            DBHostname=DB_HOST,
            Port=int(DB_PORT),
            DBUsername=DB_USER,
            Region=aws_region
        )
        ssl_args = {'sslmode': 'require'}
    else:
        password = os.environ.get("DB_PASSWORD")
    
    DATABASE_URL = f"postgresql+psycopg2://{DB_USER}:{password}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    
    engine = create_engine(DATABASE_URL, connect_args=ssl_args, echo=False)
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    return engine, SessionLocal
```

### 3.6 Schemas de Respuesta

```python
# shared/schemas/response_schema.py
from pydantic import BaseModel
from typing import Optional, Any

class ResponseErrorSchema(BaseModel):
    success: bool = False
    message: str

class ResponseSuccessSchema(BaseModel):
    success: bool = True
    message: str
    data: Optional[Any] = None
```

### 3.7 Utilidades Varias

```python
# shared/utils/validate_email.py
import re

def validate_email(email: str) -> bool:
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return re.match(pattern, email) is not None
```

---

## 4. Rutas con Blueprints (Chalice)

### 3.3 Schemas de Respuesta

```python
# shared/schemas/response_schema.py
from pydantic import BaseModel
from typing import Optional, Any

class ResponseErrorSchema(BaseModel):
    success: bool = False
    message: str

class ResponseSuccessSchema(BaseModel):
    success: bool = True
    message: str
    data: Optional[Any] = None
```

### 3.4 Configuración de MySQL

```python
# shared/mysql/base.py
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
import os

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")
DB_HOST = os.environ.get("DB_HOST", "mysql")
DB_PORT = os.environ.get("DB_PORT", "3306")
DB_NAME = os.environ.get("DB_NAME")

DATABASE_URL = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}?charset=utf8mb4"

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()
```

```python
# shared/mysql/session_manager.py
from chalicelib.dddpy.shared.mysql.base import SessionLocal
from contextlib import contextmanager

@contextmanager
def session_scope():
    """Provides a transactional scope around a series of operations."""
    session = SessionLocal()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
```

---

## 4. Flujo Completo de una Solicitud

```
┌─────────────────────────────────────────────────────────────────┐
│                      REQUEST HTTP                               │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  @api_handler (Decorator)                                       │
│  - Loguea request                                              │
│  - Maneja excepciones                                          │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                           ▼
┌─────────────────────────────────────────────────────────────────┐
│  Usecase Unificado (e.g., LeadUseCase)                         │
│  - Orchestrates cmd + query                                     │
│  - Returns ResponseSuccessSchema                                │
└──────────────────────────┬──────────────────────────────────────┘
                           │
              ┌────────────┴────────────┐
              ▼                         ▼
┌─────────────────────────┐   ┌─────────────────────────┐
│  CMD Usecase            │   │  Query Usecase         │
│  (LeadCmdUseCase)       │   │  (LeadQueryUseCase)    │
│  - Lógica de escritura  │   │  - Lógica de lectura   │
└───────────┬─────────────┘   └───────────┬─────────────┘
            │                             │
            ▼                             ▼
┌─────────────────────────┐   ┌─────────────────────────┐
│  CMD Repository         │   │  Query Repository      │
│  (LeadCmdRepository)    │   │  (LeadQueryRepository) │
└───────────┬─────────────┘   └───────────┬─────────────┘
            │                             │
            ▼                             ▼
┌─────────────────────────┐   ┌─────────────────────────┐
│  Infrastructure         │   │  Infrastructure        │
│  (LeadCmdRepositoryImpl)│   │  (LeadQueryRepository) │
└───────────┬─────────────┘   └───────────┬─────────────┘
            │                             │
            ▼                             ▼
┌─────────────────────────────────────────────────────────────────┐
│  SQLAlchemy Model (DBLeads)                                     │
│  ↔ MySQL Database                                               │
└─────────────────────────────────────────────────────────────────┘
```

---

## 4. Rutas con Blueprints (Chalice)

### 4.1 Estructura de Rutas

```
src/chalicelib/api/
├── routing/
│   ├── __init__.py
│   └── routes_routing.py
├── lead/
│   ├── __init__.py
│   └── routes_lead.py
└── campaigns/
    ├── __init__.py
    └── routes_campaigns.py
```

### 4.2 Definir Rutas con Blueprint

```python
# api/routing/routes_routing.py
from chalice import Blueprint, Response
from pydantic import ValidationError

from chalicelib.dddpy.shared.decorators.api_handler import api_handler
from chalicelib.dddpy.shared.logging.logging import Logger
from chalicelib.dddpy.routing.usecase.routing_usecase import RoutingUsecase
from chalicelib.dddpy.routing.usecase.routing_cmd_schema import LeadRoutingSchema

import boto3
import os

name_app_sqs = os.environ.get("SQS_ROUTING_NAME")
sqs = boto3.client("sqs", region_name=os.environ.get("SQS_ROUTING_REGION"))
queue_url = os.environ.get("SQS_ROUTING_URL")

logger = Logger("condo - Routing")

PREFIX = "/api/v1"

routing_routes = Blueprint(__name__)


@routing_routes.route(f"{PREFIX}/health", methods=["GET"])
def health_check() -> Response:
    return Response(status_code=200, body={"status": "healthy"})


@routing_routes.route(f"{PREFIX}/execute", methods=["POST"], cors=True)
@api_handler
def execute_routing() -> Response:
    logger.add_inside_method("execute_routing Route")
    logger.info("Received routing execution request")
    
    request = routing_routes.current_request
    data = LeadRoutingSchema.parse_obj(request.json_body)
    
    response = RoutingUsecase().execute_by_id_lead(data)
    return response.dict()


# SQS Event Handler
@routing_routes.on_sqs_message(queue=name_app_sqs)
def sqs_routing_execute(event):
    logger.add_inside_method("sqs_routing_execute")
    for record in event:
        try:
            message_body = record.body
            json_id = message_body
            logger.info(f"Processing SQS message for lead: {json_id}")
            data = LeadRoutingSchema.parse_obj({"id_lead": json_id})
            response = RoutingUsecase().execute_by_id_lead(data)
            logger.info(f"Execution result: {response}")
        except Exception as e:
            logger.error(f"Error processing SQS message: {e}")
```

### 4.3 Registrar Blueprint en app.py

```python
# app.py
from chalice import Chalice, Response
import os

from chalicelib.api.routing.routes_routing import routing_routes
from chalicelib.api.lead.routes_lead import lead_routes
from chalicelib.dddpy.shared.logging.logging import Logger

app = Chalice(app_name='condo-api')
logger = Logger('app')

# Middleware global
@app.middleware('http')
def verify_headers(event, get_response):
    request_headers = event.headers or {}
    api_user = request_headers.get('API_USER')
    api_key = request_headers.get('API_KEY')
    expected_user = os.environ.get('API_USER')
    expected_key = os.environ.get('API_KEY')

    if api_user != expected_user or api_key != expected_key:
        return Response(status_code=401, body={"error": "Unauthorized"})

    return get_response(event)

# Registrar Blueprints
app.register_blueprint(routing_routes)
app.register_blueprint(lead_routes)

@app.route('/')
def index():
    return {'hello': 'condo'}
```

---

## 5. Ejemplo: Crear un Nuevo Módulo

### Paso 1: Estructura de Carpetas
```
src/chalicelib/dddpy/
└── mi_modulo/
    ├── domain/
    │   ├── __init__.py
    │   ├── mi_modulo.py           # Entidad
    │   ├── mi_modulo_exception.py  # Excepciones
    │   ├── mi_modulo_success.py    # Mensajes
    │   └── mi_modulo_repository.py # Interfaces
    ├── infrastructure/
    │   ├── __init__.py
    │   ├── mi_modulo.py           # Modelo SQLAlchemy
    │   ├── mi_modulo_cmd_repository.py
    │   └── mi_modulo_query_repository.py
    └── usecase/
        ├── __init__.py
        ├── mi_modulo_cmd_schema.py
        ├── mi_modulo_query_schema.py
        ├── mi_modulo_cmd_usecase.py
        ├── mi_modulo_query_usecase.py
        ├── mi_modulo_factory.py
        └── mi_modulo_usecase.py
```

### Paso 2: Definir el Modelo SQLAlchemy
```python
# infrastructure/mi_modulo.py
from sqlalchemy import Column, Integer, String, DateTime
from chalicelib.dddpy.shared.mysql.base import Base

class DBDatos(Base):
    __tablename__ = "mitabla"
    
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100), nullable=False)
    estado = Column(Integer, default=1)
    created_at = Column(DateTime)
    updated_at = Column(DateTime)
```

### Paso 3: Definir la Entidad
```python
# domain/mi_modulo.py
from datetime import datetime
from typing import Optional
from chalicelib.dddpy.infrastructure.mi_modulo import DBDatos

class MiModulo:
    def __init__(self, id: int, nombre: str, estado: int):
        self.id = id
        self.nombre = nombre
        self.estado = estado
    
    @classmethod
    def from_db(cls, db: DBDatos) -> 'MiModulo':
        return cls(id=db.id, nombre=db.nombre, estado=db.estado)
    
    def to_dict(self):
        return {"id": self.id, "nombre": self.nombre}
```

### Paso 4: Definir Excepciones
```python
# domain/mi_modulo_exception.py
from chalicelib.dddpy.shared.decorators.domain_exception import DomainException

class MiModuloNotFoundException(DomainException):
    def __init__(self):
        super().__init__(message="Registro no encontrado", status_code=404)
```

### Paso 5: Implementar Repositorios
```python
# infrastructure/mi_modulo_cmd_repository.py
from chalicelib.dddpy.domain.mi_modulo import MiModulo
from chalicelib.dddpy.domain.mi_modulo_repository import MiModuloRepository
from chalicelib.dddpy.infrastructure.mi_modulo import DBDatos
from chalicelib.dddpy.shared.mysql.session_manager import session_scope

class MiModuloCmdRepositoryImpl(MiModuloRepository):
    def create(self, data: dict) -> MiModulo:
        with session_scope() as session:
            db = DBDatos(**data)
            session.add(db)
            session.commit()
            return MiModulo.from_db(db)
```

### Paso 6: Definir Schemas
```python
# usecase/mi_modulo_cmd_schema.py
from pydantic import BaseModel
from typing import Optional

class CreateMiModuloSchema(BaseModel):
    nombre: str

class MiModuloResponseSchema(BaseModel):
    id: int
    nombre: str
    estado: int
```

### Paso 7: Implementar Usecases
```python
# usecase/mi_modulo_cmd_usecase.py
from chalicelib.dddpy.mi_modulo.domain.mi_modulo import MiModulo
from chalicelib.dddpy.mi_modulo.usecase.mi_modulo_cmd_schema import CreateMiModuloSchema

class MiModuloCmdUseCase:
    def __init__(self, repository):
        self.repository = repository
    
    def create(self, data: CreateMiModuloSchema) -> MiModulo:
        return self.repository.create(data.model_dump())
```

### Paso 8: Crear Factory
```python
# usecase/mi_modulo_factory.py
from chalicelib.dddpy.mi_modulo.usecase.mi_modulo_cmd_usecase import MiModuloCmdUseCase
from chalicelib.dddpy.mi_modulo.usecase.mi_modulo_query_usecase import MiModuloQueryUseCase
from chalicelib.dddpy.mi_modulo.infrastructure.mi_modulo_cmd_repository import MiModuloCmdRepositoryImpl
from chalicelib.dddpy.mi_modulo.infrastructure.mi_modulo_query_repository import MiModuloQueryRepositoryImpl

def mi_modulo_cmd_factory() -> MiModuloCmdUseCase:
    return MiModuloCmdUseCase(MiModuloCmdRepositoryImpl())

def mi_modulo_query_factory() -> MiModuloQueryUseCase:
    return MiModuloQueryUseCase(MiModuloQueryRepositoryImpl())
```

### Paso 9: Crear Usecase Unificado
```python
# usecase/mi_modulo_usecase.py
from chalicelib.dddpy.mi_modulo.usecase.mi_modulo_factory import (
    mi_modulo_cmd_factory,
    mi_modulo_query_factory,
)
from chalicelib.dddpy.shared.logging.logging import Logger

logging = Logger("mi_modulo_usecase")

class MiModuloUseCase:
    def __init__(self):
        self.cmd = mi_modulo_cmd_factory()
        self.query = mi_modulo_query_factory()
    
    def create(self, data):
        return self.cmd.create(data)
    
    def get_by_id(self, id):
        return self.query.get_by_id(id)
```

---

## 6. Logging: Importancia para Debug

El sistema de logging permite:

1. **Trace completo** de cada request
2. **Debugging** de errores en producción
3. **Auditoría** de operaciones
4. **Monitoreo** del flujo del sistema

**Niveles:**
- `logging.info()` - Procesos normales
- `logging.warning()` - Situaciones anómalas pero manejables
- `logging.error()` - Errores que requieren atención
- `logging.debug()` - Información detallada para debug

**Patrón de uso:**
```python
logging = Logger("mi_modulo")

def mi_funcion():
    logging.add_inside_method("mi_funcion")
    logging.info("Iniciando...")
    try:
        # lógica...
        logging.info("Completado exitosamente")
    except Exception as e:
        logging.error(f"Error: {e}")
        raise
```

---

*Guía generada automáticamente basada en la arquitectura de chalice-zatanna.routing y chalice-aca_health.insert-python*
