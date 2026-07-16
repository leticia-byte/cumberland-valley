# STATE — Cumberland Valley Veterinary Clinic & Pet Resort

**practice_slug:** cumberland-valley
**Domain:** cumberlandvalleyvets.com · Hagerstown, MD
**Salesforce:** Account 001PX00000aJN4EYAW
**Designer:** Leticia Mora
**Last updated:** 2026-07-14

## Phase

**Creative Builder** — direction is locked, homepage v1 rendered and in refinement.

## Locked direction

**A — "The Stone That Stayed."** The clinic burned to the ground in 1996; the stone sign holder out front was the only thing left standing, and it became the logo. The site answers the independent-vs-corporate tension with permanence instead of argument.

- **Palette (sampled from CVVC-final-logo_color.jpg):** Logo Navy `#0D244D` · Signal Blue `#175097` · Fieldstone `#808286` · Mortar `#D4D5D7` · Oat Paper `#F4F1EA` · Barn Clay `#A24E32` (CTA) · Hearth `#E8A33D` (accent, once per screen)
- **Type:** Fraunces 600 (headings) / Inter 400 (body, 17px floor)
- **Borrowed elements:** none — direction stands on its own

## Approved sections

Homepage v1 rendered in full with Alie's complete copy: hero, trust bar, Who We Are, What We Believe (3 numbered slabs), Services (7, boarding promoted to a wide card), Community, FAQ (6 Q's, Q1 open by default), CTA close. None individually signed off yet.

**Real stone artwork now in use.** Client's `stone-background.png` (3403×1444) was in the connected local folder `/Users/leticiamora/Documents/Claude/Projects/Cumberland/images`; copied into `assets/`. Processed to `stone-background-cut.png` (mortar chroma-keyed to transparent so the page shows through as mortar) and masked to fade the top edge — this is what makes the blend seamless. The regenerated `stone-wall*.svg` files are now unused and can be deleted.

**Hero = "Rising Wall"** (chosen from 3 concept explorations after pushing past background-placement). Dawn-navy CSS sky + rolling hills + blended dry-stack wall (navy mortar so it seams into the sky) along the bottom. Background wired to `assets/hero-home.mp4` (autoplay/muted/loop) with a farmland poster + CSS sky as fallback until the file lands. Floating stones and the cat/dog silhouettes were tried and removed per designer. Standalone hero explorations kept in the folder: `-hero-rising-wall.html`, `-hero-threshold.html`, `-hero-variations.html`, `-hero-variations-v2.html`.

## Pending refinements

- Logo sizing settled: full stacked lockup, `object-fit: contain`, 114px header / 99px on scroll / 122px footer. An emblem-only crop was tried and reverted — it clipped the wordmark.
- Awaiting designer review of the rest of the page.

## Open questions

**For Alie / Dr. Dolan:**
- `[VERIFY]` Year Dr. Dolan bought the practice — appears 3× in the copy as a placeholder.
- `[VERIFY]` Exact Tuesday evening hours + emergency policy; scope of services during evening hours.
- Do pocket pet and avian services stay featured, or recede?
- Pricing page — Dr. Dolan is "on the fence."

**Blocking:**
- **`assets/hero-home.mp4` is referenced by the Rising Wall hero but not yet in the folder.** Drop the file into `cumberland-valley/assets/` and it auto-plays behind the wall; until then a farmland poster + CSS dawn sky show as fallback.
- **All photography is placeholder.** The client's Drive Images/Videos folder is empty. Only the logo has landed. Outstanding asks: the real stone sign out front, the two stained-glass logo windows in the clinic, Dr. Dolan on her farm, updated staff headshots, the GoPro clinic tour ("This is Stan"), the Chihuahua-and-four-puppies foster story.

## Input notes

- **No Brand Discovery Brief exists** for this practice. Brand grounding came from Alie's homepage copy (incl. its Internal Context / Strategic Background block, Apr 20 2026) and the Dr. Jen Dolan onboarding call transcript (Apr 9 2026).
- Copy is locked and client-safe. Do not rewrite it.
- **DE Brain MCP is not authorized in this session** — no live Salesforce pull was possible.

## Non-negotiables

- Phone CTA is primary everywhere. Dr. Dolan refuses online self-scheduling. `Call (301) 739-3121`.
- Legibility over flourish — blue-collar, farming, heavily geriatric clientele; many won't drive 40 minutes over the mountain.
- Body copy never below 17px.
- Trust bar must render as live text, not an image (SEO).
- H1 stays verbatim: "Hagerstown's veterinarian, keeping care close to home."
- FAQ schema (JSON-LD) + LocalBusiness schema required at build.

## Recommended next action

Walk the homepage section by section with the designer and collect refinements, then build approved sections as real Astro components.

## Files

```
cumberland-valley/
├── STATE.md
├── cumberland-valley-creative-thesis.md
├── cumberland-valley-homepage-v1.html      ← current render
└── directions/
    ├── cumberland-valley-direction-a.html  ← LOCKED
    ├── cumberland-valley-direction-b.html
    ├── cumberland-valley-direction-c.html
    └── cumberland-valley-direction-d.html
```
