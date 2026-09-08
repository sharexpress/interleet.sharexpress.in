# Rule 02 — Color System & Theme Tokens

Interleet employs a strict, semantic design token architecture. Components must never hardcode hex, rgb, or ad-hoc tailwind colors.

---

## 1. Signature Brand Palette: Orange & Black

Interleet's identity is defined by its signature **Orange & Black** visual signature:
- **Base Background**: Deep Black (`#000000`)
- **Primary Brand Accent**: Interleet Orange (`#FF6500`)
- **Surfaces & Cards**: Elevated `#0A0A0A` and `#141414`
- **Borders & Dividers**: Crisp `#262626`
- **Secondary & Accent Tints**: `#1A1A1A`

The redesign is strictly focused on **structure, layout, density, typography, and UX flow** — never altering the core Orange & Black identity.

---

## 2. Background Elevations (Interleet Layering Model)

Surfaces layer smoothly above the pure black canvas:

| Elevation Tier | Token | Dark Theme Value | Purpose |
| :--- | :--- | :--- | :--- |
| **Base** | `--background` | `#000000` | Viewport canvas, main background |
| **Surface / Card** | `--card` | `#0A0A0A` | Navigation bars, cards, table frames, left IDE pane |
| **Panel** | `--panel` | `#141414` | Inner containers, testcase drawers, code boxes |
| **Overlay / Accent** | `--accent` | `#1A1A1A` | Dropdown menus, tooltips, popovers, hover tints |

---

## 3. Borders & Dividers

- Borders are razor-thin: **1px solid `#262626`** (`--border`).
- No glowing border outlines, no rainbow gradients.

---

## 4. Semantic Status Colors

Status and difficulty colors:

| Status / Difficulty | Color Family | Hex Value | Purpose |
| :--- | :--- | :--- | :--- |
| **Easy / Solved / Success** | Emerald Green | `#4FB286` / `#22c55e` | Solved glyphs, success alerts |
| **Medium / Warning / In Progress** | Interleet Orange | `#FF6500` | Medium difficulty, pending status |
| **Hard / Error / Failed** | Crimson Red | `#E84A5F` / `#ef4444` | Hard difficulty, test failure |
| **Neutral / Unattempted** | Muted Gray | `#8b949e` / `#A1A1A1` | Unattempted dash, metadata |

---

## 5. Token Variable Definitions

```css
:root, .dark {
  --radius: 0.375rem; /* 6px disciplined radius */
  --background: #000000;
  --foreground: #FFFFFF;
  --card: #0A0A0A;
  --card-foreground: #FFFFFF;
  --popover: #0A0A0A;
  --popover-foreground: #FFFFFF;
  --panel: #141414;
  --panel-foreground: #FFFFFF;
  --primary: #FF6500;
  --primary-foreground: #FFFFFF;
  --secondary: #1A1A1A;
  --secondary-foreground: #FFFFFF;
  --muted: #0F0F0F;
  --muted-foreground: #A1A1A1;
  --accent: #1A1A1A;
  --accent-foreground: #FFFFFF;
  --destructive: #E84A5F;
  --destructive-foreground: #FFFFFF;
  --success: #4FB286;
  --success-foreground: #06120A;
  --warning: #FF6500;
  --warning-foreground: #FFFFFF;
  --border: #262626;
  --input: #141414;
  --ring: #FF6500;
}
```

---

## 6. Contrast & WCAG AA Rule

- All normal text (`< 18px`) must achieve at least **4.5:1** contrast ratio against its surface.
- High-contrast white `#FFFFFF` text on deep black `#000000` / card `#0A0A0A` delivers **18:1+ contrast**, well exceeding WCAG AAA standards.
- Never use low-opacity text that fails WCAG AA checks.
