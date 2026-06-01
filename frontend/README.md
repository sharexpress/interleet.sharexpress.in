# Interleet Frontend — Vite + React + JavaScript

Refactored from the original TanStack Start + TypeScript project into a clean Vite + React (JSX) project with Redux Toolkit and React Router DOM. UI, theme, styling, and behavior are preserved exactly.

## Stack

- **Vite 7** + **React 19** (JSX, no TypeScript)
- **React Router DOM v6** (`createBrowserRouter` with data loaders)
- **Redux Toolkit** + **react-redux** for global state
- **Tailwind CSS v4** (via `@tailwindcss/vite`) with the original design tokens
- **shadcn/ui** primitives (Radix + class-variance-authority)
- **Framer-motion-style animations** preserved via `tw-animate-css`
- **Recharts**, **Sonner** (toasts), **Lucide** icons, **react-hook-form** + **zod**

## Folder structure

```
src/
├── assets/                  (add your static imports here)
├── components/
│   ├── ui/                  shadcn primitives (Button, Card, Dialog, ...)
│   ├── auth/                AuthShell
│   ├── brand/               Logo
│   ├── domain/              ChallengeCard, Tags
│   ├── layout/              AppShell, PageHeader
│   └── marketing/           Marketing nav + footer
├── hooks/
│   └── use-mobile.jsx
├── lib/
│   ├── mock.js              mock data
│   └── utils.js             cn() helper
├── pages/                   one file per route (was src/routes/)
│   ├── index.jsx            "/"
│   ├── login.jsx, signup.jsx, forgot.jsx, recruiter.jsx, admin.jsx
│   ├── NotFound.jsx
│   └── app/
│       ├── dashboard.jsx, leaderboard.jsx, settings.jsx, system-design.jsx
│       ├── challenges/index.jsx, challenges/$id.jsx
│       ├── editor.$id.jsx
│       ├── interviews/index.jsx, interviews/live.jsx, interviews/$id.report.jsx
│       └── profile/$username.jsx
├── redux/                   (was src/store/)
│   ├── index.js             configureStore + store
│   ├── hooks.js             useAppDispatch / useAppSelector
│   └── slices/              7 feature slices (challenges, user, leaderboard, ...)
├── routes/
│   └── AppRoutes.jsx        createBrowserRouter config (all routes + loaders)
├── styles.css               Tailwind tokens + theme
├── main.jsx                 entry: Provider + RouterProvider + Toaster
└── App.jsx                  (not used — main.jsx wires everything directly)
```

## Routing

All routes are declared in `src/routes/AppRoutes.jsx` using `createBrowserRouter`. Dynamic params follow React Router's `:param` convention (e.g. `/app/challenges/:id`).

Pages that need preloaded data export both `default` (the component) and a named `loader` — React Router calls the loader before rendering and the component reads it with `useLoaderData()`.

```jsx
// src/pages/app/challenges/$id.jsx
export const loader = ({ params }) => {
  const c = challenges.find((x) => x.slug === params.id);
  if (!c) throw new Error("Not found");
  return c;
};
export default ChallengeDetail;
```

## State management

Redux Toolkit, no TanStack Query. The store is configured in `src/redux/index.js`:

```js
import { configureStore } from "@reduxjs/toolkit";
import challenges from "./slices/challengesSlice";
// ...
export const store = configureStore({ reducer: { challenges, user, ... } });
```

Use `useAppDispatch` / `useAppSelector` from `@/redux/hooks` in components. Add `createAsyncThunk` calls inside the appropriate slice when wiring real APIs.

## Scripts

```bash
bun install     # or: npm install / pnpm install
bun run dev     # start Vite on http://localhost:5173
bun run build   # production build to dist/
bun run preview # preview the production build
```

## Notes from the refactor

- Removed: `@tanstack/react-start`, `@tanstack/react-router`, `@tanstack/router-plugin`, `@tanstack/react-query`, `@lovable.dev/vite-tanstack-config`, `vite-tsconfig-paths`, all TypeScript tooling (`typescript`, `@types/*`, `tsconfig.json`).
- The `@/` alias is configured in both `vite.config.js` and `jsconfig.json` so editors resolve imports.
- All `.tsx → .jsx` / `.ts → .js` conversions strip TS types only; component code, classNames, and JSX are identical to the original.
- TanStack-specific APIs were rewritten:
  - `createFileRoute(...)({...})` → plain default export + optional `loader` export, wired up in `src/routes/AppRoutes.jsx`.
  - `<Link to="/x/$id" params={{ id }}>` → `<Link to={\`/x/${id}\`}>`.
  - `navigate({ to: "/x/$id", params: { id } })` → `navigate(\`/x/${id}\`)`.
  - `Route.useParams()` → `useParams()` from `react-router-dom`.
  - `Route.useLoaderData()` → `useLoaderData()` from `react-router-dom`.
  - `useRouterState({ select: s => s.location.pathname })` → `useLocation().pathname`.
- Per-route `head()` metadata was dropped (TanStack-specific). If you need per-page `<title>`, install `react-helmet-async` or set `document.title` in a `useEffect` per page.
