#!/usr/bin/env python3
"""Translate a normalized FilmForge render packet into an ark-media command preview."""

from __future__ import annotations

import argparse
import json
import shlex
import sys
from pathlib import Path


def load_packet(args: argparse.Namespace) -> dict:
    if args.packet_json:
        return json.loads(Path(args.packet_json).read_text(encoding="utf-8"))
    if args.packet:
        return json.loads(args.packet)
    return json.load(sys.stdin)


def quote(value: str) -> str:
    return shlex.quote(value)


def build_command(packet: dict) -> list[str]:
    kind = packet["kind"]
    prompt = packet["prompt_cn"]
    references = packet.get("references", [])
    render_profile = packet.get("render_profile", "preview")
    transition = packet.get("transition", {})
    transition_mode = transition.get("mode", "cut")

    if kind == "image":
        cmd = [
            "python",
            "scripts/ark_media.py",
            "generate-image",
            prompt,
            "--model",
            "seedream-5.0",
        ]
        if render_profile == "lookdev":
            cmd.extend(["--size", "2K"])
        else:
            cmd.extend(["--size", "1K"])
    elif kind == "video":
        cmd = [
            "python",
            "scripts/ark_media.py",
            "generate-video",
            prompt,
            "--model",
            "seedance-1.5",
            "--resolution",
            "480p" if render_profile == "preview" else "720p",
            "--ratio",
            "16:9",
            "--duration",
            "5",
        ]
    else:
        raise ValueError(f"Unsupported packet kind: {kind}")

    if kind == "video" and transition_mode == "seedance-track-fill":
        raise ValueError(
            "seedance-track-fill needs reference_video support; current ark_media adapter cannot preview that flow yet"
        )

    image_refs = [ref for ref in references if ref.get("type") == "image"]
    if kind == "image" and image_refs:
        if len(image_refs) == 1:
            cmd.extend(["--image", image_refs[0]["path"]])
        else:
            cmd.append("--images")
            cmd.extend(ref["path"] for ref in image_refs)
    if kind == "video" and image_refs:
        first_frame = next(
            (ref for ref in image_refs if ref.get("role") in {"first_frame", "reference_image"}),
            None,
        )
        last_frame = next(
            (ref for ref in image_refs if ref.get("role") == "last_frame"),
            None,
        )
        if first_frame:
            cmd.extend(["--image", first_frame["path"]])
        if last_frame:
            cmd.extend(["--last-frame", last_frame["path"]])
    if kind == "video" and transition.get("emit_last_frame"):
        cmd.append("--return-last-frame")

    return cmd


def main() -> int:
    parser = argparse.ArgumentParser(description="Preview an ark-media command for a render packet")
    parser.add_argument("--packet-json", help="Path to a JSON render packet")
    parser.add_argument("--packet", help="Inline JSON render packet")
    args = parser.parse_args()

    packet = load_packet(args)
    command = build_command(packet)
    print(" ".join(quote(part) for part in command))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
