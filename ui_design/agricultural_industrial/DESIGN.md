---
name: Agricultural Industrial
colors:
  surface: '#fbf8ff'
  surface-dim: '#d5d8f9'
  surface-bright: '#fbf8ff'
  surface-container-lowest: '#ffffff'
  surface-container-low: '#f4f2ff'
  surface-container: '#ececff'
  surface-container-high: '#e5e6ff'
  surface-container-highest: '#dee0ff'
  on-surface: '#161a32'
  on-surface-variant: '#414844'
  inverse-surface: '#2b2f48'
  inverse-on-surface: '#f0efff'
  outline: '#717973'
  outline-variant: '#c1c8c2'
  surface-tint: '#3f6653'
  primary: '#012d1d'
  on-primary: '#ffffff'
  primary-container: '#1b4332'
  on-primary-container: '#86af99'
  inverse-primary: '#a5d0b9'
  secondary: '#0e6c4a'
  on-secondary: '#ffffff'
  secondary-container: '#a0f4c8'
  on-secondary-container: '#19724f'
  tertiary: '#401b1b'
  on-tertiary: '#ffffff'
  tertiary-container: '#5a302f'
  on-tertiary-container: '#d29895'
  error: '#ba1a1a'
  on-error: '#ffffff'
  error-container: '#ffdad6'
  on-error-container: '#93000a'
  primary-fixed: '#c1ecd4'
  primary-fixed-dim: '#a5d0b9'
  on-primary-fixed: '#002114'
  on-primary-fixed-variant: '#274e3d'
  secondary-fixed: '#a0f4c8'
  secondary-fixed-dim: '#85d7ad'
  on-secondary-fixed: '#002113'
  on-secondary-fixed-variant: '#005236'
  tertiary-fixed: '#ffdad8'
  tertiary-fixed-dim: '#f5b7b4'
  on-tertiary-fixed: '#331111'
  on-tertiary-fixed-variant: '#673a39'
  background: '#fbf8ff'
  on-background: '#161a32'
  surface-variant: '#dee0ff'
typography:
  display-lg:
    fontFamily: Inter
    fontSize: 32px
    fontWeight: '700'
    lineHeight: 40px
    letterSpacing: -0.02em
  headline-md:
    fontFamily: Inter
    fontSize: 24px
    fontWeight: '600'
    lineHeight: 32px
  headline-sm:
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
  body-sm:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
  label-bold:
    fontFamily: Inter
    fontSize: 12px
    fontWeight: '600'
    lineHeight: 16px
    letterSpacing: 0.05em
  table-data:
    fontFamily: Inter
    fontSize: 13px
    fontWeight: '400'
    lineHeight: 18px
  code-sm:
    fontFamily: JetBrains Mono
    fontSize: 12px
    fontWeight: '400'
    lineHeight: 16px
rounded:
  sm: 0.125rem
  DEFAULT: 0.25rem
  md: 0.375rem
  lg: 0.5rem
  xl: 0.75rem
  full: 9999px
spacing:
  unit: 4px
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  gutter: 16px
  sidebar_width: 260px
---

## Brand & Style
The design system is built for "Agricultural Industrial" utility: a hybrid of high-precision data management and rugged environmental reliability. It targets agricultural back-office operations and fleet managers who require high-density information without cognitive fatigue. 

The aesthetic is **Modern-Industrial Minimalism**. It prioritizes clarity, structural integrity, and professional trust. The UI uses a "Functional Brutalist" influence—utilizing strong alignment, subtle borders, and clear status indicators—to ensure that the application feels like a dependable tool rather than a consumer app. The emotional response should be one of control, efficiency, and industrial-grade durability.

## Colors
The palette is rooted in the "Deep Forest" primary, providing a grounded, authoritative foundation for headers and primary actions. "Sage" serves as a functional highlight and success indicator, softening the industrial edges. 

"Slate Gray" is utilized for secondary data points, metadata, and iconography to maintain professional neutrality. The "Warning Orange" is reserved strictly for high-priority exceptions, ensuring "Needs Review" items are immediately scannable. The background remains a crisp "Off-White" to minimize glare during long work sessions, with pure white surfaces used to define card-based containment.

## Typography
Inter is the workhorse of this design system, chosen for its exceptional legibility in dense data tables and technical interfaces. Headings use a tighter letter-spacing and heavier weight to feel "stamped" and permanent. 

JetBrains Mono is used as a functional secondary font for alphanumeric receipt strings, log timestamps, and calculated values. This distinction helps the user differentiate between descriptive text and raw data. Labels utilize uppercase styling with increased tracking to serve as clear section identifiers without overwhelming the layout.

## Layout & Spacing
The design system employs a **Fixed-Fluid Hybrid** layout. A persistent left sidebar (260px) provides global navigation, while the main content area utilizes a fluid 12-column grid. 

Spacing follows a strict 4px baseline grid to maintain industrial precision. Data-heavy views utilize "Compact" spacing (8px gutters) to maximize information density, while dashboard views utilize "Comfortable" spacing (24px) for high-level monitoring. Margins are locked at 24px on desktop to provide a solid frame for the data.

## Elevation & Depth
Depth is conveyed through **Tonal Layering and Low-Contrast Outlines** rather than heavy shadows. This reinforces the "flat/robust" industrial feel.

- **Level 0 (Background):** Off-white (#F8F9FA) base layer.
- **Level 1 (Surface):** Pure white (#FFFFFF) containers with a 1px solid border (#DDE2E5). No shadow.
- **Level 2 (Interactive):** Elements like dropdowns or active modals use a very subtle, tight ambient shadow (4px blur, 5% opacity) to suggest they are sitting just above the work surface.
- **Level 3 (Focus):** Active inputs or selected table rows use a 2px "Deep Forest" left-edge border or a subtle Sage-tinted background.

## Shapes
The shape language is "Soft-Industrial." The system uses a **0.25rem (4px)** base radius for buttons and containers. This creates a profile that is clean and modern but retains a "machined" look. Circular shapes are used exclusively for status pips and user avatars to provide a clear visual contrast against the otherwise rectilinear grid.

## Components

### Buttons
Primary actions (e.g., "Start Processing") use the "Deep Forest" background with white text. Secondary actions use the "Slate Gray" as a ghost-button style (outline only). Buttons have a height of 40px for standard tasks and 48px for critical "Machine-Start" style triggers.

### Data Tables
High-density rows with a 1px bottom border. Header rows use "Slate Gray" text with a "label-bold" style and a light gray background (#F1F3F5). Alternate row striping is recommended for tables exceeding 10 rows.

### Status Badges
Small, pill-shaped indicators with high-contrast text. 
- **Processed:** Sage background (#D8F3DC) with Deep Forest text.
- **Needs Review:** Warning Orange background (#FFE8CC) with Dark Orange text.
- **Duplicate:** Slate Gray background with White text.

### Real-Time Monitors
Processing monitors use a "Sage" progress bar on a light gray track. "Live View" thumbnails must have a 1px border and a fixed aspect ratio to maintain the grid's structural integrity.

### Input Fields
Rectangular with a 1px border. On focus, the border transitions to "Deep Forest" with a 2px thickness. Error states utilize a crimson red border and 12px helper text.

### Sidebar
The navigation uses "Deep Forest" for the background to create a strong visual anchor. Active states are indicated by a "Sage" vertical bar on the left edge and a subtle increase in font weight.