# Observaciones de arquitectura sobre `condo-py`

## 1. Qué tipo de sistema es este

`condo-py` es un backend modular para gestión de entidades condominiales.
No es un framework interno, no es una plataforma horizontal, y no debería evolucionar como un contenedor indiscriminado de lógica administrativa.

Su centro actual gira alrededor de:

- condominios,
- edificios,
- tipos,
- unidades,
- usuarios,
- relaciones de residentes.

### ¿Por qué esto importa?
Porque si el equipo olvida la misión del sistema, empieza a meter cualquier responsabilidad nueva y el proyecto se vuelve un laberinto de CRUDs sin semántica.

---

## 2. Qué tiene de bueno hoy

El proyecto ya muestra varias decisiones correctas:

- separación por módulos,
- entrypoints HTTP claramente identificables,
- capa `usecase/` para orquestación,
- `domain/` separado de `infrastructure/`,
- uso de mappers en al menos parte del flujo,
- respuesta HTTP estandarizada con `ResponseSchema`.

### ¿Por qué eso vale?
Porque no estás partiendo de un caos plano.
Hay intención arquitectónica.
Y eso significa que todavía puede ganarse la partida sin destruir el tablero.

---

## 3. Qué problemas importantes siguen visibles

## 3.1 Naming inconsistente
El proyecto mezcla nombres como:

- `unitys`
- `unittys_types`
- `users`
- `core_users`
- `users_residents`
- `core_users_residents`

### ¿Por qué es un problema?
Porque el naming inconsistente no solo se ve feo. También:

- dificulta navegar el código,
- vuelve incierto dónde vive cada responsabilidad,
- induce a crear más duplicidad,
- complica la documentación y el onboarding.

### Recomendación
No corregir esto “de pasada” durante features normales. Si se va a arreglar, que sea una iniciativa intencional y bien acotada.

---

## 3.2 Dominio todavía delgado
Hay entidades con algo de comportamiento, pero en general el dominio aún no gobierna suficientes reglas.

### ¿Por qué importa?
Porque si las entidades solo cargan datos, la semántica termina dispersa en use cases, routers o repositorios.
Y cuando la semántica se dispersa, nadie sabe realmente quién manda.

### Recomendación
Enriquecer el dominio gradualmente con:

- invariantes,
- transiciones de estado,
- validaciones de negocio,
- value objects cuando añadan semántica real.

---

## 3.3 Riesgo de DDD ceremonial
La estructura de carpetas sugiere DDD, pero una estructura bonita no garantiza arquitectura sana.

### ¿Por qué es un riesgo?
Porque puedes terminar con:

- muchas carpetas,
- muchos archivos,
- poca claridad real,
- y cero autoridad del dominio.

### Recomendación
Medir el éxito no por cantidad de capas, sino por la calidad de las fronteras y por cuánto sobrevive el diseño a cambios futuros.

---

## 3.4 Shared puede volverse basurero
`shared/` es útil, pero siempre está a una mala decisión de convertirse en el cementerio imperial de todo lo incómodo.

### ¿Por qué importa?
Porque cuando una pieza no encaja y siempre la mandas a `shared/`, dejas de diseñar.
Solo escondes el problema.

### Recomendación
Aceptar en `shared/` solo piezas realmente transversales:

- db/session,
- logging,
- response schemas,
- constantes compartidas,
- utilidades reutilizables de verdad.

---

## 4. Qué está razonablemente bien planteado

### 4.1 FastAPI como entrypoint
Los routers están actuando como borde HTTP y eso es correcto.

### 4.2 Use cases como capa de aplicación
La idea de separar command/query y exponer una fachada es defendible cuando mantiene claridad.

### 4.3 Mappers en infraestructura
Mover traducciones DB ↔ dominio a infraestructura es una señal de madurez arquitectónica.

---

## 5. Qué sigue faltando

Todavía faltan pasos importantes para que el proyecto deje de parecer “DDD por carpetas” y se convierta en DDD útil:

- más semántica en entidades,
- mejor definición de agregados y límites,
- aclarar la historia entre módulos `core_*` y no `core_*`,
- formalizar mejor las reglas para nuevas features.

---

## 6. Lección final

El valor del proyecto no está en que tenga carpetas llamadas `domain`.
El valor está en que cada capa sepa cuál es su reino y no invada el ajeno.

La arquitectura sana no se mide por ceremonia.
Se mide por control del tablero.
