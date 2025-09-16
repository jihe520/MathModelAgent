# Repository Guidelines

## Project Structure & Module Organization
The FastAPI backend lives in `backend/app`, with `core/` hosting agent workflows, `routers/` exposing HTTP and WebSocket endpoints, and `services/` or `utils/` handling shared integrations. Configuration presets sit in `backend/app/config`, and generated notebooks or papers land under `backend/project/work_dir`. The Vue 3 front end is in `frontend/src`, where `pages/` defines screens and `components/` houses reusable UI primitives; supporting assets and docs are in `docs/` and `demo/`.

## Build, Test, and Development Commands
Install backend dependencies via `cd backend && uv sync`, then launch the API for local work with `ENV=DEV uv run uvicorn app.main:app --reload --port 8000`. The client relies on pnpm: `cd frontend && pnpm install`, `pnpm dev` for hot-reload, and `pnpm build` for production bundles. To bootstrap both services together, supply the env files and run `docker-compose up -d` from the repo root.

## Coding Style & Naming Conventions
Python modules follow Ruff formatting (`uv run ruff format .`), 4-space indents, 88-character lines, and double-quoted strings; keep modules lowercase with underscores and classes in `PascalCase`. TypeScript, Vue SFCs, and CSS use Biome (`pnpm exec biome lint src`) with tab indentation and double quotes. Name agents and services descriptively (`ModelerAgent`, `redis_manager.py`) and keep Vue components as `PascalCase.vue` co-located with their barrel exports.

## Commit & Pull Request Guidelines
Commit history mixes concise English statements with prefixes like `Fix:` or `Add`; keep messages imperative (e.g., `Fix: handle redis reconnects`) and reference issues in parentheses when applicable. Before opening a PR, ensure linting and unit tests are green, summarize backend/frontend impacts, and attach screenshots or CLI snippets for user-facing changes. Cross-link related tickets or discussion threads so reviewers can trace requirements quickly.

## Configuration & Security Tips
Copy `.env.dev.example` to `.env.dev` for the backend and `.env.example` to `.env.development` for the front end, keeping API secrets out of version control. Redis must be available locally, and generated artifacts in `backend/project/work_dir` should be scrubbed before sharing bundles or logs.
