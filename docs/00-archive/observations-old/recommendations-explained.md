# Recomendaciones para `condo-py` explicadas en lenguaje humano

Este archivo resume recomendaciones arquitectónicas vigentes para el proyecto tomando como base la estructura `shared/` + `example/` + `api/`.

---

## 1. Tratar `example` como módulo patrón

### Recomendación
Usar `src/library/dddpy/example/` como referencia práctica para construir módulos nuevos.

### Por qué
Porque ahora mismo es la estructura base más cercana al estándar deseado.

### Beneficio
- menos improvisación,
- más consistencia entre módulos,
- onboarding más claro,
- menor costo para humanos y agentes.

---

## 2. Mantener el mapper como frontera DB ↔ dominio

### Recomendación
La traducción entre `DB*` y entidad de dominio debe vivir en `infrastructure/*_mapper.py`.

### Por qué
Porque el dominio no debe depender del ORM para existir.

### Beneficio
- más pureza de dominio,
- mejor testabilidad,
- menos acoplamiento técnico.

---

## 3. Usar `DomainException` como base común de errores semánticos

### Recomendación
Toda excepción de negocio concreta debe heredar de `shared.decorators.domain_exception.DomainException`.

### Por qué
Porque así el sistema tiene una base compartida para:
- mensaje,
- status code,
- manejo consistente en el borde.

### Beneficio
- menos `Exception` genérica,
- menos `ValueError` accidental,
- mejor integración con `@api_handler`.

---

## 4. Mantener exceptions concretas dentro de `domain/`

### Recomendación
Las excepciones específicas del módulo deben vivir en `domain/*_exception.py`.

### Por qué
Porque pertenecen a la semántica del negocio, no a la infraestructura ni al framework.

### Beneficio
- ownership claro,
- mejor lectura del dominio,
- menos contaminación técnica.

---

## 5. Estandarizar respuestas con schemas compartidos

### Recomendación
Usar `ResponseSuccessSchema` y `ResponseErrorSchema` como contrato de salida común.

### Por qué
Porque la estructura de éxito/error no debe cambiar caprichosamente entre módulos.

### Beneficio
- consistencia en respuestas,
- menos ambigüedad para consumidores,
- mejor predictibilidad.

---

## 6. Dejar la API limpia con `@api_handler`

### Recomendación
Las rutas deben limitarse a:
- obtener request,
- parsear schema,
- llamar use case,
- devolver `response.dict()`.

### Por qué
Porque el manejo de errores ya está centralizado en `@api_handler`.

### Beneficio
- menos repetición,
- rutas más legibles,
- menor mezcla de responsabilidades,
- mejor trazabilidad.

---

## 7. Permitir que el use case devuelva `ResponseSuccessSchema`

### Recomendación
En este proyecto, el camino de éxito debe salir del use case/fachada como `ResponseSuccessSchema`.

### Por qué
Porque así la API solo adapta la request y entrega el resultado, mientras el contrato de éxito sigue uniforme.

### Beneficio
- borde más limpio,
- contrato estable,
- menos lógica repetida en routes.

### Aclaración importante
Esto no es una impureza accidental.
Es una decisión deliberada del proyecto.

---

## 8. Mantener repositorios abstractos en `domain` y repositorios concretos en `infrastructure`

### Recomendación
Los contratos deben vivir en el dominio y la implementación técnica en infraestructura.

### Por qué
Porque el dominio debe expresar qué necesita, no cómo se persiste.

### Beneficio
- menor acoplamiento,
- mejor reemplazabilidad,
- diseño más limpio.

### Aclaración arquitectónica importante
En este proyecto se mantiene deliberadamente esta tríada:
- `Repository`
- `CmdRepository`
- `QueryRepository`

`Repository` no es redundancia decorativa.
Se entiende como el **repositorio agregado del módulo**.

Eso significa que existe para modelar capacidades que:
- no encajan limpiamente en solo cmd o query,
- combinan varias intenciones,
- o aparecen en sistemas donde la lógica custom pesa más que la DB como pieza central.

La existencia del contrato agregado comunica la visión del proyecto: el módulo puede tener semántica y capacidades más amplias que un CRUD estrecho.

---

## 9. Mantener factories en `usecase`

### Recomendación
El ensamblaje de repositorios concretos con use cases debe centralizarse en factories del módulo.

### Por qué
Porque el wiring disperso es deuda silenciosa.

### Beneficio
- composición explícita,
- menos repetición,
- mejor mantenibilidad.

---

## 10. Proteger `shared/`

### Recomendación
`shared/` debe contener solo piezas realmente transversales.

### Por qué
Porque si todo termina en `shared/`, ya no existe frontera real.

### Beneficio
- arquitectura más legible,
- menos desorden,
- ownership más claro.

---

## 11. Escribir también para agentes de IA

### Recomendación
Mantener `docs/BULMA/` actualizado cada vez que cambie el patrón base del proyecto.

### Por qué
Porque la IA necesita instrucciones compactas, no solo documentación narrativa.

### Beneficio
- menos consumo de contexto,
- menos errores por interpretación,
- más velocidad de ejecución.

---

## 12. Regla final

Cada módulo nuevo debería poder responder claramente estas preguntas:

1. ¿Dónde vive la entidad?
2. ¿Dónde viven las exceptions?
3. ¿Dónde vive el mapper?
4. ¿Dónde vive el éxito estructurado?
5. ¿Dónde vive el error estructurado?
6. ¿Qué hace la API y qué no hace?
7. ¿Qué resuelve `@api_handler`?

Si eso no está claro, el módulo todavía no está listo para entrar al reino.
