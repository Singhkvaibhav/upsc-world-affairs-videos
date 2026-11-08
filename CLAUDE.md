# India and the World, Simply Briefed: video production

This repo makes 40 five-minute animated briefings on **current international relations** for UPSC aspirants, **plus a vertical YouTube Short for every episode**, and from December 2026 a monthly "World This Month" episode. It's for the same channel as the Polity, Geography, Modern History, Ancient India, Medieval India, Art and Culture and Environment series (each in its own repo).

**This series is different from all the others: its facts go out of date.** Every script is researched fresh, carries an "As of" date and sources, and has a refresh-by date. Many topics are disputed between governments, so neutrality rules are strict.

**Its own look: a risograph briefing.** Two inks overprinted on off-white paper with halftone dots, like a modern foreign-affairs magazine. Keep the channel's calm pace, narrator and caption style, but don't reuse any other series' look or signatures.

- Episode list, refresh-by dates and status: `scripts/episode_plan.md`
- Format sample (the approved style, long video and Short): `scripts/sample_ep01.md`
- Scripts: `scripts/unitN_scripts.md`; monthly episodes: `scripts/monthly_YYYY_MM.md`
- Episode code: `episodes/epNN/ep.py` (long video) and `episodes/epNN/short.py` (Short)
- Finished files: `output/` (long videos) and `output/shorts/` (Shorts)
- Commands: `.claude/commands/` (`/build-look`, `/make-episode`, `/write-scripts`, `/approve`, `/status`, `/build-all`, `/refresh`)

## Rules that matter most
1. **Never render a unit before the user approves its scripts.** Write the unit's script file, commit and push it, tell the user it's ready, and **stop and wait** for approval (the user runs `/approve`). The only exceptions are Episode 1, the format sample, which you render as the test episode when the user asks, and `/build-all`: running it counts as approval for every script that passes its independent fact-check.
2. **Approved narration is used word for word**, in both the long video and the Short. If you spot a factual problem in an approved script, flag it; don't silently change it.
3. **Research every script fresh, from Indian and official sources.** Use web search and open the pages you take facts from. Every episode in a script file ends with a **Sources** list (pages actually opened, with links), an **As of** month and a **Refresh by** month. Never state a figure, date, name or office-holder from memory. Use sources in this order:
   - **Government of India:** MEA statements, briefings and joint statements (mea.gov.in), PIB, PMO, ministries, Parliament answers (sansad.in), DD News, All India Radio (newsonair.gov.in), Indian missions abroad
   - **Indian research institutions:** MP-IDSA, ICWA, ORF, Gateway House, RIS
   - **Major Indian newspapers and magazines:** The Hindu, The Indian Express, Hindustan Times, The Tribune, The Times of India, Business Standard, Deccan Herald, The Week, Outlook
   - **Documents of international bodies** (UN, WTO, courts and tribunals), read from their own sites
   - **Another government's position** is taken from that government's own official statement (its foreign ministry or state broadcaster) and stated as their position.
   
   Don't use foreign news outlets (for example Al Jazeera, Dawn, Global Times, BBC, CNN or Reuters) as sources.
4. **Attribute, don't judge.** Where governments disagree (for example India–Pakistan, India–China, Israel–Palestine, Russia–Ukraine), state each side's position as theirs ("India says…", "Pakistan says…"), on equal-sized cards, in neutral words. India's official position is stated clearly as India's position. Never declare who is right. Court rulings, votes and treaty texts are reported plainly, together with each side's response.
5. **No predictions.** The Watchlist names scheduled events and open questions only.
6. **Say the date out loud** for ongoing situations ("as of November 2026"), so a video never seems newer than it is.
7. **Maps of India follow the Government of India's official depiction.** Whenever India's outline or boundaries appear, use the official **Survey of India political map** (the edition showing the Union Territories of Jammu and Kashmir and Ladakh as created on 31 October 2019), so the whole of Jammu and Kashmir, Ladakh and Arunachal Pradesh is shown as part of India. Trace it exactly from the official map, store it once as `engine/data/india_official.svg` (or GeoJSON), and credit "Map: Survey of India" on screen. Never take India's boundaries from Natural Earth, OpenStreetMap, Google or any other source, and never draw them differently. If you can't download the official map (the network may block it), **stop and ask the user to attach it**; MEA missions publish it, for example https://cgihcmc.gov.in/page/india-s-latest-official-map. Maps of regions away from India (Europe, West Asia, Africa, the Americas) are schematic: coasts, rivers, sea lanes and named pins, without country boundaries.
8. **No flags, national emblems, party symbols, organisation logos or real leaders' likenesses.** Countries and groupings are named tokens; people are generic figures with titles.
9. **No graphic imagery** of war, attacks or casualties. Conflicts are shown through timelines, diagrams and statements.
10. **Commit only code and finished output.** Run `git status` before every commit. Never commit `vo/`, `parts/`, `.wav`, stills, logs or `*.part.mp4`.
11. **Be economical.** The user is on a usage budget. Check 3–4 stills per episode, render with two background workers, wait with a single `until` loop, and don't narrate progress.

## The engine (already built, from the Polity series)
- `engine/core.py`: palette `C`, easing, `text`, `label`, `caption`, timeline helpers, and the paper drawing helpers. `SERIES` and `SERIES_TITLE` at the top are already set. `W, H, FPS` are fixed at 1920×1080; make them configurable for the Shorts.
- `engine/templates.py`: `scene(bg, *layers)`, `TL`, `GRID`, `LIST`, `TIPS`, `MAINS`, `HOOK`, `END`, `FIG`, and other layouts
- `engine/runner.py`: `Episode` (timeline, caption chunks, render loop); `engine/cli.py`: the per-episode command line
- `engine/audiomix.py`: the mix (voice, pad, sound effects, SRT); `engine/tts.py`: narration
- `engine/town.py` and `engine/units.py` are the Polity town. Don't use them.
- `tools/`: helpers from earlier series. Adapt them first: output names `WaNN_<Title>.mp4`, `WaNN.srt` and `shorts/WaNN_short.mp4`, episode range 1–40, series name and hashtags for world affairs, and add the Shorts to QA.
- **`reference/art_shorts_pipeline/`** is the finished, working Shorts pipeline from the Art and Culture series (a `VERTICAL` switch in `core.py`, `prep_ep.py`, `deliver.py`, `qa.py`, and an example `ep.py` and `short.py`). Reuse its approach rather than building the Shorts pipeline from scratch. Don't copy its block-print look.

An episode is one `ep.py` file with `EP`, `TITLE`, `NAME`, `BEATS=[(id, narration, scene)]`, `CAPTIONS` and optional `EXTRA`, run from inside `episodes/epNN/` with `python3 ../../engine/cli.py tts|tl|still|render|audio|check`. `reference/polity_example_ep59.py` shows a complete episode in this format.

## First task: build the new look and the Shorts pipeline
Put everything new in `engine/riso.py` (the print style and backgrounds), `engine/brief.py` (scene templates) and `engine/web.py` (the passport and the relations web). Don't change the helpers other series depend on, except to make the frame size configurable.

1. **`riso(ctx, path, ink)`**: a flat fill in one of two inks, composited with multiply so overlapping teal and coral make a darker third colour; slight misregistration (offset 1–2 px, seeded per shape so it doesn't flicker); no shadows, outlines or gradients. **`halftone(ctx, path, ink, density)`**: a dot pattern for shading, generated once per size and cached.
2. **Backgrounds:** `bg_sheet` (off-white paper with fine grain, generated once as a tile and cached, with a thin ink rule and a cable line at the top for "AS OF <MONTH YEAR>") and `bg_board` (the relations web board: a soft mist field with faint grid dots).
3. **Palette** (add to `C`): paper `F3EFE6`, teal ink `1F6F78`, coral ink `E2603F`, overprint `6B4A4F`, charcoal `26282B`, mist `D7DCDA`, river blue `4E8FB0`. **Passport violet `5B4B9A` is used only for the memory-tip stamp.**
4. **Fonts:** headlines in Inter Black (large, magazine-cover style); cable text (dates, quoted official lines) in DejaVu Sans Mono; body and captions in Inter.
5. **The passport (`web.py`):** an open passport with numbered pages; each episode's stamp is its own entry (text and a simple stamp shape: round, rectangular or triangular, alternating). Earlier stamps stay. The last episode of each unit flips through that unit's pages.
6. **The relations web (`web.py`):** a board with an "India" token in the centre and partner tokens around it (countries and groupings, placed loosely by direction, with **no map shapes**). Threads are drawn as gently curved ink lines with a small label tag. It is drawn from a **state** listing every thread added so far (see the "Web thread" column in `episode_plan.md`), so any episode can draw it exactly as it should look at that point. Labels carry facts, never colour-coded judgements.
7. **Sound:** in `audiomix.py`, add a soft, original bed of muted marimba and low pads in place of the piano pad, a faint `tick` (teleprinter) when a cable line or date prints, a `stamp` thunk for the passport, and a light `pluck` when a thread is added. Keep everything well below the narration.
8. **Shorts pipeline:** make the frame size configurable so the same scene code can render 1080×1920 (see `reference/art_shorts_pipeline/`). A Short is its own small `short.py` with its own beats, about 45–55 s, with captions in the lower third, safely above YouTube's on-screen buttons (keep the bottom 300 px and the right 140 px clear).
9. **Official map:** get the Survey of India political map (rule 7), convert it to `engine/data/india_official.svg`, and build a `india_map(ctx, view, t)` helper that draws it in the riso style and supports camera fly-ins.
10. **Check:** render 4 stills (a headline sheet with the cable line, the official India map with animated rivers mid-fly-in, the relations web with five threads and the passport beside it, and a vertical Short frame) plus one 15-second motion preview, and look at them before building any episode.

## Motion: how the animation should feel
The user wants **richer animation than the earlier series**. Static slides with fades are not enough. Every scene follows these rules:
- **Nothing stands still.** Every shot has a slow camera move (a 2–4% push-in or pan over the beat). No frame stays unchanged for more than 3 seconds.
- **Depth.** Build scenes in 3 layers (background, middle, foreground) that move at different speeds (parallax) during camera moves.
- **Purposeful entrances.** Elements print in with the ink settling into register (misregistration easing to zero), staggered 0.08–0.15 s apart. Cards use a spring ease with a small overshoot. Lines draw on: timeline rules, web threads, arrows.
- **Living maps.** The camera flies from the official map of India into the region; rivers flow (moving dashes), sea lanes carry small moving ship dots, pins drop with a bounce and a ripple, and routes draw from A to B.
- **Kinetic type.** Headline words land one by one; key terms highlight in sync with the narration (use per-beat timing from `vo/durs.json`, splitting long beats into word groups).
- **Numbers move.** Figures count up, bars grow, dates tick into place on the cable line with the teleprinter sound.
- **People gesture.** Generic figures have a subtle idle motion (breathing, a head turn) and one simple gesture when they "speak" (a hand raised at a podium, two figures shaking hands).
- **Transitions.** Between segments, a 0.5 s paper-sheet slide or ink wipe; inside a segment, match cuts (a pin becomes the next card).
- **Rhythm.** Something new happens on screen every 5–8 seconds, timed to the narration beats.
- **Speed.** Cache every static layer as an image; draw only what moves on each frame.
- **Check motion, not just stills.** For each episode, also render a 15-second 540p preview of its busiest segment and look at 6 frames sampled 0.3 s apart, to confirm things actually move smoothly.

## Episode format (long video, exactly 300 s)
| Time | Segment | Template |
| --- | --- | --- |
| 0:00–0:20 | The headline: a briefing sheet slides in with a big headline and the "As of" cable line; one question, usually "Why does this matter for India?" | HEADLINE |
| 0:20–1:05 | Backstory: a horizontal timeline with 4–6 dated markers that print in one by one | TIMELINE |
| 1:05–2:05 | What's happening: key terms, the players as tokens, simple diagrams; places, rivers and sea lanes as pins on a schematic board | EXPLAIN, BOARD |
| 2:05–2:35 | Where they stand: 2–3 position cards side by side, equal in size, each attributed | STANDS |
| 2:35–3:05 | India's stake: three interest tiles with one line each | STAKES |
| 3:05–3:30 | Passport stamp: the memory tip, stamped in violet | STAMP |
| 3:30–4:25 | Exam desk: two Prelims statements that flip to True or False with a one-line reason; then a Mains question with a three-part answer frame | EXAM |
| 4:25–5:00 | Watchlist: three things to watch; a new thread is added to the relations web; "Next briefing: …" | WATCH, WEB |

Narration is about 480–600 words per episode (the sample has about 560).

## Short format (vertical 1080×1920, about 45–55 s)
| Time | What happens |
| --- | --- |
| 0–5 s | The headline as a question |
| 5–25 s | The passport stamp tip, laid out vertically |
| 25–45 s | One Prelims True/False, with "Pause", 3-2-1 and the answer |
| 45–55 s | The relations web with the series title; "Full briefing on the channel" |

## World This Month (from December 2026)
One 300 s episode per month, numbered `M2612`, `M2701`, …: a headline sheet, six mini-briefings of about 40 s each (headline, two lines of what happened, one line on India's stake), a passport stamp of the month, and the watchlist. Script it in `scripts/monthly_YYYY_MM.md` from news of that month only, with sources; it follows rule 1 like any script. Output names `WaM2612_<Title>.mp4` and so on.

## Scene templates (in `engine/brief.py` and `engine/web.py`)
- **HEADLINE:** `bg_sheet`. The sheet slides up; the headline prints in two inks; the cable line types out "AS OF NOV 2026" with ticks.
- **TIMELINE:** a horizontal rule with 4–6 dated markers that print in turn; each has a short label in mono.
- **EXPLAIN:** tokens, labels and simple riso diagrams that print in (fade up with misregistration settling), never pop.
- **BOARD:** a map board. For India and its neighbourhood: the official Survey of India map (rule 7), credited, with the camera flying in to the area; rivers, sea lanes and pins animate on top. For distant regions: a schematic board of coasts, rivers, sea lanes and pins, without country boundaries.
- **STANDS:** 2–3 cards of exactly equal size and weight, headed "India says", "<Country> says" or "<Organisation> says", with 2–3 short lines each, quoting or closely paraphrasing official statements.
- **STAKES:** three tiles with a simple icon (shield, oil drop, ship, handshake, person, leaf…) and one line each.
- **STAMP:** a passport page; the violet stamp thunks down with the `stamp` sound; up to three short lines.
- **EXAM:** two statement cards that flip to TRUE or FALSE with a one-line reason; then a Mains card with the question and a three-part answer frame.
- **WATCH:** three numbered items; dates only for scheduled events.
- **WEB:** `bg_board`. The relations web in its current state; the new thread draws in with a `pluck`.

## Writing scripts for a unit
1. **Research first.** For each episode, search the news of the last few months and open the official and reliable pages (MEA statements, government releases, court and UN documents, major news outlets). Check that the topic in `episode_plan.md` still matters; if the news has moved on, adjust the episode's angle and say so.
2. Write `scripts/unitN_scripts.md` in exactly the format of `sample_ep01.md`: a header line (Passport stamp · Web thread · As of · Refresh by), the long-video table following the eight segments, the Short table, then **Sources** and **Fact check before rendering**.
3. Every episode has a memory tip, a Where they stand section with each position attributed, two Prelims statements with clear answers, and a Mains question.
4. Commit and push the script file, tell the user, and **stop** (rule 1). They may approve only some episodes. Update the Status column in `episode_plan.md` as you go.

## Refreshing an episode (`/refresh N`)
Re-run the research for the episode. If nothing material has changed, just push a new **As of** month in the YouTube description. If something has changed (a new ruling, a deal signed, a summit held), write the changed narration lines into the script under "Refresh <month year>", push, and stop for the user's `/approve N`. Then re-render the episode and its Short with the new "As of" date, replace the files in `output/`, and add "Updated <month year>" to the YouTube title.

## Delivering each episode
- `output/WaNN_<Short_Title>.mp4` and `output/WaNN.srt`
- `output/shorts/WaNN_short.mp4` (1080×1920, 30 fps, captions burnt in)
- `output/youtube/WaNN.txt`: title, description (with an "As of <month year>" line and the Sources list), chapters, and a short title and description for the Short with #Shorts. Plus `WaNN_thumb.png`: a designed thumbnail (a big two-ink headline and one simple riso motif, **without** the caption box or corner tag). Check that every thumbnail is a real image and not blank.
- Long videos: 1920×1080, 30 fps, `libx264 -preset veryfast -crf 20`, yuv420p, AAC 192k, `-movflags +faststart`
- Commit and push each finished episode, with its Short, as soon as it's ready. If you work on a branch, keep one open pull request and tell the user the branch name.

## Setup notes
- Run `bash setup.sh` once. It installs pycairo, piper-tts and numpy, and downloads the narrator voice from **GitHub releases** to `voice/`. Hugging Face is usually blocked, so don't try it.
- The voice model is 16 kHz; the audio mix resamples it to 44.1 kHz.
- Use the same narrator voice as the other series, so the channel sounds consistent.
- Lessons from earlier series: animation that is too static (fix with the Motion rules), keep labels clear of pins and markers, make the recurring world (here, the passport and the web) a main visual and not a small inset, make sure on-screen numbers and dates match the narration exactly, make thumbnails as designed images (an earlier series shipped blank ones), and never render scripts the user hasn't approved.
