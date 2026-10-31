# FilmForge Architecture

FilmForge is a planning and continuity system layered above media generation.

## Boundary

```text
USER INTENT
    |
    v
FILMFORGE
    |
    +--> project scaffold
    +--> bible + canon
    +--> episode / scene / shot plans
    +--> continuity packets
    +--> render packets
    |
    v
ARK MEDIA ADAPTER
    |
    v
ark-media
    |
    v
image / video outputs
```

## Principles

1. Canon beats prompt history.
2. Packets beat ad hoc command strings.
3. Approved refs beat random generations.
4. State snapshots beat vague memory.
5. FilmForge plans. `ark-media` renders.

## Persistence Model

```text
project.yaml
  |
  +--> bible/                 long-form human truth
  +--> canon/                 reusable entities
  +--> episodes/              production decomposition
  +--> assets/indexes/        machine-visible registries
  +--> exports/               bundled outputs
  +--> logs/                  audit trail
```

## Continuity Model

Continuity has four layers:

- story continuity
- visual continuity
- environment continuity
- shot language continuity

Every shot should inherit from canon and current scene state before it asks for media generation.

## Transition Planning

Shot-to-shot continuity is part of planning.

FilmForge should store:
- which prior shot a new shot continues from
- whether the plan expects native continuation or stitched fallback
- whether it inherits from first frame, last frame, or last-N frame
- whether overlap frames are expected
- whether downstream stitching expects crossfade
- whether the backend should return a last frame for the next handoff

That state belongs in packets and manifests, not only in prose.
