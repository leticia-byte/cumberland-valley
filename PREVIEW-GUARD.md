# Preview guard — remove this before launch

Three things on this site are **preview-only** and must come off before it goes public:

| What | Where | Why it can't ship |
|---|---|---|
| `X-Robots-Tag: noindex, nofollow` | `vercel.json` | see below |
| `Disallow: /` | `robots.txt` | see below |
| **Feedbucket review widget** | `build/parts.py` → `FEEDBUCKET` | third-party script + floating comment UI on every page — a client review tool, not something a pet owner should load |

The first two are deliberate and **temporary**.

## Why

The first `vercel` run on a new project deploys to **production**, so the site is live at
`cumberland-leticia-de.vercel.app`. Meanwhile the homepage copy says **"open Tuesdays until
10 p.m."** in four places, while the `LocalBusiness` schema on the same page tells Google
**Tuesday closes at 5 p.m.** — those hours came from the client and are wired into the schema,
the header widget, and the Contact page.

That schema exists so Google reads it. Indexed as-is, a pet owner searching "vet near me" could
be told the clinic is open at 8 p.m. on a Tuesday when it isn't.

The URL still works and is fully shareable with the client. It just won't be indexed.

## To remove at launch

1. Resolve the Tuesday conflict with Dr. Dolan — either the copy is wrong, or the hours are.
2. Delete `robots.txt`.
3. Delete the `X-Robots-Tag` block from `vercel.json` (keep the `/assets/` caching block).
4. **Remove Feedbucket:** delete the `FEEDBUCKET` constant and its `{FEEDBUCKET}` slot in
   `head()` in `build/parts.py`, delete the `<script>` block from `index.html` (hand-written,
   not generated), then rebuild:
   ```bash
   cd build && for g in gen_contact gen_services gen_team gen_pet_resort; do python3 $g.py; done
   grep -rl feedbucket *.html   # must return nothing
   ```
5. `git push` — the repo is connected to Vercel, so `master` auto-deploys to production.

## Also outstanding

See `DEPLOY.md` for the full list — `[VERIFY: YEAR]`, dog boarding vaccine requirements,
grooming copy, the PetSites click-tracker link, and the missing team portraits.
