---
description: Mark episodes' scripts as approved, so /make-episode is allowed to render them
argument-hint: <episode numbers, e.g. 1 2 3 5>
---

I approve the scripts for these India and the World episodes: **$ARGUMENTS**

For each number:
- Check that its script exists in `scripts/` (Episode 1 uses `sample_ep01.md`). If it doesn't, don't mark it, and tell me.
- If its Status in `scripts/episode_plan.md` is `to script` or `sample script (approve)`, change it to `scripted`. Leave `done` episodes as they are.

Don't change any script text. Commit and push `scripts/episode_plan.md`, then reply with the episodes now marked approved and this line: "Run /make-episode with these numbers to make the videos." Don't render anything.
