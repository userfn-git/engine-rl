# Running this project

This import uses React 19, TypeScript, Vite 8, and Tailwind CSS 4.
Keep the existing stack and directory structure.

## Development

- Use the **Start application** workflow (the Run button), which runs `npm run dev`.
- Vite listens on `0.0.0.0:5000` and accepts Replit's proxied preview hosts.
- Dependencies are managed with npm and `package-lock.json`. For a fresh checkout, run `npm ci`.
- No secrets, database, or external services are required for the current web app.

## Checks

- `npm run build` checks TypeScript and creates a production build in `dist/`.
- `npm run lint` runs Oxlint.

## Current scope

The web entry point is `src/main.tsx`, which renders `src/App.tsx`.
The dashboard buttons currently append in-memory log messages only; they do not
launch Rocket League, G-HUB, or a macro engine. The displayed F1–F4 hotkeys
are not implemented by the web app.

`old_src/` contains archived desktop-oriented Python, PowerShell, and Lua code.
It is not part of the Vite application and is not launched by the workflow.
Running the web dashboard on Replit does not provide access to a visitor's
local Windows applications.
