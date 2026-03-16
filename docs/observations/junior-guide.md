# Guía para un developer junior en `condo-py`

Si acabas de entrar al proyecto, no empieces metiendo cambios a ciegas.
Primero entiende el tablero.

---

## 1. Aprende el flujo principal

Antes de tocar código, entiende esta secuencia:

```text
HTTP → router → schema → usecase → repository → mapper → DB → response
```

Si no entiendes ese flujo, es fácil romper algo sin darte cuenta.

---

## 2. No confundas carpetas con arquitectura

Que exista `domain/` no significa automáticamente que toda la lógica esté bien puesta.
Debes mirar responsabilidad real, no solo nombres bonitos.

---

## 3. Antes de tocar una capa, pregúntate

### Si tocas `api/`
¿Estoy adaptando HTTP o metiendo negocio donde no va?

### Si tocas `usecase/`
¿Estoy coordinando pasos o estoy absorbiendo demasiada lógica?

### Si tocas `domain/`
¿Esto representa una regla del negocio de verdad?

### Si tocas `infrastructure/`
¿Esto es persistencia/mapping o estoy decidiendo negocio desde lo técnico?

---

## 4. Qué sí conviene copiar

- uso de mappers para separar ORM y dominio,
- respuesta estándar con `ResponseSchema`,
- separación router/usecase/domain/infrastructure,
- documentación explícita de decisiones.

---

## 5. Qué no conviene copiar

- naming legacy sin entender su historia,
- código repetido por conveniencia,
- lógica de negocio dentro del router,
- meter cosas en `shared/` solo porque no sabes dónde van.

---

## 6. Cómo proponer un cambio sano

Explícalo así:

1. qué problema ves,
2. por qué afecta la arquitectura,
3. en qué capa debería resolverse,
4. qué beneficio trae.

Eso separa a quien improvisa de quien diseña.

---

## 7. Regla final

No intentes ser rápido sacrificando estructura.
La velocidad falsa crea deuda.
La velocidad con criterio gana partidas largas.
