# Continuity Rules

## The Rule

An approved image is not the full truth of a character or scene.

Use this stack:

1. `profile.md`
   Durable identity, role, anchors, constraints
2. `state.yaml`
   What is true right now
3. `refs/approved/`
   Visual anchors approved for reuse

## What Must Be Tracked

### Characters

- face / body anchors
- hair / costume anchors
- speaking style
- relationship stance
- current damage / dirt / emotional state

### Locations

- layout
- lighting
- time of day
- weather
- critical props present or missing

### Props

- baseline look
- owner
- current condition
- current story meaning

## Packet Rule

Every shot should carry:

- inherited canon refs
- inherited scene state
- allowed changes
- forbidden drift

If a shot cannot explain what it must keep, it is not ready to render.

## Shot-To-Shot Continuity

For chained video shots, independent clip stitching is never the ideal default.

Why:
- separate generations drift in look and timing
- models treat input frames as references, not true continuation state
- post stitching can only hide seams, not remove the underlying discontinuity

Default rule:
- prefer model-native continuation over post stitching
- record the handoff strategy in the packet
- use prompt convergence on both sides of the seam
- if post stitching is expected, record whether it is hard cut, overlap-frame, or crossfade fallback

Secondary rule:
- if native continuation is unavailable, simple `last_frame_url` chaining or hard cut fallback is often safer than assuming crossfade will save the seam

Minimum transition data:
- predecessor shot id
- whether the path is native continuation or stitched fallback
- handoff frame policy
- frame offset when using last-N extraction
- overlap frames or overlap seconds
- transition goal
- seam-specific forbidden drift
