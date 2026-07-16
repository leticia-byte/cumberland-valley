import sys, os
sys.path.insert(0, os.path.dirname(__file__))
from parts import head, footer, script, TEL_HREF, TEL_DISPLAY
from gen_team import VETS

# Three takes on "B3 · Dialog". All three use the native <dialog> element + showModal(), so
# focus trapping, Esc-to-close and an inert background are the platform's job, not mine.
# What differs is how the panel presents itself and how you move between doctors.

def ps(items, cls=""):
    c = f' class="{cls}"' if cls else ''
    return "\n          ".join(f"<p{c}>{x}</p>" for x in items)

def cards(prefix, btn_label, btn_cls="mbtn"):
    return "\n".join(f'''
      <article class="vcard">
        <div class="p-photo"><i class="fa-solid fa-user-doctor" aria-hidden="true"></i></div>
        <div class="p-body">
          <h3>{n}</h3>
          <div class="p-role">{role}</div>
          <p class="vlede">{p[0]}</p>
          <button class="{btn_cls}" type="button" data-dlg="{prefix}{i}">
            <span>{btn_label}</span><i class="fa-solid fa-arrow-right" aria-hidden="true"></i>
          </button>
        </div>
      </article>''' for i, (n, role, p) in enumerate(VETS))

# ---------------------------------------------------------------- D1 · Split modal + prev/next
D1_DLG = "\n".join(f'''
    <dialog class="d1" id="d1-{i}" data-i="{i}" aria-labelledby="d1h{i}">
      <button class="x-close" type="button" aria-label="Close bio"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button>
      <div class="d1-photo"><i class="fa-solid fa-user-doctor" aria-hidden="true"></i></div>
      <div class="d1-body">
        <h3 id="d1h{i}" tabindex="-1">{n}</h3>
        <div class="p-role">{role}</div>
        {ps(p)}
        <a class="callbtn" style="margin-top:22px" href="{TEL_HREF}"><i class="fa-solid fa-phone" aria-hidden="true"></i> Call {TEL_DISPLAY}</a>
      </div>
      <nav class="d1-nav" aria-label="Move between veterinarians">
        <button class="d1-prev" type="button" aria-label="Previous veterinarian"><i class="fa-solid fa-chevron-left" aria-hidden="true"></i></button>
        <span class="d1-count">{i+1} of {len(VETS)}</span>
        <button class="d1-next" type="button" aria-label="Next veterinarian"><i class="fa-solid fa-chevron-right" aria-hidden="true"></i></button>
      </nav>
    </dialog>''' for i, (n, role, p) in enumerate(VETS))

# ---------------------------------------------------------------- D2 · Side sheet
D2_DLG = "\n".join(f'''
    <dialog class="d2" id="d2-{i}" aria-labelledby="d2h{i}">
      <div class="d2-head">
        <div class="d2-photo"><i class="fa-solid fa-user-doctor" aria-hidden="true"></i></div>
        <div>
          <h3 id="d2h{i}" tabindex="-1">{n}</h3>
          <div class="p-role">{role}</div>
        </div>
        <button class="x-close d2-x" type="button" aria-label="Close bio"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button>
      </div>
      <div class="d2-body">
        {ps(p)}
      </div>
      <div class="d2-foot">
        <a class="callbtn" href="{TEL_HREF}"><i class="fa-solid fa-phone" aria-hidden="true"></i> Call {TEL_DISPLAY}</a>
      </div>
    </dialog>''' for i, (n, role, p) in enumerate(VETS))

# ---------------------------------------------------------------- D3 · Adaptive sheet
D3_DLG = "\n".join(f'''
    <dialog class="d3" id="d3-{i}" aria-labelledby="d3h{i}">
      <div class="d3-grab" aria-hidden="true"></div>
      <button class="x-close d3-x" type="button" aria-label="Close bio"><i class="fa-solid fa-xmark" aria-hidden="true"></i></button>
      <div class="d3-scroll">
        <div class="d3-hero">
          <div class="d3-photo"><i class="fa-solid fa-user-doctor" aria-hidden="true"></i></div>
          <h3 id="d3h{i}" tabindex="-1">{n}</h3>
          <div class="p-role">{role}</div>
        </div>
        <div class="d3-body">
          {ps(p)}
          <a class="callbtn" style="margin-top:22px" href="{TEL_HREF}"><i class="fa-solid fa-phone" aria-hidden="true"></i> Call {TEL_DISPLAY}</a>
        </div>
      </div>
    </dialog>''' for i, (n, role, p) in enumerate(VETS))

CSS = '''
<style>
  .vhead{background:var(--navy);color:#fff;padding:120px 0 34px}
  .vhead h1{color:#fff;font-size:38px}
  .vhead p{color:#CFDCEC;margin-top:12px;max-width:78ch;font-size:16px;line-height:1.6}
  .vbar{background:#0B1E3E;border-bottom:1px solid rgba(255,255,255,.14)}
  .vbar .wrap{display:flex;gap:8px;padding:10px 28px;flex-wrap:wrap}
  .vbar a{color:#CFDCEC;text-decoration:none;font:600 13px/1 'Inter';padding:10px 14px;border-radius:999px;border:1px solid rgba(255,255,255,.24)}
  .vbar a:hover{background:rgba(255,255,255,.10);color:#fff}
  .vlabel{background:var(--blue);color:#fff;padding:18px 0}
  .vlabel .wrap{display:flex;align-items:baseline;gap:16px;flex-wrap:wrap}
  .vlabel h2{color:#fff;font-size:26px}
  .vlabel span{font:500 14px/1.5 'Inter';color:#DCEAFB;max-width:86ch}

  .vcards{display:grid;grid-template-columns:repeat(auto-fit,minmax(min(300px,100%),1fr));gap:24px;margin-top:36px;align-items:start}
  .vcard{background:#fff;border:1px solid rgba(13,36,77,.12);border-radius:16px;overflow:hidden;
    box-shadow:var(--sh-md);transition:box-shadow .35s,transform .35s cubic-bezier(.2,.8,.2,1)}
  .vcard:hover{box-shadow:var(--sh-lg);transform:translateY(-3px)}
  .vcard .p-photo{aspect-ratio:4/3;background:linear-gradient(160deg,#E8EEF5,#D1D2D4);
    display:flex;align-items:center;justify-content:center;color:var(--blue);font-size:44px}
  .vcard .p-body{padding:26px}
  .vcard h3{font-size:23px;color:var(--navy)}
  .vlede{font:400 15px/1.7 'Inter';color:#4A525C}
  .mbtn{background:var(--blue);border:0;color:#fff;cursor:pointer;margin-top:16px;
    padding:12px 18px;border-radius:999px;font:600 14px/1 'Inter';
    display:inline-flex;align-items:center;gap:9px;box-shadow:var(--sh-sm);
    transition:transform .25s,background .25s,box-shadow .25s}
  .mbtn:hover{transform:translateY(-2px);background:#1A61B8;box-shadow:var(--sh-md)}
  .mbtn i{font-size:11px;transition:transform .25s}
  .mbtn:hover i{transform:translateX(3px)}

  /* shared dialog chrome.
     margin:auto is restored explicitly — the site's `*{margin:0}` reset wipes the UA's
     dialog{margin:auto}, which is what centres a modal in the viewport. Without it every
     dialog silently pins to the top-left corner. */
  dialog{border:0;padding:0;color:var(--ink);margin:auto}
  dialog::backdrop{background:rgba(9,26,56,.60);backdrop-filter:blur(2px)}
  .x-close{width:40px;height:40px;border-radius:50%;background:#fff;border:1px solid rgba(13,36,77,.16);
    cursor:pointer;color:var(--navy);display:flex;align-items:center;justify-content:center;
    box-shadow:var(--sh-md);z-index:3;transition:background .25s,transform .25s}
  .x-close:hover{background:var(--oat);transform:rotate(90deg)}
  .dlg-photo-fill{background:linear-gradient(160deg,#E8EEF5,#D1D2D4);
    display:flex;align-items:center;justify-content:center;color:var(--blue)}

  /* ---------- D1 · split modal + prev/next ---------- */
  .d1{max-width:820px;width:calc(100% - 40px);border-radius:20px;overflow:visible;
    box-shadow:0 40px 90px -20px rgba(3,10,24,.65)}
  .d1[open]{display:grid;grid-template-columns:220px 1fr;gap:30px;padding:34px 34px 84px}
  .d1 .x-close{position:absolute;right:-12px;top:-12px}
  .d1-photo{aspect-ratio:1/1;border-radius:14px;background:linear-gradient(160deg,#E8EEF5,#D1D2D4);
    display:flex;align-items:center;justify-content:center;color:var(--blue);font-size:44px;align-self:start}
  .d1-body{max-height:56vh;overflow-y:auto;padding-right:8px}
  .d1-body h3{font-size:28px;color:var(--navy);outline:none}
  .d1-body p{font:400 15.5px/1.75 'Inter';color:#4A525C;margin-top:12px}
  .d1-nav{position:absolute;left:34px;right:34px;bottom:24px;display:flex;align-items:center;
    justify-content:space-between;gap:14px;padding-top:16px;border-top:1px solid rgba(13,36,77,.10)}
  .d1-nav button{width:42px;height:42px;border-radius:50%;border:1px solid rgba(13,36,77,.16);
    background:#fff;cursor:pointer;color:var(--navy);transition:background .25s,transform .25s}
  .d1-nav button:hover{background:var(--oat);transform:translateY(-2px)}
  .d1-count{font:600 12px/1 'Inter';letter-spacing:.1em;text-transform:uppercase;color:#5A626C}
  @media(max-width:720px){
    .d1[open]{grid-template-columns:1fr;padding:28px 24px 78px}
    .d1-photo{max-width:130px}
    .d1-body{max-height:48vh}
  }

  /* ---------- D2 · side sheet ---------- */
  /* A dialog can be positioned like a sheet: pin it to the right edge and give it full height. */
  .d2{max-width:520px;width:100%;height:100dvh;max-height:100dvh;margin:0 0 0 auto;
    border-radius:20px 0 0 20px;box-shadow:-30px 0 80px -20px rgba(3,10,24,.6)}
  .d2[open]{display:flex;flex-direction:column;animation:slideIn .38s cubic-bezier(.2,.8,.2,1)}
  @keyframes slideIn{from{transform:translateX(30px);opacity:0}to{transform:none;opacity:1}}
  @media (prefers-reduced-motion: reduce){.d2[open]{animation:none}}
  .d2-head{display:flex;align-items:center;gap:16px;padding:26px 28px;border-bottom:1px solid rgba(13,36,77,.10);
    background:var(--oat);border-radius:20px 0 0 0;position:relative}
  .d2-photo{width:66px;height:66px;border-radius:12px;flex:none;
    background:linear-gradient(160deg,#E8EEF5,#D1D2D4);display:flex;align-items:center;
    justify-content:center;color:var(--blue);font-size:24px}
  .d2-head h3{font-size:22px;color:var(--navy);outline:none}
  .d2-x{position:absolute;right:18px;top:18px;width:34px;height:34px}
  .d2-body{flex:1;overflow-y:auto;padding:26px 28px}
  .d2-body p{font:400 15.5px/1.8 'Inter';color:#4A525C;margin-top:14px}
  .d2-body p:first-child{margin-top:0}
  .d2-foot{padding:20px 28px;border-top:1px solid rgba(13,36,77,.10);background:#fff}
  @media(max-width:560px){.d2{border-radius:0}.d2-head{border-radius:0}}

  /* ---------- D3 · adaptive sheet ---------- */
  /* NOTE: do NOT set position:relative here. A modal dialog is position:fixed (top layer) and is
     already a containing block for the absolutely-positioned .d3-x close button. Overriding it to
     relative drops the dialog out of viewport positioning — it lays out against the document and
     renders ~1500px above the screen. Same trap as putting position:relative on a fixed nav. */
  .d3{max-width:640px;width:calc(100% - 40px);border-radius:20px;
    box-shadow:0 40px 90px -20px rgba(3,10,24,.65)}
  .d3[open]{display:block;padding:0}
  .d3-grab{display:none}
  .d3-x{position:absolute;right:14px;top:14px;width:36px;height:36px}
  .d3-scroll{max-height:78vh;overflow-y:auto}
  .d3-hero{background:linear-gradient(160deg,#E8EEF5,#D1D2D4);padding:34px 30px 26px;text-align:center;
    border-radius:20px 20px 0 0}
  .d3-photo{width:96px;height:96px;border-radius:50%;margin:0 auto 16px;background:#fff;
    display:flex;align-items:center;justify-content:center;color:var(--blue);font-size:38px;
    box-shadow:var(--sh-md)}
  .d3-hero h3{font-size:26px;color:var(--navy);outline:none}
  .d3-body{padding:26px 30px 30px}
  .d3-body p{font:400 15.5px/1.8 'Inter';color:#4A525C;margin-top:14px}
  .d3-body p:first-child{margin-top:0}
  /* On a phone it becomes a bottom sheet — the native gesture people already know. */
  @media(max-width:640px){
    .d3{width:100%;max-width:none;margin:auto 0 0 0;border-radius:20px 20px 0 0;
      max-height:88dvh}
    .d3[open]{animation:sheetUp .4s cubic-bezier(.2,.8,.2,1)}
    @keyframes sheetUp{from{transform:translateY(24px);opacity:0}to{transform:none;opacity:1}}
    .d3-grab{display:block;width:42px;height:5px;border-radius:99px;background:rgba(13,36,77,.22);
      margin:10px auto 0;position:relative;z-index:2}
    .d3-hero{border-radius:0;padding-top:18px}
    .d3-scroll{max-height:calc(88dvh - 20px)}
  }
  @media (prefers-reduced-motion: reduce){.d3[open]{animation:none}}
</style>
'''

JS = '''
<script>
(function(){
  /* One handler for all three variants. showModal() gives focus trapping, Esc and an inert
     background for free — none of that is hand-rolled here. */
  const open = (dlg, trigger) => {
    dlg.showModal();
    dlg._trigger = trigger;
    const h = dlg.querySelector('h3');
    if(h) h.focus({preventScroll:true});   /* land on the name, not the close button */
  };
  document.querySelectorAll('[data-dlg]').forEach(b=>{
    const dlg=document.getElementById(b.dataset.dlg);
    if(!dlg) return;
    b.addEventListener('click',()=>open(dlg,b));
  });
  document.querySelectorAll('dialog').forEach(dlg=>{
    const x=dlg.querySelector('.x-close');
    if(x) x.addEventListener('click',()=>dlg.close());
    /* click outside the panel to dismiss (the backdrop is the dialog element itself) */
    dlg.addEventListener('click',e=>{ if(e.target===dlg) dlg.close(); });
    dlg.addEventListener('close',()=>{ if(dlg._trigger) dlg._trigger.focus(); });
  });

  /* ---- D1 only: step between doctors without closing ---- */
  const d1=[...document.querySelectorAll('.d1')];
  if(d1.length){
    const go=(from,dir)=>{
      const i=+from.dataset.i, n=(i+dir+d1.length)%d1.length;
      const t=from._trigger;
      from.close();
      open(d1[n], t);           /* keep the original trigger so focus returns somewhere real */
    };
    d1.forEach(dlg=>{
      dlg.querySelector('.d1-prev').addEventListener('click',()=>go(dlg,-1));
      dlg.querySelector('.d1-next').addEventListener('click',()=>go(dlg,1));
      dlg.addEventListener('keydown',e=>{
        if(e.key==='ArrowLeft'){e.preventDefault();go(dlg,-1);}
        if(e.key==='ArrowRight'){e.preventDefault();go(dlg,1);}
      });
    });
  }
})();
</script>
'''

html = head("Bio dialog — 3 variants | Cumberland Valley",
            "Three variants of the bio dialog.", extra_css=CSS)
html += '''
<header class="vhead">
  <div class="wrap">
    <h1>Bio dialog &mdash; three variants</h1>
    <p>Same client copy in all three. Every one uses the native &lt;dialog&gt; element with showModal(), so focus trapping, Esc-to-close and an inert background come from the platform rather than being hand-rolled &mdash; that&rsquo;s what makes a modal safe to use here. What changes is how the panel arrives and how you move between doctors.</p>
  </div>
</header>
<div class="vbar">
  <div class="wrap">
    <a href="#d1">D1 &middot; Split modal + prev/next</a>
    <a href="#d2">D2 &middot; Side sheet</a>
    <a href="#d3">D3 &middot; Adaptive sheet</a>
  </div>
</div>
<main id="main">

<div class="vlabel" id="d1"><div class="wrap"><h2>D1 &middot; Split modal + prev/next</h2>
  <span>Portrait left, bio right, centred. The addition that matters: prev/next arrows (and &larr; &rarr; keys) step through all three doctors without closing &mdash; read the whole team in one flow instead of open, close, open, close. Best when people compare doctors.</span></div></div>
<section class="sec"><div class="wrap"><div class="vcards">''' + cards("d1-", "Read full bio") + '''
</div>''' + D1_DLG + '''
</div></section>

<div class="vlabel" id="d2"><div class="wrap"><h2>D2 &middot; Side sheet</h2>
  <span>Slides in from the right at full height. Long bios scroll vertically, which is the direction the content already wants to go, and the roster stays visible behind it so you never lose your place. The pattern people know from Stripe, Linear and Gmail.</span></div></div>
<section class="sec"><div class="wrap"><div class="vcards">''' + cards("d2-", "Read full bio") + '''
</div>''' + D2_DLG + '''
</div></section>

<div class="vlabel" id="d3"><div class="wrap"><h2>D3 &middot; Adaptive sheet</h2>
  <span>A centred card with a portrait header on desktop &mdash; and on a phone the same dialog becomes a bottom sheet with a grab handle, rising from the bottom edge. One component, two behaviours, each native to its device. The most phone-friendly of the three, which matters when most pet owners arrive on mobile.</span></div></div>
<section class="sec"><div class="wrap"><div class="vcards">''' + cards("d3-", "Read full bio") + '''
</div>''' + D3_DLG + '''
</div></section>

</main>
'''
html += footer()
html += script()
html += JS

out = os.path.join(os.path.dirname(__file__), '..', 'cumberland-valley-bio-dialog-variants.html')
open(out, 'w').write(html)
print("wrote cumberland-valley-bio-dialog-variants.html", len(html), "bytes")
