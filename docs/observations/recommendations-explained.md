# Recomendaciones para `condo-py` explicadas en lenguaje humano

Este archivo resume recomendaciones arquitectónicas vigentes para el proyecto tomando como base la nueva estructura `shared/` + `campaigns/`.

---

## 1. Tratar `campaigns` como módulo patrón

### Recomendación
Usar `src/library/dddpy/campaigns/` como referencia práctica para construir módulos nuevos.

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

### Ejemplo real
`CampaignMapper` expone:
- `to_domain(...)`
- `to_infrastructure(...)`

Eso deja clara la frontera entre representación técnica y semántica.

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
- semántica de error más clara,
- mejor integración con decorators o handlers compartidos.

### Ejemplo real
- `CampaignNotFound`
- `RepeatedCampaignMediaCode`

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
- menos ambigüedad para frontend o consumidores,
- menos esfuerzo mental al navegar el sistema.

---

## 6. Mantener success messages consistentes

### Recomendación
Los mensajes de éxito deben seguir una convención estable y semántica.

### Por qué
Porque si cada módulo responde con estilos distintos, el sistema pierde coherencia.

### Beneficio
- mejor UX técnica,
- mejor predictibilidad,
- menos ruido en respuestas.

### Criterio sugerido
Preferir mensajes como:
- `Campaign created successfully`
- `Campaign updated successfully`
- `Campaign deleted successfully`

No por liturgia, sino por disciplina.

---

## 7. Mantener repositorios abstractos en `domain` y repositorios concretos en `infrastructure`

### Recomendación
Los contratos deben vivir en el dominio y la implementación técnica en infraestructura.

### Por qué
Porque el dominio debe expresar qué necesita, no cómo se persiste.

### Beneficio
- menor acoplamiento,
- mejor reemplazabilidad,
- diseño más limpio.

---

## 8. Mantener factories en `usecase`

### Recomendación
El ensamblaje de repositorios concretos con use cases debe centralizarse en factories del módulo.

### Por qué
Porque el wiring disperso es deuda silenciosa.

### Beneficio
- composición explícita,
- menos repetición,
- mejor mantenibilidad.

---

## 9. Proteger `shared/`

### Recomendación
`shared/` debe contener solo piezas realmente transversales.

### Por qué
Porque si todo termina en `shared/`, ya no existe frontera real.

### Beneficio
- arquitectura más legible,
- menos desorden,
- ownership más claro.

---

## 10. Escribir también para agentes de IA

### Recomendación
Mantener `docs/BULMA/` actualizado cada vez que cambie el patrón base del proyecto.

### Por qué
Porque la IA necesita instrucciones compactas, no solo documentación narrativa.

### Beneficio
- menos consumo de contexto,
- menos errores por interpretación,
- más velocidad de ejecución.

---

## 11. Regla final

Cada módulo nuevo debería poder responder claramente estas preguntas:

1. ¿Dónde vive la entidad?
2. ¿Dónde viven las exceptions?
3. ¿Dónde viven los contratos?
4. ¿Dónde vive el mapper?
5. ¿Dónde viven los repositorios concretos?
6. ¿Dónde vive la factory?
7. ¿Qué response schema usa?

Si eso no está claro, el módulo todavía no está listo para entrar al reino.
