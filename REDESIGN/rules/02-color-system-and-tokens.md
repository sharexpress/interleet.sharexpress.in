# Rule 02 — Color System & Theme Tokens

Interleet employs a strict, semantic design token architecture. Components must never hardcode hex, rgb, or ad-hoc tailwind colors.

---

## 1. Single Accent Rule

- **Maximum 1 accent color** active on any screen.
- Accent is strictly reserved for:
  1. Primary call-to-action buttons (e.g. "Run Code", "Submit", "Start Match")
  2. Active/selected navigation items or tabs
  3. Interactive hyperlinks
  4. Subtle focus rings
- Everything else is strictly neutral (grays, near-blacks, near-whites).
- Never mix cyan, purple, blue, and orange accents on the same view.

---

## 2. Background Elevations (GitHub Layering Model)

Surfaces are never pure black (`#000000`). They follow GitHub's layered elevation:

| Elevation Tier | Token | Dark Theme Target | Purpose |
| :--- | :--- | :--- | :--- |
| **Base** | `--color-bg-base` | `#0d1117` / `#090d12` | App canvas, main background, full viewport |
| **Surface** | `--color-bg-surface` | `#161b22` / `#12161f` | Navigation bars, sidebars, cards, table headers |
| **Overlay** | `--color-bg-overlay` | `#21262d` / `#1c2128` | Dropdown menus, modals, tooltips, popovers |

Each level is exactly one step lighter than the layer below it, providing depth without artificial drop shadows.

---

## 3. Borders & Dividers

- Borders are razor-thin: **1px solid**.
- `--color-border-default`: Used for primary container boundaries, table frames, and Monaco pane dividers.
- `--color-border-muted`: Used for subtle inner dividers, table row separators, and list boundaries.
- No glowing border outlines, no gradient borders.

---

## 4. Semantic Status Colors (Fixed & Theme-Independent)

Status and difficulty colors carry universal meaning and never vary by theme:

| Status / Difficulty | Color Family | Text / Icon Token | Subtle Badge Bg Token |
| :--- | :--- | :--- | :--- |
| **Easy / Solved / Success** | Green | `--color-success` (`#22c55e` / `#2ea043`) | `rgba(34, 197, 94, 0.12)` |
| **Medium / Warning / In Progress**| Amber/Orange | `--color-warning` (`#f59e0b` / `#d29922`) | `rgba(245, 158, 11, 0.12)` |
| **Hard / Error / Failed** | Red | `--color-danger` (`#ef4444` / `#f85149`) | `rgba(239, 68, 68, 0.12)` |
| **Neutral / Unattempted / Todo** | Slate Gray | `--color-text-tertiary` (`#8b949e`) | `rgba(139, 148, 158, 0.12)` |

---

## 5. Token Variable Definitions

Every UI component must reference these CSS custom properties or mapped Tailwind utility classes:

```css
:root {
  /* Surfaces */
  --color-bg-base: #0d1117;
  --color-bg-surface: #161b22;
  --color-bg-overlay: #21262d;

  /* Borders */
  --color-border-default: #30363d;
  --color-border-muted: #21262d;

  /* Typography */
  --color-text-primary: #f0f6fc;
  --color-text-secondary: #8b949e;
  --color-text-tertiary: #6e7681;

  /* Accent */
  --color-accent: #238636; /* Default refined emerald/green or brand accent */
  --color-accent-hover: #2ea043;
  --color-accent-muted: rgba(35, 134, 54, 0.15);

  /* Semantic */
  --color-success: #238636;
  --color-warning: #d29922;
  --color-danger: #f85149;
}
```

---

## 6. Contrast & WCAG AA Rule

- All normal text (`< 18px`) must achieve at least **4.5:1** contrast ratio against its surface.
- Large text (`>= 18px bold` or `>= 24px`) must achieve at least **3:1** contrast ratio.
- Never use low-opacity text (`opacity-40` or gray-500 on dark gray) that fails WCAG AA checks.
