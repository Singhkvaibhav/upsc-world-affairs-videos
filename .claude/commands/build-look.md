---
description: One-time setup - build the risograph look, the passport and relations web, sounds and Shorts pipeline, then show 3 stills
---

Read CLAUDE.md and run `bash setup.sh`.

Then do the whole **"First task: build the new look and the Shorts pipeline"** section of CLAUDE.md:
- `engine/riso.py`: `riso`, `halftone`, `bg_sheet` (with the "AS OF" cable line), `bg_board`, and the new palette and fonts
- `engine/brief.py`: the scene templates (HEADLINE, TIMELINE, EXPLAIN, BOARD, STANDS, STAKES, STAMP, EXAM, WATCH)
- `engine/web.py`: the passport and the relations web, both drawn from a state of everything added so far, plus the WEB template
- the new sounds in `engine/audiomix.py` (marimba bed, teleprinter tick, stamp, pluck)
- configurable frame size, so the same scenes can render as 1080×1920 Shorts (reuse the approach in `reference/art_shorts_pipeline/`)
- the official India map: get the Survey of India political map (CLAUDE.md rule 7), store it as `engine/data/india_official.svg`, and build the `india_map` helper with camera fly-ins (if you can't download it, stop and ask me for the file)
- the Motion rules in CLAUDE.md: camera moves, parallax, spring entrances, draw-on lines, flowing rivers, kinetic type
- adapt `tools/` for this series (names `WaNN_…`, range 1–40, Shorts included in QA, blank-thumbnail check)

Don't change helpers that other code depends on, except to make the frame size configurable.

Finally, render 4 stills (a headline sheet with the cable line, the official India map mid-fly-in with flowing rivers, the relations web with five threads and the passport beside it, and a vertical Short frame) and a 15-second motion preview. Show me the contact sheet and the preview, commit and push the engine code, and **stop**. Don't make any episode yet.
