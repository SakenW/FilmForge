#!/usr/bin/env python3
"""Create a new FilmForge project scaffold."""

from __future__ import annotations

import argparse
import datetime as dt
import shutil
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
TEMPLATE_ROOT = ROOT / "templates" / "project"
PROJECT_DIRS = [
    "canon/characters",
    "canon/locations",
    "canon/props",
    "canon/motifs",
    "episodes",
    "assets/cache",
    "exports/lookbooks",
    "exports/storyboards",
    "exports/animatics",
    "exports/pitch-packs",
    "logs",
]


def slugify(text: str) -> str:
    chars = []
    last_dash = False
    for ch in text.lower().strip():
        if ch.isalnum():
            chars.append(ch)
            last_dash = False
        else:
            if not last_dash:
                chars.append("-")
                last_dash = True
    slug = "".join(chars).strip("-")
    return slug or "filmforge-project"


def replace_tokens(text: str, tokens: dict[str, str]) -> str:
    for key, value in tokens.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def copy_template_tree(src: Path, dst: Path, tokens: dict[str, str]) -> None:
    for path in src.rglob("*"):
        relative = path.relative_to(src)
        target = dst / relative
        if path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
            continue
        text = path.read_text(encoding="utf-8")
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(replace_tokens(text, tokens), encoding="utf-8")


def write_text(path: Path, body: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body.rstrip() + "\n", encoding="utf-8")


def create_core_directories(project_root: Path) -> None:
    for relative in PROJECT_DIRS:
        (project_root / relative).mkdir(parents=True, exist_ok=True)


def create_starter_entities(project_root: Path) -> None:
    for relative in [
        "canon/characters/char-001-lead/refs/approved",
        "canon/characters/char-001-lead/refs/explorations",
        "canon/characters/char-001-lead/renders",
        "canon/locations/loc-001-main-set/refs/approved",
        "canon/locations/loc-001-main-set/refs/explorations",
        "canon/locations/loc-001-main-set/renders",
        "canon/props/prop-001-hero-item/refs/approved",
        "canon/props/prop-001-hero-item/refs/explorations",
        "canon/props/prop-001-hero-item/renders",
    ]:
        (project_root / relative).mkdir(parents=True, exist_ok=True)

    write_text(
        project_root / "canon" / "characters" / "char-001-lead" / "profile.md",
        """# Character: Lead

- Role: protagonist
- Goal: replace me
- Anchors:
  - replace me
- Forbidden drift:
  - replace me
""",
    )
    write_text(
        project_root / "canon" / "characters" / "char-001-lead" / "state.yaml",
        """status: "draft"
costume: "default"
emotion: "neutral"
notes: "Replace with current character state."
""",
    )
    write_text(
        project_root / "canon" / "characters" / "char-001-lead" / "manifest.yaml",
        """id: "char-001-lead"
approved_refs: []
render_history: []
""",
    )

    write_text(
        project_root / "canon" / "locations" / "loc-001-main-set" / "profile.md",
        """# Location: Main Set

- Purpose:
- Layout anchors:
- Lighting anchors:
- Forbidden drift:
""",
    )
    write_text(
        project_root / "canon" / "locations" / "loc-001-main-set" / "state.yaml",
        """time_of_day: "night"
weather: "dry"
damage: "none"
""",
    )
    write_text(
        project_root / "canon" / "locations" / "loc-001-main-set" / "manifest.yaml",
        """id: "loc-001-main-set"
approved_refs: []
render_history: []
""",
    )

    write_text(
        project_root / "canon" / "props" / "prop-001-hero-item" / "profile.md",
        """# Prop: Hero Item

- Owner:
- Look anchors:
- Story meaning:
""",
    )
    write_text(
        project_root / "canon" / "props" / "prop-001-hero-item" / "state.yaml",
        """condition: "clean"
holder: "char-001-lead"
visibility: "hidden"
""",
    )
    write_text(
        project_root / "canon" / "props" / "prop-001-hero-item" / "manifest.yaml",
        """id: "prop-001-hero-item"
approved_refs: []
render_history: []
""",
    )


def create_starter_episode(project_root: Path) -> None:
    ep_root = project_root / "episodes" / "ep-001"
    sc_root = ep_root / "scenes" / "sc-001"
    sh_root = sc_root / "shots" / "sh-001"

    write_text(
        ep_root / "outline.md",
        """# Episode 001 Outline

- Theme:
- Starting state:
- Ending state:
- Key turns:
""",
    )
    write_text(
        ep_root / "beats.md",
        """# Episode 001 Beats

1. Hook
2. Escalation
3. Turn
4. Exit
""",
    )
    write_text(
        ep_root / "continuity.yaml",
        """must_keep:
  - "project tone"
allowed_changes:
  - "scene state"
forbidden_drifts:
  - "break canonical identity"
""",
    )
    write_text(
        sc_root / "scene.md",
        """# Scene 001

- Purpose:
- Characters:
- Location:
- Props:
- Conflict:
""",
    )
    write_text(
        sc_root / "continuity.yaml",
        """must_keep:
  - "char-001-lead identity"
  - "loc-001-main-set layout"
allowed_changes:
  - "emotional intensity"
forbidden_drifts:
  - "teleport prop state"
""",
    )
    write_text(
        sh_root / "shot.md",
        """# Shot 001

- Framing:
- Camera move:
- Subject:
- Action:
- Dialogue:
- Emotion:
""",
    )
    write_text(
        sh_root / "continuity-packet.json",
        """{
  "packet_id": "cont-ep001-sc001-sh001",
  "shot_id": "sh-001",
  "must_keep": [
    "char-001-lead face anchors",
    "loc-001-main-set lighting anchors"
  ],
  "allowed_changes": [
    "camera angle"
  ],
  "forbidden_drifts": [
    "costume swap without state update"
  ],
  "story_state": {
    "beat": "opening"
  },
  "look_state": {
    "weather": "dry"
  },
  "shot_handoff": {
    "from_shot_id": "",
    "to_shot_id": "sh-001",
    "frame_strategy": "none",
    "frame_offset": 0,
    "overlap_frames": 0,
    "transition_goal": "establish the visual state cleanly",
    "avoid": [
      "extreme pose seam"
    ]
  }
}""",
    )
    write_text(
        sh_root / "render-packet.json",
        """{
  "packet_id": "render-ep001-sc001-sh001",
  "shot_id": "sh-001",
  "kind": "image",
  "purpose": "storyboard",
  "prompt_cn": "替换成给 ark-media 的中文提示词",
  "references": [],
  "constraints": {
    "must_keep": [
      "char-001-lead face anchors"
    ],
    "can_change": [
      "framing"
    ]
  },
  "transition": {
    "source_shot_id": "",
    "mode": "cut",
    "extract_frame_policy": "none",
    "extract_frame_offset": 0,
    "overlap_frames": 0,
    "overlap_seconds": 0.0,
    "xfade_duration_s": 0.0,
    "xfade_transition": "fade",
    "bridge_prompt_cn": "",
    "emit_last_frame": false
  },
  "render_profile": "preview"
}""",
    )
    write_text(
        sh_root / "manifest.yaml",
        """id: "sh-001"
outputs: []
approved_output: ""
notes: ""
""",
    )


def init_project(title: str, output_root: Path, force: bool) -> Path:
    slug = slugify(title)
    project_root = output_root / slug
    if project_root.exists():
        if not force:
            raise FileExistsError(f"{project_root} already exists; use --force to replace it")
        shutil.rmtree(project_root)
    project_root.mkdir(parents=True, exist_ok=True)

    generated_at = dt.datetime.now(dt.UTC).replace(microsecond=0).isoformat()
    tokens = {
        "PROJECT_ID": slug,
        "PROJECT_TITLE": title,
        "PROJECT_SLUG": slug,
        "GENERATED_AT": generated_at,
    }
    copy_template_tree(TEMPLATE_ROOT, project_root, tokens)
    create_core_directories(project_root)
    create_starter_entities(project_root)
    create_starter_episode(project_root)
    return project_root


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a FilmForge project scaffold")
    parser.add_argument("--title", required=True, help="Project title")
    parser.add_argument(
        "--output",
        default=".",
        help="Directory that will contain the generated project folder",
    )
    parser.add_argument("--force", action="store_true", help="Replace existing project directory")
    args = parser.parse_args()

    output_root = Path(args.output).expanduser().resolve()
    project_root = init_project(args.title, output_root, args.force)
    print(project_root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
