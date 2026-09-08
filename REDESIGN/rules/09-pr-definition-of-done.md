# Rule 09 — PR Review & Gatekeeping Checklist

Before any PR touching frontend UI is approved or merged into `main`, the author and reviewer must verify each item on this checklist.

---

## The UI 2.0 Gatekeeper Checklist

### 1. Token & Color Discipline
- [ ] Uses only semantic design tokens (`--color-bg-base`, `--color-border-default`, etc.) — zero hardcoded hex codes (`#1f2937`) or arbitrary Tailwind utilities (`bg-zinc-850`).
- [ ] Maximum 1 accent color used across the screen.
- [ ] Difficulty/status indicators strictly follow semantic green (Easy/Pass), amber (Medium/Warn), red (Hard/Fail), gray (Neutral).
- [ ] Contrast passes WCAG AA standards (4.5:1 for body text, 3:1 for large text).

### 2. Spacing & Typography
- [ ] Every padding, margin, gap, and dimension is a multiple of 4 or 8 (the 8px base grid).
- [ ] Typography uses only the defined scale (`display`, `title`, `body`, `caption`, `micro`).
- [ ] Monospace font used for code, test inputs, schemas, and numeric table metrics.
- [ ] All body text is left-aligned; all numeric table columns are right-aligned.

### 3. Component Architecture
- [ ] Buttons use only the 3 standard variants: Primary (accent fill, 0px shadow), Secondary (outline/ghost), Danger (destructive).
- [ ] No new button or card variants invented without design system documentation.
- [ ] Tables are zebra-free with 1px border dividers and sticky headers (GitHub pattern).
- [ ] Problem lists adhere to LeetCode's 1-row density (status glyph, title, difficulty, acceptance %, tags).
- [ ] Empty states contain a calm sentence and zero cartoon illustrations.

### 4. Motion & Interactivity
- [ ] Transitions are 150ms–200ms ease-out. No spring or bouncy animations.
- [ ] Content loading states use skeleton loaders rather than full-page blocking spinners.
- [ ] No confetti or celebratory modal popups on problem solve.

### 5. Content & Copy
- [ ] Sentence case used across all titles, buttons, and labels.
- [ ] Zero exclamation marks in system copy.
- [ ] Error messages state what happened and what to do next.
- [ ] Zero marketing language inside authenticated product screens.

### 6. Anti-Pattern Blacklist Check
- [ ] Zero purple/blue hero gradients.
- [ ] Zero decorative glassmorphism or backdrop-filter blurs.
- [ ] Zero rounded corners greater than 12px on functional UI elements.
- [ ] Zero emoji used as UI icons.
- [ ] Zero floating card soup or unnecessary drop shadows.

---

*Verified by: Interleet Engineering & Design Review*
