# Recomendaciones explicadas y por qué se hicieron

Este archivo resume las principales recomendaciones hechas durante el análisis del proyecto y las explica en lenguaje directo.

---

## 1. Unificar logging

### Recomendación
Reemplazar `print()` por `Logger` y hacer consistente el logging del flujo principal.

### ¿Por qué?
Porque `print()` sirve para salir del paso, pero no para operar un sistema serio.

### Beneficios
- mejor trazabilidad,
- mejor debugging,
- menos ruido,
- más consistencia entre módulos.

### Lección
Lo que no puedes observar bien, no lo puedes mantener bien.

---

## 2. Limpiar imports y ruido técnico

### Recomendación
Eliminar imports duplicados, sin usar y artefactos de ruido.

### ¿Por qué?
Porque el desorden pequeño se acumula y vuelve más difícil leer el flujo.

### Beneficios
- menos fricción para developers,
- menos confusión,
- mejor legibilidad.

### Lección
La claridad visual también es una decisión arquitectónica.

---

## 3. Corregir excepciones de dominio

### Recomendación
Usar errores semánticos y no errores genéricos como `ValueError` para eventos de negocio.

### ¿Por qué?
Porque “algo salió mal” no es suficiente cuando quieres entender de verdad qué pasó.

### Beneficios
- errores más claros,
- mejores respuestas HTTP,
- menos ambigüedad,
- más semántica de negocio.

### Lección
Un sistema maduro falla diciendo la verdad, no escondiéndose detrás de errores genéricos.

---

## 4. Formalizar estados

### Recomendación
Eliminar números mágicos y usar constantes/enums para estados.

### ¿Por qué?
Porque `1`, `3`, `5`, `9` no cuentan ninguna historia por sí solos.

### Beneficios
- más claridad,
- menos errores humanos,
- mejor mantenimiento,
- mejor comunicación entre developers.

### Lección
Si el código necesita memoria tribal para entenderse, está perdiendo.

---

## 5. Definir dueño único de la transacción

### Recomendación
Dejar a `session_scope()` como owner oficial del commit.

### ¿Por qué?
Porque dos dueños para una transacción significan ambigüedad y bugs futuros.

### Beneficios
- modelo mental más claro,
- menos deuda invisible,
- mejor base para operaciones compuestas.

### Lección
En arquitectura, cuando dos piezas creen mandar al mismo tiempo, ya empezaste a perder.

---

## 6. Alinear el schema real del lead

### Recomendación
Hacer que el schema formal represente el payload real usado por la integración.

### ¿Por qué?
Porque si el schema dice una cosa y el flujo usa otra, el sistema está mintiendo.

### Beneficios
- menos errores tardíos,
- integración más estable,
- mejor comunicación entre backend y consumidores.

### Lección
El contrato de entrada debe describir la realidad, no una fantasía más bonita.

---

## 7. Hacer explícita la capa de aplicación

### Recomendación
Dejar más claro qué hace `LeadUseCase`, qué hace `ExecuteUseCase` y qué hacen los adapters externos.

### ¿Por qué?
Porque si las fronteras no están claras, el código termina mezclando todo.

### Beneficios
- mejor entendimiento del flujo,
- menos mezcla de responsabilidades,
- base más limpia para escalar el proyecto.

### Lección
Una arquitectura fuerte no solo funciona. También deja claro quién manda en cada tramo.

---

## 8. Desacoplar el dominio del ORM

### Recomendación
Sacar imports `DB*` del dominio y mover el mapeo a infraestructura.

### ¿Por qué?
Porque el dominio no debería depender de la base de datos para existir.

### Beneficios
- más pureza de dominio,
- mejor testabilidad,
- menos acoplamiento,
- mejor base para DDD real.

### Lección
Si el dominio obedece a la base de datos, entonces la base de datos es tu verdadero jefe.
Y eso es mala arquitectura.

---

## 9. Formalizar adapters externos

### Recomendación
Tratar integraciones como Leadspedia como adapters externos, no como parte del dominio central.

### ¿Por qué?
Porque el proveedor puede cambiar, fallar o multiplicarse.
Y no quieres contaminar tu negocio con esos detalles.

### Beneficios
- menos acoplamiento al provider,
- mejor escalabilidad,
- arquitectura más flexible.

### Lección
Tu dominio no debería hablar con acento del vendor.

---

## 10. Enriquecer el dominio después

### Recomendación
Luego de ordenar estructura y pureza, mover comportamiento real al dominio.

### ¿Por qué no se hizo primero?
Porque primero había que limpiar ruido, contratos y límites.
Si no, enriquecer el dominio encima del caos solo produce caos más sofisticado.

### Ejemplos futuros
- transiciones de estado del lead,
- éxito o fallo del routing log,
- fallback semántico de media code,
- invariantes propias de entidades.

### Lección
Primero orden. Luego profundidad.
Ese fue el orden correcto en este proyecto.
