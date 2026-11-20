# Notes for Claude (Léim)

## ⚠ Payhip: check the store before EVERY Payhip action
Claire-Louise has more than one Payhip store: **Léim** (payhip.com/Leim), **Spraoi Learning** (payhip.com/SpraoiLearning) and Lessons That Click. The Claude browser pane is shared by ALL chats, and Payhip keeps only one account signed in at a time, so another chat may have switched it.

1. **Before adding, editing or deleting any product**, check which store the pane is in: on payhip.com run `fetch('/products').then(r=>r.text())` and see which store link (`payhip.com/SpraoiLearning` or `payhip.com/Leim`) appears. If it isn't the store you need, **stop** and ask her to switch accounts (she types the password herself).
2. **After creating a product**, fetch its `payhip.com/b/<code>` page with `{credentials:'omit'}` and confirm it's sold by the right store.
3. **If you switch the pane to another store, tell her at the end** which account it's now signed in to, so the next chat doesn't sell in the wrong store.

(Rule added 15 Nov 2026 after 21 Léim products were created in the Spraoi Learning store by mistake.)

**Duplicates (19 Nov 2026, 19:20):** two chats put the Register & Tone, Tenses and Persuasive Writing teacher packs on Payhip at the same time. The site uses SnLO0, 70GDz and sZUcO. The copies **zheIT, cLkp5 and j89KS** are set to **Invisible** (not deleted). Leave them alone, or delete them only if she asks. To stop this happening again, check WORKING.md right before ANY Payhip step, even in the middle of a job.

The full Léim job list lives in the claude.ai project "LEIM REVISION" (claude/leim-todo.md).

**Scheduled auto-build runs log their work in claude/leim-autobuild-log.md (newer than leim-todo.md, which is too long for them to retype). Read it right after leim-todo.md. 20 Nov 17:40: Orders 20 Ad Breaker, 21 Stage It, 22 Format Sort, 23 Mood Match, 24 Speech Marks Sprint, 26 Proofread Patrol and 27 Shot Spotter are LIVE; their packs are held as P7 (tmp-839010c8), P8 (tmp-d196610c), P9 (tmp-30c15d86), P10 (tmp-038768ad), P11 (tmp-97aba7b8), P12 (tmp-c0ac3487) and P13 (tmp-8ae32cba); next build job is Order 28 Shakespeare (HL) → Who Said It?. New game mains must start with `<main id="main">` — copy src/speech-marks-sprint.main.html.**

## ⚠ More than one chat can work on Léim at once — claim your job first
Before starting ANY job (a Maths topic, a Payhip change, a page edit), read **WORKING.md** in this repo and follow its rules: claim the job with a pushed commit before you start, pick a different job if another chat has claimed it, and remove your line when you finish. (Rule added 16 Nov 2026 after two chats nearly built the same Maths topic.)

## Subject display order (she asked 19 Nov 2026)
Wherever subjects are listed on the site (cards, buttons, menus, page sections, titles), use the official Irish order: **Irish, English, Maths**, then other subjects (Spanish). Subjects not live yet (e.g. Irish "coming soon") still go in their place. This is the display order only; the build order (Spanish → Maths → English → Irish) is separate.

## What Came Up (job 7, LIVE 20 Nov 2026)
The 2022–2026 topic grids are on the Spanish and Maths Exam Centres and the JC English page (`#came-up`), and every Maths/English game page + all three checklists show a "Came up in" line. Data: **src/came_up_data.py** (facts only: topic + year + question number — never copy SEC questions, texts or marking-scheme wording; the SEC said 20 Nov that it doesn't allow reproduction, linking to examinations.ie is fine). **When a new English game goes live, re-run `python3 src/build_came_up.py`** after assembling it (it fills the page's `<p class="came">` line from the topic's order number), then `python3 src/build_english_page.py` and `python3 src/build_checklists.py english` as usual. Add the 2027 papers to came_up_data.py after June 2027.
