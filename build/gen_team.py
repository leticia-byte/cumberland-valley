import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from parts import head, topstrip, nav, herolite, footer, script, TEL_HREF, TEL_DISPLAY

# Client copy. The bios arrived TRUNCATED ("She went to…") — they're the teaser excerpts from
# the current site's team grid, not full bios. Rendered as supplied; the missing remainder is
# flagged rather than invented.
# All three veterinarians in ONE group. Dr. Dolan's ownership is carried by her role label
# rather than by a section of her own — which also fixes the sizing: a lone card in an auto-fit
# grid stretched to full width, so her photo rendered 2x her colleagues'.
#
# Full bios, client copy. Split into paragraphs at the client's own sentence groupings; the words
# are untouched except for two obvious typos in the source, marked [sic-fix] below.
#
# LEDE = the short line on the card, before the sheet opens. These are the client's OWN teasers —
# the truncated excerpts they first sent, which are what their current site already shows. Using
# them means the card copy is excerpted, not invented, and not just paragraph 1 dumped in full.
LEDES = {
    "Dr. Jennifer Dolan":     "Dr. Dolan grew up in Reston, Virginia, a suburb of Washington, D.C.",
    "Dr. Michele A. McKenna": "A 1986 graduate of the Virginia-Maryland Regional College of Veterinary Medicine.",
    "Dr. Robert Wesley":      "Gettysburg College and Towson State University, then veterinary school at Virginia-Maryland.",
}

VETS = [
    ("Dr. Jennifer Dolan", "Owner &amp; Veterinarian", [
        "Dr. Dolan grew up in Reston, Virginia, a suburb of Washington, D.C. She went to Virginia Tech for her undergraduate studies, earning a B.S. in biology. She went on to earn a M.S. in biology from The College of William and Mary and returned to Virginia Tech to earn her DVM at the Virginia-Maryland Regional College of Veterinary Medicine. She joined Cumberland Valley Veterinary Clinic in 1996.",
        # [sic-fix] source read "4 horses,4 dogs" (missing space) and ended "2 cows.." (double period)
        "She is married to a dairy veterinarian, Dr. Edward Wurmb, and has a young daughter, Abigail. Her family also includes 4 horses, 4 dogs &ndash; 2 of which are rescues, 5 cats, 3 rabbits, 3 goats and 2 cows.",
        "Dr. Dolan&rsquo;s greatest passion includes horseback riding; she participates in horse trials and combined training. She also enjoys golfing, skiing, antiquing, and gardening. She is a member of Hagerstown Sunrise Rotary Club and prior to the birth of her daughter enjoyed volunteering at a local horseback riding program for the handicapped. Go Hokies!",
    ]),
    ("Dr. Michele A. McKenna", "Veterinarian", [
        "Dr. McKenna is a 1986 graduate of Virginia-Maryland Regional College of Veterinary Medicine. She completed her undergraduate degree at the University of Maryland, College Park. She has been with Cumberland Valley Veterinary Clinic since January 2010. She previously worked in Gaithersburg, Germantown, and did relief work in Montgomery and Frederick counties. She had her own practice in Frederick from 1988-2000.",
        "She currently lives on a horse farm in Boonsboro with her husband, dogs, cats, horses and a pony. She has two grown children; a son who is working on his Masters and PhD degrees in Seattle, Washington and a daughter who is graduating from college and applying to medical school. She and her husband are avid foxhunters and are Whippers-in for the local foxhunting club (New Market-Middletown Valley Hounds).",
        "Dr. McKenna enjoys spending time with her family and friends, riding and competing her horses, fox hunting, gardening, and traveling. She believes that being a veterinarian is a great profession, and that patients/pets are AWESOME!",
    ]),
    ("Dr. Robert Wesley", "Veterinarian", [
        "Dr. Wesley went to Gettysburg College and Towson State University for his undergraduate degree in Biology. He then worked at Johns Hopkins School of Medicine as a research technician for several years, and part time at a small animal hospital in Baltimore as a Veterinary Technician. His increased interest in veterinary medicine led him to a full time position at the small animal hospital, and then to the University of Maryland School of Medicine followed by veterinary school at Virginia Maryland Regional College of Veterinary Medicine.",
        "He enjoys ice hockey, reading history and biography, Shakespeare, classic movies and building his own computers. He has two cats named Nick and Nora.",
    ]),
]

SCHEMA = '''
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "VeterinaryCare",
  "name": "Cumberland Valley Veterinary Clinic & Pet Resort",
  "url": "https://cumberlandvalleyvets.com/team",
  "telephone": "+1-301-739-3121",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "17747 Virginia Ave.",
    "addressLocality": "Hagerstown",
    "addressRegion": "MD",
    "postalCode": "21740",
    "addressCountry": "US"
  },
  "employee": [
    { "@type": "Person", "name": "Dr. Jennifer Dolan", "jobTitle": "Owner and Veterinarian" },
    { "@type": "Person", "name": "Dr. Michele A. McKenna", "jobTitle": "Veterinarian" },
    { "@type": "Person", "name": "Dr. Robert Wesley", "jobTitle": "Veterinarian" },
    { "@type": "Person", "name": "Tammy Snyder", "jobTitle": "Practice Manager" },
    { "@type": "Person", "name": "Tara Martin", "jobTitle": "Business Manager" }
  ]
}
</script>
'''


def person(i, name, role, paras):
    """Card shows the portrait, name, role and the first paragraph only; the full bio opens in
    an adaptive sheet (D3). Photo slot stays an empty tile — no stock photo. A stranger's face
    on a vet's bio card is worse than an honest gap. Real portraits still outstanding."""
    return f'''      <article class="person">
        <div class="p-photo">
          <i class="fa-solid fa-user-doctor" aria-hidden="true"></i>
        </div>
        <div class="p-body">
          <h3>{name}</h3>
          <div class="p-role">{role}</div>
          <p class="p-lede">{LEDES[name]}</p>
          <button class="biobtn" type="button" data-bio="bio{i}">
            <span>Read full bio</span><i class="fa-solid fa-arrow-right" aria-hidden="true"></i>
          </button>
        </div>
      </article>'''


def sheet(i, name, role, paras):
    body = "\n          ".join(f"<p>{p}</p>" for p in paras)
    return f'''    <dialog class="biosheet" id="bio{i}" aria-labelledby="bioh{i}">
      <div class="bs-grab" aria-hidden="true"></div>
      <button class="bs-x" type="button" aria-label="Close bio"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button>
      <div class="bs-scroll">
        <div class="bs-hero">
          <div class="bs-photo"><i class="fa-solid fa-user-doctor" aria-hidden="true"></i></div>
          <h3 id="bioh{i}" tabindex="-1">{name}</h3>
          <div class="p-role">{role}</div>
        </div>
        <div class="bs-body">
          {body}
          <a class="callbtn" style="margin-top:22px" href="{TEL_HREF}"><i class="fa-solid fa-phone" aria-hidden="true"></i> Call {TEL_DISPLAY}</a>
        </div>
      </div>
    </dialog>'''


html = head(
    "Our Team | Cumberland Valley Veterinary Clinic | Hagerstown, MD",
    "Meet the veterinarians and care team of Cumberland Valley Veterinary Clinic in Hagerstown, MD. Call (301) 739-3121.",
    schema=SCHEMA,
)
html += topstrip()
# herolite is a LIGHT hero — nav stays navy-on-light, not .ondark
html += nav("team.html")
html += herolite(
    "Our caring and compassionate<br><em>veterinary care team.</em>",
    "Meet the veterinarians and team of Cumberland Valley Veterinary Clinic in Hagerstown. We're pleased to provide exceptional vet care for your pets.",
    "We answer the phone. No portal, no booking form, no phone tree.",
    video="team-hero",
)

vets   = "\n".join(person(i, n, role, paras) for i, (n, role, paras) in enumerate(VETS))
sheets = "\n".join(sheet(i, n, role, paras)  for i, (n, role, paras) in enumerate(VETS))

# Management staff groups. Role mapping follows the CLIENT's own filenames, not my reading of
# the pictures. Alt text describes what is actually in each file (checked, not assumed):
#   management-csr        -> team member in scrubs at a workstation beside a pet carrier
#   management-tech       -> gloved hands examining a dog with a stethoscope
#   management-assistant  -> team member holding a grey cat over her shoulder
# (img, icon, title, alt, body)
GROUPS = [
    ("management-csr", "fa-solid fa-headset", "Client Service Representatives",
     "A Cumberland Valley team member in scrubs at a workstation, checking on a pet in a carrier",
     "Our client service representatives are the front line of customer service at Cumberland Valley Veterinary Clinic. Whether they are answering your phone call, checking you in for a visit with the doctor, or scheduling a future appointment, the client service representatives strive to make your experience at Cumberland Valley a pleasant one."),
    ("management-tech", "fa-solid fa-user-nurse", "Veterinary Technicians and Veterinary Nurses",
     "A veterinary technician listening to a dog's chest with a stethoscope during an exam",
     "Our veterinary technicians and veterinary nurses are instrumental in providing the highest quality veterinary care for your pet. They work closely with the veterinarians to provide diagnostic care, hospitalization, treatment, as well as some routine services such as nail clips and anal gland expressions. Our technicians and nurses are on staff throughout our entire business day to provide care for hospitalized animals, support for our doctors during appointments, and to provide client education."),
    ("management-assistant", "fa-solid fa-hand-holding-medical", "Veterinary Assistants",
     "A Cumberland Valley team member smiling as she holds a grey cat over her shoulder",
     "Our assistants are responsible for providing hands-on assistance to the doctors and veterinary technicians during surgical procedures and x-rays. They also assist in the clean up of all surgical equipment. Another responsibility of the veterinary assistant is to release and provide client education for the after care of patients who are hospitalized for illnesses and surgery."),
]

groups = "\n".join(f'''      <div class="slab">
        <div class="slabimg">
          <picture>
            <source srcset="assets/{img}.webp" type="image/webp">
            <img src="assets/{img}.jpg" alt="{alt}">
          </picture>
          <span class="badge" aria-hidden="true"><i class="{icon}"></i></span>
        </div>
        <div class="body">
          <h3>{title}</h3>
          <p>{body}</p>
        </div>
      </div>''' for img, icon, title, alt, body in GROUPS)

html += f'''
<main id="main">

<!-- ONE .tex band spans Veterinarians AND Management.
     They used to be two abutting .tex sections, each with its own .whobg parallaxing from its
     own origin — the stone pattern jumped ~139px at the join and read as two pages stitched
     together. A single section means a single continuous texture. -->
<section class="sec tex">
  <div class="texclip" aria-hidden="true"><div class="whobg"></div></div>
  <div class="wrap">
    <div class="rv">
      <h2 class="big">Veterinarians</h2>
      <div class="rule"></div>
      <p class="lead" style="margin-top:18px">Our caring and compassionate veterinary care team! Meet the Veterinarians &amp; Team of Cumberland Valley Veterinary Clinic in Hagerstown! We&rsquo;re pleased to provide exceptional vet care for your pets! Please call us at <a class="telinline" href="{TEL_HREF}">301-739-3121</a> to speak to one of our caring veterinary staff members!</p>
    </div>
    <div class="people rv">
{vets}
    </div>
  </div>
  <!-- one adaptive sheet per doctor; outside .wrap so no ancestor can clip or restack it -->
{sheets}

  <!-- Management + the three staff groups. Client copy, verbatim.
       Same band as Veterinarians above — .band-gap just supplies the vertical rhythm the old
       section padding used to give. -->
  <div class="wrap band-gap">
    <div class="rv">
      <h2 class="big">Management</h2>
      <div class="rule"></div>
      <div class="prose" style="margin-top:20px">
        <p>Tammy Snyder is the practice manager and Tara Martin is the business manager at Cumberland Valley Veterinary Clinic. Both have been with the practice since 1996. Together, they handle the daily operations of the clinic.</p>
      </div>
    </div>
    <!-- same .slab card as the homepage's "What Community-Based Veterinary Care Looks Like",
         with the client's real photography. The 01/02/03 number badge is replaced by the role
         icon, sitting in the same corner slot. -->
    <div class="slabgrid rv">
{groups}
    </div>
  </div>
</section>

<section class="close-cta">
  <div class="wrap inner rv">
    <h2>Come meet them.</h2>
    <p>Please call us to speak to one of our caring veterinary staff members.</p>
    <a class="phone" href="{TEL_HREF}" aria-label="Call Cumberland Valley at {TEL_DISPLAY}">{TEL_DISPLAY}</a>
  </div>
</section>

</main>
'''

html += footer()
html += script()

out = os.path.join(os.path.dirname(__file__), '..', 'team.html')
open(out, 'w').write(html)
print("wrote team.html", len(html), "bytes")
