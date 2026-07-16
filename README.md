# Cumberland Valley Veterinary Clinic & Pet Resort

Static prototype site. No build step — plain HTML + one shared stylesheet.

## Structure

- `index.html` · `services.html` · `team.html` · `pet-resort.html` · `contact.html` — the live pages
- `assets/site.css` — the entire design system (one sheet, shared by every page)
- `assets/` — logo, photography, hero video, favicons
- `build/` — Python generators. **The HTML is generated; edit these, not the HTML.**
  - `parts.py` — shared head/nav/footer/hours/scripts. Single source of truth.
  - `gen_*.py` — one per page. Run `python3 build/gen_<page>.py` to rebuild.
- `*-variants.html` — design comparison pages, not part of the site

## Rebuilding

```
for g in build/gen_contact.py build/gen_services.py build/gen_team.py build/gen_pet_resort.py; do python3 $g; done
```

`index.html` is hand-maintained; its nav/footer are re-generated from `parts.py`.

## Known gaps before launch

- `[VERIFY: YEAR]` — the year Dr. Dolan bought the practice (3 places in homepage copy)
- Homepage copy claims **"open Tuesdays until 10 p.m."** in 4 places; the client's confirmed
  hours close Tuesday at 5 p.m. The hours widget + schema use the client's hours. **Conflict.**
- Dog boarding vaccine requirements are unstated (the cat copy specifies Rabies + Distemper)
- Grooming is sold on the Services page but has no copy and no section
- PetSites nav link is a click-tracker URL with a signed token, not a durable link
- Team portraits are placeholder tiles — no photos supplied
- FAQ JSON-LD schema not yet added
