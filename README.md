# India and the World, Simply Briefed

Animated 5-minute briefings, with English and Hindi audio on every video, on current international relations for UPSC: 40 episodes in 6 units, each with a vertical YouTube Short, plus a monthly "World This Month" episode from December 2026. Printed in a two-ink risograph style with lively motion (camera moves, map fly-ins, flowing rivers, kinetic type). Maps of India follow the official Survey of India depiction, and facts come from Indian and official sources. Every episode answers what happened, why it matters for India, and how UPSC will ask it; stamps a memory tip into a briefing passport; and adds a thread to a growing web of India's relations.

Because the news moves, every script is researched fresh, shows an "As of" date, lists its sources, and has a refresh-by date.

- `scripts/episode_plan.md`: all 40 episodes, their web threads, refresh-by dates and status
- `scripts/sample_ep01.md`: the sample script (long video and Short) that sets the format
- `CLAUDE.md`: instructions the Claude Code cloud session reads automatically
- `output/`: finished videos and captions; `output/shorts/`: Shorts; `output/youtube/`: descriptions and thumbnails

## Commands (the easy way)
Type these in a Claude Code session on this repository. Each one runs a whole step.

| Command | What it does |
| --- | --- |
| `/build-look` | One-time setup: builds the risograph look, the passport and relations web, sounds and the Shorts pipeline, then shows 3 stills and stops |
| `/make-episode 1` | Makes the test episode (Indus Waters Treaty) with its Short and YouTube files, checks it, and pushes it |
| `/write-scripts 1` | Researches and writes all of Unit 1's scripts, pushes them, and stops for your review |
| `/approve 2 3 4` | Marks those episodes' scripts as approved (nothing is rendered without this) |
| `/make-episode 2 3 4` | Makes those approved episodes, one after another |
| `/refresh 1 9` | Re-checks episodes against the latest news; proposes changed lines for approval, then re-renders |
| `/status` | Shows progress across all 40 episodes and the next step |
| `/build-all` | **Everything at once:** the look, the test episode, all scripts, an independent fact-check, then all 40 videos and Shorts, pushing each as it's finished. Run it again to resume. |

A typical cycle: `/write-scripts 2`, review on GitHub, `/approve 9 10 11 12 13`, `/make-episode 9 10 11 12 13`. Every few months: `/refresh` on the episodes past their refresh-by date.

## Messages to paste into the cloud session (if commands don't show up)
1. **Build the new look:**
   > Read CLAUDE.md and run setup.sh. Do the "First task" section: engine/riso.py, engine/brief.py and engine/web.py, the palette, fonts and sounds, configurable frame size for Shorts (reuse reference/art_shorts_pipeline/), and adapt tools/ for this series. Show me 3 stills (a headline sheet, the relations web with the passport, and a vertical Short frame) and stop.
2. **Test episode:**
   > Render Episode 1 and its Short from scripts/sample_ep01.md as the test. Check the news hasn't moved first. Push both and show me 4 stills from the long video and 2 from the Short.
3. **Scripts for a unit:**
   > Research and write the Unit 1 scripts (Episodes 2–8, each with its Short) following CLAUDE.md, with sources and as-of dates. Push them and stop. Don't render until I approve.
4. **After you've reviewed them:**
   > Unit 1 scripts are approved. Render Episodes 2–8, with their Shorts.
