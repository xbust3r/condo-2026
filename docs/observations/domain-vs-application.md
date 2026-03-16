# Dominio vs Aplicación vs Infraestructura en `condo-py`

Esta separación es una de las reglas centrales del proyecto.
Si se rompe, el sistema empieza a degradarse aunque siga compilando.

---

## 1. Domain

### Qué es
La parte que representa el negocio.

### Debe contener

- entidades,
- comportamiento semántico,
- invariantes,
- estados válidos,
- excepciones de dominio,
- contratos abstractos de repositorio.

### Ejemplo aplicado
`Condominium` ya encapsula acciones como activar, desactivar y actualizar ciertos campos.
Eso va en la dirección correcta.

### Qué no debe conocer

- modelos `DB*`,
- sesiones SQLAlchemy,
- `FastAPI`,
- `HTTPException`,
- detalles de transporte o persistencia.

### Regla mental
Si la pregunta es “¿qué significa esto para el negocio?”, probablemente pertenece a `domain/`.

---

## 2. Application / UseCase

### Qué es
La capa que coordina pasos para cumplir un caso de uso.

### Debe contener

- secuencia del flujo,
- coordinación entre repositorios,
- división command/query si aporta claridad,
- decisiones de proceso.

### Ejemplo aplicado
Un use case sí puede:

- recibir un schema,
- cargar entidades,
- llamar repositorios,
- decidir si crea, actualiza o consulta,
- devolver una entidad o colección.

### Qué no debe hacer

- convertirse en el dominio entero,
- esconder lógica de negocio que debería vivir en la entidad,
- meter SQLAlchemy crudo o detalles HTTP innecesarios.

### Regla mental
Si la pregunta es “¿qué pasos debo coordinar?”, probablemente pertenece a `usecase/`.

---

## 3. Infrastructure

### Qué es
La capa técnica.

### Debe contener

- modelos ORM,
- repositorios concretos,
- mappers,
- sesiones,
- detalles de base de datos.

### Ejemplo aplicado
`condominiums_mapper.py` pertenece correctamente aquí, porque traduce entre persistencia y dominio.

### Qué no debe hacer

- decidir reglas del negocio,
- imponer semántica a las entidades,
- contaminar el dominio con dependencias técnicas.

### Regla mental
Si la pregunta es “¿cómo hago técnicamente que esto ocurra?”, probablemente pertenece a `infrastructure/`.

---

## 4. API / Entrypoint

### Qué es
La frontera HTTP.

### Debe contener

- rutas,
- recepción de payload,
- adaptación de input/output,
- traducción de errores a códigos HTTP.

### Qué no debe hacer

- ejecutar reglas de negocio,
- hablar con la DB directamente,
- duplicar la semántica del caso de uso.

### Regla mental
Si solo estás recibiendo o devolviendo requests, estás en el borde, no en el núcleo.

---

## 5. Regla de oro

- **Domain** decide significado.
- **UseCase** coordina pasos.
- **Infrastructure** ejecuta detalles técnicos.
- **API** adapta el mundo exterior.

Si una pieza rompe esa regla, estás dejando que un peón gobierne al rey.
