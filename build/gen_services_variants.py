import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from parts import head, topstrip, nav, footer, script, TEL_HREF, TEL_DISPLAY
from gen_services import OFFER, ADDITIONAL

# Three layouts for the SAME client copy. Not one word changes between them — only the
# arrangement. Each is shown in full so the rhythm can be judged, not just the idea.

def ticks(cls="ticks"):
    return "\n".join(
        f'        <li><i class="fa-solid fa-check" aria-hidden="true"></i><span>{t}</span></li>' for t in OFFER)

def pills():
    return "\n".join(
        f'        <div class="pill-item"><i class="{ic}" aria-hidden="true"></i><span>{n}</span></div>'
        for n, ic in ADDITIONAL)

INTRO_1 = "At Cumberland Valley Veterinary Clinic your pet's health and vitality is our number one concern. We believe the best medicine is preventative and we always take time to educate our clients and to provide them with the best approach to their pet's health."
INTRO_2 = "Using state-of-the-art equipment, keeping abreast of advances and technologies and our kind, caring attitude is what separates us from the rest. We believe that pets are full members of your family, and should be treated as such."

# ---------------------------------------------------------------- A
A = f'''
<section class="sec">
  <div class="wrap split">
    <div class="rv">
      <h2 class="big">Your pet's health and vitality is our number one concern</h2>
      <div class="rule"></div>
      <div class="prose">
        <p>{INTRO_1}</p>
        <p>{INTRO_2}</p>
      </div>
      <a class="callbtn" style="margin-top:28px" href="{TEL_HREF}"><i class="fa-solid fa-phone" aria-hidden="true"></i> Call {TEL_DISPLAY}</a>
    </div>
    <div class="fig rv"><img src="assets/home-s3-1.jpg" alt="A veterinarian examining a dog"></div>
  </div>
</section>
<section class="sec oat">
  <div class="wrap split">
    <div class="rv">
      <h2 class="big">Services we offer</h2>
      <div class="rule"></div>
      <ul class="ticks">
{ticks()}
      </ul>
    </div>
    <div class="fig rv"><img src="assets/home-s3-2.jpg" alt="A technician caring for a patient"></div>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="rv">
      <h2 class="big">Additional services</h2>
      <div class="rule"></div>
      <p class="lead" style="margin-top:18px">Everything below happens under one roof on Virginia Ave.</p>
    </div>
    <div class="pills rv">
{pills()}
    </div>
  </div>
</section>
'''

# ---------------------------------------------------------------- B
B = f'''
<section class="sec">
  <div class="wrap narrow" style="text-align:center">
    <h2 class="big" style="margin:0 auto">Your pet's health and vitality is our number one concern</h2>
    <div class="rule" style="margin:22px auto"></div>
    <div class="prose vB-prose">
      <p>{INTRO_1}</p>
      <p>{INTRO_2}</p>
    </div>
  </div>
</section>
<section class="sec oat vB-offer">
  <div class="wrap">
    <div class="rv" style="text-align:center">
      <h2 class="big" style="margin:0 auto">Services we offer</h2>
      <div class="rule" style="margin:22px auto 0"></div>
    </div>
    <ul class="ticks vB-grid rv">
{ticks()}
    </ul>
  </div>
</section>
<section class="sec">
  <div class="wrap">
    <div class="rv" style="text-align:center">
      <h2 class="big" style="margin:0 auto">Additional services</h2>
      <div class="rule" style="margin:22px auto 0"></div>
    </div>
    <div class="pills rv">
{pills()}
    </div>
  </div>
</section>
'''

# ---------------------------------------------------------------- C
C = f'''
<section class="sec vC-intro">
  <div class="wrap vC-grid">
    <div class="vC-sticky rv">
      <h2 class="big">Your pet's health and vitality is our number one concern</h2>
      <div class="rule"></div>
      <a class="callbtn" style="margin-top:24px" href="{TEL_HREF}"><i class="fa-solid fa-phone" aria-hidden="true"></i> Call {TEL_DISPLAY}</a>
    </div>
    <div class="vC-flow rv">
      <div class="prose">
        <p class="vC-drop">{INTRO_1}</p>
        <p>{INTRO_2}</p>
      </div>
      <h3 class="vC-sub">Services we offer</h3>
      <ul class="ticks">
{ticks()}
      </ul>
      <h3 class="vC-sub">Additional services</h3>
      <div class="pills" style="margin-top:20px">
{pills()}
      </div>
    </div>
  </div>
</section>
'''

CSS = '''
<style>
  /* ---- shared to the comparison page only ---- */
  .vhead{background:var(--navy);color:#fff;padding:120px 0 34px}
  .vhead h1{color:#fff;font-size:38px}
  .vhead p{color:#CFDCEC;margin-top:12px;max-width:70ch;font-size:16px;line-height:1.6}
  .vbar{position:sticky;top:0;z-index:40;background:#0B1E3E;border-bottom:1px solid rgba(255,255,255,.14)}
  .vbar .wrap{display:flex;gap:8px;padding-top:10px;padding-bottom:10px;flex-wrap:wrap}
  .vbar a{color:#CFDCEC;text-decoration:none;font:600 13px/1 'Inter';padding:10px 14px;border-radius:999px;border:1px solid rgba(255,255,255,.24)}
  .vbar a:hover{background:rgba(255,255,255,.10);color:#fff}
  .vlabel{background:var(--blue);color:#fff;padding:18px 0}
  .vlabel .wrap{display:flex;align-items:baseline;gap:16px;flex-wrap:wrap}
  .vlabel h2{color:#fff;font-size:26px}
  .vlabel span{font:500 14px/1.5 'Inter';color:#DCEAFB}

  /* ---- B: centred, single column ---- */
  .vB-prose{margin:0 auto}
  .vB-prose p{margin-left:auto;margin-right:auto}
  .vB-grid{margin-top:40px;display:grid;grid-template-columns:repeat(auto-fit,minmax(min(300px,100%),1fr));
    gap:14px 40px;max-width:900px;margin-left:auto;margin-right:auto}

  /* ---- C: sticky rail + one continuous column ---- */
  .vC-grid{display:grid;grid-template-columns:minmax(0,.85fr) minmax(0,1.15fr);gap:64px;align-items:start}
  .vC-sticky{position:sticky;top:170px}
  .vC-sub{font-size:26px;color:var(--navy);margin-top:44px}
  .vC-flow .ticks{margin-top:20px}
  /* a real drop cap — the one place a display serif earns its keep in body copy */
  .vC-drop::first-letter{float:left;font-family:'DM Serif Display',Georgia,serif;font-size:62px;
    line-height:.86;padding:4px 10px 0 0;color:var(--blue)}
  @media(max-width:900px){
    .vC-grid{grid-template-columns:1fr;gap:30px}
    .vC-sticky{position:static}
  }
</style>
'''

html = head("Services — 3 body-copy layouts | Cumberland Valley",
            "Three layout options for the Services page body copy.", extra_css=CSS)
html += '''
<header class="vhead">
  <div class="wrap">
    <h1>Services &mdash; three body-copy layouts</h1>
    <p>Same client copy in all three, word for word. Only the arrangement changes. The hero, nav and footer are unchanged and omitted here so the body is easy to compare.</p>
  </div>
</header>
<div class="vbar">
  <div class="wrap">
    <a href="#vA">A &middot; Alternating</a>
    <a href="#vB">B &middot; Centred column</a>
    <a href="#vC">C &middot; Sticky rail</a>
  </div>
</div>
<main id="main">

<div class="vlabel" id="vA"><div class="wrap"><h2>A &middot; Alternating</h2>
  <span>Current build. Copy and photo trade sides down the page; Additional Services opens to full width. Familiar, photo-led, and the safest fit with the homepage rhythm.</span></div></div>
''' + A + '''
<div class="vlabel" id="vB"><div class="wrap"><h2>B &middot; Centred column</h2>
  <span>No photos. The copy runs down a narrow centred measure, and the nine offers break into a calm multi-column list. Reads like a statement of intent &mdash; and it&rsquo;s the honest option while the photography is still placeholder.</span></div></div>
''' + B + '''
<div class="vlabel" id="vC"><div class="wrap"><h2>C &middot; Sticky rail</h2>
  <span>The heading and CTA pin to the left while every service scrolls past on the right. One continuous read instead of three stops, and the phone number stays on screen the whole way down.</span></div></div>
''' + C + '''
</main>
'''
html += footer()
html += script()

out = os.path.join(os.path.dirname(__file__), '..', 'cumberland-valley-services-layout-variants.html')
open(out, 'w').write(html)
print("wrote cumberland-valley-services-layout-variants.html", len(html), "bytes")
