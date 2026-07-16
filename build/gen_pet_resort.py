import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from parts import head, topstrip, nav, herolite, footer, script, TEL_HREF, TEL_DISPLAY

# Client copy, verbatim. Structured as one page with anchored sections rather than four pages:
# Feline Boarding is ~90 words and Grooming has no copy at all — as standalone pages those
# would launch thin, which costs more in SEO than the extra keyword targeting gains.
# Each section has its own id so it's linkable today and can be promoted to its own page later.

SECTIONS = [
    {
        "id": "canine-boarding",
        "nav": "Canine Boarding",
        "h2": "Canine Boarding",
        "icon": "fa-solid fa-dog",
        "lede": "When going out of town, a reliable pet sitter is definitely a need. At our pet resort, your doggie will be tended to by our amazing and caring staff. With the ability to choose group play, your pup will get lots of play time with or without playmates. Our staff works diligently to provide the best care for your pets, and have a vet available just a building away!",
        "paras": [
            "There are two boarding options, standard, and luxury. Standard is a smaller kennel compared to luxury. Suites include raised beds and raised food/water bowls.",
            "In both Standard and Luxury kennels are equipped with heated floors, separate air exchanges, and complete climate control. We provide bedding, blankets, and water/food bowls.",
            "While dropping-off or picking-up your pet don&rsquo;t forget to check out our awesome pet boutique located in the lobby of the Pet Resort!",
        ],
        # The operational facts a pet owner needs BEFORE they call — pulled out of the prose so
        # they're scannable. Every one is the client's own wording, just lifted into a list.
        "facts": [
            ("fa-solid fa-tag", "Multi-pet discount",
             "25% per animal, as long as your animals stay in the same kennel. The discount does not apply if they must be separated for feedings."),
            ("fa-solid fa-bowl-food", "Feeding &amp; medication",
             "Must be supplied at drop-off, with instructions."),
            ("fa-solid fa-scissors", "Before pick-up",
             "Don&rsquo;t forget about clean up baths or grooming prior to pick-up."),
        ],
    },
    {
        "id": "feline-boarding",
        "nav": "Feline Boarding",
        "h2": "Feline Boarding",
        "icon": "fa-solid fa-cat",
        "bg": "navy",          # #0D254D — the same navy as the homepage community band
        "lede": "Cats need the perfect balance of laziness and stimulation and our cat condos provide just that. A multi-level space for cats to climb or to lounge in, with separate compartments for litter boxes is perfect for a cats stay.",
        "paras": [
            "We provide bedding, litter boxes, and water/food bowls. All food and medications that must be administered throughout their stay must be provided with instructions.",
        ],
        "facts": [
            ("fa-solid fa-syringe", "Vaccines required",
             "Rabies and Distemper vaccines are required for your cat&rsquo;s stay here."),
        ],
    },
    {
        "id": "doggie-daycare",
        "nav": "Doggie Daycare",
        "h2": "Doggie Daycare",
        "icon": "fa-solid fa-bone",
        "lede": "Being in doggy daycare a few times a week will keep your dog mentally stimulated and physically active, all while meeting new furry friends to play with. Your pooch will also be relaxed and exhausted by the time you pick them up, meaning an evening walk will be less necessary.",
        "paras": [
            "The dogs have a big indoor playroom, meaning no matter the weather, they won&rsquo;t have to stop playing! There are also doggy doors that allow dogs to go out into a fenced yard as they please. But puppy naps are always necessary, so in the middle of the day, we allow a quiet time.",
            "If feedings or medication administration is needed during your pet&rsquo;s stay, please supply those items upon drop-off with instructions.",
        ],
        "facts": [
            ("fa-solid fa-calendar-days", "Hours",
             "Available 7 days a week. Drop-off and pick-up between 7&ndash;9 a.m. and 4&ndash;6 p.m."),
            ("fa-solid fa-paw", "Group play requirement",
             "Dogs must be spayed or neutered by 1 year of age for group play."),
            ("fa-solid fa-credit-card", "Paying",
             "Pay by the day, or buy a package &mdash; packages do not need to be used consecutively."),
        ],
    },
    # Grooming section removed on request — no copy was supplied for it.
    # NOTE: the service is still referenced elsewhere on the site (Services page lists
    # "Grooming at our Pet Resort", and the canine boarding copy above says "don't forget about
    # clean up baths or grooming prior to pick-up"). Those mentions now have nowhere to point.
]

SCHEMA = '''
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "AnimalShelter",
  "name": "Cumberland Valley Pet Resort",
  "description": "Dog and cat boarding and doggie daycare at Cumberland Valley Veterinary Clinic & Pet Resort in Hagerstown, MD.",
  "url": "https://cumberlandvalleyvets.com/pet-resort",
  "telephone": "+1-301-739-3121",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "17747 Virginia Ave.",
    "addressLocality": "Hagerstown",
    "addressRegion": "MD",
    "postalCode": "21740",
    "addressCountry": "US"
  },
  "parentOrganization": {
    "@type": "VeterinaryCare",
    "name": "Cumberland Valley Veterinary Clinic & Pet Resort"
  }
}
</script>
'''


def railsec(s):
    """One topic inside the sticky-rail body. No per-section band: the rail layout puts all
    three services inside ONE .tex section, which is the trade-off — the navy Feline band
    can't survive here (flagged when this layout was chosen)."""
    lede = f'<p class="lead" style="margin-top:18px">{s["lede"]}</p>' if s["lede"] else ''
    paras = "\n            ".join(f'<p>{p}</p>' for p in s["paras"])
    prose = f'<div class="prose" style="margin-top:18px">\n            {paras}\n          </div>' if paras else ''
    facts = ""
    if s["facts"]:
        items = "\n".join(f'''            <div class="fact">
              <div class="fact-i"><i class="{ic}" aria-hidden="true"></i></div>
              <div>
                <div class="fact-t">{t}</div>
                <p>{b}</p>
              </div>
            </div>''' for ic, t, b in s["facts"])
        facts = f'\n          <div class="facts">\n{items}\n          </div>'
    return f'''
        <div class="railsec rv" id="{s["id"]}">
          <div class="pr-eyebrow"><i class="{s["icon"]}" aria-hidden="true"></i> Pet Resort</div>
          <h2 class="big">{s["h2"]}</h2>
          <div class="rule"></div>
          {lede}
          {prose}{facts}
        </div>'''


CSS = '''
<style>
  /* Rail styles live in assets/site.css (.railgrid/.rail/.railsec) — shared, so the sticky and
     min-width fixes apply everywhere. Only the Pet Resort's own bits are here. */
  .pr-eyebrow{font:600 11px/1 'Inter';letter-spacing:.18em;text-transform:uppercase;
    color:var(--blue);margin-bottom:14px;display:inline-flex;align-items:center;gap:9px}
  .pr-eyebrow i{font-size:14px}

  /* the practical facts, lifted out of the prose so they're scannable before someone calls */
  .facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(260px,100%),1fr));
    gap:18px;margin-top:30px}
  /* a lone card in an auto-fit grid stretches the whole track — cap it so one fact reads as a
     card, not a banner (Feline Boarding has exactly one) */
  .facts .fact:only-child{max-width:520px}
  .fact{display:flex;gap:14px;align-items:flex-start;background:#fff;
    border:1px solid rgba(13,36,77,.12);border-radius:14px;padding:20px;box-shadow:var(--sh-sm);
    transition:transform .3s cubic-bezier(.2,.8,.2,1),box-shadow .3s}
  .fact:hover{transform:translateY(-3px);box-shadow:var(--sh-md)}
  .fact-i{width:40px;height:40px;border-radius:10px;flex:none;background:rgba(22,82,155,.10);
    color:var(--blue);display:flex;align-items:center;justify-content:center;font-size:16px}
  .fact-t{font:700 14px/1.3 'Inter';color:var(--navy);margin-bottom:5px}
  .fact p{font:400 14px/1.6 'Inter';color:#4A525C}
</style>
'''

html = head(
    "Pet Resort | Dog &amp; Cat Boarding in Hagerstown, MD | Cumberland Valley",
    "Dog and cat boarding and doggie daycare at the Cumberland Valley Pet Resort in Hagerstown, MD — with a veterinarian just a building away. Call (301) 739-3121.",
    extra_css=CSS, schema=SCHEMA,
)
html += topstrip()
html += nav("pet-resort.html")
html += herolite(
    "The Pet Resort,<br><em>a building away from the vet.</em>",
    "Boarding and daycare for dogs and cats — looked after by our own staff, with a veterinarian on site.",
    "We answer the phone. No portal, no booking form, no phone tree.",
    video="pet-resort",
)

rail_links = "\n".join(
    f'        <a href="#{s["id"]}"><span class="r-i"><i class="{s["icon"]}" aria-hidden="true"></i></span>{s["nav"]}</a>'
    for s in SECTIONS)

html += f'''
<main id="main">

<!-- Layout B · sticky rail. The three services pin on the left while the content scrolls past,
     phone number always in the rail — so the whole offering stays visible. Someone boarding a
     cat and someone booking daycare are different people landing on the same page.
     TRADE-OFF: all three live in ONE .tex band, so per-service backgrounds (the navy Feline
     band) aren't possible in this layout. -->
<section class="sec tex">
  <div class="texclip" aria-hidden="true"><div class="whobg"></div></div>
  <div class="wrap">
    <div class="railgrid">
      <nav class="rail" aria-label="Pet Resort services">
        <div class="rail-t">Our services</div>
{rail_links}
        <a class="rail-call" href="{TEL_HREF}" aria-label="Call Cumberland Valley at {TEL_DISPLAY}"><i class="fa-solid fa-phone" aria-hidden="true"></i> {TEL_DISPLAY}</a>
      </nav>
      <div class="railbody">
'''
html += "\n".join(railsec(s) for s in SECTIONS)
html += f'''
      </div>
    </div>
  </div>
</section>

<section class="close-cta">
  <div class="wrap inner rv">
    <h2>Planning a trip?</h2>
    <p>Call and we&rsquo;ll walk you through kennel options, what to bring, and what your pet needs before their stay.</p>
    <a class="phone" href="{TEL_HREF}" aria-label="Call Cumberland Valley at {TEL_DISPLAY}">{TEL_DISPLAY}</a>
    <div class="sm">The Pet Resort keeps its own schedule &mdash; call for drop-off and pick-up times</div>
  </div>
</section>

</main>
'''

html += footer()
html += script()

out = os.path.join(os.path.dirname(__file__), '..', 'pet-resort.html')
open(out, 'w').write(html)
print("wrote pet-resort.html", len(html), "bytes")
