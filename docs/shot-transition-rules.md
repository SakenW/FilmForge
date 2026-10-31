# Shot Transition Rules

This document turns video seam know-how into FilmForge planning rules.

## Core Point

A seam is not only an editing problem.

It is a planning problem with three layers:
- motion continuity
- look continuity
- transition tooling

More importantly, the current practical limit is this:

**Independently generated clips do not become truly seamless just because we stitch them more cleverly.**

Model-native continuation is the gold standard. Post stitching is fallback.

## Recommended Modes

### 1. model-native-continuation

Default choice for chained shots.

Use backend-native continuation or extension when available.

Examples:
- Seedance 2.0 video extension / native bridging
- workflows that return `last_frame_url` and feed it into the next generation as part of one planned chain

Why:
- only model-native continuation has a real chance at feeling continuous
- independent clip generation always re-renders look, timing, and micro-motion

### 2. seedance-track-fill

Use when the backend can bridge multiple clips natively with reference videos.

This is stronger than post stitching. FilmForge should model this intent even if the current adapter cannot fully express it yet.

### 3. overlap-frames

Fallback, not default.

Use a frame from slightly before the previous shot ends, not the literal last frame.

Why:
- avoids extreme-pose starts
- can reduce visible jumps a bit

But:
- this does not make two independently generated clips truly continuous
- crossfade on mismatched content can create visible ghosting

If used, suggested planning defaults are:
- `extract_frame_policy = "last_n_frame"`
- `extract_frame_offset = 10`
- `overlap_frames = 10`
- `overlap_seconds = 0.4`

### 4. hard-cut

Valid fallback for independently generated clips.

Counterintuitive, but often better than crossfade when clip content is not pixel-aligned.

### 5. prompt-convergence

Use on both sides of a seam.

The ending prompt should describe the exit pose or motion state.
The next prompt should start from that same state.

### 6. crossfade

Last-resort post technique.

Use only when clips are already very close, or when the purpose is rough preview.

Do not assume crossfade improves quality. It can make seams worse by introducing ghosting.

## Packet Implications

Render packets should say:
- which shot they follow
- whether the chosen path is native continuation or stitched fallback
- what frame extraction strategy they expect
- whether first-frame and/or last-frame refs are present
- whether a last frame should be returned for chaining
- whether downstream post expects crossfade

Continuity packets should say:
- what the seam must preserve
- what seam drift is forbidden
- what motion direction or action phase must continue

## Failure Smells

- hard cut with no seam plan at all
- assuming overlap-frames guarantees seamless continuity
- prompt says "continue naturally" with no explicit seam state
- no record of how the next shot got its first frame
- no last-frame export despite intent to chain more shots
- crossfade used by default on independently generated clips
