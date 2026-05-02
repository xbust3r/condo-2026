# Swipe Landing Page — Plan de Implementación
**Proyecto:** condo-net (`/home/miguel/servers/condo-net/src`)
**Template origen:** https://shadcnstudio.com/templates/swipe-mobile-app-template
**Asignado a:** Bulma S
**Versión tech:** Next.js 16 + shadcn/ui + Tailwind v4 + TypeScript

---

## Resumen

El template **Swipe** es una landing page mobile-first para apps móviles. Se integra en el routing de Next.js como `/src/src/app/(marketing)/page.tsx`. El routing actual de la app (login, dashboard, select-condo) se mantiene intacto — solo se añade una sección marketing.

---

## Secciones del template (8 bloques)

| # | Sección | Descripción |
|---|---|---|
| 1 | Hero | Headline + CTA + preview visual |
| 2 | Feature Highlights | Grid de features con iconos |
| 3 | Benefits | Lista de beneficios con icons |
| 4 | Testimonials | Cards de testimonios |
| 5 | Pricing | Tabla/scards de planes |
| 6 | FAQ | Accordion de preguntas frecuentes |
| 7 | CTA | Banner de llamada a la acción |
| 8 | Footer | Links + legal + social |

---

## FASES

### FASE 1 — Análisis y scaffold ✅
**Objetivo:** Mapear componentes existentes vs. gaps, crear estructura de archivos.

**Tareas:**
- [ ] Inventariar componentes shadcn/ui ya disponibles en `/src/components/ui/`
- [ ] Identificar gaps (Accordion, Tabs, Badge, Avatar, etc.) → agregar con `npx shadcn@latest add`
- [ ] Crear directorio `/src/src/app/(marketing)/` con route group de Next.js
- [ ] Crear archivo `globals.css` de marketing si requiere variables custom distintas
- [ ] Definir constantes de contenido en `/src/src/lib/marketing-content.ts` (textos, links, precios placeholder)

**Entregable:** Estructura de carpetas montada, componentes instalados.

---

### FASE 2 — Hero + Feature Highlights
**Objetivo:** Primeras dos secciones visuales.

**Tareas:**
- [ ] Crear `app/(marketing)/page.tsx` con estructura de layout
- [ ] Implementar sección **Hero** (`components/marketing/hero.tsx`)
  - Headline + subheadline + 2 botones CTA
  - Imagen/ilustración placeholder con aspect ratio 3:4
  - Animación de entrada (framer-motion o tw-animate-css ya disponible)
- [ ] Implementar sección **Features** (`components/marketing/features.tsx`)
  - Grid responsive 1 col mobile → 3 col desktop
  - Iconos Lucide (ya instalados)
  - Hover states sutiles

**Entregable:** Hero y Features renderizadas, responsive, con dark mode.

---

### FASE 3 — Benefits + Testimonials
**Objetivo:** Contenido persuasivo de mitad de página.

**Tareas:**
- [ ] Implementar sección **Benefits** (`components/marketing/benefits.tsx`)
  - Lista vertical con check icons
  - Alternating layout (texto-illo) en desktop
- [ ] Implementar sección **Testimonials** (`components/marketing/testimonials.tsx`)
  - Cards con Avatar, nombre, rol, quote
  - Shadcn `Card` + `Avatar` components
  - Carousel horizontal en mobile (scroll snap)

**Entregable:** Benefits y Testimonials listos, integrados en la página.

---

### FASE 4 — Pricing + FAQ
**Objetivo:** Secciones de conversión y soporte.

**Tareas:**
- [ ] Implementar sección **Pricing** (`components/marketing/pricing.tsx`)
  - 3 cards: Free / Pro / Enterprise
  - Toggle mensual/anual (useState)
  - Card destacada (Pro) con border diferenciado
- [ ] Implementar sección **FAQ** (`components/marketing/faq.tsx`)
  - Shadcn `Accordion` (instalar si no existe: `npx shadcn@latest add accordion`)
  - 6-8 preguntas placeholder
  - Animación de expansión

**Entregable:** Pricing y FAQ funcionales con toggle y acordeón.

---

### FASE 5 — CTA + Footer
**Objetivo:** Cierre de la landing y navegación.

**Tareas:**
- [ ] Implementar sección **CTA** (`components/marketing/cta.tsx`)
  - Banner con fondo degradado o dark
  - Headline + description + botón primario
- [ ] Implementar **Footer** (`components/marketing/footer.tsx`)
  - Logo + tagline
  - Links organizados en columns (Product, Company, Legal, Social)
  - Copyright 2026
- [ ] Ensamblar todo en `app/(marketing)/page.tsx` con espaciados correctos entre secciones

**Entregable:** Landing completa montada en `/(marketing)/page.tsx`.

---

### FASE 6 — Theme + Dark Mode + SEO
**Objetivo:** Pulido visual y compatibilidad.

**Tareas:**
- [ ] Verificar que todas las secciones respeten el sistema de tokens de `globals.css` (colores, bordes, radius)
- [ ] Testear dark mode completo (todas las secciones)
- [ ] Agregar `metadata` en `app/(marketing)/layout.tsx` (title, description, og:image)
- [ ] Revisar que `next/font` no tenga conflictos con las fuentes del template
- [ ] Verificar mobile-first (375px → 768px → 1024px → 1280px)

**Entregable:** Landing lista para deployment, sin warnings de lint.

---

### FASE 7 — Integración + Revisión final
**Objetivo:** Conectar landing con el flujo de la app.

**Tareas:**
- [ ] Definir CTA de Hero → `/login` (usar `useRouter` de next/navigation)
- [ ] Definir CTA de Pricing → flow de signup
- [ ] Revisión con Lelouch del diseño final
- [ ] Pull request con todos los cambios documentados

---

## Notas técnicas

- **Tailwind v4** ya instalado — usar `@apply` con moderación; priorizar utility classes directas
- **shadcn v4** — instalación: `npx shadcn@latest add [component]`
- **tw-animate-css** ya disponible — usar para animaciones CSS sin framer-motion
- **Lucide React** ya instalado — no instalar iconos adicionales
- **next/font** ya configurado — no agregar Google Fonts manualmente
- **Dark mode:** usar la clase `.dark` en el `<html>` tag (ya configurado en globals.css)

## Pre-requisitos antes de empezar

1. Comprar/descargar el template en shadcnstudio.com (es pro, requiere plan)
2. Revisar los archivos Figma si vienen incluidos (diseño → código parity)
3. Definir los textos reales de condo-net para cada sección antes de la Fase 2

##估计 esfuerzo

| Fase | Complejidad |估计 tiempo |
|---|---|---|
| F1 | Baja | 1-2h |
| F2 | Media | 3-4h |
| F3 | Media | 3-4h |
| F4 | Media-Alta | 3-4h |
| F5 | Baja | 2h |
| F6 | Media | 2h |
| F7 | Baja | 1-2h |
| **Total** | — | **~15-22h** |

---

*Coordinado por Misato — 2026-04-30*