---
description: Make one or more finished episodes (long video + Short + YouTube files) from approved scripts
argument-hint: <episode numbers, e.g. 5 or 5 6 7>
---

Make these India and the World episodes: **$ARGUMENTS**

Follow CLAUDE.md throughout. For each episode number, in order:

1. **Check it's approved.** Find the episode in `scripts/episode_plan.md`. Continue only if its Status is `scripted` (approved), or if it is Episode 1 (the format sample). If it's `to script` or `sample script (approve)`, skip it and tell me it needs a script or my approval first. Never render an unapproved script.
2. **Check the engine exists.** If `engine/riso.py`, `engine/brief.py` and `engine/web.py` don't exist yet, stop and tell me to run `/build-look` first.
3. **Check the news hasn't moved.** Look at the script's "As of" month and its "Fact check before rendering" notes. Do a quick search on the topic. If something material has happened since the script was written, don't render: tell me what changed and suggest running `/refresh` on it.
4. **Build the episode code.** Find the episode's script in `scripts/` (`sample_ep01.md` for Episode 1, otherwise `unitN_scripts.md`). Create `episodes/epNN/ep.py` for the long video and `episodes/epNN/short.py` for the Short, using the Narration column word for word. Add the episode's passport stamp and web thread to `engine/web.py` if they aren't there, and make sure the web and passport match every earlier episode.
5. **Narration:** run the `tts` step for both the long video and the Short.
6. **Check stills.** Render 4 stills from the long video at its busiest moments (the timeline, Where they stand, the exam desk, the relations web) and 2 from the Short. Put them in one contact sheet and look at it once. Fix overlaps (especially with the caption box), any date or number that doesn't match the narration, unequal position cards, any India map not drawn from the official Survey of India file, and scenes that sit still for more than 3 seconds. Also render the 15-second motion preview described in CLAUDE.md and check that things move smoothly.
7. **Render** the long video with two background workers and wait with a single `until` loop. Then build the audio, assemble, and check it's exactly 300 s. Then render and assemble the Short (45–55 s, 1080×1920).
8. **YouTube files:** write `output/youtube/WaNN.txt` (title, description with an "As of <month year>" line and the Sources list, chapters, and the Short's title and description with #Shorts) and a designed `WaNN_thumb.png`. Open the thumbnail and check it isn't blank.
9. **QA:** run `python3 tools/qa.py` for this episode, and fix any problems it reports.
10. **Deliver:** copy the files to `output/WaNN_<Short_Title>.mp4`, `output/WaNN.srt` and `output/shorts/WaNN_short.mp4`. Set the episode's Status to `done` in `scripts/episode_plan.md`. Run `git status`, make sure no scratch files (`vo/`, `parts/`, `.wav`, stills, logs, `*.part.mp4`) are staged, then commit and push.

When all are finished, reply with a short table (episode, length, Short length, status, as-of month) and the contact sheet for each episode. Don't narrate progress in between.
