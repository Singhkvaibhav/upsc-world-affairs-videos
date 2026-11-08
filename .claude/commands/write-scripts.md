---
description: Research and write the scripts (long video + Short) for one unit, push them and stop for approval
argument-hint: <unit number, 1-6>
---

Write the scripts for **Unit $ARGUMENTS** of India and the World, Simply Briefed.

1. Take the unit's episodes from `scripts/episode_plan.md`. Skip any episode whose Status is already `scripted` or `done`, and skip Episode 1 (the format sample).
2. **Research each episode first.** Search the news of the last few months and open the pages you take facts from, using Indian and official sources in the order CLAUDE.md rule 3 gives (MEA, PIB, Parliament, Indian institutions, Indian newspapers; another government's position from its own official statement). Don't use foreign news outlets. If the topic's angle in the plan is out of date, adjust it and tell me.
3. Write them all into `scripts/unit$ARGUMENTS_scripts.md`, in exactly the format of `scripts/sample_ep01.md`: the header line (Passport stamp · Web thread · As of · Refresh by), the long-video table following the eight segments, the Short table, then **Sources** (pages actually opened, with links) and **Fact check before rendering**.
4. Every episode needs: a memory tip, a Where they stand section with each position attributed on equal terms, India's stake, two Prelims statements with clear answers, a Mains question with a three-part frame, a watchlist without predictions, and about 480–600 words of narration. Ongoing situations say "as of <month year>" out loud.
5. Follow every rule in CLAUDE.md, especially: no figures or dates from memory; Indian and official sources only; attribute disputed positions and never judge them; India's map only as the official Survey of India depiction; no flags, emblems or leaders' likenesses. Write Visual cells with the Motion rules in mind (camera moves, map fly-ins, things that draw on).
6. Commit and push the script file.

Then reply with a list of the episodes written, any facts you couldn't confirm, and this line: "Review the scripts on GitHub, then run /approve with the episode numbers you're happy with." **Stop there. Don't render anything.**
