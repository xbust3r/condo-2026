# Recomendaciones para `condo-py` explicadas en lenguaje humano

Este archivo resume recomendaciones arquitectónicas vigentes para el proyecto.

---

## 1. Mantener FastAPI en el borde

### Recomendación
Los routers deben seguir siendo entrypoints y nada más.

### Por qué
Porque si el router empieza a decidir reglas de negocio o hablar con la DB, destruyes las fronteras.

### Beneficio
- menos acoplamiento al framework,
- más claridad,
- más facilidad para probar y evolucionar.

---

## 2. Fortalecer el dominio gradualmente

### Recomendación
Mover semántica real a entidades y value objects cuando tenga sentido.

### Por qué
Porque un dominio anémico obliga a meter lógica de negocio en lugares equivocados.

### Beneficio
- modelo más expresivo,
- reglas más visibles,
- menor dispersión de comportamiento.

---

## 3. No maquillar la deuda de naming

### Recomendación
Documentar nombres legacy e inconsistencias, pero no "arreglarlos" durante tareas funcionales si no hay plan explícito.

### Por qué
Porque refactor accidental + feature en la misma jugada = caos.

### Beneficio
- menor riesgo,
- cambios más auditables,
- menos roturas invisibles.

---

## 4. Proteger `shared/`

### Recomendación
Usar `shared/` solo para piezas verdaderamente transversales.

### Por qué
Porque cuando todo va a `shared/`, nada tiene frontera clara.

### Beneficio
- arquitectura más legible,
- menos basura estructural,
- mejor separación de responsabilidades.

---

## 5. Mantener mappers como frontera DB ↔ dominio

### Recomendación
La traducción entre modelos ORM y entidades debe vivir en infraestructura.

### Por qué
Porque el dominio no debe depender de SQLAlchemy para existir.

### Beneficio
- más pureza de dominio,
- mejor testabilidad,
- menor acoplamiento técnico.

---

## 6. Usar CQRS solo cuando ayude

### Recomendación
Separar command/query solo si mejora claridad, no por moda.

### Por qué
Porque si no aporta valor, solo duplica archivos y fatiga cognitiva.

### Beneficio
- menos ceremonia,
- más foco,
- mejor mantenimiento.

---

## 7. Escribir también para agentes de IA

### Recomendación
Mantener `docs/BULMA/` como capa táctica para automatización y edición asistida.

### Por qué
Porque una IA pierde contexto traduciendo prosa larga. Las reglas compactas reducen ambigüedad y costo.

### Beneficio
- menos consumo de contexto,
- menos errores por interpretación,
- más velocidad de ejecución.

---

## 8. Regla final

Cada mejora debería poder explicarse así:

1. problema observado,
2. por qué importa,
3. qué capa debe resolverlo,
4. qué deuda evita a futuro.

Si no puedes explicarlo así, todavía no has visto todo el tablero.
