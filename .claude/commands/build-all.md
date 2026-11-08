---
description: Build the whole series in one go - look, test episode, all scripts, fact-check, and all 40 videos with Shorts. Resumable.
---

Build the whole India and the World series, start to finish, without stopping for my approval between steps. **Running this command is my approval** for every script it writes, once those scripts pass the fact-check in step 4. Follow every other rule in CLAUDE.md.

**This command is resumable.** Before starting, read `scripts/episode_plan.md`, `engine/` and `output/`, and skip anything already done. If the session stops part-way, running `/build-all` again picks up where it left off.

**Where to push:** commit and push to `main` after every finished step, so finished videos appear on GitHub straight away. If you can't push to `main`, use a single branch, `claude/build-all`, with one open pull request, and tell me its name in the first message.

### 1. The look (skip if `engine/riso.py`, `engine/brief.py` and `engine/web.py` exist)
Do the whole "First task" section of CLAUDE.md: run `setup.sh`, build the new look, sounds and Shorts pipeline, and adapt `tools/`. Render the 3 check stills and look at them yourself. Fix anything unreadable, overlapping or off-style. Commit and push.

### 2. Test episode (skip if Episode 1 is `done`)
Make Episode 1 and its Short from `scripts/sample_ep01.md`, exactly as `/make-episode` describes. Look at 4 stills from it and fix any problems in the engine before going on, because every later episode inherits them. Commit and push.

### 3. All scripts (skip units whose script file already covers every episode)
For Units 1 to 6, write `scripts/unitN_scripts.md` exactly as `/write-scripts` describes: the same format as the sample, every rule in CLAUDE.md, fresh research with a Sources list, As of and Refresh by under every episode. Commit and push each unit's file as soon as it's written.

### 4. Independent fact-check (before anything else is rendered)
Start a **separate agent** that hasn't seen the scripts being written. Give it CLAUDE.md and all the unit script files, and ask it to check every episode for:
- every factual claim, date, name and office-holder, checked against the episode's own Sources (open them) and against a fresh search for anything newer
- disputed positions not attributed, unequal treatment of the sides, loaded words, or any verdict on who is right
- predictions in the Watchlist
- ongoing situations that don't say "as of <month year>" in the narration
- Prelims statements with a debatable answer
- any source that isn't Indian or official (foreign news outlets are not allowed), and any other government's position not taken from its own official statement
- any India map that isn't the official Survey of India depiction, and any flag, emblem, logo or leader's likeness in the Visual column
- narration outside 480–600 words, or a missing memory tip, Where they stand, India's stake or exam desk

Fix everything it finds in the scripts. Then set every scripted episode's Status to `scripted` in `scripts/episode_plan.md`, and add a line at the top of that file: "Scripts approved via /build-all after an independent fact-check, on <date>." Commit and push. Put a short summary of what the fact-check found and fixed in `scripts/factcheck_report.md`.

### 5. All episodes (skip any that are `done`)
Make every episode from 1 to 40 in order, each exactly as `/make-episode` describes: long video, Short, captions, YouTube text and thumbnail, 4 checked stills, QA, then copy to `output/`, mark `done`, and commit and push **that episode on its own** before starting the next. Don't save up episodes for one big commit.

If one episode fails twice (a render error, or QA problems you can't fix), mark it `needs attention` in `episode_plan.md` with one line on why, and move on to the next.

### 6. Finish
Run `python3 tools/qa.py` across the whole series and fix what you can. Then reply once, with:
- a table by unit: episodes done, needing attention, and total running time
- the top 5 issues from the fact-check report
- anything I should review before publishing

**Don't narrate progress between steps.** The only exception: if something blocks the whole build (setup fails, or you can't push at all), stop and tell me straight away.
