# Rule 06 — Motion & Interaction Standards

Interleet adheres to the Apple Human Interface Guidelines and GitHub principles regarding motion: **motion must clarify state, never entertain**.

---

## 1. Timing & Easing Constraints

- **Duration**: Strict **150ms – 200ms**. Anything longer feels sluggish to developers typing or switching tabs.
- **Easing**: `ease-out` (starts quickly and settles gently).
- **Prohibited Easing**: No spring physics, no bounce effects, no wobble, no elastic overshoots.

```css
/* Approved transition standard */
.ui-transition {
  transition: background-color 150ms ease-out, border-color 150ms ease-out, opacity 150ms ease-out;
}
```

---

## 2. Approved Use Cases for Motion

Motion is permitted **only** to communicate state changes:

1. **Hover Shifts**: 150ms subtle background color shift on interactive rows and buttons.
2. **Drawer / Accordion Expansion**: Clean ease-out expand/collapse of the testcase console or collapsible hints.
3. **Dropdown / Popover Appearance**: Fast 150ms opacity fade and subtle 2px vertical translation when opening.
4. **Active Tab Indicator**: 150ms smooth transition between active tabs.

---

## 3. Loading States: Skeletons Over Spinners

- **Content-heavy views** (e.g. Challenge list, Leaderboard, Submissions history):
  - Must render **skeleton screens** mimicking the shape of the table rows or cards.
  - Skeletons use a calm, low-contrast pulse animation (`bg-muted/30`).
  - Full-page blocking spinner overlays are banned for page transitions.
- **In-place actions** (e.g. "Run code", "Submit", "Sign in"):
  - Use an inline 14px spinner inside the button itself, keeping the button disabled and fixed-width.

---

## 4. Empty States

- **No cartoon illustrations or colorful mascots.**
- A restrained empty state consists of:
  1. A quiet icon in `--color-text-tertiary` (e.g. `Inbox`, `FileCode`, `CheckCircle`).
  2. One concise sentence stating the reality (e.g. "No submissions recorded for this problem yet.").
  3. Optional single secondary action button (e.g. "Run code to test your solution").
- Matches GitHub's sober, reliable tone.

---

## 5. Success Feedback (No Confetti)

- When a problem is accepted or all test cases pass:
  - Display a quiet, clear status badge in the execution panel: **"Accepted"** with runtime (ms) and memory (MB) percentiles.
  - Flash a subtle green checkmark icon in the status bar.
  - **Zero celebratory confetti or modal popups.** The engineer wants to inspect their performance metrics and move to the next challenge immediately.
