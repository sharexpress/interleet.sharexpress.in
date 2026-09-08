# Rule 04 — Layout & Navigation Architecture

Interleet is organized into two primary page layouts:
1. **The Tool / IDE Layout** (Full viewport, resizable panes, split view)
2. **The Content / Data Layout** (Constrained max-width, top navigation)

---

## 1. Top Navigation Bar (`AppShell.jsx`)

- **Fixed height**: Exactly **56px** (`h-14`), never taller.
- **Z-Index**: Sticky or fixed top (`z-40`), crisp 1px bottom border (`--color-border-default`), background elevation `--color-bg-surface`.
- **Navigation Links**:
  - Horizontal items (Problems, Contests, System Design, Interviews, Store, Leaderboard).
  - Active state: Subdued background highlight or quiet bottom indicator border in accent color — no giant glowing buttons.
  - Hover state: Subtle text color shift from `--color-text-secondary` to `--color-text-primary`.
- **Right Action Cluster**:
  - Streak pill (compact text + fire glyph, low-contrast background).
  - XP counter.
  - User avatar dropdown.
  - Zero secondary stacked marketing banners beneath navigation.

---

## 2. The Problem-Solving IDE Workspace (`editor.$id.jsx`)

Follows the canonical LeetCode / VS Code engineering pattern:

```
+-------------------------------------------------------------------------+
| [Interleet Nav / Workspace Header]                                 56px |
+------------------------------------+------------------------------------+
| LEFT PANE (Problem & Context)      | RIGHT PANE (Editor & Console)      |
|                                    |                                    |
| [Tabs: Description|Hints|Solutions]| [Language Selector | Pinned Actions]|
|                                    |                                    |
| 760px reading max-width container  | Monaco Code Editor (Full Height)   |
| Markdown statement, tables, schema |                                    |
|                                    +------------------------------------+
|                                    | [Testcase | Output Console]        |
|                                    | Tabs: Case 1 | Case 2 | Raw Stdin  |
+------------------------------------+------------------------------------+
```

### IDE Specific Rules:
- **Two-Pane Split**:
  - Resizable horizontal divider between Left and Right panes.
  - Resizable vertical divider between Editor and Bottom Console.
  - Pane dimensions must be persisted in `localStorage` per user session.
- **Reading-Focused Container in Left Pane**:
  - Max text width of **760px–840px** inside the description tab to avoid overly wide lines that degrade reading comprehension.
- **Pinned Toolbar**:
  - Language dropdown (`Python`, `SQL`, `TypeScript`, `C++`, etc.), Reset starter button, Run Code button, and Submit button are pinned in a dedicated header bar above the editor. They never shift or disappear when scrolling.

---

## 3. Data-Dense Tables & Explorer Views (`challenges/index.jsx`, `leaderboard.jsx`)

- Full container width up to **1280px** (`max-w-7xl`).
- Filter bar sits immediately above the table:
  - Search input with standard magnifier icon.
  - Domain filter pills (Algorithms, Backend, Databases, DevOps, Frontend).
  - Difficulty filter (Easy, Medium, Hard).
  - Status filter (Solved, Attempted, Todo).
- No floating cards with oversized white borders; clean, unified table surface.
