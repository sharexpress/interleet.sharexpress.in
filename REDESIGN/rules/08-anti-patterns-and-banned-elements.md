# Rule 08 — Explicit Anti-Patterns & Banned Elements

This rule documents patterns that are **banned outright** across the codebase. Any PR containing these elements will fail design review automatically.

---

## The Blacklist

| Banned Element | Why It Fails | Approved Alternative |
| :--- | :--- | :--- |
| **❌ Purple-to-blue hero gradients** | Looks like generic AI template / crypto landing page. Destroys readability. | Flat near-black surface (`--color-bg-base`) with crisp 1px borders. |
| **❌ Floating card soup** | Every single stat or paragraph wrapped in a heavy bordered box with drop shadow. Causes severe visual fatigue. | Unified section surfaces with subtle 1px divider lines (GitHub model). |
| **❌ Glassmorphism / Frosted Blur** | Decorative backdrop-filter blur slows down canvas rendering and looks dated. | Solid, opaque background elevation layers (`--color-bg-surface` or `--color-bg-overlay`). |
| **❌ Oversized rounded corners (>12px)** | Pills and giant rounded cards look childish on code editors and developer tools. | Strict 6px–8px radius on cards, 4px on buttons and code chips. |
| **❌ Emoji as UI icons** | Emojis vary across operating systems and look informal/unprofessional. | Standard SVG Lucide outline icons with consistent 1.5px or 1.75px stroke. |
| **❌ Multiple accent colors on one screen** | Mixing cyan, amber, purple, and green makes buttons compete for attention. | Exactly 1 accent color per view for primary action and active state. |
| **❌ Centered body paragraphs in app** | Hard to read; breaks left-to-right eye scanning rhythm. | Always left-align body text, descriptions, and lists. |
| **❌ Auto-playing sound or celebratory confetti** | Irritating in workplace or library environments. | Quiet inline status indicator (green badge + runtime metrics). |
| **❌ Dense walls of bold text** | When everything is bold, nothing is emphasized. | Reserve bold (`font-semibold`) strictly for titles and key labels. |
| **❌ Arbitrary padding/margin values** | Breaks the visual rhythm of the interface. | Strict multiples of 4px or 8px on the base grid. |
