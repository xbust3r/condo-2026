# ♟️ Análisis Estratégico Profundo — condo-py vs. mercado

> Fecha: 2026-04-13  
> Autor: Lelouch S  
> Base de partida: `analysis/competitive-analysis.md` + inspección del código real de `condo-py`

---

## 1. Dictamen ejecutivo

La posición actual de `condo-py` **no es la de un rival funcional inmediato** frente a plataformas maduras como Buildium, Condo Control o Superlógica.

Su posición real hoy es otra:

- **proyecto backend en etapa temprana**,
- con **arquitectura mejor pensada que muchos incumbentes**,
- pero con una **brecha funcional enorme** frente al mercado.

La buena noticia: el tablero todavía no está perdido.

El mercado de condominios/HOA muestra un patrón claro:

1. Los jugadores maduros ganan por **finanzas + operaciones + portal de residentes**.
2. Los jugadores más fuertes en condo/HOA ganan además por **gobernanza**: votaciones, actas, documentos, auditoría.
3. En LATAM, el actor realmente peligroso no gana solo por software: gana por **pagos y servicios financieros integrados**.

### Conclusión brutal, sin anestesia

Si `condo-py` quiere competir en 6–12 meses, no debe intentar parecerse a “todo AppFolio”. Eso sería sacrificar la reina por un peón.

Debe posicionarse como:

> **plataforma API-first, self-hosted o managed, enfocada en condominios de LATAM hispanohablante, con núcleo fuerte de operaciones + cobranza local + portal de residentes.**

Ese es el flanco menos defendido del mercado.

---

## 2. Límite ético y operativo del research

Se pidió también “buscar documentación filtrada”. No voy a apoyar recolección ni uso de material filtrado, privado o obtenido de forma ilícita.

Sí tomé y usaré:

- documentación pública de producto,
- pricing oficial cuando existe,
- claims públicos verificables,
- integraciones publicadas,
- señales públicas de madurez comercial.

Ese enfoque sirve para inteligencia competitiva seria sin cruzar líneas que luego destruyen reputación o generan riesgo legal.

---

## 3. Qué existe realmente hoy en `condo-py`

Inspección directa del repositorio `/home/miguel/servers/condo-py`:

### Implementado de verdad
- `FastAPI`
- patrón `DDD/CQRS` pragmático
- módulo funcional `core_condominiums`
- capa `shared/` reutilizable
- módulo `example/` como plantilla arquitectónica
- Docker y Alembic presentes

### Evidencia concreta en código
- `src/main.py` registra solo:
  - `condominium_routes`
  - `example_routes`
- `src/api/condominiums/routes_condominiums.py` expone CRUD + búsqueda por `id`, `uuid`, `code`
- `src/library/dddpy/core_condominiums/` sí tiene `domain / infrastructure / usecase`

### No implementado aún como capacidad de negocio competitiva
- autenticación/autorización
- multi-tenant real con aislamiento comercial documentado
- usuarios/residentes completos
- edificios
- unidades
- cobranzas/pagos
- contabilidad / conciliación
- notificaciones email/SMS/push
- portal de residentes
- reserva de amenidades
- mantenimiento/work orders
- gobernanza digital (actas, votos, asambleas)
- app móvil o frontend web usable
- analítica comercial/operativa

### Veredicto técnico

`condo-py` hoy es **más una base arquitectónica prometedora que un producto competitivo de mercado**.

Eso no es un insulto. Es un diagnóstico. Y un buen diagnóstico evita perder la guerra por autoengaño.

---

## 4. Análisis profundo de competidores

## 4.1 Buildium
**Tipo:** property management SaaS maduro  
**Señal clave:** pricing público y portafolio amplio  
**Fuente pública:** `buildium.com/pricing`

### Lo importante
Buildium publica planes desde:
- **Essential:** USD 62/mes
- **Growth:** USD 192/mes
- **Premium:** USD 400/mes

También declara capacidades que importan mucho para condo/association management:
- resident portal
- online payments & autopay
- amenity booking
- community calendar
- maintenance/work orders
- owner portal
- comunicaciones
- reporting
- automatizaciones
- **Open API** en plan premium

### Fortalezas reales
- pricing visible: reduce fricción comercial
- suite amplia de operaciones + pagos + comunicaciones
- madurez funcional alta
- API pública como arma de integración
- sirve como referencia para PMs que quieren estandarizar operación

### Debilidades reales
- fuerte sesgo USA
- inglés-first
- no se siente “LATAM-native”
- puede resultar pesado para comunidades pequeñas autogestionadas
- el valor sube rápido si necesitas features avanzadas

### Qué significa para condo-py
Buildium no gana por arquitectura elegante; gana por **producto utilizable hoy**.

La lección es simple: al mercado le importa más poder cobrar, comunicar y operar que si el repositorio sigue DDD con pureza ceremonial.

---

## 4.2 AppFolio
**Tipo:** plataforma enterprise  
**Señal clave:** benchmark de sofisticación, no necesariamente rival inmediato  
**Fuente pública:** `appfolio.com/pricing`

### Lo importante
Su pricing público accesible es opaco: la página empuja a **customizar plan** y hablar con ventas. Eso ya revela el posicionamiento.

No está compitiendo por simplicidad. Está compitiendo por:
- plataforma unificada
- servicios agregados
- automatización avanzada
- motion enterprise

### Fortalezas reales
- marca fuerte
- producto percibido como avanzado
- excelente benchmark de madurez operativa y automatización
- probable ventaja en workflows complejos y upsell de servicios

### Debilidades reales
- barrera comercial más alta
- enfoque más enterprise/professional manager que condo self-managed
- menor afinidad natural con un GTM inicial para LATAM hispanohablante
- pricing no transparente

### Qué significa para condo-py
AppFolio es menos amenaza inmediata y más **techo de referencia**. Es el rey al fondo del tablero: no es la primera pieza que te captura, pero sí muestra hasta dónde escala un incumbente serio.

No copiar. **Aprender qué módulos generan lock-in**.

---

## 4.3 Condo Control
**Tipo:** competidor más alineado al problema condo/HOA  
**Fuentes públicas:** `condocontrol.com/`, `condocontrol.com/integrations/`

### Señales públicas fuertes
- más de **3.5 millones de residentes**
- foco explícito en property management companies y self-managed condos & HOAs
- claims públicos de:
  - AI resident assistant
  - knowledge base
  - e-voting
  - agendas/minutes
  - document retention
  - payments/autopay/reminders
  - amenity bookings
  - visitor management
  - package tracking
  - access control integrations
  - integración con **QuickBooks, Yardi y Stripe**
- métricas públicas citadas desde ratings verificados:
  - 98% Quality of Support
  - 99% Ease of Setup
  - 97% Value for Money
  - 99.9% Uptime

### Fortalezas reales
- muy enfocado en el caso condo/HOA, no solo rentals
- entiende el dolor operacional de residentes, boards y managers
- mezcla tres frentes clave:
  - operaciones
  - gobernanza
  - finanzas
- onboarding aparentemente sencillo
- integración contable madura

### Debilidades reales
- foco principal en Norteamérica
- pricing no transparente públicamente en la evidencia disponible
- no parece posicionarse como open platform ni self-hosted
- español/LATAM no es su centro de gravedad

### Qué significa para condo-py
Este sí es un rival conceptual directo.

Si `condo-py` no construye rápido:
- portal residente,
- comunicaciones,
- amenidades,
- pagos,
- gobernanza,

entonces Condo Control ya tiene el jaque armado en exactamente el segmento correcto.

---

## 4.4 Propertyware
**Tipo:** plataforma madura para property managers, más cercana a rental/SFR  
**Fuente pública:** `propertyware.com/pricing`

### Señales públicas útiles
Propertyware no publica un precio base simple en la evidencia accesible, pero sí muestra:
- Basic / Plus / Premium
- owner portals
- tenant portals
- maintenance
- accounting
- reporting
- text messaging
- eSignature
- inspections
- vendor portals
- **Enterprise/API: add USD 1 por unidad/mes**

### Fortalezas reales
- orientación a customización
- API como capacidad comercializable
- módulos maduros de operación
- portal para varios actores

### Debilidades reales
- sesgo fuerte a rental/property management tradicional
- menos alineado al corazón de gobernanza condominial
- UX y complejidad suelen ser mayores en este tipo de suites
- no se percibe como LATAM-first

### Qué significa para condo-py
Propertyware es importante porque demuestra algo clave:

> el mercado sí paga por APIs cuando el producto base ya resuelve el negocio.

Moraleja: “API-first” solo es diferenciador si primero hay negocio resolviendo negocio.

---

## 4.5 Superlógica
**Tipo:** el actor regional más serio  
**Fuentes públicas:** `superlogica.com/condominios/`, `superlogica.com/condominios/modulo-financeiro/`

### Señales públicas de dominio de mercado
- **+3 mil administradoras**
- **+100 mil condomínios**
- ecosistema de software + servicios financieros + app para moradores
- productos integrados:
  - gestão financeira
  - conta digital
  - PIX
  - boleto
  - tarjeta/crédito
  - inadimplência zero
  - seguros
  - crédito para condomínios
  - conciliación bancaria
  - reportes/métricas
  - app de comunidad/residentes

### Fortalezas reales
- no vende “solo software”; vende **infraestructura económica del condominio**
- integración financiera profundísima
- distribución y confianza sectorial masivas
- app residente + operaciones + pagos + capacitación
- compliance regulatorio y narrativa de institución financiera

### Debilidades reales
- brasilcentrismo total
- idioma y rails locales (portugués/BRL/PIX/boleto)
- expansión a LATAM hispana no es trivial
- pricing opaco al público general

### Qué significa para condo-py
Superlógica es el rival más peligroso **estratégicamente**.

No porque hoy domine Perú o México, sino porque ya resolvió la pregunta más difícil:

> ¿cómo convertir software de condominio en plataforma de pagos, cobranza y servicios financieros?

Ese modelo genera stickiness brutal.

Si `condo-py` ignora finanzas y cobranzas, será una capa bonita alrededor de un problema central que otro ya monetiza mejor.

---

## 4.6 TownSq
**Tipo:** community management app / HOA software  
**Fuente pública accesible:** `townsq.io`

### Lo observable públicamente
La evidencia accesible pública fue escasa en este pase; el sitio visible empuja a demo. Eso sugiere un motion comercial más cerrado y menos transparente.

### Lectura estratégica
TownSq parece jugar más cerca de:
- app de comunidad,
- experiencia residente,
- operación cotidiana,
que de una tesis financiera profunda al estilo Superlógica.

### Qué significa para condo-py
TownSq es una advertencia, no necesariamente el enemigo principal:

si `condo-py` deja fuera el frente de experiencia de residente, otro actor mobile-first puede apropiarse de la relación diaria aunque la base operativa esté en otro sistema.

---

## 4.7 CondoLivre
**Tipo:** fintech complementaria del ecosistema  
**Lectura:** adyacente, no rival full-stack

No parece un competidor directo de gestión integral. Es más bien evidencia de que el vertical condominial permite especialización financiera.

### Qué significa para condo-py
Confirma la tesis:

> el dinero no es un módulo accesorio; es uno de los centros de gravedad del producto.

---

## 4.8 Kastle
**Tipo:** seguridad física / access control  
**Lectura:** adyacente, no rival directo

Sirve como benchmark de integración para:
- visitor management
- access control
- hardware/security ecosystem

### Qué significa para condo-py
No debería ser prioridad temprana competir en hardware/security profundo. Mejor dejar ese frente como:
- integraciones futuras,
- webhooks,
- arquitectura extensible.

---

## 5. Los 3 rivales más peligrosos para condo-py en LATAM hispanohablante

## 1) Superlógica — el más peligroso estratégicamente
**Por qué:**
- probó escala real en condominio
- domina finanzas integradas
- app + operación + cobranza + crédito
- si quisiera expandirse a hispanoamérica con localización correcta, sería devastador

**Nivel de amenaza:** Muy alta  
**Tipo de amenaza:** modelo de negocio + plataforma financiera

## 2) Condo Control — el más peligroso funcionalmente
**Por qué:**
- está mejor alineado al caso condo/HOA que Buildium o Propertyware
- resuelve resident experience + governance + payments + operations
- parece más fácil de adoptar que suites enterprise pesadas

**Nivel de amenaza:** Muy alta  
**Tipo de amenaza:** producto directamente alineado al dolor

## 3) Buildium — el más peligroso comercialmente
**Por qué:**
- pricing público
- feature set amplio
- marca consolidada
- API en tier alto
- enough product breadth para entrar donde el cliente no exige localización fuerte

**Nivel de amenaza:** Alta  
**Tipo de amenaza:** suite madura con compra relativamente fácil

### Mención especial: AppFolio
AppFolio es el benchmark más serio de sofisticación, pero no lo pondría hoy en top 3 de amenaza inmediata para `condo-py` en LATAM hispanohablante por su posicionamiento más enterprise y fricción comercial mayor.

---

## 6. Gap analysis técnico y de producto

## 6.1 Gaps mortales
Si estos no se corrigen, `condo-py` no compite; solo demuestra arquitectura:

1. **Auth + RBAC multi-rol**
   - admin
   - board
   - resident
   - concierge/front desk
   - accountant/operator

2. **Modelo núcleo inmobiliario completo**
   - condominiums
   - buildings
   - units
   - users
   - residents/occupancy
   - ownership/tenancy relationships

3. **Portal de residentes**
   - estado de cuenta
   - documentos
   - tickets/incidencias
   - notificaciones
   - reservas
   - visitas

4. **Finanzas/cobranza**
   - cuotas
   - cargos recurrentes
   - mora/penalidades
   - ledger por unidad
   - conciliación
   - exportes contables

5. **Comunicaciones y notificaciones**
   - email
   - SMS/WhatsApp opcional
   - in-app notifications
   - anuncios
   - recibos/lecturas

## 6.2 Gaps serios de segunda línea
6. Work orders / mantenimiento  
7. Amenity booking  
8. Visitor/package management  
9. Document repository + governance  
10. Audit trail / activity log  
11. Reporting operativo y financiero  
12. Integraciones de pago/ERP

## 6.3 Gaps técnicos invisibles pero críticos
13. tenancy / account isolation claro  
14. permisos por condominio/edificio/unidad  
15. idempotencia en pagos/eventos  
16. background jobs  
17. observabilidad  
18. estrategia de archivos/documentos  
19. testing automatizado  
20. hardening de seguridad

---

## 7. Roadmap recomendado 6–12 meses

## Fase 1 — 0 a 8 semanas
**Objetivo:** dejar de ser “backend bonito” y convertirse en núcleo operable.

### Prioridades
- Auth JWT/OAuth2
- RBAC
- módulos:
  - `core_buildings`
  - `core_unitys`
  - `users`
  - `users_residents`
- seeds/base catalogs
- auditoría básica
- OpenAPI limpia
- tests de contrato API

### Resultado esperado
Una instalación ya puede representar correctamente:
- un condominio,
- sus edificios,
- sus unidades,
- sus usuarios y residentes.

Sin esto, todo lo demás se apoya en arena.

## Fase 2 — 2 a 4 meses
**Objetivo:** resolver la operación mínima por la que alguien pagaría.

### Prioridades
- cuentas por cobrar / cuotas / cargos / mora
- ledger por unidad
- comprobantes/estado de cuenta
- notificaciones transaccionales
- announcements / bulletin board
- portal residente básico web
- carga y consulta de documentos

### Resultado esperado
`condo-py` ya puede venderse como:

> “sistema base para administración de condominios con residentes, cuotas y comunicación”.

Ese ya es un producto, no solo un repositorio.

## Fase 3 — 4 a 8 meses
**Objetivo:** entrar al terreno donde Condo Control empieza a dominar.

### Prioridades
- maintenance/work orders
- amenity booking
- visitor pre-registration
- package logging
- meeting minutes / document governance
- e-voting inicial
- dashboards operativos

### Resultado esperado
Ahora sí hay una narrativa seria de condo operations platform.

## Fase 4 — 8 a 12 meses
**Objetivo:** construir moat regional.

### Prioridades
- integraciones de pago LATAM
  - país por país
- multi-country billing abstractions
- exportes contables/local compliance
- canales locales de cobranza
- WhatsApp/inbox operational layer
- marketplace/API/webhooks públicos

### Resultado esperado
Aquí nace la verdadera ventaja frente a incumbentes anglo o brasilcentrados.

---

## 8. Qué NO priorizar todavía

No sacrifiques foco por brillo.

### Evitar en etapa temprana
- app móvil nativa antes de validar portal web fuerte
- AI assistant “de marketing” sin resolver datos/operación
- microservicios prematuros
- integraciones hardware complejas de access control
- analítica avanzada tipo BI enterprise
- expansion a Europa como prioridad inicial

### Razón
El producto todavía no tiene aseguradas las piezas que cobran, comunican y sostienen gobernanza. Lo demás es decoración sobre una fortaleza incompleta.

---

## 9. Posicionamiento recomendado para condo-py

## Tesis de posicionamiento

`condo-py` no debe presentarse como:
- “otro Buildium”, ni
- “mini AppFolio”, ni
- “Condo Control open source”.

Debe presentarse como:

> **Infraestructura moderna para administración de condominios en LATAM hispanohablante: API-first, desplegable en nube o self-hosted, con foco en operaciones, cobranza local y experiencia residente.**

## Diferenciadores que sí importan
1. **LATAM-first** en español  
2. **Self-hosted / managed**  
3. **API-first real**  
4. **arquitectura mantenible**  
5. **integraciones locales de pago y mensajería**  
6. **modularidad para administradoras medianas**

## Diferenciadores que NO bastan solos
- “está en Python”
- “usa DDD/CQRS”
- “tiene Docker”
- “podemos agregar IA luego”

Eso impresiona arquitectos. No cierra ventas.

---

## 10. Tabla final de posicionamiento estratégico

| Criterio | condo-py hoy | Objetivo 12 meses | Rival más fuerte en ese frente |
|---|---|---|---|
| Arquitectura backend | Fuerte | Muy fuerte | Ninguno visible públicamente |
| Funcionalidad condominio core | Débil | Media | Condo Control |
| Finanzas/cobranza | Nula | Fuerte | Superlógica |
| Portal residente | Nulo | Medio/Fuerte | Condo Control / TownSq |
| Gobernanza (actas, voto, documentos) | Nula | Media | Condo Control |
| Integraciones/API | Potencial alto, real bajo | Fuerte | Buildium / Propertyware |
| Adaptación LATAM hispana | Potencial muy alto | Muy fuerte | Mercado aún fragmentado |
| Time-to-value comercial | Bajo | Medio | Buildium |
| Escalabilidad estratégica | Alta en teoría | Alta real si ejecuta | AppFolio como benchmark |

---

## 11. Plan de ataque recomendado

Si yo moviera las piezas del tablero, el orden sería este:

### Sprint estratégico A
- auth
- roles
- buildings
- units
- residents/users

### Sprint estratégico B
- cuotas/cargos
- ledger
- estados de cuenta
- notificaciones

### Sprint estratégico C
- portal residente web
- documentos
- anuncios
- tickets/mantenimiento básico

### Sprint estratégico D
- amenidades
- visitas
- gobernanza
- integraciones de pago locales

Ese orden maximiza:
- credibilidad de producto,
- posibilidad de piloto,
- capacidad de cobro,
- y futura defensibilidad.

---

## 12. Dictamen final

`condo-py` **todavía no está jugando la misma liga funcional** que los incumbentes.

Pero sí tiene algo que varios de ellos no muestran con claridad:

- base arquitectónica limpia,
- posibilidad de despliegue flexible,
- y oportunidad real de diseñarse para LATAM desde el inicio en vez de “traducirse” después.

El jaque mate no consiste en perseguir al rival más grande en todos los frentes.
Consiste en capturar el centro del tablero donde ellos están mal localizados:

- español,
- pagos y operación regional,
- despliegue flexible,
- integrabilidad,
- y foco específico en condo/HOA hispanohablante.

Si `condo-py` ejecuta bien los próximos 2–3 bloques de roadmap, deja de ser promesa técnica y se convierte en amenaza real.

Si no, será otro castillo de arquitectura impecable… vacío por dentro.

---

## 13. Fuentes públicas usadas

### Producto / pricing / claims oficiales
- <https://www.buildium.com/pricing/>
- <https://www.appfolio.com/pricing>
- <https://www.condocontrol.com/>
- <https://www.condocontrol.com/integrations/>
- <https://www.propertyware.com/pricing/>
- <https://www.superlogica.com/condominios/>
- <https://www.superlogica.com/condominios/modulo-financeiro/>
- <https://www.townsq.io/>

### Código y documentación interna analizada
- `README.md`
- `docs/architecture.md`
- `docs/BULMA/MODULES.md`
- `src/main.py`
- `src/api/condominiums/routes_condominiums.py`
- `src/library/dddpy/core_condominiums/`

### Nota metodológica
- G2/Capterra y varios agregadores bloquearon scraping directo en este entorno.
- Donde existían métricas citadas en el research previo, se conservaron como referencia indirecta y no como scraping fresco del agregador.
