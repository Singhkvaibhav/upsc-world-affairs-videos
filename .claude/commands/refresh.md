---
description: Re-check an episode against the latest news; propose changed lines if needed, then re-render after approval
argument-hint: <episode numbers, e.g. 1 or 1 9 16>
---

Refresh these India and the World episodes: **$ARGUMENTS**

For each episode:

1. Read its script, "As of" month and Sources. Search the news since that month and open the pages you rely on.
2. **If nothing material has changed:** update the "As of" line in `output/youtube/WaNN.txt` to this month, push, and report "no change".
3. **If something has changed** (a ruling, a deal signed or collapsed, a summit held, a ceasefire broken, an office-holder replaced): write the replacement narration lines for the affected rows under a heading "Refresh <month year>" below the episode in its script file, with new Sources. Keep everything else word for word. Set the episode's Status to `refresh (approve)` in `scripts/episode_plan.md`, push, and **stop**.
4. After I run `/approve N`, re-render the long video and the Short with the new lines and the new "As of" date (as `/make-episode` describes), replace the files in `output/`, add "Updated <month year>" to the YouTube title, set the Status back to `done`, and push.

Reply with a table: episode, what changed (or "no change"), and what's waiting for my approval.
