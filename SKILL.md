---
name: filmforge
description: AI 短剧制作技能（OpenClaw）。创建或继续需要可复用项目脚手架、故事圣经、角色/场景/道具设定集、分集/场景/分镜规划、渲染包与一致性控制的剧本视频项目时使用。FilmForge 负责规划与一致性；ark-media 只负责图像与视频生成。
---

# FilmForge

FilmForge is the director layer for AI drama production.

It does not compete with `ark-media`. It feeds `ark-media`.

## Use This Skill For

- Starting a new AI drama or short-form scripted video project
- Turning a concept into a reusable project scaffold
- Building and maintaining the project bible
- Defining canonical characters, locations, props, and motifs
- Planning episodes, scenes, and shots
- Preparing render packets for downstream media generation
- Checking continuity drift across story, look, and shot logic

## Hard Boundaries

- FilmForge owns story structure, canon, continuity, and shot planning.
- `ark-media` owns image/video generation, model selection, task polling, cost reporting, and downloaded outputs.
- FilmForge should never duplicate `ark-media` model matrices or download logic.
- Generated media may live outside the workspace, for example in `~/Downloads`; FilmForge records those paths in manifests and registries.

## Source of Truth

Consistency is never image-only.

Every durable entity should be represented by three layers:

1. `spec`
   Human-editable truth in Markdown/YAML
2. `approved refs`
   Visual anchors approved for reuse
3. `state`
   What is true right now in the current episode, scene, or shot

If a project has images but no state, continuity will drift.

## Core Workflow

### 1. Initialize or open a project

For a new project, generate the scaffold:

```bash
python scripts/forge_init.py --title "Neon Rain Courtship" --output /path/to/projects
```

This creates:
- `project.yaml`
- `bible/`
- `canon/`
- `episodes/`
- `assets/indexes/`
- `exports/`
- `logs/`

### 2. Establish canon before rendering

Before any shot rendering:
- fill in the bible
- define canonical characters, locations, and props
- approve visual refs
- write current state snapshots

Read [docs/continuity-rules.md](docs/continuity-rules.md) when deciding what must stay stable.

### 3. Plan production top-down

The order is:

```text
concept -> project -> bible -> episode -> scene -> shot -> continuity packet -> render packet
```

Do not jump from concept straight to final video generation unless the user explicitly wants a throwaway prototype.

### 4. Emit packets, then render

Each shot should produce:
- a continuity packet
- a render packet

The continuity packet says what must remain true.
The render packet says what to ask the media backend to generate.

Use [schema/continuity-packet.schema.json](schema/continuity-packet.schema.json) and
[schema/render-packet.schema.json](schema/render-packet.schema.json) as the transport contract.

### 5. Hand off to ark-media

Use the adapter scaffold to turn a normalized packet into an `ark-media` command preview:

```bash
python scripts/adapters/ark_media_adapter.py --packet-json /path/to/render-packet.json
```

The adapter prints a command. It does not execute it.

### 6. Write results back

After media generation:
- record output paths in the shot manifest
- update asset registries
- note which refs are approved vs exploratory
- update entity state if the shot changes story truth

## References

- Read [docs/architecture.md](docs/architecture.md) before changing directory structure or boundaries.
- Read [docs/directory-scaffold.md](docs/directory-scaffold.md) when extending the project tree.
- Read [docs/continuity-rules.md](docs/continuity-rules.md) before changing canon or packet structure.
- Read [docs/shot-transition-rules.md](docs/shot-transition-rules.md) when chaining multiple video shots.

## Scripts

- `scripts/forge_init.py`
  Create a new FilmForge project scaffold
- `scripts/adapters/ark_media_adapter.py`
  Convert a normalized render packet into an `ark-media` command preview

## Implementation Guidance

- Prefer explicit IDs like `char-001-lead`, `loc-001-alley`, `sh-001`.
- Keep long-form creative thinking in Markdown.
- Keep machine contracts in JSON schemas.
- Keep packets narrow and deterministic.
- Treat episode/scene/shot folders as production views over canon, not replacements for canon.
- If a user asks for a new feature that smells like render backend work, push it to `ark-media` unless it changes planning or continuity.
- Treat seam strategy as explicit data, not hidden prompt lore.
- Prefer model-native continuation over post-stitched continuity whenever the backend can do it.
