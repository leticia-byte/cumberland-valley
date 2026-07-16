# RETIRED. This page was turned into a nav LABEL (dropdown parent) — it is not a page.
# Kept for reference only; it is no longer run by the build.
# Its children live in the nav submenu instead.
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from parts import head, topstrip, nav, pagehead, footer, script, TEL_HREF, TEL_DISPLAY

# NOTE: no client copy was supplied for this page. Everything below is either (a) lifted from
# copy already approved on the homepage, or (b) marked [VERIFY]. Nothing new is asserted as fact.

html = head(
    "About Us | Cumberland Valley Veterinary Clinic | Hagerstown, MD",
    "Cumberland Valley Veterinary Clinic is one of the last independently owned veterinary practices in Washington County, Maryland.",
)
html += topstrip()
html += nav("about.html", ondark=True)
html += pagehead(
    "About",
    "Independent, and <em>staying that way.</em>",
    "One of the last few independently owned veterinary practices in Washington County — and that's a deliberate choice, renewed every year.",
)

html += f'''
<main id="main">

<!-- This section reuses copy already approved on the homepage. Same words, longer form. -->
<section class="sec">
  <div class="wrap split">
    <div class="fig rv">
      <img src="assets/home-s2.jpg" alt="A dog rising to greet its owner at dusk">
    </div>
    <div class="rv">
      <h2 class="big">What it means to choose an independent veterinarian</h2>
      <div class="rule"></div>
      <div class="prose">
        <p>Dr. Jen Dolan has worked at Cumberland Valley Veterinary Clinic for over thirty years. In <span class="vflag">[VERIFY: YEAR]</span>, she bought the practice, and from that day forward she committed to keeping it independent. Today, Cumberland Valley is one of the last few independent veterinary practices in Washington County.</p>
        <p>Being a small business means you'll see a lot of familiar faces here. Many of our doctors, technicians, and receptionists have been at Cumberland Valley longer than Dr. Dolan has. That's part of what being privately owned means to us: continuity of care, knowing your name, knowing your pet's name, and showing up for our community year after year.</p>
      </div>
    </div>
  </div>
</section>

<!-- Team. Deliberately structural — we have no names, roles, or photos. -->
<section class="sec oat">
  <div class="wrap">
    <div class="rv">
      <h2 class="big">The people you'll actually see</h2>
      <div class="rule"></div>
      <p class="lead" style="margin-top:18px">The same faces, visit after visit. Many of our doctors, technicians and receptionists have been here longer than Dr. Dolan has.</p>
      <a class="callbtn" style="margin-top:26px" href="team.html">Meet the team <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>
    </div>
  </div>
</section>

<!-- Community. Pulls the same geographic story as the homepage map section. -->
<section class="sec">
  <div class="wrap split">
    <div class="rv">
      <h2 class="big">Rooted in Washington County</h2>
      <div class="rule"></div>
      <div class="prose">
        <p>We see families from Hagerstown, Funkstown, Williamsport, Boonsboro, Smithsburg, and Maugansville — most of them a short drive from Virginia Ave. Keeping care close to home is the whole point.</p>
        <p>If you're new to the area or new to us, call <a class="telinline" href="{TEL_HREF}">{TEL_DISPLAY}</a>. Someone here will pick up.</p>
      </div>
      <a class="callbtn" style="margin-top:26px" href="contact.html">See our hours &amp; directions <i class="fa-solid fa-arrow-right" aria-hidden="true"></i></a>
    </div>
    <div class="fig rv">
      <img src="assets/home-s3-3.jpg" alt="Cumberland Valley Veterinary Clinic staff with a patient">
    </div>
  </div>
</section>

</main>
'''

html += footer()
html += script()

out = os.path.join(os.path.dirname(__file__), '..', 'about.html')
open(out, 'w').write(html)
print("wrote about.html", len(html), "bytes")
