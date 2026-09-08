# Rule 05 — Component Specifications

This rule establishes the exact design requirements for the primary building blocks of the Interleet UI.

---

## 1. Buttons

Exactly **three variants** exist in the design system:

| Variant | Visual Treatment | Use Case |
| :--- | :--- | :--- |
| **Primary** | Solid accent background (`--color-accent`), white text, 0px shadow. Hover = `--color-accent-hover`. | Primary screen action (Submit, Run Code, Save). Max 1 per view. |
| **Secondary** | Transparent / surface background, 1px border (`--color-border-default`), neutral text. Hover = `--color-bg-overlay`. | Secondary actions (Reset, Cancel, Filters, Back). |
| **Danger** | Transparent or subtle red tint, border/text `--color-danger`. Solid red only for modal confirm. | Destructive actions (Delete, Surrender match, Reset progress). |

### Button Rules:
- **No Drop Shadows**: Flat surface or 1px border only.
- **No Scale Transitions**: Hover triggers a subtle background color shift (150ms ease-out), never a scale-up or button "lifting" animation.
- **Sentence Case Verbs Only**: Use "Run code" (not "Run Code!" and never "RUN 🚀").
- **Loading State**: When `loading === true`, display an inline 14px spinner inside the button alongside dimmed text. The button width must remain fixed to prevent layout shift.

---

## 2. Problem List Rows (`challenges/index.jsx`)

Follows the LeetCode table row pattern:

```
[Status Icon]   [Title]                   [Difficulty]   [Acceptance %]   [Tags (+N)]
      ✓         1. Two Sum                    Easy           52.4%        Array, Hash...
      -         24. Add Two Numbers           Med            41.2%        Linked List
                128. Longest Consec...        Hard           33.8%        Union Find
```

- **Row Height**: Exactly **40px–44px** per row.
- **Status Column**: Dedicated 32px column with quiet glyph:
  - Solved: Small green checkmark (`Check` icon, 14px).
  - Attempted: Small amber dash / circle (`Minus` icon, 14px).
  - Unsolved: Blank.
- **Title**: High-contrast text (`--color-text-primary`), truncated with ellipsis if exceeding container. Entire row is clickable.
- **Difficulty Tag**: Text + low-contrast semantic background (e.g. `bg-emerald-500/10 text-emerald-400 font-medium px-2 py-0.5 rounded text-xs`). Never solid neon pills.
- **Hover State**: Subtle background tint shift (`--color-bg-surface` -> `--color-bg-overlay`). Zero border changes, zero drop shadows.

---

## 3. Tables (Submissions, Contests, Leaderboards)

Follows GitHub's table architecture:

- **Zebra Striping Banned**: Do not alternate dark and light gray rows. Use 1px bottom border separators (`--color-border-muted`).
- **Sticky Header**: Table header is sticky on scroll with `--color-bg-surface` and 1px bottom border.
- **Monospace Numeric Alignment**:
  - Timestamps, memory consumption, latency figures, and rank numbers must use monospace typography and right-align.

---

## 4. Code Editor Chrome & Console (`editor.$id.jsx`)

- **Monaco Theme Integration**:
  - The editor background must match the application surface (`--color-bg-base`).
  - No default bright blue VS Code title bar bleeding through.
- **Console / Testcase Output Drawer**:
  - Idle state: Clean, empty state prompt ("Run your code to evaluate against test fixtures").
  - Running state: Minimal spinner indicator in output header.
  - Success state: Thin green left accent border + "Passed (3/3 test cases)" banner.
  - Error / Failure state: Thin red left accent border + exact diff / stderr output in monospaced code block with clean word break.

---

## 5. Badges & Tags

- **Maximum 3 visible tags** per problem card before a `+N` overflow indicator.
- Styled as low-contrast metadata chips: `text-[11px] font-mono px-2 py-0.5 rounded border border-border/40 bg-muted/20 text-muted-foreground`.
- Never use colorful rainbow badges that distract from the problem difficulty.

---

## 6. Modals & Overlays

- Capped width: `max-w-md` or `max-w-lg`.
- Centered on screen with dark semi-transparent backdrop (`bg-black/60`).
- Always dismissible via `Escape` key or clicking outside.
- Exactly 1 primary button (right-aligned) and 1 cancel button.
- Modal-in-modal (nested dialogs) is strictly forbidden.
