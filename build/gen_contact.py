import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from parts import head, topstrip, nav, pagehead, footer, script, HOURS, MAPS_URL, TEL_HREF, TEL_DISPLAY, grouped_hours

# Grouped rows: Mon–Fri / Sat / Sun instead of seven near-identical lines.
rows = []
for label, txt, days in grouped_hours():
    cls = ' class="closed"' if txt == "Closed" else ''
    rows.append(f'      <tr{cls} data-days="{",".join(days)}"><th scope="row">{label}</th><td>{txt}</td></tr>')
hours_rows = "\n".join(rows)

SCHEMA = '''
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "VeterinaryCare",
  "name": "Cumberland Valley Veterinary Clinic & Pet Resort",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "17747 Virginia Ave.",
    "addressLocality": "Hagerstown",
    "addressRegion": "MD",
    "postalCode": "21740",
    "addressCountry": "US"
  },
  "telephone": "+1-301-739-3121",
  "url": "https://cumberlandvalleyvets.com/contact",
  "openingHoursSpecification": [
    { "@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday","Tuesday","Wednesday","Thursday","Friday"], "opens": "07:00", "closes": "17:00" },
    { "@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "07:30", "closes": "13:00" },
    { "@type": "OpeningHoursSpecification", "dayOfWeek": "Sunday", "opens": "00:00", "closes": "00:00" }
  ]
}
</script>
'''

html = head(
    "Contact Us | Cumberland Valley Veterinary Clinic | Hagerstown, MD",
    "Cumberland Valley Veterinary Clinic, 17747 Virginia Ave., Hagerstown, MD 21740. Call (301) 739-3121. Open Monday through Saturday.",
    schema=SCHEMA,
)
html += topstrip()
html += nav("contact.html", ondark=True)
html += pagehead(
    None,                       # kicker removed — the h1 already says where you are
    "Come see us on <em>Virginia Ave.</em>",
    "We answer the phone. No portal, no booking form, no phone tree — call and you'll reach someone in Hagerstown who knows the practice.",
    photo="building-img",
)

html += f'''
<main id="main">

<!-- .tex = oat + parallax stone texture, matching the homepage's "Comprehensive Veterinary
     Services in Hagerstown, MD" section. -->
<section class="sec tex">
  <div class="texclip" aria-hidden="true"><div class="whobg"></div></div>
  <div class="wrap cgrid">

    <div>
      <div class="infocard rv">
        <h2>Contact Us</h2>
        <div class="ic-sub">One location, serving Washington County.</div>

        <div class="ic-row">
          <i class="fa-solid fa-location-dot" aria-hidden="true"></i>
          <div>
            <div class="lbl">Address</div>
            <a href="{MAPS_URL}" target="_blank" rel="noopener">17747 Virginia Ave.<br>Hagerstown, Maryland, 21740</a>
          </div>
        </div>

        <div class="ic-row">
          <i class="fa-solid fa-phone" aria-hidden="true"></i>
          <div>
            <div class="lbl">Phone</div>
            <a href="{TEL_HREF}" aria-label="Call Cumberland Valley at {TEL_DISPLAY}">301-739-3121</a>
          </div>
        </div>

        <div class="ic-row">
          <i class="fa-solid fa-car" aria-hidden="true"></i>
          <div>
            <div class="lbl">Getting here</div>
            <a href="{MAPS_URL}" target="_blank" rel="noopener">Open directions in Google Maps</a>
          </div>
        </div>

        <a class="callbtn" style="margin-top:24px" href="{TEL_HREF}" aria-label="Call Cumberland Valley at {TEL_DISPLAY}"><i class="fa-solid fa-phone" aria-hidden="true"></i> Call {TEL_DISPLAY}</a>
      </div>

      <div class="infocard rv">
        <h2 id="hours">Clinic hours</h2>
        <div class="ic-sub">Times shown are Hagerstown local time.</div>
        <!-- Live open/closed status. The table below is the accessible source of truth
             (real <th> row headers); this pill just answers "are they open right now". -->
        <div class="hoursbox light" id="hoursbox-contact" style="min-width:0;margin-bottom:6px">
          <div class="hb-head" style="margin-bottom:0">
            <span class="hb-status" id="hbStatus-contact"><span class="dot"></span><span class="t">Hours</span></span>
          </div>
        </div>
        <table class="hourstable">
          <caption class="sr-only">Cumberland Valley Veterinary Clinic opening hours by day of the week</caption>
          <tbody>
{hours_rows}
          </tbody>
        </table>
        <p class="hours-note">Our Pet Resort keeps its own schedule for boarding drop-offs and pickups. Call {TEL_DISPLAY} to arrange a time.</p>
      </div>
    </div>

    <div class="rv">
      <div class="mapframe">
        <iframe
          title="Map showing Cumberland Valley Veterinary Clinic at 17747 Virginia Ave., Hagerstown, Maryland"
          src="https://www.google.com/maps?q=17747+Virginia+Ave,+Hagerstown,+MD+21740&output=embed"
          loading="lazy" referrerpolicy="no-referrer-when-downgrade"></iframe>
      </div>

      <div class="infocard rv" style="margin-top:24px">
        <h2>Something's wrong today?</h2>
        <div class="ic-sub">Same-day and urgent visits</div>
        <div class="prose">
          <p>If your pet needs to be seen and it can't wait, call us first at <a class="telinline" href="{TEL_HREF}">{TEL_DISPLAY}</a>. We keep time in the schedule for the days that don't go as planned.</p>
          <p>Outside our hours, contact your nearest emergency veterinary hospital.</p>
        </div>
      </div>
    </div>

  </div>
</section>

</main>
'''

# No footer on this page — requested. The footer's only job is the NAP block, and this page
# already carries the address, phone and map as its actual content; repeating it below would
# be the same information twice on one screen.
html += script()

# highlight today's row in the hours table, on the clinic's clock
html = html.replace('</body>', '''<script>
(function(){
  /* mark today's ROW RANGE in the hours table — same clinic-clock rule as the header widget */
  var d;
  try{ d=new Date(new Date().toLocaleString('en-US',{timeZone:'America/New_York'})); }catch(e){ d=new Date(); }
  var names=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday'];
  var today=names[d.getDay()];
  document.querySelectorAll('.hourstable tr').forEach(function(r){
    if((r.dataset.days||'').split(',').indexOf(today)>-1) r.classList.add('today');
  });
})();
</script>
</body>''')

out = os.path.join(os.path.dirname(__file__), '..', 'contact.html')
open(out, 'w').write(html)
print("wrote contact.html", len(html), "bytes")
