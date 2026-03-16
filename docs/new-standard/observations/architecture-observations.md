# Observaciones de arquitectura

## 1. Qué tipo de sistema es este

Este proyecto es un **microservicio**.
No es un sistema monolítico enorme, ni un CRM completo, ni una plataforma generalista.

Su misión es concreta:
- recibir leads,
- guardarlos,
- disparar el routing por SQS,
- registrar lo que ocurrió,
- y actualizar estados.

### ¿Por qué esto importa?
Porque cuando un equipo olvida cuál es la misión del sistema, empieza a meter cualquier cosa dentro del mismo proyecto.
Y así nacen monstruos difíciles de mantener.

---

## 2. Qué tenía de bueno desde el inicio

Desde el análisis inicial, el proyecto ya mostraba cosas positivas:

- propósito de negocio claro,
- estructura modular,
- separación por capas,
- uso correcto de SQS para desacoplar el proceso,
- logs de routing para trazabilidad.

### ¿Por qué eso era valioso?
Porque la base no estaba improvisada.
No era un caos total.
Era una arquitectura con intención, aunque todavía con deuda.

---

## 3. Qué problemas importantes se detectaron

## 3.1 El dominio conocía al ORM
Había entidades de dominio que importaban modelos `DB*`.

### ¿Por qué es un problema?
Porque en DDD el dominio debería representar el negocio, no la base de datos.
Si una entidad depende directamente de SQLAlchemy:
- cuesta más probarla,
- cuesta más cambiar la persistencia,
- y el dominio termina obedeciendo a infraestructura.

### Recomendación hecha
Mover conversiones `DB ↔ dominio` a mappers en infraestructura.

---

## 3.2 El dominio era delgado
Las entidades representaban datos, pero casi no protegían reglas.

### ¿Qué significa “dominio delgado”?
Que la entidad existe, pero casi no decide nada.
Es como un personaje con nombre y uniforme, pero sin autoridad real.

### ¿Por qué es un problema?
Porque las reglas terminan dispersas en use cases, repositorios o adapters.
Y eso hace más difícil entender el negocio.

### Recomendación hecha
Empezar a mover reglas simples hacia el dominio más adelante:
- transiciones de estado,
- fallback de media code,
- semántica de éxito/fallo,
- consistencia del log de routing.

---

## 3.3 Había doble control transaccional
`session_scope()` hacía commit y varios repositorios también.

### ¿Por qué es malo?
Porque no queda claro quién manda sobre la transacción.
Cuando eso pasa:
- hay más riesgo de bugs,
- es más difícil razonar el flujo,
- y las operaciones compuestas se vuelven peligrosas.

### Recomendación hecha
Definir un solo dueño de la transacción.
Se eligió esta regla:

> `session_scope()` es el owner oficial de la transacción.

---

## 3.4 El contrato del lead no coincidía del todo con el uso real
El sistema usaba campos en la integración que no estaban modelados claramente en el schema principal.

### ¿Por qué es peligroso?
Porque el sistema parece aceptar una cosa, pero en realidad necesita otra.
Eso provoca:
- errores tardíos,
- integraciones frágiles,
- más confusión para frontend o integradores.

### Recomendación hecha
Alinear el schema del lead con el payload real usado en el flujo completo.

---

## 3.5 Las responsabilidades no estaban suficientemente explicadas
Aunque el sistema funcionaba, no siempre estaba claro:
- qué pertenece a `LeadUseCase`,
- qué pertenece a `ExecuteUseCase`,
- qué pertenece al adapter externo,
- y qué no deberían hacer los repositorios.

### ¿Por qué importa?
Porque si no entiendes quién manda en cada parte, el proyecto empieza a mezclar responsabilidades y se degrada con el tiempo.

### Recomendación hecha
Documentar y reforzar fronteras entre:
- application,
- domain,
- infrastructure,
- external adapters.

---

## 4. Qué mejoras importantes ya se hicieron

### Sprint 1
Se atacó la disciplina base:
- logging,
- imports,
- excepciones,
- estados.

### ¿Por qué fue correcto empezar por ahí?
Porque primero había que limpiar ruido y mejorar legibilidad.
No conviene hacer cirugía mayor en un sistema si antes no limpias el campo de batalla.

### Sprint 2
Se atacó coherencia interna:
- transacciones,
- schema real del lead,
- claridad de capa de aplicación.

### ¿Por qué eso fue importante?
Porque un sistema debe saber:
- quién controla el commit,
- qué datos acepta realmente,
- y dónde vive la orquestación.

### Sprint 3 (en progreso)
Se empezó a atacar pureza arquitectónica:
- desacoplar dominio del ORM.

### ¿Por qué esta mejora pesa tanto?
Porque separa el negocio de la persistencia.
Y esa es una condición clave para una DDD más seria.

---

## 5. Qué sigue faltando

Aunque la arquitectura ya es fuerte, todavía faltan piezas importantes:

- enriquecer entidades con comportamiento,
- normalizar mejor `routing_leadspedia` como adapter,
- seguir fortaleciendo fronteras entre dominio y aplicación,
- introducir value objects donde realmente valga la pena.

### Traducción simple
El sistema ya está ordenado.
Ahora falta volverlo más inteligente en su núcleo.

---

## 6. Lección para un dev junior

No copies solo “cómo está escrito”.
Entiende **por qué** está escrito así.

Las mejores decisiones que se fueron tomando no fueron estéticas.
Fueron decisiones para lograr esto:
- menos acoplamiento,
- más claridad,
- más control del negocio,
- menos sorpresas al cambiar algo.

Eso es arquitectura real.
