---
name: SIF Copilot V2
colors:
  surface: '#051424'
  surface-dim: '#051424'
  surface-bright: '#2c3a4c'
  surface-container-lowest: '#010f1f'
  surface-container-low: '#0d1c2d'
  surface-container: '#122131'
  surface-container-high: '#1c2b3c'
  surface-container-highest: '#273647'
  on-surface: '#d4e4fa'
  on-surface-variant: '#c2c6d6'
  inverse-surface: '#d4e4fa'
  inverse-on-surface: '#233143'
  outline: '#8c909f'
  outline-variant: '#424754'
  surface-tint: '#adc6ff'
  primary: '#adc6ff'
  on-primary: '#002e6a'
  primary-container: '#4d8eff'
  on-primary-container: '#00285d'
  inverse-primary: '#005ac2'
  secondary: '#4edea3'
  on-secondary: '#003824'
  secondary-container: '#00a572'
  on-secondary-container: '#00311f'
  tertiary: '#ffb3ad'
  on-tertiary: '#68000a'
  tertiary-container: '#ff5451'
  on-tertiary-container: '#5c0008'
  error: '#ffb4ab'
  on-error: '#690005'
  error-container: '#93000a'
  on-error-container: '#ffdad6'
  primary-fixed: '#d8e2ff'
  primary-fixed-dim: '#adc6ff'
  on-primary-fixed: '#001a42'
  on-primary-fixed-variant: '#004395'
  secondary-fixed: '#6ffbbe'
  secondary-fixed-dim: '#4edea3'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#ffdad7'
  tertiary-fixed-dim: '#ffb3ad'
  on-tertiary-fixed: '#410004'
  on-tertiary-fixed-variant: '#930013'
  background: '#051424'
  on-background: '#d4e4fa'
  surface-variant: '#273647'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 48px
    fontWeight: '700'
    lineHeight: 56px
    letterSpacing: -0.02em
  headline-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '600'
    lineHeight: 40px
    letterSpacing: -0.01em
  headline-lg-mobile:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-md:
    fontFamily: Inter
    fontSize: 20px
    fontWeight: '600'
    lineHeight: 28px
  body-lg:
    fontFamily: Inter
    fontSize: 16px
    fontWeight: '400'
    lineHeight: 24px
  body-md:
    fontFamily: Inter
    fontSize: 14px
    fontWeight: '400'
    lineHeight: 20px
  label-md:
    fontFamily: Geist
    fontSize: 12px
    fontWeight: '500'
    lineHeight: 16px
    letterSpacing: 0.02em
  mono-data:
    fontFamily: Geist
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
rounded:
  sm: 0.25rem
  DEFAULT: 0.5rem
  md: 0.75rem
  lg: 1rem
  xl: 1.5rem
  full: 9999px
spacing:
  base: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  gutter: 16px
  margin: 24px
---

## Brand & Style

This design system is engineered for the intersection of institutional finance and generative AI. The aesthetic, characterized as "Bloomberg-meets-Perplexity," prioritizes high-density data visualization with an ultra-premium, technical finish. It evokes an emotional response of absolute reliability, precision, and forward-thinking intelligence.

The visual style utilizes a refined **Glassmorphism** approach. Rather than excessive blur, it focuses on surface-on-surface stacking with subtle translucency to maintain a sense of depth without compromising legibility. The interface is intentionally "cool" and dark, suggesting a command-center environment where critical decisions are made.

## Colors

The palette is anchored in deep oceanic blacks and navy tones to provide a stable, high-contrast foundation for data. 

- **Primary Accent:** A vibrant Blue (#3B82F6) used for AI-driven insights and primary actions.
- **Semantic Colors:** Success Green and Risk Red are used sparingly for directional data indicators (market gains/losses).
- **Surface Strategy:** We use a tiered dark system. The main background is near-black, while panels use a slightly lifted blue-tinted dark. Borders provide the structural definition, acting as the primary separator rather than heavy shadows.

## Typography

Typography is systematic and functional. **Inter** serves as the primary typeface for its exceptional legibility in dense interfaces. For technical data, financial figures, and code snippets, **Geist** is utilized as the secondary font to provide a monospaced, developer-centric feel that reinforces the "Copilot" intelligence aspect.

Tight tracking (letter-spacing) is applied to larger headlines to maintain a premium, editorial look. Body text remains open to ensure readability during long-form research sessions.

## Layout & Spacing

This design system employs a **Fluid Grid** model optimized for high information density. 

- **Grid:** A 12-column layout for desktop with 16px gutters allows for complex multi-panel dashboard views.
- **Density:** Spacing is compact (4px/8px increments). This "high-density" approach is critical for institutional tools where users need to see maximum data with minimal scrolling.
- **Breakpoints:** On mobile devices, panels stack vertically, and horizontal margins reduce to 16px to maximize screen real estate.

## Elevation & Depth

Depth is achieved through **Tonal Layering** and **Glassmorphism** rather than traditional elevation.

- **Surface Stacking:** Elements closer to the user are rendered in slightly lighter shades of the panel background (#071122).
- **Backdrop Blur:** Modal overlays and floating menus use a 12px backdrop blur with a 60% opacity fill to maintain context of the underlying data.
- **Glow Effects:** Critical AI components or active states feature a "subtle glow"—a low-spread, primary-colored outer shadow (e.g., `0px 0px 15px rgba(59, 130, 246, 0.15)`) to signify activity and intelligence.
- **Borders:** All containers use a 1px solid border (#152238). This provides the "Bloomberg" structural rigor.

## Shapes

The shape language is sophisticated and controlled. We utilize a dual-radius system to create visual hierarchy:

- **Large Containers (Cards, Panels):** These use a 12px radius (`rounded-lg` in this system), giving the interface a modern, "Perplexity-style" soft edge.
- **Small Components (Buttons, Inputs, Tags):** These use an 8px radius, maintaining a sharp, professional look that fits within the larger containers without creating awkward negative space.
- **Interactive Elements:** Checkboxes and small toggles maintain a 4px radius for a technical, precise feel.

## Components

### Buttons
Primary buttons feature a solid Accent Blue fill with white text. Secondary buttons are "Ghost" style—transparent with an #152238 border, utilizing the subtle glow on hover to indicate interactivity.

### Cards & Panels
All cards must use the 12px corner radius. Backgrounds are strictly #071122. Headlines within cards should be followed by a 1px separator line to define header/content areas.

### Inputs
Fields use the #020617 background to "recess" into the panel. On focus, the border transitions to Accent Blue with a subtle 4px inner glow.

### Chips & Tags
Data tags (e.g., Ticker Symbols) use the Geist font and an 8px radius. Backgrounds for tags should be low-opacity versions of the accent colors (e.g., 10% Blue for informational tags).

### Data Tables
Tables are the heart of the system. They feature 0px border-radius, using only horizontal #152238 borders to maximize row density. Alternating row zebra-striping is prohibited; use hover highlights instead.