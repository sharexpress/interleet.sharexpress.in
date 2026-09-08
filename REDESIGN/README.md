# Interleet UI 2.0 — Master Specification & Architectural Context

> **Branch**: `ui-2.0-redesign`  
> **Status**: Design System & Rules Definition Phase  
> **Governing Principles**: LeetCode Information Density · GitHub Data Discipline · Apple Typography & Restraint

---

## 1. Application Context & Product Ecosystem

**Interleet** (`interleet.sharexpress.in`) is an enterprise-grade technical interview preparation, engineering simulation, and live contest platform. Unlike generic algorithm trainers, Interleet supports multi-domain, production-realistic engineering workloads with real runtime sandboxes.

### 1.1 Core Product Domains & Features

| Domain / Engine | Core Capabilities & Architecture | Primary UI Route |
| :--- | :--- | :--- |
| **Algorithms & Data Structures** | Sandboxed multi-language code execution (Python, JS, TS, C++, Go, Java, Rust) with hidden test suites, memory limits, and p95 latency verification. | `/app/editor/:id` |
| **SQL & Relational Databases** | Isolated relational sandboxes (PostgreSQL, SQLite, MySQL). Executes queries against dynamic schema definitions and seeded table fixtures with table visualization. | `/app/editor/:id` |
| **System Design Studio** | Interactive node-and-edge architecture simulator powered by ReactFlow. Simulates RPS throughput, cache hits, database replication lag, and single-point-of-failure bottlenecks. | `/app/system-design` |
| **Sara AI Mock Interviews** | Real-time voice + text technical conversational interview simulator. Features dynamic decision trees, live transcript evaluation, and multi-dimensional rubric scoring (radar charts). | `/app/interviews`, `/app/interviews/live`, `/app/interviews/:id/report` |
| **Live Contests & 1v1 Arena** | Real-time competitive coding arena with 1v1 matchmaking, lobby chat, timed problem sets, anti-cheat detection, and live Elo leaderboard standings. | `/app/contest`, `/app/contest/:id/lobby`, `/app/contest/:id/workspace` |
| **Challenge Catalog** | Searchable directory with domain filters (Algorithms, Backend, Databases, DevOps, Frontend), difficulty pills, completion status, and tags. | `/app/challenges` |
| **Store & Gamification** | Streak protection, XP rewards, collectible profile badges, and Pro tier upgrades. | `/app/store`, `/app/profile/:username` |
| **Admin Control Plane** | Challenge authoring, seed database configuration, contest management, user moderation, and platform metrics. | `/admin` |

---

## 2. Why UI 2.0? The Problem Statement

Over iterative feature sprints, the application accumulated **design debt** and visual inconsistencies common to modern SaaS prototypes:

1. **"AI-Generated Slop" Aesthetics**:
   - Random purple-to-blue gradient banners and decorative card outlines.
   - Heavy drop shadows ("floating card soup") causing visual fatigue.
   - Large, rounded emoji badges and non-standard pill buttons.
   - Decorative frosted glass / glassmorphism applied without functional purpose.
2. **Inconsistent Density & Layout Friction**:
   - The challenge list has excess vertical whitespace compared to LeetCode's razor-sharp, 1-line-per-problem grid.
   - The code editor layout suffered from oversized paddings, redundant starter code cards, and disjointed toolbars.
   - Inconsistent typography scales across pages (varying heading sizes, ad-hoc font weights, and centered body text).
3. **Information Noise**:
   - Exclamation marks and marketing copy inside authenticated product pages.
   - Competing accent colors (cyan, purple, emerald, blue) fighting for visual attention on the same screen.

---

## 3. UI 2.0 Design Benchmarks

We measure every UI screen against three industry standards:

1. **LeetCode** (Information Density & Solving UX):
   - High information per vertical pixel.
   - 1-line problem table rows with subtle status glyphs, difficulty tags, and acceptance rates.
   - Focused, 2-pane resizable IDE workspace where the code editor and test console remain front-and-center.
2. **GitHub** (Data Discipline & Dark Mode Restraint):
   - Strict near-black palette (`#0d1117` class) with clear surface elevations (base → surface → overlay).
   - Low-contrast, text-forward label badges (no saturated neon pills).
   - Zebra-free data tables with 1px border dividers, monospace numerals, and right-aligned metrics.
3. **Apple / Apple HIG** (Typography & Motion Discipline):
   - Single clean UI typeface stack paired with single monospace code stack.
   - Fixed 8px spacing grid — zero arbitrary margin or padding values.
   - 150–200ms ease-out transitions solely for state changes — zero bouncing, springs, or gratuitous animations.

---

## 4. UI 2.0 Design Rules Index

The complete rule specifications are documented in the [`rules/`](file:///Users/santushtkotai/Desktop/sharexpress/interleet.sharexpress.in/REDESIGN/rules) directory:

- [**01. Design Philosophy**](file:///Users/santushtkotai/Desktop/sharexpress/interleet.sharexpress.in/REDESIGN/rules/01-design-philosophy.md) — The 5 cardinal laws: Function first, density with clarity, silence over noise, consistency, and zero AI slop.
- [**02. Color System & Theme Tokens**](file:///Users/santushtkotai/Desktop/sharexpress/interleet.sharexpress.in/REDESIGN/rules/02-color-system-and-tokens.md) — Strict CSS variables, 1-accent restriction, semantic difficulty colors (green/amber/red), and WCAG AA contrast.
- [**03. Typography & Spacing Grid**](file:///Users/santushtkotai/Desktop/sharexpress/interleet.sharexpress.in/REDESIGN/rules/03-typography-and-spacing-grid.md) — 8px base grid, 4-tier type scale (`display`, `title`, `body`, `caption`), and font pairing rules.
- [**04. Layout & Navigation Architecture**](file:///Users/santushtkotai/Desktop/sharexpress/interleet.sharexpress.in/REDESIGN/rules/04-layout-and-navigation.md) — Fixed 56px top bar, 2-pane LeetCode IDE with persisted widths, and reading-width caps.
- [**05. Component Specifications**](file:///Users/santushtkotai/Desktop/sharexpress/interleet.sharexpress.in/REDESIGN/rules/05-component-specifications.md) — Detailed specs for Buttons, Problem Rows, GitHub Tables, Monaco Chrome, Modals, Empty States, and Tags.
- [**06. Motion & Interaction Standards**](file:///Users/santushtkotai/Desktop/sharexpress/interleet.sharexpress.in/REDESIGN/rules/06-motion-and-states.md) — 150–200ms ease-out transitions, skeleton loaders (no full-page spinners), and quiet feedback.
- [**07. Content & Microcopy Rules**](file:///Users/santushtkotai/Desktop/sharexpress/interleet.sharexpress.in/REDESIGN/rules/07-content-and-microcopy.md) — Sentence case, zero exclamation marks, and tool-first clarity.
- [**08. Anti-Patterns & Banned Elements**](file:///Users/santushtkotai/Desktop/sharexpress/interleet.sharexpress.in/REDESIGN/rules/08-anti-patterns-and-banned-elements.md) — Banned visual patterns with approved alternatives.
- [**09. PR Review & Gatekeeping Checklist**](file:///Users/santushtkotai/Desktop/sharexpress/interleet.sharexpress.in/REDESIGN/rules/09-pr-definition-of-done.md) — Mandatory checklist before merging any UI PR.

---

## 5. UI 2.0 Screen-by-Screen Transformation Map

| Target Screen / Component | Current Design Debt | UI 2.0 Transformation Plan |
| :--- | :--- | :--- |
| **Navigation (`AppShell.jsx`)** | Inconsistent height, mixed button styles, badge clutter. | Fixed 56px height, single accent indicator for active route, clean profile dropdown, zero marketing tags. |
| **Challenge Directory (`challenges/index.jsx`)** | Bulky card rows, scattered filter dropdowns, excess padding. | LeetCode-style tight grid: small status glyph (solved/attempted/todo), bold title, subdued difficulty pill, acceptance rate, tags with overflow "+N". |
| **Challenge Detail (`challenges/$id.jsx`)** | Empty 2nd column, oversized headings. | Clean single-column 780px reading container, standardized Markdown typography, clear action bar pinned at bottom. |
| **Workspace IDE (`editor.$id.jsx`)** | Inconsistent Monaco theme border, cluttered left sidebar, duplicate description tabs. | Full-bleed 2-pane IDE with Monaco editor matching app dark theme, tabbed left panel (Description / Hints / Submissions / Notes), pinned toolbar for Run/Submit with inline spinner. |
| **Contest Workspace (`ContestWorkspace.jsx`)** | Mismatched font scales, unformatted descriptions. | Seamless LeetCode contest mode: top countdown timer bar, integrated Markdown description, compact test case runner. |
| **System Design (`system-design.jsx`)** | Busy sidebars, heavy floating properties panels. | Minimalist dark canvas, muted node styles with high-contrast text, sleek bottom telemetry bar for latency/RPS simulation. |
| **AI Mock Interview (`interviews/`)** | Loud gradients, large speech bubbles. | Quiet conversation stream, audio wave visualizer with subtle accent, structured rubric report with GitHub-grade tables. |
| **User Profile & Dashboard (`profile/`, `dashboard.jsx`)** | Floating card soup, oversized stats widgets. | GitHub-style contribution activity heatmap, clean 1-line recent solves list, subdued badge grid without neon glows. |

---

## 6. Execution Protocol & Safety Constraints

1. **Branch Isolation**: All UI 2.0 work happens on `ui-2.0-redesign`.
2. **Zero Deployment to Production without Explicit Approval**: Never run deploy scripts or push to `main` until Santush reviews and approves.
3. **No Regressions**: All backend APIs, WebSocket connections, Monaco bindings, and existing tests (Vitest + ESLint) must stay green on every commit.
4. **Token-First Implementation**: Build the foundational CSS variables and tokens in `index.css` before rewriting individual components.
