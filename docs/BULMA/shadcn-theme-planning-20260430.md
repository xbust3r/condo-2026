# Planning — Shadcn Theme System para Condo-Net
**Proyecto:** `condo-net` (`/home/miguel/servers/condo-net/src`)
**Estrategia:** shadcn/ui puro, copiar catálogo de temas desde `Condo-backdmin`
**API base:** `condo-py` (ya tiene `theme_id` en `core_condominiums`)
**Asignado a:** Bulma S
**Documentos base:** `condo-net/docs/condo-theme-strategy.md`, `condo-net/docs/roadmap.md`
**Fecha:** 2026-04-30

---

## Arquitectura general

El sistema funciona así:

```
condo-py (API)
  └─ core_condominiums.theme_id → "twitter", "cyberpunk", etc.

condo-net (Frontend)
  ├─ /themes/          ← port del registry desde Condo-backdmin
  ├─ /lib/theme-runtime.ts   ← applyTheme(), getThemeById(), resetTheme()
  ├─ auth-context.tsx        ← extiende Condominium con theme_id
  └─ (marketing) page.tsx    ← landing page nueva
```

**Momento de aplicación:** después de seleccionar condominio en `/select-condo`, antes de navegar a `/dashboard`.

---

## Sprints

### Sprint A — Fundación (Semana 1)
**Objetivo:** tener el motor de temas funcional y conectado.

---

#### FASE 0 — Auditoría + Scope confirm
**Archivos a revisar:**
- `condo-net/src/lib/auth-context.tsx` → tipo Condominium actual
- `condo-net/src/app/select-condo/page.tsx` → lógica actual de selección
- `condo-net/src/lib/api-client.ts` → cómo hace requests
- `condo-py` → endpoints `/condominiums/{id}`, `/me/contexts` (confirmar que devuelven `theme_id`)

**Tareas:**
- [ ] Confirmar que `GET /condominiums/{id}` devuelve `theme_id` en la response
- [ ] Confirmar que `GET /me/contexts` incluye `theme_id` o si hay que enrichecerlo
- [ ] Mapear todos los archivos de `condo-net` que usan colores hardcodeados (para FASE 4)
- [ ] Definir fallback theme oficial (`twitter` recomendado)

**Entregable:** scoped confirmado, sin ambigüedades.

---

#### FASE 1 — Port del catálogo de temas
**Origen:** `/home/miguel/servers/Condo-backdmin/src/themes/`
**Destino:** `/home/miguel/servers/condo-net/src/themes/`

**Tareas:**
- [ ] Crear `/themes/` en `condo-net/src`
- [ ] Copiar los 10 JSON: `twitter.json`, `amber-minimal.json`, `violet-bloom.json`, `northern-lights.json`, `candyland.json`, `ocean-breeze.json`, `graphite.json`, `cyberpunk.json`, `cyberpunk-2077.json`, `facebook.json`
- [ ] Copiar y adaptar `themes/index.ts` (Theme interface + registry + helpers)
- [ ] Crear helper `getThemeById(id: string): Theme | undefined`
- [ ] Crear helper `getDefaultTheme(): Theme`
- [ ] Crear helper `isValidTheme(id: string): boolean`
- [ ] Exportar `themes` array completo

**Catálogo destino:**

| Theme ID | Nombre |
|---|---|
| `twitter` | Twitter |
| `amber-minimal` | Amber Minimal |
| `violet-bloom` | Violet Bloom |
| `northern-lights` | Northern Lights |
| `candyland` | Candyland |
| `ocean-breeze` | Ocean Breeze |
| `graphite` | Graphite |
| `cyberpunk` | Cyberpunk |
| `cyberpunk-2077` | Cyberpunk 2077 |
| `facebook` | Facebook |

**Dependencias:** Ninguna. Solo copiar archivos.

---

#### FASE 2 — Theme Runtime (motor de aplicación)
**Archivo nuevo:** `/src/lib/theme-runtime.ts`

**Tareas:**
- [ ] Crear `applyTheme(themeId: string): void`
  - Busca el theme en registry
  - Si existe: inyecta CSS variables de `--light` en `document.documentElement`
  - Si no existe: aplica `fallbackTheme` + log warning en consola
- [ ] Crear `resetTheme(): void` → remueve todas las variables CSS injectadas
- [ ] Crear `getActiveTheme(): Theme | null`
- [ ] Persistir theme activo en `localStorage` (key: `condo_active_theme`)
- [ ] Escuchar `dark` mode preference para inyectar `--dark` vars en vez de `--light` si es necesario
- [ ] Asegurar que nunca lance excepciones — fallback siempre funciona

**Nota:** Condo-backdmin usa `next-themes` con `attribute="class"`. Para condo-net, aplicamos CSS vars directo en el `documentElement` (más simple, más control). No necesitamos toda la magia de next-themes para esto.

**Tests manuales:**
- Cambiar themeId a mano → los colores del DOM cambian inmediatamente
- Recargar → el tema persiste
- Poner id inexistente → fallback `twitter` sin crash

---

#### FASE 3 — Integración con AuthContext + Select Condo
**Archivos a tocar:**
- `src/lib/auth-context.tsx`
- `src/app/select-condo/page.tsx`

**Tareas:**

**AuthContext:**
- [ ] Extender interfaz `Condominium` con `theme_id?: string`
- [ ] Agregar `activeTheme: string` al estado global
- [ ] En `selectCondominium(condo)`:
  1. Guardar condominio en localStorage
  2. Extraer `condo.theme_id`
  3. Llamar `applyTheme(condo.theme_id || 'twitter')`
  4. Guardar theme activo en localStorage
- [ ] En el bootstrap de `AuthProvider`:
  - Al restaurar `selectedCondominium` desde localStorage, llamar `applyTheme` inmediatamente
  - Para evitar flash visual, aplicar ANTES del primer render
- [ ] En `logout()`: llamar `resetTheme()` + limpiar localStorage

**Select Condo:**
- [ ] Verificar que la lista de condominios ya venga con `theme_id` (si no, hacer fetch individual)
- [ ] Mostrar preview del color del tema al hacer hover/seleccionar condominio (opcional, mejora UX)

**Aceptación:**
- Seleccionar condominio A con theme `cyberpunk` → UI cambia a cyberpunk
- Cambiar a condominio B con theme `ocean-breeze` → UI cambia a ocean-breeze
- Refrescar página → tema se restaura desde localStorage
- Logout → tema vuelve a default

---

### Sprint B — Landing Page (Semana 2)
**Objetivo:** reemplazar la landing page actual (splash con loader) por una landing real.

---

#### FASE 4 — Landing Page: Hero + Features
**Archivo nuevo:** `/src/app/(marketing)/page.tsx` (route group de Next.js)
**Carpeta componentes:** `/src/components/marketing/`

**Tareas:**
- [ ] Crear route group `(marketing)` en `/src/app/`
- [ ] Crear `app/(marketing)/layout.tsx` con metadata básica
- [ ] Crear sección **Hero** (`hero.tsx`)
  - Headline: "Gestión condominial, simplificada"
  - Subheadline con propuesta de valor
  - 2 CTAs: "Iniciar sesión" → `/login` | "Saber más" → `#features`
  - Ilustración placeholder (div con gradiente)
  - Animación de entrada (usar `tw-animate-css` que ya está instalado)
- [ ] Crear sección **Features** (`features.tsx`)
  - 6 features con iconos Lucide (Shield, Building2, BarChart3, Users, Bell, Settings)
  - Grid responsive: 1 col mobile → 2 col tablet → 3 col desktop
  - Hover: elevación sutil con shadow

**Contenido default (placeholder, se ajusta después):**
```
- Gestión de residentes
- Control de gastos y finanzas
- Agenda y reservas
- Comunicados y announcements
- Panel de administración
- Acceso desde cualquier dispositivo
```

---

#### FASE 5 — Landing Page: Benefits + Testimonials + Pricing + FAQ

**Tareas:**

**Benefits** (`benefits.tsx`):
- [ ] Lista con check icons
- [ ] Layout alternado imagen/texto en desktop
- [ ] 4 beneficios clave

**Testimonials** (`testimonials.tsx`):
- [ ] Cards con `Avatar`, nombre, rol, quote
- [ ] Usar shadcn `Card` + `Avatar`
- [ ] Scroll horizontal con snap en mobile

**Pricing** (`pricing.tsx`):
- [ ] 3 cards: Básico / Pro / Empresarial
- [ ] Toggle mensual/anual (useState)
- [ ] Card Pro destacada con border primario
- [ ] Agregar `npx shadcn@latest add tabs` si no existe

**FAQ** (`faq.tsx`):
- [ ] Accordion con 6-8 preguntas
- [ ] Agregar `npx shadcn@latest add accordion` si no existe
- [ ] Animación de expansión suave

**CTA** (`cta.tsx`):
- [ ] Banner con gradiente de fondo
- [ ] Headline + description + botón primario
- [ ] Enlace a `/login`

**Footer** (`footer.tsx`):
- [ ] Logo + tagline
- [ ] Links organizados en 3 columnas
- [ ] Copyright 2026

**Ensamblaje:**
- [ ] Crear `app/(marketing)/page.tsx` que importe y ordene todas las secciones
- [ ] Espaciado consistente entre secciones (py-16 a py-24)

---

### Sprint C — Limpieza y QA (Semana 3)
**Objetivo:** eliminar hardcodes, asegurar consistencia, verificar todo.

---

#### FASE 6 — Refactor visual: eliminar hardcodes
**Archivos a auditar:**
- `src/app/login/page.tsx`
- `src/app/select-condo/page.tsx`
- `src/app/dashboard/page.tsx`
- `src/components/login-form.tsx`

**Tareas:**
- [ ] Buscar todos los colores hardcodeados: `bg-blue-`, `text-purple-`, `bg-zinc-50 dark:bg-zinc-950` en exceso, etc.
- [ ] Reemplazar por tokens semánticos: `bg-background`, `bg-card`, `text-foreground`, `border-border`, `bg-primary`, `text-primary-foreground`
- [ ] Verificar que todos los componentes shadcn/ui ya usen tokens (deberían estar correctos)
- [ ] Verificar contraste en dark mode para todos los temas activos
- [ ] Ajustar `globals.css` si algún tema requiere overrides de radius o tipografía

**Regla:** si un color no usa un token de `globals.css`, está mal.

---

#### FASE 7 — Conexión landing + app
**Tareas:**
- [ ] Definir routing: `(marketing)/page.tsx` es la landing pública (raíz `/`)
- [ ] El redirect de `app/page.tsx` actual (que redirige a `/login` o `/select-condo`) se mantiene para usuarios autenticados
- [ ] Pero ahora `app/page.tsx` no debe ser landing page — debe ser el splash loader que ya existe (o reemplazarlo por redirect directo)
- [ ] **Decisión arquitectura:** evaluar si la landing va en `/` (raíz) y la app autenticada va en `/app/*`, o si la landing convive con el flujo de auth en la misma raíz
- [ ] Implementar lo que Lelouch defina como estructura correcta

---

#### FASE 8 — QA funcional
**Casos de prueba obligatorios:**

| # | Escenario | Esperado |
|---|---|---|
| 1 | Login con usuario → selecciona condominio A (theme: cyberpunk) | UI cambia a cyberpunk |
| 2 | Login con usuario → selecciona condominio B (theme: twitter) | UI cambia a twitter |
| 3 | Refrescar con condominio activo seleccionado | Tema se restaura sin flash |
| 4 | Seleccionar condominio con `theme_id = null` | Aplica fallback `twitter` |
| 5 | Seleccionar condominio con `theme_id = "inexistente"` | Aplica fallback `twitter` + warning |
| 6 | Logout | Tema se resetea a default |
| 7 | Landing page en mobile (375px) | Responsive, sin overflow |
| 8 | Landing page en desktop (1280px) | Layout correcto |
| 9 | Dark mode en landing + app | Tokens correctos |
| 10 | Cambiar de condominio en `/dashboard` → nuevo theme | Cambio inmediato sin residuos |

---

## Notas técnicas importantes

### No usar next-themes para brand themes
Condo-backdmin lo usa con `attribute="class"`. Eso funciona para light/dark switching (clases tipo `.dark`). Para brand themes (cyberpunk vs twitter vs facebook) necesitamos inyectar CSS vars, no clases. Por eso el runtime manual en `theme-runtime.ts`.

### Dark mode
El runtime aplica `--light` por defecto. Si el OS/user prefiere dark, el runtime debería detectar `prefers-color-scheme` y aplicar `--dark` vars. Implementar eso en FASE 2 como mejora.

### Tailwind v4
Ya instalado. Usar utility classes directas, evitar `@apply` excesivo.

### Shadcn v4
Componentes instalados. Agregar con `npx shadcn@latest add [component]`.

### Fonts
`next/font` ya configurado. No agregar Google Fonts manualmente.

---

## Orden de ejecución

```
FASE 0 → FASE 1 → FASE 2 → FASE 3 → Sprint B landing (F4+F5) → FASE 6 → FASE 7 → FASE 8
```

**Sprint A:** F0 + F1 + F2 + F3 (~1 semana)
**Sprint B:** F4 + F5 (~1 semana)
**Sprint C:** F6 + F7 + F8 (~1 semana)

---

## Dependencias externas

- `condo-py` API debe devolver `theme_id` en `/condominiums/{id}` ✅ (ya confirmado por Lelouch)
- Template JSON de temas desde `Condo-backdmin` ✅ (ya identificados)

## Archivos a crear/modificar

**Nuevos:**
- `src/themes/` (carpeta con 10 JSON + index.ts)
- `src/lib/theme-runtime.ts`
- `src/components/marketing/` (carpeta + 7 componentes)
- `src/app/(marketing)/` (route group)
- `src/app/(marketing)/page.tsx`
- `src/app/(marketing)/layout.tsx`

**A modificar:**
- `src/lib/auth-context.tsx`
- `src/app/select-condo/page.tsx`
- `src/app/login/page.tsx` (tokens)
- `src/app/dashboard/page.tsx` (tokens)
- `src/components/login-form.tsx` (tokens)
- `src/app/page.tsx` (redirection logic)

**Instalar shadcn:**
- `npx shadcn@latest add accordion`
- `npx shadcn@latest add tabs` (para pricing toggle)
- `npx shadcn@latest add avatar`
- `npx shadcn@latest add badge`

---

*Coordinado por Misato — 2026-04-30*
*Basado en docs de Lelouch: condo-theme-strategy.md + roadmap.md*