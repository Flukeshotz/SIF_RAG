# SIF Copilot — Accessibility (A11y) Report

## Audit Scope
A thorough accessibility sweep was performed across the React frontend to ensure compliance with WCAG 2.1 AA standards, focusing on keyboard navigation, focus management, and contrast.

## Improvements Made

### 1. Keyboard Navigation & Focus Management
- **Explicit Focus Rings:** Added `focus-within:ring-2 focus-within:ring-primary/50` to the main search input container, ensuring users navigating via `Tab` have a clear visual indicator of their cursor.
- **Button Outlines:** The primary "Send" button now features an explicit `:focus` offset ring (`focus:ring-2 focus:ring-secondary focus:ring-offset-2`).
- **Tour Trapping:** The Guided Tour overlay modal requires explicit interaction (Next or Skip) and captures immediate attention.

### 2. Semantic HTML
- **ARIA Labels:** Added `aria-label="Research Query Input"` to the main search bar. Added `aria-label="View Source N"` to citation pills.
- **Landmarks:** Ensured the application structure correctly utilizes `<header>`, `<nav>`, `<aside>`, and `<main>` tags for screen readers to parse the layout effectively.

### 3. Color Contrast
- The dark mode color palette (background `#020617`, surface `#071122`, text `#E2E8F0` and primary `#ADC6FF`) passes WCAG AA contrast ratio requirements for both normal (4.5:1) and large text (3:1).
- Error and Success states use distinct iconography alongside color cues (red/green) so meaning is not conveyed by color alone.

### 4. Readability
- Base font size remains at 16px (`text-base` / `font-body-md`) for maximum readability.
- Monospace data fields (`font-mono-data`) utilize a slightly smaller 12px-14px size but maintain high contrast against their surface containers.
