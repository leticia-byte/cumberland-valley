import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from parts import head, topstrip, nav, footer, script, TEL_HREF, TEL_DISPLAY
from gen_team import VETS

# Three bio layouts for the SAME client copy. Not one word changes — only the arrangement.
# The current build is 3 x (365 x 955px) columns: readable measure, but a very tall skinny card,
# and the reader must commit to a full bio before seeing who else is on staff.

def paras(ps, cls=""):
    c = f' class="{cls}"' if cls else ''
    return "\n        ".join(f"<p{c}>{p}</p>" for p in ps)

# ---------------------------------------------------------------- A · Roster rows
A_ITEMS = "\n".join(f'''
      <article class="vrow">
        <div class="vrow-photo"><i class="fa-solid fa-user-doctor" aria-hidden="true"></i></div>
        <div class="vrow-body">
          <h3>{n}</h3>
          <div class="p-role">{role}</div>
          {paras(ps)}
        </div>
      </article>''' for n, role, ps in VETS)

A = f'''
<section class="sec">
  <div class="wrap">
    <div class="rv">
      <h2 class="big">Veterinarians</h2>
      <div class="rule"></div>
    </div>
    <div class="vrows rv">{A_ITEMS}
    </div>
  </div>
</section>'''

# ---------------------------------------------------------------- B · Card + expand
B_ITEMS = "\n".join(f'''
      <article class="vcard">
        <div class="p-photo"><i class="fa-solid fa-user-doctor" aria-hidden="true"></i></div>
        <div class="p-body">
          <h3>{n}</h3>
          <div class="p-role">{role}</div>
          <p class="vlede">{ps[0]}</p>
          <details class="vmore">
            <summary><span class="more-t">Read full bio</span><i class="fa-solid fa-chevron-down" aria-hidden="true"></i></summary>
            <div class="vmore-body">
              {paras(ps[1:]) if len(ps) > 1 else ''}
            </div>
          </details>
        </div>
      </article>''' for n, role, ps in VETS)

B = f'''
<section class="sec">
  <div class="wrap">
    <div class="rv">
      <h2 class="big">Veterinarians</h2>
      <div class="rule"></div>
    </div>
    <div class="vcards rv">{B_ITEMS}
    </div>
  </div>
</section>'''

# ---------------------------------------------------------------- C · Tabbed
C_TABS = "\n".join(
    f'        <button class="vtab" role="tab" id="tab{i}" aria-controls="panel{i}" '
    f'aria-selected="{"true" if i==0 else "false"}" tabindex="{0 if i==0 else -1}">'
    f'<span class="vtab-ph"><i class="fa-solid fa-user-doctor" aria-hidden="true"></i></span>'
    f'<span class="vtab-txt"><b>{n}</b><em>{role}</em></span></button>'
    for i, (n, role, ps) in enumerate(VETS))

C_PANELS = "\n".join(
    f'''      <div class="vpanel" role="tabpanel" id="panel{i}" aria-labelledby="tab{i}"{"" if i==0 else " hidden"}>
        <div class="vpanel-photo"><i class="fa-solid fa-user-doctor" aria-hidden="true"></i></div>
        <div class="vpanel-body">
          <h3>{n}</h3>
          <div class="p-role">{role}</div>
          {paras(ps)}
        </div>
      </div>''' for i, (n, role, ps) in enumerate(VETS))

C = f'''
<section class="sec">
  <div class="wrap">
    <div class="rv">
      <h2 class="big">Veterinarians</h2>
      <div class="rule"></div>
    </div>
    <div class="vtabs rv">
      <div class="vtablist" role="tablist" aria-label="Veterinarians">
{C_TABS}
      </div>
      <div class="vpanels">
{C_PANELS}
      </div>
    </div>
  </div>
</section>'''

CSS = '''
<style>
  .vhead{background:var(--navy);color:#fff;padding:120px 0 34px}
  .vhead h1{color:#fff;font-size:38px}
  .vhead p{color:#CFDCEC;margin-top:12px;max-width:74ch;font-size:16px;line-height:1.6}
  .vbar{position:sticky;top:0;z-index:40;background:#0B1E3E;border-bottom:1px solid rgba(255,255,255,.14)}
  .vbar .wrap{display:flex;gap:8px;padding:10px 28px;flex-wrap:wrap}
  .vbar a{color:#CFDCEC;text-decoration:none;font:600 13px/1 'Inter';padding:10px 14px;border-radius:999px;border:1px solid rgba(255,255,255,.24)}
  .vbar a:hover{background:rgba(255,255,255,.10);color:#fff}
  .vlabel{background:var(--blue);color:#fff;padding:18px 0}
  .vlabel .wrap{display:flex;align-items:baseline;gap:16px;flex-wrap:wrap}
  .vlabel h2{color:#fff;font-size:26px}
  .vlabel span{font:500 14px/1.5 'Inter';color:#DCEAFB;max-width:80ch}

  /* ---------- A · Roster rows ---------- */
  .vrows{display:flex;flex-direction:column;gap:22px;margin-top:36px}
  .vrow{display:grid;grid-template-columns:260px 1fr;gap:34px;align-items:start;
    background:#fff;border:1px solid rgba(13,36,77,.12);border-radius:16px;padding:26px;
    box-shadow:var(--sh-md);transition:box-shadow .35s,transform .35s cubic-bezier(.2,.8,.2,1)}
  .vrow:hover{transform:translateY(-3px);box-shadow:var(--sh-lg)}
  .vrow-photo{aspect-ratio:1/1;border-radius:12px;background:linear-gradient(160deg,#E8EEF5,#D1D2D4);
    display:flex;align-items:center;justify-content:center;color:var(--blue);font-size:46px}
  .vrow-body h3{font-size:26px;color:var(--navy)}
  .vrow-body p{font:400 15.5px/1.75 'Inter';color:#4A525C;margin-top:12px;max-width:70ch}
  @media(max-width:760px){
    .vrow{grid-template-columns:1fr;gap:20px}
    .vrow-photo{max-width:180px}
  }

  /* ---------- B · Card + expand ---------- */
  .vcards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(300px,100%),1fr));gap:24px;margin-top:36px;align-items:start}
  .vcard{background:#fff;border:1px solid rgba(13,36,77,.12);border-radius:16px;overflow:hidden;
    box-shadow:var(--sh-md);transition:box-shadow .35s}
  .vcard:hover{box-shadow:var(--sh-lg)}
  .vcard .p-photo{aspect-ratio:4/3;background:linear-gradient(160deg,#E8EEF5,#D1D2D4);
    display:flex;align-items:center;justify-content:center;color:var(--blue);font-size:44px}
  .vcard .p-body{padding:26px}
  .vcard h3{font-size:23px;color:var(--navy)}
  .vlede{font:400 15px/1.7 'Inter';color:#4A525C}
  .vmore{margin-top:14px}
  .vmore summary{list-style:none;cursor:pointer;display:inline-flex;align-items:center;gap:8px;
    font:600 14px/1 'Inter';color:var(--blue);padding:10px 0;
    /* 24px min target (WCAG 2.5.8) */
    min-height:24px}
  .vmore summary::-webkit-details-marker{display:none}
  .vmore summary i{font-size:11px;transition:transform .3s}
  .vmore[open] summary i{transform:rotate(180deg)}
  .vmore[open] .more-t::after{content:"";}
  .vmore summary:hover{text-decoration:underline}
  .vmore-body p{font:400 15px/1.7 'Inter';color:#4A525C;margin-top:12px}
  .vmore[open] summary .more-t{}

  /* ---------- C · Tabbed ---------- */
  .vtabs{margin-top:36px;display:grid;grid-template-columns:300px 1fr;gap:32px;align-items:start}
  .vtablist{display:flex;flex-direction:column;gap:10px;position:sticky;top:170px}
  .vtab{display:flex;align-items:center;gap:14px;text-align:left;cursor:pointer;
    background:#fff;border:1px solid rgba(13,36,77,.12);border-radius:14px;padding:12px;
    box-shadow:var(--sh-sm);transition:all .3s cubic-bezier(.2,.8,.2,1)}
  .vtab:hover{transform:translateX(3px);box-shadow:var(--sh-md)}
  .vtab[aria-selected="true"]{background:var(--navy);border-color:var(--navy);box-shadow:var(--sh-md)}
  .vtab-ph{width:52px;height:52px;border-radius:10px;flex:none;
    background:linear-gradient(160deg,#E8EEF5,#D1D2D4);display:flex;align-items:center;
    justify-content:center;color:var(--blue);font-size:20px}
  .vtab-txt{display:flex;flex-direction:column;gap:4px;min-width:0}
  .vtab-txt b{font-family:'DM Serif Display',Georgia,serif;font-weight:400;font-size:17px;color:var(--navy);line-height:1.2}
  .vtab-txt em{font:600 10px/1 'Inter';letter-spacing:.12em;text-transform:uppercase;color:var(--blue);font-style:normal}
  .vtab[aria-selected="true"] .vtab-txt b{color:#fff}
  .vtab[aria-selected="true"] .vtab-txt em{color:#8FBEEF}
  .vpanel{display:grid;grid-template-columns:200px 1fr;gap:28px;align-items:start;
    background:#fff;border:1px solid rgba(13,36,77,.12);border-radius:16px;padding:30px;box-shadow:var(--sh-lg)}
  .vpanel-photo{aspect-ratio:1/1;border-radius:12px;background:linear-gradient(160deg,#E8EEF5,#D1D2D4);
    display:flex;align-items:center;justify-content:center;color:var(--blue);font-size:40px}
  .vpanel-body h3{font-size:26px;color:var(--navy)}
  .vpanel-body p{font:400 15.5px/1.75 'Inter';color:#4A525C;margin-top:12px;max-width:68ch}
  @media(max-width:900px){
    .vtabs{grid-template-columns:1fr}
    .vtablist{position:static;flex-direction:row;overflow-x:auto;padding-bottom:6px}
    .vtab{flex:0 0 auto}
    .vpanel{grid-template-columns:1fr}
    .vpanel-photo{max-width:170px}
  }
</style>
'''

TABJS = '''
<script>
(function(){
  const tabs=[...document.querySelectorAll('.vtab')];
  if(!tabs.length) return;
  const panels=[...document.querySelectorAll('.vpanel')];
  const show=i=>{
    tabs.forEach((t,n)=>{
      const on = n===i;
      t.setAttribute('aria-selected',on?'true':'false');
      t.tabIndex = on?0:-1;
      panels[n].hidden=!on;
    });
  };
  tabs.forEach((t,i)=>{
    t.addEventListener('click',()=>show(i));
    /* arrow-key roving tabindex — the expected keyboard model for a tablist */
    t.addEventListener('keydown',e=>{
      const k=e.key;
      if(k!=='ArrowDown'&&k!=='ArrowUp'&&k!=='ArrowLeft'&&k!=='ArrowRight'&&k!=='Home'&&k!=='End') return;
      e.preventDefault();
      let n=i;
      if(k==='ArrowDown'||k==='ArrowRight') n=(i+1)%tabs.length;
      if(k==='ArrowUp'||k==='ArrowLeft') n=(i-1+tabs.length)%tabs.length;
      if(k==='Home') n=0;
      if(k==='End') n=tabs.length-1;
      show(n); tabs[n].focus();
    });
  });
})();
</script>
'''

html = head("Team — 3 bio layouts | Cumberland Valley",
            "Three layout options for the veterinarian bios.", extra_css=CSS)
html += '''
<header class="vhead">
  <div class="wrap">
    <h1>Veterinarian bios &mdash; three layouts</h1>
    <p>Same client copy in all three, word for word. The current build stacks three 365&times;955px columns &mdash; the measure reads fine, but it&rsquo;s a tall, thin card, and you have to scroll past a full bio to reach the next doctor. Each option below solves that differently. Nav, hero and footer are unchanged and omitted so the bios are easy to compare.</p>
  </div>
</header>
<div class="vbar">
  <div class="wrap">
    <a href="#vA">A &middot; Roster rows</a>
    <a href="#vB">B &middot; Card + expand</a>
    <a href="#vC">C &middot; Tabbed roster</a>
  </div>
</div>
<main id="main">

<div class="vlabel" id="vA"><div class="wrap"><h2>A &middot; Roster rows</h2>
  <span>One full-width row per doctor: square portrait left, bio right at a comfortable 70ch. Nothing is hidden, nothing is truncated, and you can skim the three names in one screen. The most conventional &mdash; and the kindest to long bios.</span></div></div>
''' + A + '''
<div class="vlabel" id="vB"><div class="wrap"><h2>B &middot; Card + expand</h2>
  <span>Keeps the three-up grid you have now, but only the first paragraph shows &mdash; the rest sits behind &ldquo;Read full bio&rdquo;. Cards drop from 955px to roughly 520px, so all three doctors fit on one screen. Built on native &lt;details&gt;, so it works without JavaScript and is keyboard-operable for free.</span></div></div>
''' + B + '''
<div class="vlabel" id="vC"><div class="wrap"><h2>C &middot; Tabbed roster</h2>
  <span>The three doctors live in a sticky rail; clicking one swaps the bio beside it. Compact and modern, and the whole team stays visible while you read. The trade-off: only one bio is in the DOM-visible state at a time, which is slightly weaker for SEO and for anyone who wants to Ctrl+F the page.</span></div></div>
''' + C + '''
</main>
'''
html += footer()
html += script()
html += TABJS

out = os.path.join(os.path.dirname(__file__), '..', 'cumberland-valley-team-bio-variants.html')
open(out, 'w').write(html)
print("wrote cumberland-valley-team-bio-variants.html", len(html), "bytes")
