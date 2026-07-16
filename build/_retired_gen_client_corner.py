# RETIRED. This page was turned into a nav LABEL (dropdown parent) — it is not a page.
# Kept for reference only; it is no longer run by the build.
# Its children live in the nav submenu instead.
import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from parts import head, topstrip, nav, pagehead, footer, script, TEL_HREF, TEL_DISPLAY, PHARMACY_URL, PETSITES_URL

# The two real destinations supplied by the client (VetSource pharmacy, PetSites login) are now
# wired. The rest are still [VERIFY] — linking a pet owner to a form that doesn't exist is worse
# than not linking at all, so those CTAs stay inert until confirmed.
# (icon, title, body, cta label, href or None, flag or None)
CARDS = [
    ("fa-solid fa-file-signature", "New Patient Forms",
     "Save time at your first visit by filling out your paperwork before you arrive.",
     "Download forms", None, "[VERIFY: do these forms exist? Jotform, PDF, or paper-only?]"),
    ("fa-solid fa-calendar-check", "Request an Appointment",
     "Call and you'll reach someone in Hagerstown. No portal, no phone tree.",
     "Call " + TEL_DISPLAY, TEL_HREF, None),
    ("fa-solid fa-prescription-bottle-medical", "Online Pharmacy",
     "Refill prescriptions and have food and medication delivered to your door through our VetSource home delivery store.",
     "Visit the pharmacy", PHARMACY_URL, None),
    ("fa-solid fa-right-to-bracket", "PetSites Login",
     "Sign in to PetSites to view your pet's records, reminders and appointment history.",
     "Go to PetSites", PETSITES_URL, None),
    ("fa-solid fa-credit-card", "Payment Options",
     "What we accept, and how to plan for the cost of care.",
     "See payment options", None, "[VERIFY: accepted cards, CareCredit/Scratchpay?, deposit policy]"),
    ("fa-solid fa-folder-open", "Medical Records",
     "Request your pet's records, or have them sent to a specialist.",
     "Request records", None, "[VERIFY: process — email, form, phone?]"),
    ("fa-solid fa-circle-question", "Common Questions",
     "Hours, boarding, urgent visits, and what to expect at your first appointment.",
     "Read the FAQ", None, "[VERIFY: point at homepage #faq, or build a standalone FAQ page?]"),
]

def card(icon, title, body, cta, href, flag):
    ext = bool(href) and href.startswith(("http://", "https://"))
    attrs = ' target="_blank" rel="noopener"' if ext else ''
    # external links announce themselves rather than silently stealing the tab
    xicon = ' <i class="fa-solid fa-arrow-up-right-from-square xicon" aria-hidden="true"></i>' if ext else ' <i class="fa-solid fa-arrow-right" aria-hidden="true"></i>'
    sr = ' <span class="sr-only">(opens in a new tab)</span>' if ext else ''
    f = f'<p><span class="vflag">{flag}</span></p>' if flag else ''
    link = (f'<a class="go" href="{href}"{attrs}>{cta}{xicon}{sr}</a>' if href
            else f'<span class="go go-off">{cta}{xicon}</span>')
    return f'''      <div class="ccard">
        <div class="ci"><i class="{icon}" aria-hidden="true"></i></div>
        <h3>{title}</h3>
        <p>{body}</p>
        {f}
        {link}
      </div>'''

html = head(
    "Client Corner | Cumberland Valley Veterinary Clinic | Hagerstown, MD",
    "Forms, prescriptions, payment options and records for Cumberland Valley Veterinary Clinic clients in Hagerstown, MD.",
)
html += topstrip()
html += nav("client-corner.html", ondark=True)
html += pagehead(
    "Client Corner",
    "Everything you need, <em>in one place.</em>",
    "Forms, refills, records, and the answers to the questions we get asked most.",
)

cards = "\n".join(card(*c) for c in CARDS)

html += f'''
<main id="main">

<section class="sec">
  <div class="wrap">
    <div class="rv">
      <h2 class="big">Client resources</h2>
      <div class="rule"></div>
      <p class="lead" style="margin-top:18px">If you can't find what you need here, call <a class="telinline" href="{TEL_HREF}">{TEL_DISPLAY}</a>. We'd rather talk to you than have you hunt through a website.</p>
    </div>
    <div class="ccards rv">
{cards}
    </div>
  </div>
</section>

<section class="sec navy">
  <div class="wrap" style="text-align:center">
    <h2 class="big" style="margin:0 auto">New to Cumberland Valley?</h2>
    <p class="lead" style="margin:18px auto 0;text-align:center">We're taking new patients. Call and we'll get your pet on the schedule and answer anything you want to ask first.</p>
    <a class="callbtn" style="margin-top:30px" href="{TEL_HREF}" aria-label="Call Cumberland Valley at {TEL_DISPLAY}"><i class="fa-solid fa-phone" aria-hidden="true"></i> Call {TEL_DISPLAY}</a>
  </div>
</section>

</main>
'''

html += footer()
html += script()

out = os.path.join(os.path.dirname(__file__), '..', 'client-corner.html')
open(out, 'w').write(html)
print("wrote client-corner.html", len(html), "bytes")
