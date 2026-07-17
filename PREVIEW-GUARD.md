# Preview guard — remove this before launch

`vercel.json` sends `X-Robots-Tag: noindex, nofollow` on every route, and `robots.txt`
disallows everything. Both are deliberate and **temporary**.

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
4. `npx vercel --prod`

## Also outstanding

See `DEPLOY.md` for the full list — `[VERIFY: YEAR]`, dog boarding vaccine requirements,
grooming copy, the PetSites click-tracker link, and the missing team portraits.
