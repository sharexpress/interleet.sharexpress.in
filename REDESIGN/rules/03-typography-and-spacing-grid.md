# Rule 03 — Typography & Spacing Grid

Typography and spacing define structural hierarchy. Random margins and arbitrary font sizes dilute readability.

---

## 1. Typeface Stacks

Interleet strictly enforces **two typeface families**:

1. **Primary UI Sans**:
   - Stack: `Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif`
   - Purpose: Navigation, labels, titles, descriptions, buttons, and dialogs.
2. **Code & Tabular Monospace**:
   - Stack: `"JetBrains Mono", "SF Mono", Menlo, Consolas, Monaco, monospace`
   - Purpose: Monaco code editor, test case inputs/outputs, SQL schemas, execution runtime/memory figures, and timestamps.

---

## 2. Fixed Type Scale (No Ad-Hoc Sizes)

| Token | Size | Line Height | Weight | Approved Use |
| :--- | :--- | :--- | :--- | :--- |
| `display` | 28px – 32px | 1.2 | `600` / `700` | High-level page titles (e.g. "Contest Arena", "System Design Studio") — rare. |
| `title` | 18px – 20px | 1.25 | `600` | Problem title, section headers, modal headers. |
| `body` | 14px | 1.5 | `400` / `500` | Default UI text, problem description statements, list entries. |
| `caption` | 12px | 1.4 | `400` / `500` | Meta info, timestamps, table cells, tags, execution telemetry. |
| `micro` | 11px | 1.3 | `600` mono | Uppercase table headers, code snippet language badges. |

---

## 3. Hierarchy Rules

- **Weight carries emphasis, not size or color.** Use font weight `500` or `600` to distinguish labels from values, rather than bumping font sizes or splashing multiple colors.
- **Left-alignment is mandatory.** Left-align all headings, body paragraphs, and descriptions. Centered body text is strictly banned inside the authenticated product experience.
- **Numbers are right-aligned and monospaced.** In data tables (e.g. acceptance rate, runtime ms, memory MB, XP, Elo rating), numbers must be right-aligned and use monospace figures (`tabular-nums`) to allow instant vertical scanning.

---

## 4. The 8px Base Grid

Every padding, margin, width, and height must resolve to a multiple of **4px or 8px**:

| Grid Step | Pixel Value | Typical Utility |
| :--- | :--- | :--- |
| **0.5x** | `4px` | Pill padding, inline icon gaps |
| **1x** | `8px` | Small element gap, button vertical padding |
| **1.5x** | `12px` | Card internal padding, button horizontal padding |
| **2x** | `16px` | Standard container padding, form field gap |
| **3x** | `24px` | Section gap, modal padding |
| **4x** | `32px` | Major block margin, page gutter |
| **6x** | `48px` | Page section separation |
| **8x** | `64px` | Hero / major view spacing |

❌ **Banned arbitrary values**: `padding: 13px`, `gap: 18px`, `margin-top: 22px`.
