# Observaciones de arquitectura sobre `condo-py`

## 1. Qué tipo de sistema es este

`condo-py` no debe leerse hoy como un backend CRUD tradicional ni como una colección de módulos legacy.
La arquitectura activa del proyecto está pivotando hacia una base más explícita y reusable formada por:

- `shared/` como capa transversal,
- `example/` como módulo plantilla,
- `api/example/` como demostración del borde limpio con decorador.

### ¿Por qué esto importa?
Porque el objetivo actual ya no es solo “tener endpoints que funcionen”, sino dejar una base doctrinal que otros developers y agentes puedan copiar sin reintroducir caos.

---

## 2. Qué tiene de bueno hoy

El proyecto ya muestra varias decisiones correctas:

- separación clara entre `domain`, `usecase`, `infrastructure` y `shared`,
- mapper explícito en infraestructura,
- `DomainException` como contrato semántico de error,
- `ResponseSuccessSchema` / `ResponseErrorSchema` como contrato común,
- `@api_handler` como adaptación transversal de errores en API,
- logger compartido para trazabilidad,
- presencia de `example/` como plantilla reusable.

### ¿Por qué eso vale?
Porque no estás documentando teoría vacía.
Ya hay una línea de diseño real que puede replicarse.

---

## 3. Qué decisiones arquitectónicas son centrales

## 3.1 La API debe quedar limpia
La función de route no debe volverse un pequeño framework de manejo de errores.
Su trabajo es:

- parsear schema,
- llamar use case,
- devolver `response.dict()`.

El resto del camino de error le pertenece a `@api_handler`.

---

## 3.2 El camino de éxito sale del use case
En esta arquitectura, el use case/fachada devuelve `ResponseSuccessSchema` deliberadamente.

### ¿Por qué importa?
Porque esta decisión simplifica el borde HTTP y deja consistente el contrato de éxito.
No es una impureza accidental. Es una convención del proyecto.

---

## 3.3 El camino de error sale del dominio
Las fallas semánticas se expresan como `DomainException` o derivadas.

### ¿Por qué importa?
Porque así el sistema habla en términos de negocio cuando falla, y `@api_handler` puede traducir eso a `ResponseErrorSchema` con `status_code` correcto.

---

## 3.4 Existen tres contratos de repositorio a propósito
La arquitectura mantiene:

- `Repository`
- `CmdRepository`
- `QueryRepository`

### ¿Por qué esto importa?
Porque el proyecto no está diseñado solo para CRUD estrecho.
`Repository` existe como **repositorio agregado del módulo** para casos donde la capacidad del módulo no cabe limpiamente en solo lectura o solo escritura.

Eso comunica una visión importante: la DB puede ser soporte, no siempre centro del diseño.

---

## 4. Qué riesgos siguen existiendo

## 4.1 Shared puede volverse basurero
Sigue siendo un riesgo clásico. `shared/` debe contener piezas transversales, no atajos para ownership confuso.

## 4.2 Los módulos futuros podrían copiar la forma y olvidar la intención
Tener carpetas correctas no basta.
Si alguien copia `example/` pero ignora:

- el rol de `DomainException`,
- el rol de `@api_handler`,
- el contrato del `Repository` agregado,
- o la responsabilidad del use case,

entonces el diseño vuelve a degradarse.

## 4.3 La disciplina de logging debe mantenerse
El logger ya está mejor planteado, pero su valor depende de que los developers lo usen para trazabilidad real, no para ruido.

---

## 5. Qué sigue faltando

Todavía pueden mejorarse cosas, pero ya no en el nivel de “arquitectura rota”, sino de refinamiento:

- reforzar la disciplina de uso del repositorio agregado,
- extender el patrón limpio a nuevos módulos reales,
- mantener documentación y código sincronizados,
- seguir evitando que legacy vuelva a colonizar la base nueva.

---

## 6. Lección final

El valor del proyecto ya no está en tener nombres bonitos de carpetas.
El valor está en esta secuencia clara:

- el dominio expresa semántica,
- el use case orquesta y devuelve el éxito,
- la infraestructura implementa,
- `shared` estandariza,
- la API queda limpia,
- y el decorador captura el error.

Eso sí es control del tablero.
