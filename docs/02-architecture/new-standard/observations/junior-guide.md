# Guía para un developer junior humano

Si acabas de entrar a este proyecto, esto es lo más importante que debes entender.

---

## 1. No vengas a “meter features” a ciegas
Primero entiende esto:
- el proyecto es un microservicio de leads,
- no un backend generalista,
- no un playground,
- no un lugar para meter cualquier lógica de negocio nueva sin criterio.

### Regla
Antes de cambiar algo, pregúntate:

> ¿Esto ayuda al flujo principal de intake → routing → log → status?

Si la respuesta es no, probablemente estás intentando meter otra responsabilidad que no pertenece aquí.

---

## 2. Aprende el flujo principal primero
Debes entender este pipeline antes de tocar código:

```text
API → LeadUseCase.create() → persistencia → SQS
SQS → ExecuteUseCase → integración externa → routing log → update status
```

Si no entiendes ese flujo, cualquier cambio puede romper cosas aunque compile.

---

## 3. No copies malas prácticas viejas
Que un patrón haya existido antes no significa que debas repetirlo.

Ejemplos de cosas que se corrigieron o se quieren evitar:
- `print()` en flujo productivo
- errores genéricos para negocio
- números mágicos
- dominio importando `DB*`
- contratos implícitos no documentados

### Regla
No copies una práctica solo porque la viste en un archivo antiguo.
Mira si ya fue marcada como deuda técnica.

---

## 4. Antes de tocar una capa, entiende su rol

### Si tocas `domain/`
Pregúntate:
- ¿esto es realmente negocio?
- ¿es una regla o una invariante?
- ¿estoy evitando dependencias técnicas?

### Si tocas `usecase/`
Pregúntate:
- ¿esto es orquestación?
- ¿coordino pasos o estoy metiendo demasiada lógica técnica aquí?

### Si tocas `infrastructure/`
Pregúntate:
- ¿esto es persistencia, mapping o integración?
- ¿estoy evitando que esta capa decida reglas de negocio?

---

## 5. Qué debes copiar
Sí conviene copiar estos principios:
- usar logging consistente
- usar excepciones semánticas
- usar estados explícitos
- respetar ownership de transacciones
- documentar cambios en `docs/technica-debt/` y `docs/observations/` cuando sean relevantes

---

## 6. Qué no debes copiar
No conviene copiar:
- viejos patrones acoplados al ORM
- decisiones de negocio metidas en infraestructura
- magia numérica
- código que “funciona” pero no explica nada

---

## 7. Cómo pensar una mejora
Cuando quieras proponer un cambio, explícalo así:

1. **problema observado**
2. **por qué es un problema**
3. **qué capa debería resolverlo**
4. **qué beneficio concreto produce**

Si puedes explicarlo así, normalmente entiendes bien lo que vas a tocar.
Si no puedes, todavía te falta analizar el tablero.

---

## 8. Qué hacer si dudas
Si dudas entre dos sitios para poner una lógica, usa esta guía:

### Si es una regla del negocio
→ `domain`

### Si es una secuencia de pasos
→ `application/usecase`

### Si es una llamada técnica a DB/API/cola
→ `infrastructure`

### Si sigue sin estar claro
→ documenta primero y no improvises.

---

## 9. Mentalidad correcta
No intentes ser “rápido” rompiendo arquitectura.
Intenta ser útil sin ensuciar el reino.

La velocidad falsa crea deuda.
La velocidad con criterio crea sistemas fuertes.

---

## 10. Resumen final
Si eres junior, quédate con esto:

- entiende el flujo principal,
- no mezcles capas,
- no copies deuda técnica vieja,
- documenta por qué cambias algo,
- y recuerda que una buena arquitectura no es la que solo compila,
- sino la que otro humano puede entender y extender sin romperla.

Ese es el verdadero examen.
