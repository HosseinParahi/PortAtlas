# Development Setup

Status: **Proposed Phase 3 contract, not a working application setup guide**

The only executable repository workflow at Gate 2 is documentation validation:

```bash
python3 scripts/validate_docs.py
```

No production dependencies are installed by this checkpoint. Exact runtime versions, package-manager commands, workspace layout, and lockfiles must be selected and verified at Gate 3 before this guide can claim a functional development environment.

## Proposed principles

- Pin a supported Python line and use `uv` with a committed lockfile.
- Pin a supported Node line compatible with the selected Vite release and use Corepack-managed pnpm with a committed lockfile.
- Keep Python service and React UI scripts reproducible from repository-local configuration.
- Make SQLite the zero-service default; place all state in an isolated temporary directory during tests.
- Keep Docker, PostgreSQL, Ollama, and Rust outside the default bootstrap path.
- Provide fakes and fixtures so core development and tests work offline.
- Do not modify global shell profiles, system Python, Docker settings, or user-wide package configuration.

## Proposed setup verification

The future bootstrap must report tool versions, create isolated environments, install from lockfiles, run migrations against temporary state, execute core tests without optional services, build the browser assets, start the loopback service, and confirm authenticated health. Every command will be added only after it exists and has been tested from a clean checkout.

## Optional profiles

| Profile | Purpose | Default state |
|---|---|---|
| Docker | Live Engine collector verification | Disabled unless explicitly selected |
| PostgreSQL | Repository compatibility tests | Disabled |
| Ollama | Conditional AI evaluation | Disabled and never auto-installs models |
| Packaging | Signed/native-service experiments | Separate from everyday development |

## Environment safety

Development configuration uses ignored local files derived from redacted examples. Tests generate synthetic credentials and paths. Secrets, real project roots, database dumps, model prompts, and diagnostic bundles are never committed.

## Promotion to an operational guide

Gate 3 replaces each proposal with verified commands, expected output, supported version ranges, clean-up steps, and common failure modes. Until then, research versions in [research-sources.md](../project/research-sources.md) are observations rather than prerequisites.
