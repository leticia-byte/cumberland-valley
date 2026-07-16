import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from parts import head, footer, script, TEL_HREF, TEL_DISPLAY
from gen_pet_resort import SECTIONS

# Three layouts for the SAME client copy — imported from gen_pet_resort so the words can't drift
# out of sync with the live page. Only the arrangement changes.
# Current build = stacked full-width bands + a sticky jump bar.

def paras(s):
    return "\n          ".join(f"<p>{p}</p>" for p in s["paras"])

def facts(s, cls="facts"):
    if not s["facts"]: return ""
    items = "\n".join(f'''          <div class="fact">
            <div class="fact-i"><i class="{ic}" aria-hidden="true"></i></div>
            <div><div class="fact-t">{t}</div><p>{b}</p></div>
          </div>''' for ic, t, b in s["facts"])
    return f'\n        <div class="{cls}">\n{items}\n        </div>'

# Each section carries its own background ("bg"), including the navy on Feline Boarding — the
# variants honour it so the comparison matches the live page rather than quietly reverting it.
def bg_of(s):      return s.get("bg", "tex")
def band(s):       return f' {bg_of(s)}' if bg_of(s) else ''
def whobg(s):      return '<div class="texclip" aria-hidden="true"><div class="whobg"></div></div>' if bg_of(s) == "tex" else ''

# ---------------------------------------------------------------- A · Split rows
A = "\n".join(f'''
<section class="sec{band(s)} vsec">
  {whobg(s)}
  <div class="wrap">
    <div class="split{' split-flip' if i%2 else ''}">
      <div class="rv">
        <div class="pr-eyebrow"><i class="{s["icon"]}" aria-hidden="true"></i> Pet Resort</div>
        <h2 class="big">{s["h2"]}</h2>
        <div class="rule"></div>
        <p class="lead" style="margin-top:18px">{s["lede"]}</p>
        <div class="prose" style="margin-top:16px">
          {paras(s)}
        </div>
      </div>
      <div class="rv">
        <div class="factstack">{facts(s,"facts factstack-in")}
        </div>
      </div>
    </div>
  </div>
</section>''' for i, s in enumerate(SECTIONS))

# ---------------------------------------------------------------- B · Sticky rail
B_RAIL = "\n".join(
    f'        <a href="#b-{s["id"]}"><span class="r-i"><i class="{s["icon"]}" aria-hidden="true"></i></span>{s["nav"]}</a>'
    for s in SECTIONS)
B_BODY = "\n".join(f'''
      <div class="railsec" id="b-{s["id"]}">
        <h2 class="big">{s["h2"]}</h2>
        <div class="rule"></div>
        <p class="lead" style="margin-top:18px">{s["lede"]}</p>
        <div class="prose" style="margin-top:16px">
          {paras(s)}
        </div>{facts(s)}
      </div>''' for s in SECTIONS)
B = f'''
<section class="sec tex">
  <div class="texclip" aria-hidden="true"><div class="whobg"></div></div>
  <div class="wrap">
    <div class="railgrid">
      <nav class="rail" aria-label="Pet Resort services">
        <div class="rail-t">Our services</div>
{B_RAIL}
        <a class="rail-call" href="{TEL_HREF}"><i class="fa-solid fa-phone" aria-hidden="true"></i> {TEL_DISPLAY}</a>
      </nav>
      <div class="railbody rv">
{B_BODY}
      </div>
    </div>
  </div>
</section>'''

# ---------------------------------------------------------------- C · Choose-your-service cards
C_CARDS = "\n".join(f'''
      <a class="pick" href="#c-{s["id"]}">
        <div class="pick-i"><i class="{s["icon"]}" aria-hidden="true"></i></div>
        <h3>{s["h2"]}</h3>
        <p>{s["lede"][:96].rsplit(" ",1)[0]}&hellip;</p>
        <span class="pick-go">Read more <i class="fa-solid fa-arrow-down" aria-hidden="true"></i></span>
      </a>''' for s in SECTIONS)
C_SECS = "\n".join(f'''
<section class="sec{band(s)} vsec" id="c-{s["id"]}">
  {whobg(s)}
  <div class="wrap">
    <div class="rv">
      <div class="pr-eyebrow"><i class="{s["icon"]}" aria-hidden="true"></i> Pet Resort</div>
      <h2 class="big">{s["h2"]}</h2>
      <div class="rule"></div>
      <p class="lead" style="margin-top:18px">{s["lede"]}</p>
      <div class="prose" style="margin-top:16px">
        {paras(s)}
      </div>{facts(s)}
    </div>
  </div>
</section>''' for i, s in enumerate(SECTIONS))
C = f'''
<section class="sec">
  <div class="wrap">
    <div class="rv" style="text-align:center">
      <h2 class="big" style="margin:0 auto">What do you need?</h2>
      <div class="rule" style="margin:22px auto 0"></div>
    </div>
    <div class="picks rv">
{C_CARDS}
    </div>
  </div>
</section>
{C_SECS}'''

CSS = '''
<style>
  .vhead{background:var(--navy);color:#fff;padding:120px 0 34px}
  .vhead h1{color:#fff;font-size:38px}
  .vhead p{color:#CFDCEC;margin-top:12px;max-width:80ch;font-size:16px;line-height:1.6}
  .vbar{background:#0B1E3E;border-bottom:1px solid rgba(255,255,255,.14)}
  .vbar .wrap{display:flex;gap:8px;padding:10px 28px;flex-wrap:wrap}
  .vbar a{color:#CFDCEC;text-decoration:none;font:600 13px/1 'Inter';padding:10px 14px;border-radius:999px;border:1px solid rgba(255,255,255,.24)}
  .vbar a:hover{background:rgba(255,255,255,.10);color:#fff}
  .vlabel{background:var(--blue);color:#fff;padding:18px 0}
  .vlabel .wrap{display:flex;align-items:baseline;gap:16px;flex-wrap:wrap}
  .vlabel h2{color:#fff;font-size:26px}
  .vlabel span{font:500 14px/1.5 'Inter';color:#DCEAFB;max-width:88ch}
  .vsec{padding:74px 0}

  .pr-eyebrow{font:600 11px/1 'Inter';letter-spacing:.18em;text-transform:uppercase;
    color:var(--blue);margin-bottom:14px;display:inline-flex;align-items:center;gap:9px}
  .pr-eyebrow i{font-size:14px}
  .facts{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(280px,100%),1fr));gap:18px;margin-top:34px}
  .facts .fact:only-child{max-width:520px}
  .fact{display:flex;gap:14px;align-items:flex-start;background:#fff;border:1px solid rgba(13,36,77,.12);
    border-radius:14px;padding:20px;box-shadow:var(--sh-sm);
    transition:transform .3s cubic-bezier(.2,.8,.2,1),box-shadow .3s}
  .fact:hover{transform:translateY(-3px);box-shadow:var(--sh-md)}
  .fact-i{width:40px;height:40px;border-radius:10px;flex:none;background:rgba(22,82,155,.10);
    color:var(--blue);display:flex;align-items:center;justify-content:center;font-size:16px}
  .fact-t{font:700 14px/1.3 'Inter';color:var(--navy);margin-bottom:5px}
  .fact p{font:400 14px/1.6 'Inter';color:#4A525C}

  /* ---------- A · split rows: facts become a vertical stack beside the copy ---------- */
  .factstack-in{grid-template-columns:1fr !important;margin-top:0 !important}
  .factstack .fact:only-child{max-width:none}

  /* ---------- B · sticky rail ---------- */
  .railgrid{display:grid;grid-template-columns:250px 1fr;gap:56px;align-items:start}
  .rail{position:sticky;top:190px;display:flex;flex-direction:column;gap:8px}
  .rail-t{font:600 11px/1 'Inter';letter-spacing:.16em;text-transform:uppercase;color:#5A626C;margin-bottom:8px}
  .rail a{display:flex;align-items:center;gap:12px;text-decoration:none;color:var(--navy);
    font:600 15px/1.2 'Inter';padding:12px 14px;border-radius:12px;border:1px solid rgba(13,36,77,.12);
    background:#fff;box-shadow:var(--sh-sm);transition:all .3s cubic-bezier(.2,.8,.2,1)}
  .rail a:hover{transform:translateX(3px);box-shadow:var(--sh-md);border-color:var(--blue)}
  .r-i{width:32px;height:32px;border-radius:8px;flex:none;background:rgba(22,82,155,.10);color:var(--blue);
    display:flex;align-items:center;justify-content:center;font-size:14px}
  .rail-call{margin-top:12px;justify-content:center;background:var(--blue) !important;color:#fff !important;
    border-color:var(--blue) !important}
  .rail-call:hover{background:#1A61B8 !important}
  .railsec{scroll-margin-top:200px}
  .railsec + .railsec{margin-top:64px;padding-top:56px;border-top:1px solid rgba(13,36,77,.12)}
  @media(max-width:900px){
    .railgrid{grid-template-columns:1fr;gap:32px}
    .rail{position:static;flex-direction:row;overflow-x:auto;padding-bottom:6px}
    .rail-t{display:none}
    .rail a{flex:0 0 auto}
  }

  /* ---------- C · pick cards ---------- */
  .picks{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(260px,100%),1fr));gap:22px;margin-top:38px}
  .pick{background:#fff;border:1px solid rgba(13,36,77,.12);border-radius:16px;padding:30px;
    text-decoration:none;display:flex;flex-direction:column;gap:12px;box-shadow:var(--sh-md);
    transition:transform .35s cubic-bezier(.2,.8,.2,1),box-shadow .35s}
  .pick:hover{transform:translateY(-5px);box-shadow:var(--sh-lg)}
  .pick-i{width:54px;height:54px;border-radius:13px;background:rgba(22,82,155,.10);color:var(--blue);
    display:flex;align-items:center;justify-content:center;font-size:22px}
  .pick h3{font-size:21px;color:var(--navy)}
  .pick p{font:400 14.5px/1.6 'Inter';color:#4A525C;flex:1}
  .pick-go{font:600 13px/1 'Inter';color:var(--blue);display:inline-flex;align-items:center;gap:8px}
  .pick:hover .pick-go i{transform:translateY(2px)}
  .pick-go i{transition:transform .25s;font-size:11px}
  .sec[id]{scroll-margin-top:150px}
  @media(max-width:900px){.split .factstack{margin-top:8px}}
</style>
'''

html = head("Pet Resort — 3 layouts | Cumberland Valley",
            "Three layout options for the Pet Resort page.", extra_css=CSS)
html += '''
<header class="vhead">
  <div class="wrap">
    <h1>Pet Resort &mdash; three layouts</h1>
    <p>Same client copy in all three, word for word &mdash; imported from the live page so it can&rsquo;t drift. The current build is full-width stacked bands with a sticky jump bar. Each option below organises the same three services differently. Nav, hero and footer omitted so the body is easy to compare.</p>
  </div>
</header>
<div class="vbar">
  <div class="wrap">
    <a href="#va">A &middot; Split rows</a>
    <a href="#vb">B &middot; Sticky rail</a>
    <a href="#vc">C &middot; Pick your service</a>
  </div>
</div>
<main id="main">

<div class="vlabel" id="va"><div class="wrap"><h2>A &middot; Split rows</h2>
  <span>Each service is one row: the story on one side, the practical facts stacked on the other, alternating sides down the page. The prose and the &ldquo;what do I need to know before I call&rdquo; details sit side by side instead of one under the other &mdash; so the page is shorter and no jump bar is needed.</span></div></div>
''' + A + '''

<div class="vlabel" id="vb"><div class="wrap"><h2>B &middot; Sticky rail</h2>
  <span>The three services pin to the left while the content scrolls past on the right, with the phone number always in the rail. You can see the whole offering at every moment &mdash; useful here, because someone boarding a cat and someone booking daycare are different people arriving on the same page.</span></div></div>
''' + B + '''

<div class="vlabel" id="vc"><div class="wrap"><h2>C &middot; Pick your service</h2>
  <span>Opens with three cards &mdash; dog boarding, cat boarding, daycare &mdash; that jump to the detail below. Front-loads the choice rather than making people scroll to find their animal. The strongest fit if most visitors arrive already knowing what they want.</span></div></div>
''' + C + '''

</main>
'''
html += footer()
html += script()

out = os.path.join(os.path.dirname(__file__), '..', 'cumberland-valley-pet-resort-layout-variants.html')
open(out, 'w').write(html)
print("wrote cumberland-valley-pet-resort-layout-variants.html", len(html), "bytes")
