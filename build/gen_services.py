import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from parts import head, topstrip, nav, herolite, footer, script, TEL_HREF, TEL_DISPLAY

# "Services we offer" — verbatim from the client. These are promises/positioning, not a nav list,
# so they stay as a checklist rather than becoming clickable cards.
OFFER = [
    "Comprehensive state-of-the-art veterinary care for your dog or cat",
    "Complete medical and surgical care",
    "Dentistry services",
    "Pet boarding at our Pet Resort",
    "Grooming at our Pet Resort",
    "The very best in customer service",
    "Highly qualified and caring staff dedicated to the finest preventative &amp; therapeutic care",
    "Maintain a leading edge standard in veterinary medicine",
    "Dedicated to the health &amp; vitality of your pets",
]

# "Additional Services" — verbatim client list, alphabetical as supplied. Icons mapped by meaning.
ADDITIONAL = [
    ("Anesthesia and Patient Monitoring", "fa-solid fa-wave-square"),
    ("Avian Medicine and Surgery",        "fa-solid fa-dove"),
    ("Breeding Services",                 "fa-solid fa-dna"),
    ("Grooming",                          "fa-solid fa-scissors"),
    ("Health Screening Tests",            "fa-solid fa-vial"),
    ("Medical Services",                  "fa-solid fa-stethoscope"),
    ("Nutritional Counseling",            "fa-solid fa-bowl-food"),
    ("Pet Resort",                        "fa-solid fa-house"),
    ("Preventive Services",               "fa-solid fa-shield-heart"),
    ("Surgical Services",                 "fa-solid fa-briefcase-medical"),
    ("Wellness and Vaccination Programs", "fa-solid fa-syringe"),
]

SCHEMA = '''
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "VeterinaryCare",
  "name": "Cumberland Valley Veterinary Clinic & Pet Resort",
  "url": "https://cumberlandvalleyvets.com/services",
  "telephone": "+1-301-739-3121",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "17747 Virginia Ave.",
    "addressLocality": "Hagerstown",
    "addressRegion": "MD",
    "postalCode": "21740",
    "addressCountry": "US"
  },
  "hasOfferCatalog": {
    "@type": "OfferCatalog",
    "name": "Veterinary Services",
    "itemListElement": [
''' + ",\n".join(
    '      { "@type": "Offer", "itemOffered": { "@type": "Service", "name": "%s" } }' % n.replace('&amp;', '&')
    for n, _ in ADDITIONAL
) + '''
    ]
  }
}
</script>
'''

html = head(
    "Veterinary Services in Hagerstown, MD | Cumberland Valley Veterinary Clinic",
    "Comprehensive veterinary care in Hagerstown, MD — medical, surgical, dental, avian, boarding and grooming at the Cumberland Valley Pet Resort.",
    schema=SCHEMA,
)
html += topstrip()
# nav stays LIGHT here — herolite is a light hero, so navy links read fine (15.25:1).
# .ondark would make them white on white.
html += nav("services.html")
html += herolite(
    "Advanced medicine,<br><em>compassionate care.</em>",
    "At Cumberland Valley Veterinary Clinic your pet's health and vitality is our number one concern. We believe the best medicine is preventative.",
    "We answer the phone. No portal, no booking form, no phone tree.",
    video="services-hero",
)

offer_li = "\n".join(
    f'          <li><i class="fa-solid fa-check" aria-hidden="true"></i><span>{t}</span></li>' for t in OFFER
)
pills = "\n".join(
    f'      <div class="pill-item"><i class="{ic}" aria-hidden="true"></i><span>{n}</span></div>'
    for n, ic in ADDITIONAL
)

html += f'''
<main id="main">

<!-- intro — client copy, verbatim.
     .tex = oat + parallax stone texture, matching the homepage's "Comprehensive Veterinary
     Services in Hagerstown, MD" section (.services + .whobg). -->
<section class="sec tex">
  <div class="texclip" aria-hidden="true"><div class="whobg"></div></div>
  <div class="wrap split">
    <div class="rv">
      <h2 class="big">Your pet's health and vitality is our number one concern</h2>
      <div class="rule"></div>
      <div class="prose">
        <p>At Cumberland Valley Veterinary Clinic your pet's health and vitality is our number one concern. We believe the best medicine is preventative and we always take time to educate our clients and to provide them with the best approach to their pet's health.</p>
        <p>Using state-of-the-art equipment, keeping abreast of advances and technologies and our kind, caring attitude is what separates us from the rest. We believe that pets are full members of your family, and should be treated as such.</p>
      </div>
      <a class="callbtn" style="margin-top:28px" href="{TEL_HREF}" aria-label="Call Cumberland Valley at {TEL_DISPLAY}"><i class="fa-solid fa-phone" aria-hidden="true"></i> Call {TEL_DISPLAY}</a>
    </div>
    <div class="fig rv">
      <!-- alt written from the actual frame, not the filename -->
      <picture>
        <source srcset="assets/services-img-2.webp" type="image/webp">
        <img src="assets/services-img-2.jpg" alt="A man in teal scrubs bending down to greet a golden retriever holding a tennis ball">
      </picture>
    </div>
  </div>
</section>

<!-- "Services we offer" — client copy, verbatim.
     Image left / copy right, the mirror of the intro section above it, so the page alternates
     rather than running two identical copy-left rows back to back.
     .split-flip only swaps the COLUMN WIDTHS (the wider track follows the copy); the DOM order
     is genuinely image-then-copy, so it isn't a visual-vs-reading-order mismatch (WCAG 1.3.2). -->
<section class="sec navy">
  <div class="wrap">
    <div class="split split-flip">
      <div class="fig rv">
        <picture>
          <source srcset="assets/services-img-1.webp" type="image/webp">
          <img src="assets/services-img-1.jpg" alt="Two pet owners in a park, each carrying a dog over their shoulder">
        </picture>
      </div>
      <div class="rv">
        <h2 class="big">Services we offer</h2>
        <div class="rule"></div>
        <ul class="ticks">
{offer_li}
        </ul>
      </div>
    </div>
  </div>
</section>

<!-- "Additional Services" — client copy, verbatim, alphabetical as supplied. Same .tex treatment. -->
<section class="sec tex">
  <div class="texclip" aria-hidden="true"><div class="whobg"></div></div>
  <div class="wrap">
    <div class="rv">
      <h2 class="big">Additional services</h2>
      <div class="rule"></div>
      <p class="lead" style="margin-top:18px">Everything below happens under one roof on Virginia Ave. To ask about any of it, call <a class="telinline" href="{TEL_HREF}">{TEL_DISPLAY}</a>.</p>
    </div>
    <div class="pills rv">
{pills}
    </div>
  </div>
</section>

<!-- closing CTA — reuses the homepage's .close-cta treatment verbatim so the two pages
     end on the same note (same navy field, same radial glow, same big phone number). -->
<section class="close-cta">
  <div class="wrap inner rv">
    <h2>Not sure what your pet needs?</h2>
    <p>Call us and describe what you're seeing. We'll tell you honestly whether it's something to watch, something to schedule, or something to come in for today.</p>
    <a class="phone" href="{TEL_HREF}" aria-label="Call Cumberland Valley at {TEL_DISPLAY}">{TEL_DISPLAY}</a>
  </div>
</section>

</main>
'''

html += footer()
html += script()

out = os.path.join(os.path.dirname(__file__), '..', 'services.html')
open(out, 'w').write(html)
print("wrote services.html", len(html), "bytes")
