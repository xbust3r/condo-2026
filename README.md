# Sistema de Gestión para Condominios - Documentación Técnica

> **Proyecto Original:** `~/servers/condo-laravel` (Laravel PHP)
> 
> **Estado Actual:** ~10% completado
> 
> **Próxima Iteración:** Conversión a Python (pendiente)
> 
> **Fecha de Documentación:** Marzo 2026

---

## 1. Visión General del Proyecto

### 1.1 Descripción
Sistema de gestión integral para condominios que permite administrar residentes, áreas comunes, finanzas, visitantes, seguridad y comunicación entre administrador y propietarios.

### 1.2 Tecnologías del Original (Laravel)
- **Framework:** Laravel 5.x / 6.x
- **ORM:** Eloquent
- **Autenticación:** JWT (tymon/jwt-auth) + Session tradicional
- **Frontend:** Blade Templates + Theme system
- **Módulos:** Arquitectura modular (app/Modules)

---

## 2. Arquitectura Modular

### 2.1 Módulos Existentes

| Módulo | Propósito | Estado |
|--------|-----------|--------|
| **Core** | Modelos base compartidos | Básico |
| **Heimdall** | Gestión de usuarios, roles, permisos, autenticación | Principal |
| **M7vBlack** | Interfaz de administración (themes, layouts) | UI |
| **Continental** | (Por definir) | Inicial |
| **Publico** | Portal público, login, dashboard público | Básico |

---

## 3. Modelos de Datos (Heimdall)

### 3.1 Tablas Identificadas

#### `heimdall_companies` - Empresas/Condominios
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BIGINT | PK |
| company | VARCHAR(255) | Nombre del condominio |
| code | VARCHAR(50) | Código identificador |
| description | TEXT | Descripción |

**Relaciones:**
- `users()` → hasMany(User::class)

---

#### `users` - Usuarios del Sistema
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BIGINT | PK |
| name | VARCHAR(255) | Nombre completo |
| email | VARCHAR(255) | Email (único) |
| password | VARCHAR(255) | Hash bcrypt |
| phone | VARCHAR(20) | Teléfono |
| avatar | VARCHAR(255) | URL avatar |
| linkedin | VARCHAR(255) | Perfil LinkedIn |
| facebook | VARCHAR(255) | Perfil Facebook |
| instagram | VARCHAR(255) | Perfil Instagram |
| twitter | VARCHAR(255) | Perfil Twitter |
| company_id | BIGINT | FK → heimdall_companies |
| occupation_id | BIGINT | FK → heimdall_occupations |
| active | TINYINT | Estado (1=activo) |
| remember_token | VARCHAR(100) | Token recordar sesión |

**Relaciones:**
- `Companies()` → belongsTo(Companies::class)
- `Occupations()` → belongsTo(Occupations::class)
- `From()` / `To()` → belongsTo(UsersMessages::class) - para mensajería
- `roles()` → belongsToMany(Role::class) - via shinobi
- `permissions()` → belongsToMany(Permission::class)

---

#### `heimdall_roles` - Roles
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BIGINT | PK |
| name | VARCHAR(255) | Nombre visible |
| slug | VARCHAR(255) | Identificador único |
| description | TEXT | Descripción |
| special | VARCHAR(50) | Rol especial (null/all/access) |

**Traits:**
- `RolTrait` - lógica de gestión de roles

---

#### `heimdall_permissions` - Permisos
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BIGINT | PK |
| name | VARCHAR(255) | Nombre visible |
| slug | VARCHAR(255) | Identificador único |
| description | TEXT | Descripción |

**Traits:**
- `PermissionTrait` - lógica de gestión de permisos

---

#### `heimdall_occupations` - Ocupaciones/Cargos
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BIGINT | PK |
| occupation | VARCHAR(255) | Nombre del cargo |
| description | TEXT | Descripción |

**Relaciones:**
- `users()` → hasMany(User::class)

---

#### `heimdall_modules` - Módulos del Sistema
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BIGINT | PK |
| name | VARCHAR(255) | Nombre del módulo |
| slug | VARCHAR(255) | Identificador |
| description | TEXT | Descripción |
| active | TINYINT | Estado |

---

#### `users_messages` - Mensajería Interna
| Campo | Tipo | Descripción |
|-------|------|-------------|
| id | BIGINT | PK |
| from | BIGINT | FK → users (remitente) |
| to | BIGINT | FK → users (destinatario) |
| subject | VARCHAR(255) | Asunto |
| message | TEXT | Contenido |
| read | TINYINT | Leído (0/1) |
| created_at | TIMESTAMP | Fecha envío |

---

### 3.2 Modelos del Módulo Core

#### `core_business_type` - Tipos de Negocio
#### `core_social` - Redes Sociales
#### `core_social_type` - Tipos de Red Social

---

## 4. Servicios (Heimdall/Services)

### 4.1 AuthService
**Propósito:** Gestión de autenticación JWT

**Métodos Principales:**
```php
signIn(email, password) → array[guards, meta, profile]
- Genera token JWT
- Mantiene sesión Laravel tradicional
- Retorna roles, permisos y perfil

removeLoginSession()
- Cierra sesión

validateToken(token) → array
- Valida token JWT

validateGuard(roles, permissions) → array
- Valida roles y permisos del usuario
```

### 4.2 UserService
**Propósito:** CRUD de usuarios

**Métodos Principales:**
```php
getUsers(cant?, basicSearch?, advanceSearch?) → Collection
- Lista usuarios con paginación
- Búsqueda por email, first_name, last_name
- Includes: roles, brands, agencies, reports

getUser(id) → User
- Obtiene usuario específico con relaciones

setUser(data) → User
- Crea nuevo usuario
- Hashea password
- Sincroniza roles

updateUser(data, id) → User
- Actualiza usuario
- Sincroniza roles, brands, agencies, reports
- Limpia cache

deleteUser(id) → User
- Elimina usuario

total() → int
- Cuenta usuarios activos
```

### 4.3 RoleService
**Propósito:** Gestión de roles

**Métodos:**
- `listAll()` - Lista todos los roles
- `create(data)` - Crea rol
- `update(data, id)` - Actualiza rol
- `delete(id)` - Elimina rol

### 4.4 PermissionService
**Propósito:** Gestión de permisos

**Métodos:**
- `listAll()` - Lista todos los permisos
- `create(data)` - Crea permiso
- `update(data, id)` - Actualiza permiso
- `delete(id)` - Elimina permiso

### 4.5 ProfileService
**Propósito:** Gestión de perfil de usuario

### 4.6 GroupService
**Propósito:** Gestión de grupos

### 4.7 MessageService
**Propósito:** Sistema de mensajería entre usuarios

---

## 5. Controladores (Heimdall/Http/Controllers)

### 5.1 AuthController
- `signIn()` - Login
- `signOut()` - Logout
- `me()` - Datos del usuario actual

### 5.2 UserController
- `listAll()` - Listado de usuarios
- `create()` - Formulario nuevo usuario
- `store(request)` - Guarda usuario
- `edit(id)` - Formulario edición
- `update(request, id)` - Actualiza usuario
- `delete(id)` - Formulario eliminación
- `destroy(id)` - Elimina usuario

### 5.3 RolesController
- `listAll()` - Listado de roles
- `create()` - Formulario nuevo rol
- `store(request)` - Guarda rol
- `edit(id)` - Formulario edición
- `update(request, id)` - Actualiza rol
- `destroy(id)` - Elimina rol

### 5.4 PermissionsController
- `listAll()` - Listado de permisos
- `create()` - Formulario nuevo permiso
- `store(request)` - Guarda permiso
- `edit(id)` - Formulario edición
- `update(request, id)` - Actualiza permiso
- `destroy(id)` - Elimina permiso

### 5.5 ProfileController
- `edit()` - Edición de perfil
- `update(request)` - Actualiza perfil

### 5.6 MessageController
- `index()` - Lista de mensajes
- `create()` - Enviar mensaje
- `read(id)` - Leer mensaje
- `delete(id)` - Eliminar mensaje

### 5.7 ModulesController
- `listAll()` - Listado de módulos
- `create()` - Crear módulo
- `edit(id)` - Editar módulo

### 5.8 DashboardController
- `index()` - Dashboard principal

---

## 6. Rutas (Heimdall/Routes)

### 6.1 Web Routes
```
/heimdall              - Dashboard
/heimdall/users        - Gestión usuarios
/heimdall/users/create - Crear usuario
/heimdall/users/{id}/edit - Editar usuario
/heimdall/users/{id}/delete - Eliminar usuario

/heimdall/roles        - Gestión roles
/heimdall/roles/create - Crear rol
/heimdall/roles/{id}/edit - Editar rol

/heimdall/permissions  - Gestión permisos
/heimdall/permissions/create - Crear permiso

/heimdall/modules      - Gestión módulos
/heimdall/profile      - Perfil usuario

/heimdall/messages     - Mensajería
```

### 6.2 API Routes
```
/api/auth/signin       - Login JWT
/api/auth/signout      - Logout
/api/auth/me          - Usuario actual

/api/users            - CRUD usuarios
/api/roles            - CRUD roles
/api/permissions      - CRUD permisos
/api/modules          - CRUD módulos
/api/messages         - Mensajería
```

---

## 7. Autenticación y Seguridad

### 7.1 Sistema de Auth
- **JWT:** `tymon/jwt-auth` para API REST
- **Session:** Laravel tradicional para web
- **Roles/Permisos:** `caffeinated/shinobi`

### 7.2 Flujo de Login
1. Usuario envía credentials (email/password)
2. AuthService.signIn() valida y genera JWT token
3. Mantiene sesión Laravel para compatibilidad
4. Retorna: token, roles, permisos, perfil

### 7.3 Validación de Acceso
- JWT token en header `Authorization: Bearer {token}`
- Validación de roles y permisos por middleware
- Protección de rutas por guards

---

## 8. Pendientes y Mejoras Identificadas

### 8.1 Modelos Pendientes
- [ ] Residents - Residentes/Unidades
- [ ] Properties - Propiedades/Unidades Habitacionales
- [ ] Expenses - Gastos/Cxp
- [ ] Income - Ingresos
- [ ] Areas - Áreas Comunes
- [ ] Reservations - Reservas de áreas
- [ ] Visitors - Visitantes
- [ ] Vehicles - Vehículos
- [ ] Payments - Pagos
- [ ] Announcements - Avisos/Comunicados

### 8.2 Servicios Pendientes
- [ ] ExpenseService - Gestión de gastos
- [ ] IncomeService - Gestión de ingresos
- [ ] AreaService - Gestión de áreas comunes
- [ ] ReservationService - Reservas
- [ ] VisitorService - Control de visitantes
- [ ] VehicleService - Gestión de vehículos
- [ ] PaymentService - Gestión de pagos
- [ ] NotificationService - Notificaciones

### 8.3 Módulos Pendientes
- [ ] Finanzas - Contabilidad del condominio
- [ ] Áreas - Reservas de áreas comunes
- [ ] Seguridad - Control de acceso y visitantes
- [ ] Comunicación - Avisos y announcements

---

## 9. Consideraciones para Conversión Python

### 9.1 Recomendaciones Técnicas
1. **ORM:** SQLAlchemy o Django ORM
2. **Auth:** Django JWT o Python-Jose
3. **API:** FastAPI o Django REST Framework
4. **Frontend:** Separar en React/Vue (no blade)

### 9.2 Estructura Sugerida Python
```
condo-py/
├── app/
│   ├── models/          # Modelos SQLAlchemy
│   ├── services/        # Servicios de negocio
│   ├── controllers/     # Endpoints API
│   ├── schemas/        # Pydantic models
│   └── auth/           # JWT handling
├── modules/            # Módulos plugables
├── database/           # Migraciones
└── requirements.txt
```

---

## 10. Diagrama de Relaciones (Simplificado)

```
┌─────────────────┐       ┌──────────────────┐
│    Companies    │       │    Occupations    │
└────────┬────────┘       └────────┬─────────┘
         │                        │
         │ 1:N                    │ 1:N
         ▼                        ▼
┌──────────────────────────────────────┐
│              Users                    │
│  (id, name, email, password, ...)    │
└──────────────┬───────────────────────┘
              │
              │ N:M (shinobi)
    ┌─────────┴─────────┐
    │                    │
    ▼                    ▼
┌─────────┐       ┌──────────────┐
│  Roles  │       │  Permissions │
└─────────┘       └──────────────┘
    │
    │ N:M
    ▼
┌──────────────────┐
│   Modules        │
└──────────────────┘
```

---

*Documento generado automáticamente del código fuente Laravel*
*Para la próxima iteración en Python*
