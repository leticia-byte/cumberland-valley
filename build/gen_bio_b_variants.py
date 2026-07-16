import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from parts import head, topstrip, nav, footer, script, TEL_HREF, TEL_DISPLAY
from gen_team import VETS

# Three takes on "B · Card + expand". Same client copy in all three, word for word.
# Only the disclosure mechanic changes.

def ps(items):
    return "\n            ".join(f"<p>{x}</p>" for x in items)


# ---------------------------------------------------------------- B1 · Inline reveal
B1 = "\n".join(f'''
      <article class="vcard">
        <div class="p-photo"><i class="fa-solid fa-user-doctor" aria-hidden="true"></i></div>
        <div class="p-body">
          <h3>{n}</h3>
          <div class="p-role">{role}</div>
          <p class="vlede">{p[0]}</p>
          <details class="vmore">
            <summary><span>Read full bio</span><i class="fa-solid fa-chevron-down" aria-hidden="true"></i></summary>
            <div class="vmore-body">
            {ps(p[1:])}
            </div>
          </details>
        </div>
      </article>''' for n, role, p in VETS)

# ---------------------------------------------------------------- B2 · Full-width drawer
B2_CARDS = "\n".join(f'''
      <article class="dcard" data-i="{i}">
        <div class="p-photo"><i class="fa-solid fa-user-doctor" aria-hidden="true"></i></div>
        <div class="p-body">
          <h3>{n}</h3>
          <div class="p-role">{role}</div>
          <p class="vlede">{p[0]}</p>
          <button class="dbtn" type="button" aria-expanded="false" aria-controls="drawer{i}">
            <span>Read full bio</span><i class="fa-solid fa-chevron-down" aria-hidden="true"></i>
          </button>
        </div>
      </article>''' for i, (n, role, p) in enumerate(VETS))

B2_DRAWERS = "\n".join(f'''
      <div class="drawerpanel" id="drawer{i}" hidden>
        <div class="dp-inner">
          <div class="dp-photo"><i class="fa-solid fa-user-doctor" aria-hidden="true"></i></div>
          <div class="dp-body">
            <h3>{n}</h3>
            <div class="p-role">{role}</div>
            {ps(p)}
          </div>
          <button class="dp-close" type="button" aria-label="Close bio"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button>
        </div>
      </div>''' for i, (n, role, p) in enumerate(VETS))

# ---------------------------------------------------------------- B3 · Dialog
B3_CARDS = "\n".join(f'''
      <article class="vcard">
        <div class="p-photo"><i class="fa-solid fa-user-doctor" aria-hidden="true"></i></div>
        <div class="p-body">
          <h3>{n}</h3>
          <div class="p-role">{role}</div>
          <p class="vlede">{p[0]}</p>
          <button class="mbtn" type="button" data-dlg="dlg{i}">
            <span>Read full bio</span><i class="fa-solid fa-arrow-right" aria-hidden="true"></i>
          </button>
        </div>
      </article>''' for i, (n, role, p) in enumerate(VETS))

B3_DIALOGS = "\n".join(f'''
    <dialog class="bio-dlg" id="dlg{i}" aria-labelledby="dlgh{i}">
      <button class="dlg-close" type="button" aria-label="Close"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button>
      <div class="dlg-photo"><i class="fa-solid fa-user-doctor" aria-hidden="true"></i></div>
      <div class="dlg-body">
        <h3 id="dlgh{i}">{n}</h3>
        <div class="p-role">{role}</div>
        {ps(p)}
        <a class="callbtn" style="margin-top:22px" href="{TEL_HREF}"><i class="fa-solid fa-phone" aria-hidden="true"></i> Call {TEL_DISPLAY}</a>
      </div>
    </dialog>''' for i, (n, role, p) in enumerate(VETS))

CSS = '''
<style>
  .vhead{background:var(--navy);color:#fff;padding:120px 0 34px}
  .vhead h1{color:#fff;font-size:38px}
  .vhead p{color:#CFDCEC;margin-top:12px;max-width:76ch;font-size:16px;line-height:1.6}
  .vbar{position:sticky;top:0;z-index:40;background:#0B1E3E;border-bottom:1px solid rgba(255,255,255,.14)}
  .vbar .wrap{display:flex;gap:8px;padding:10px 28px;flex-wrap:wrap}
  .vbar a{color:#CFDCEC;text-decoration:none;font:600 13px/1 'Inter';padding:10px 14px;border-radius:999px;border:1px solid rgba(255,255,255,.24)}
  .vbar a:hover{background:rgba(255,255,255,.10);color:#fff}
  .vlabel{background:var(--blue);color:#fff;padding:18px 0}
  .vlabel .wrap{display:flex;align-items:baseline;gap:16px;flex-wrap:wrap}
  .vlabel h2{color:#fff;font-size:26px}
  .vlabel span{font:500 14px/1.5 'Inter';color:#DCEAFB;max-width:84ch}

  /* shared card shell */
  .vcards,.dcards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(300px,100%),1fr));
    gap:24px;margin-top:36px;align-items:start}
  .vcard,.dcard{background:#fff;border:1px solid rgba(13,36,77,.12);border-radius:16px;overflow:hidden;
    box-shadow:var(--sh-md);transition:box-shadow .35s}
  .vcard:hover,.dcard:hover{box-shadow:var(--sh-lg)}
  .vcard .p-photo,.dcard .p-photo{aspect-ratio:4/3;background:linear-gradient(160deg,#E8EEF5,#D1D2D4);
    display:flex;align-items:center;justify-content:center;color:var(--blue);font-size:44px}
  .vcard .p-body,.dcard .p-body{padding:26px}
  .vcard h3,.dcard h3{font-size:23px;color:var(--navy)}
  .vlede{font:400 15px/1.7 'Inter';color:#4A525C}

  /* ---------- B1 · inline reveal ---------- */
  .vmore{margin-top:12px}
  .vmore summary{list-style:none;cursor:pointer;display:inline-flex;align-items:center;gap:8px;
    font:600 14px/1 'Inter';color:var(--blue);padding:11px 0;min-height:24px}
  .vmore summary::-webkit-details-marker{display:none}
  .vmore summary:hover{text-decoration:underline}
  .vmore summary i{font-size:11px;transition:transform .3s}
  .vmore[open] summary i{transform:rotate(180deg)}
  .vmore[open] summary span::after{content:" (hide)";font-weight:500;opacity:.7}
  .vmore-body p{font:400 15px/1.7 'Inter';color:#4A525C;margin-top:12px}

  /* ---------- B2 · full-width drawer ---------- */
  .dbtn{background:transparent;border:0;padding:11px 0;cursor:pointer;
    display:inline-flex;align-items:center;gap:8px;font:600 14px/1 'Inter';color:var(--blue);min-height:24px}
  .dbtn:hover{text-decoration:underline}
  .dbtn i{font-size:11px;transition:transform .3s}
  .dbtn[aria-expanded="true"] i{transform:rotate(180deg)}
  .dcard.active{border-color:var(--blue);box-shadow:var(--sh-lg)}
  .drawerwrap{margin-top:24px}
  .drawerpanel{background:#fff;border:1px solid rgba(13,36,77,.14);border-radius:16px;
    box-shadow:var(--sh-lg);overflow:hidden;position:relative;
    animation:dOpen .4s cubic-bezier(.2,.8,.2,1)}
  @keyframes dOpen{from{opacity:0;transform:translateY(-8px)}to{opacity:1;transform:none}}
  @media (prefers-reduced-motion: reduce){.drawerpanel{animation:none}}
  .dp-inner{display:grid;grid-template-columns:190px 1fr;gap:30px;padding:30px;align-items:start}
  .dp-photo{aspect-ratio:1/1;border-radius:12px;background:linear-gradient(160deg,#E8EEF5,#D1D2D4);
    display:flex;align-items:center;justify-content:center;color:var(--blue);font-size:40px}
  .dp-body h3{font-size:26px;color:var(--navy)}
  .dp-body p{font:400 15.5px/1.75 'Inter';color:#4A525C;margin-top:12px;max-width:70ch}
  .dp-close{position:absolute;right:14px;top:14px;width:38px;height:38px;border-radius:50%;
    background:var(--oat);border:1px solid rgba(13,36,77,.14);cursor:pointer;color:var(--navy);
    display:flex;align-items:center;justify-content:center}
  .dp-close:hover{background:#E6E1D5}
  @media(max-width:760px){.dp-inner{grid-template-columns:1fr;gap:20px}.dp-photo{max-width:150px}}

  /* ---------- B3 · dialog ---------- */
  .mbtn{background:var(--blue);border:0;color:#fff;cursor:pointer;margin-top:14px;
    padding:12px 18px;border-radius:999px;font:600 14px/1 'Inter';
    display:inline-flex;align-items:center;gap:9px;box-shadow:var(--sh-sm);
    transition:transform .25s,background .25s,box-shadow .25s}
  .mbtn:hover{transform:translateY(-2px);background:#1A61B8;box-shadow:var(--sh-md)}
  .mbtn i{font-size:11px}
  .bio-dlg{border:0;border-radius:18px;padding:0;max-width:760px;width:calc(100% - 40px);
    box-shadow:0 40px 90px -20px rgba(3,10,24,.65);overflow:visible}
  .bio-dlg::backdrop{background:rgba(9,26,56,.62)}
  .bio-dlg{display:grid;grid-template-columns:200px 1fr;gap:30px;padding:34px}
  .bio-dlg:not([open]){display:none}
  .dlg-photo{aspect-ratio:1/1;border-radius:12px;background:linear-gradient(160deg,#E8EEF5,#D1D2D4);
    display:flex;align-items:center;justify-content:center;color:var(--blue);font-size:40px}
  .dlg-body{max-height:64vh;overflow-y:auto;padding-right:6px}
  .dlg-body h3{font-size:28px;color:var(--navy)}
  .dlg-body p{font:400 15.5px/1.75 'Inter';color:#4A525C;margin-top:12px}
  .dlg-close{position:absolute;right:-10px;top:-10px;width:40px;height:40px;border-radius:50%;
    background:#fff;border:1px solid rgba(13,36,77,.16);cursor:pointer;color:var(--navy);
    display:flex;align-items:center;justify-content:center;box-shadow:var(--sh-md);z-index:2}
  .dlg-close:hover{background:var(--oat)}
  @media(max-width:700px){
    .bio-dlg{grid-template-columns:1fr;padding:26px}
    .dlg-photo{max-width:140px}
  }
</style>
'''

JS = '''
<script>
/* ---- B2 drawer ---- */
(function(){
  const cards=[...document.querySelectorAll('.dcard')];
  const panels=[...document.querySelectorAll('.drawerpanel')];
  if(!cards.length) return;
  const closeAll=()=>{
    cards.forEach(c=>{c.classList.remove('active'); c.querySelector('.dbtn').setAttribute('aria-expanded','false');});
    panels.forEach(p=>p.hidden=true);
  };
  cards.forEach((c,i)=>{
    const btn=c.querySelector('.dbtn');
    btn.addEventListener('click',()=>{
      const isOpen=!panels[i].hidden;
      closeAll();
      if(!isOpen){
        panels[i].hidden=false;
        c.classList.add('active');
        btn.setAttribute('aria-expanded','true');
        /* move focus into the panel so keyboard users land on what just appeared */
        panels[i].querySelector('h3').setAttribute('tabindex','-1');
        panels[i].querySelector('h3').focus({preventScroll:true});
      }
    });
  });
  panels.forEach((p,i)=>{
    p.querySelector('.dp-close').addEventListener('click',()=>{
      closeAll();
      cards[i].querySelector('.dbtn').focus();   /* focus returns to the trigger, never lost */
    });
  });
  document.addEventListener('keydown',e=>{
    if(e.key!=='Escape') return;
    const open=panels.findIndex(p=>!p.hidden);
    if(open>-1){ closeAll(); cards[open].querySelector('.dbtn').focus(); }
  });
})();

/* ---- B3 dialog ---- */
(function(){
  document.querySelectorAll('.mbtn').forEach(b=>{
    const dlg=document.getElementById(b.dataset.dlg);
    if(!dlg) return;
    /* showModal() gives focus trapping + Esc + inert background for free */
    b.addEventListener('click',()=>dlg.showModal());
    dlg.querySelector('.dlg-close').addEventListener('click',()=>dlg.close());
    /* click the backdrop to dismiss */
    dlg.addEventListener('click',e=>{ if(e.target===dlg) dlg.close(); });
    dlg.addEventListener('close',()=>b.focus());
  });
})();
</script>
'''

html = head("Veterinarian bios — 3 takes on Card + expand | Cumberland Valley",
            "Three variants of the card-and-expand bio layout.", extra_css=CSS)
html += '''
<header class="vhead">
  <div class="wrap">
    <h1>Card + expand &mdash; three variants</h1>
    <p>Same client copy in all three, word for word. Every card shows the first paragraph; the rest is one interaction away. What changes is <em>where the rest appears</em> &mdash; and each choice trades something. Nav, hero and footer omitted so the bios are easy to compare.</p>
  </div>
</header>
<div class="vbar">
  <div class="wrap">
    <a href="#b1">B1 &middot; Inline reveal</a>
    <a href="#b2">B2 &middot; Full-width drawer</a>
    <a href="#b3">B3 &middot; Dialog</a>
  </div>
</div>
<main id="main">

<div class="vlabel" id="b1"><div class="wrap"><h2>B1 &middot; Inline reveal</h2>
  <span>The bio unfolds inside its own card. Built on native &lt;details&gt;, so it works with JavaScript off and is keyboard-operable with zero custom code &mdash; the most robust of the three. Trade-off: an open card grows taller than its neighbours and the row goes ragged.</span></div></div>
<section class="sec"><div class="wrap"><div class="vcards">''' + B1 + '''
</div></div></section>

<div class="vlabel" id="b2"><div class="wrap"><h2>B2 &middot; Full-width drawer</h2>
  <span>The full bio opens in a panel beneath the row, at a comfortable 70ch measure &mdash; the cards themselves never move or change height. One bio at a time, and the whole team stays on screen above it. Trade-off: needs JavaScript, and the drawer pushes anything below it down the page.</span></div></div>
<section class="sec"><div class="wrap"><div class="dcards">''' + B2_CARDS + '''
</div><div class="drawerwrap">''' + B2_DRAWERS + '''
</div></div></section>

<div class="vlabel" id="b3"><div class="wrap"><h2>B3 &middot; Dialog</h2>
  <span>The bio opens over the page in a modal. Uses the native &lt;dialog&gt; element, so focus trapping, Esc-to-close and an inert background come for free rather than being hand-rolled. The grid never shifts at all. Trade-off: a modal is a heavier gesture than a disclosure &mdash; and on a phone it covers the whole screen, which can feel like a detour.</span></div></div>
<section class="sec"><div class="wrap"><div class="vcards">''' + B3_CARDS + '''
</div>''' + B3_DIALOGS + '''
</div></section>

</main>
'''
html += footer()
html += script()
html += JS

out = os.path.join(os.path.dirname(__file__), '..', 'cumberland-valley-bio-cardexpand-variants.html')
open(out, 'w').write(html)
print("wrote cumberland-valley-bio-cardexpand-variants.html", len(html), "bytes")
