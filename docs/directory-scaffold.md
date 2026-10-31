# Directory Scaffold

FilmForge uses two scaffolds.

## 1. Skill Scaffold

The skill repo contains:

- `SKILL.md`
- `schema/`
- `templates/project/`
- `scripts/`
- `docs/`
- `examples/`

## 2. Generated Project Scaffold

Each drama project gets its own workspace:

```text
<project-root>/
├── project.yaml
├── bible/
├── canon/
├── episodes/
├── assets/indexes/
├── exports/
└── logs/
```

## Rules

- `bible/` is for project-wide creative truth.
- `canon/` is for reusable entities.
- `episodes/` is for production decomposition.
- `assets/indexes/` is for registries, not raw outputs.
- `exports/` is for packaged deliverables.
- `logs/` is for generation and audit events.

## Entity Convention

Each canonical entity should follow this shape:

```text
canon/<kind>/<entity-id>/
├── profile.md
├── state.yaml
├── refs/
│   ├── approved/
│   └── explorations/
├── renders/
└── manifest.yaml
```
