# Shared chrome for the Cumberland Valley site.
# Single source of truth: every page's <head>, top strip, nav and footer are generated
# from here, so a change to the nav can't land on four pages and miss the fifth.

# The client's VetSource storefront. External — opens in a new tab.
PHARMACY_URL = ("https://cumberlandvalleyvetclinic.securevetsource.com/site/view/site/view/HomeDelivery.pml"
                "?retUrl=http://cumberlandvalleyvetclinic.vetsourcecms.com"
                "&cmsTitle=Cumberland%20Valley%20Veterinary%20Clinic")

# PetSites client login, as supplied.
# NOTE: this is a click-TRACKER wrapper (b.shspclick.com/click/...) with a long signed token,
# not the destination itself. Those tokens are tied to a campaign and commonly expire or rot.
# Shipping it as given, but the durable link is almost certainly a plain petsites.com URL —
# flagged for the client to confirm before launch.
PETSITES_URL = ("http://b.shspclick.com/click/308496326/www.petsites.com/"
                "?p=esEtjMQqPPsqSHjcktHLuQTV7ZiGe_DA7OzrbeqlS7KIGDO725aZedHZr8nJF0_X6mjhdaS0qaGaYV9VPRAVriUqi0y1E9E9"
                "-JGRBUfArfuHRNtSo1G2TzK42Lrzdt8yGdEXpAWDq2sIOPD48b3hIDh_tVXesh6T-HNbTjtFPQb9diLtTkmQdBQXXoaD"
                "-UlOzqP1ljBu272AxyGP_ccMsIanKg-r_m8owblI-3pLJn4jtDs-i11POOd0cyJ6ZHDz9vOl0mdfq_Rkq-xrP6sVk5kXpOObrkrLJQpO6pCVKVNA_8p_fhgreE91Q5DCeYMbl0FTsOI9IHzdKdHNfub6gw==")

# Nav: Home, About, Services, Client Corner, Contact. Third element = submenu children.
# href=None means the item is a LABEL, not a page — it only opens its submenu.
# "About" and "Client Corner" are both labels: neither is a page, they only parent their children.
NAV_ITEMS = [
    ("Home",          "index.html",      []),
    ("About",         None,              [("Team", "team.html")]),
    ("Services",      "services.html",   []),
    # The practice is "Veterinary Clinic & Pet Resort" — the Resort is half the brand and a
    # separate revenue line, so it gets equal billing rather than living under Services.
    ("Pet Resort",    "pet-resort.html", []),
    ("Client Corner", None,              [("Online Pharmacy", PHARMACY_URL),
                                          ("PetSites Login", PETSITES_URL)]),
    ("Contact",       "contact.html",    []),
]

def is_external(href):
    return href.startswith(("http://", "https://"))

def _flat():
    """Every internal page in the nav, parents and children."""
    out = []
    for label, href, kids in NAV_ITEMS:
        out.append((label, href))
        out.extend(k for k in kids if not is_external(k[1]))
    return out

ADDRESS_HTML = '17747 Virginia Ave.<br>Hagerstown, Maryland 21740'
MAPS_URL = "https://maps.google.com/?q=17747+Virginia+Ave,+Hagerstown,+MD+21740"
TEL_HREF = "tel:3017393121"
TEL_DISPLAY = "(301) 739-3121"

# Client-confirmed 2026-07-15. Minutes from midnight; None = closed.
HOURS = [
    ("Sunday",    None,      None),
    ("Monday",    7*60,      17*60),
    ("Tuesday",   7*60,      17*60),
    ("Wednesday", 7*60,      17*60),
    ("Thursday",  7*60,      17*60),
    ("Friday",    7*60,      17*60),
    ("Saturday",  7*60+30,   13*60),
]

def head(title, desc, extra_css="", schema=""):
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>{title}</title>
<meta name="description" content="{desc}">

<link rel="icon" href="assets/favicon.ico" sizes="any">
<link rel="icon" type="image/png" sizes="32x32" href="assets/favicon-32x32.png">
<link rel="apple-touch-icon" sizes="180x180" href="assets/apple-touch-icon.png">
<link rel="manifest" href="assets/site.webmanifest">
<meta name="theme-color" content="#0D244D">
{schema}
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Fraunces:opsz,wght@9..144,400;9..144,600;9..144,700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.5.2/css/all.min.css">
<link rel="stylesheet" href="assets/site.css">
{extra_css}</head>
<body>

<a class="skip" href="#main">Skip to main content</a>
'''

def topstrip():
    return f'''
<div class="topstrip">
  <div class="bar2">
    <a class="loc" href="{MAPS_URL}" target="_blank" rel="noopener"><i class="fa-solid fa-location-dot" aria-hidden="true"></i> 17747 Virginia Ave., Hagerstown, MD</a>
    <div class="status" id="status">
      <button class="pill" id="statusBtn" type="button" aria-expanded="false" aria-controls="hoursPanel">
        <span class="dot" id="statusDot"></span>
        <span id="statusText">Hours</span>
        <i class="fa-solid fa-chevron-down chev" aria-hidden="true"></i>
      </button>
      <div class="panel" id="hoursPanel" role="region" aria-label="Opening hours">
        <div class="panel-title">Our Hours</div>
        <div id="hoursRows"></div>
        <a class="callrow" href="{TEL_HREF}"><i class="fa-solid fa-phone" aria-hidden="true"></i> Call {TEL_DISPLAY}</a>
      </div>
    </div>
  </div>
</div>
'''

def nav(current, ondark=False):
    """ondark=True for pages that open on the navy banner. Without it the navy nav links sit on
    a navy background at 1.00:1 — identical colour, completely invisible.

    Items with children render as a submenu. It opens on hover AND on click/focus: hover-only
    menus are unreachable by keyboard and unusable on touch, where there is no hover state."""
    links, drawer = [], []
    for i, (label, href, kids) in enumerate(NAV_ITEMS):
        cur = ' aria-current="page"' if href == current else ''
        if kids:
            kid_cur = any(k[1] == current for k in kids)
            open_cls = ' class="has-sub open-trail"' if kid_cur else ' class="has-sub"'
            def _sub_a(k, cls=""):
                ext = is_external(k[1])
                # external links: new tab + rel=noopener, and say so rather than surprising people
                attrs = ' target="_blank" rel="noopener"' if ext else ''
                cur_a = ' aria-current="page"' if k[1] == current else ''
                icon = ' <i class="fa-solid fa-arrow-up-right-from-square xicon" aria-hidden="true"></i>' if ext else ''
                sr = ' <span class="sr-only">(opens in a new tab)</span>' if ext else ''
                c = f' class="{cls}"' if cls else ''
                return f'<a href="{k[1]}"{cur_a}{attrs}{c} role="menuitem">{k[0]}{icon}{sr}</a>'
            sub = "".join(_sub_a(k) for k in kids)

            if href is None:
                # Label-only parent. It MUST be a <button>, not an <a href="#"> or a bare <span>:
                # a button is focusable and operable by keyboard for free, and it doesn't lie
                # about being a link to a page that doesn't exist.
                trigger = (f'<button class="subtoggle-main" type="button" aria-haspopup="true" '
                           f'aria-expanded="false" aria-controls="sub{i}" id="sub{i}-t">{label}'
                           f'<i class="fa-solid fa-chevron-down chev" aria-hidden="true"></i></button>')
                links.append(f'<span{open_cls}>{trigger}'
                             f'<span class="submenu" id="sub{i}" role="menu" aria-labelledby="sub{i}-t">{sub}</span>'
                             f'</span>')
                # In the drawer a label-only parent is just a heading — nothing to tap.
                drawer.append(f'      <div class="drawer-head">{label}</div>')
            else:
                links.append(
                    f'<span{open_cls}>'
                    f'<a href="{href}"{cur} aria-haspopup="true" aria-expanded="false" id="sub{i}-t">{label}</a>'
                    f'<button class="subtoggle" type="button" aria-expanded="false" aria-controls="sub{i}" aria-label="Show {label} submenu"><i class="fa-solid fa-chevron-down" aria-hidden="true"></i></button>'
                    f'<span class="submenu" id="sub{i}" role="menu" aria-labelledby="sub{i}-t">{sub}</span>'
                    f'</span>')
                drawer.append(f'      <a href="{href}"{cur}>{label}</a>')
            for k in kids:
                drawer.append('      ' + _sub_a(k, cls="sub"))
        else:
            links.append(f'<a href="{href}"{cur}>{label}</a>')
            drawer.append(f'      <a href="{href}"{cur}>{label}</a>')
    cls = "ondark" if ondark else ""
    return f'''
<nav id="nav" class="{cls}" aria-label="Primary">
  <div class="wrap bar">
    <div class="mark"><a href="index.html" aria-label="Cumberland Valley Veterinary Clinic &amp; Pet Resort — home"><picture><source srcset="assets/cvvc-logo.webp" type="image/webp"><img src="assets/cvvc-logo.png" alt="Cumberland Valley Veterinary Clinic &amp; Pet Resort"></picture></a></div>
    <div class="links">
      {''.join(links)}
    </div>
    <div style="display:flex;align-items:center;gap:12px">
      <a class="callbtn" href="{TEL_HREF}" aria-label="Call Cumberland Valley at {TEL_DISPLAY}"><i class="fa-solid fa-phone" aria-hidden="true"></i> <span class="lbl">{TEL_DISPLAY}</span></a>
      <button class="navtoggle" id="navToggle" type="button" aria-expanded="false" aria-controls="navDrawer" aria-label="Open menu">
        <i class="fa-solid fa-bars" aria-hidden="true"></i>
      </button>
    </div>
  </div>
  <div class="drawer" id="navDrawer">
{chr(10).join(drawer)}
  </div>
</nav>
'''

def pagehead(kicker, h1, lede, photo=None):
    """Interior-page banner. Deliberately NOT the homepage hero — no video, no stone.
    Those belong to the homepage; reusing them would flatten the site's hierarchy.

    photo: optional basename in /assets (no extension) rendered behind the copy under a navy
    scrim. The scrim is not decoration — it is what keeps the white h1 above 4.5:1 on a photo
    whose luminance we don't control."""
    k = f'<div class="ph-kicker">{kicker}</div>' if kicker else ''
    l = f'<p class="ph-lede">{lede}</p>' if lede else ''
    if photo:
        bg = f'''  <picture class="ph-photo">
    <source srcset="assets/{photo}.webp" type="image/webp">
    <img src="assets/{photo}-fallback.jpg" alt="" aria-hidden="true">
  </picture>
  <div class="ph-scrim" aria-hidden="true"></div>'''
        cls = "pagehead haspic"
    else:
        bg = '  <div class="ph-tex" aria-hidden="true"></div>'
        cls = "pagehead"
    return f'''
<header class="{cls}">
{bg}
  <div class="wrap ph-inner">
    {k}
    <h1>{h1}</h1>
    {l}
  </div>
</header>
'''

def herolite(h1, sub=None, note=None, video="hero-home"):
    """The homepage hero, verbatim, for an interior page: same scrim, same stone wall, same
    83vh height. Only the copy and the footage change.

    video: basename in /assets — expects <name>.mp4 + <name>-poster.jpg."""
    s = f'<p class="sub">{sub}</p>' if sub else ''
    n = f'<div class="note">{note}</div>' if note else ''
    return f'''
<header class="hero herolite">
  <video class="bgvid" aria-hidden="true" autoplay muted loop playsinline preload="auto"
         poster="assets/{video}-poster.jpg">
    <source src="assets/{video}.mp4" type="video/mp4">
  </video>
  <div class="scenetint"></div>
  <div class="grain"></div>
  <div class="wrap inner">
    <h1>{h1}</h1>
    {s}
    <a class="cta-big" href="{TEL_HREF}" aria-label="Call Cumberland Valley at {TEL_DISPLAY}"><i class="fa-solid fa-phone" aria-hidden="true"></i> Call {TEL_DISPLAY}</a>
    {n}
  </div>
  <div class="wall">
    <div class="tex">
      <img src="assets/stone-background.svg" alt="" aria-hidden="true">
    </div>
    <div class="topshade"></div><div class="graze"></div>
  </div>
</header>
'''


def grouped_hours():
    """Collapse consecutive days with identical hours into ranges.
    Seven near-identical rows is a wall of noise; Mon–Fri / Sat / Sun is the same information
    in three lines. Returns [(label, timetext, [member day names]), ...] in week order Mon→Sun,
    because a hours list that opens on Sunday reads wrong even though the JS array is 0-indexed
    from Sunday."""
    week = HOURS[1:] + HOURS[:1]            # Monday-first for display
    groups = []
    for d, o, c in week:
        key = (o, c)
        if groups and groups[-1][0] == key:
            groups[-1][1].append(d)
        else:
            groups.append([key, [d]])
    out = []
    for (o, c), days in groups:
        label = days[0] if len(days) == 1 else f"{days[0][:3]} &ndash; {days[-1][:3]}"
        txt = "Closed" if o is None else f"{_fmt(o)} &ndash; {_fmt(c)}"
        out.append((label, txt, days))
    return out


def hours_block(idsuffix, title="Clinic Hours"):
    """Live hours list + open/closed status. Rendered from the same HOURS array the header
    widget uses, so the two can never disagree. idsuffix keeps ids unique when a page shows
    this more than once."""
    rows = []
    for label, txt, days in grouped_hours():
        cl = ' class="cl"' if txt == "Closed" else ''
        rows.append(f'      <div class="hrow" data-days="{",".join(days)}"><span>{label}</span><span{cl}>{txt}</span></div>')
    return f'''
  <div class="hoursbox" id="hoursbox-{idsuffix}">
    <div class="hb-head">
      <div class="hb-title">{title}</div>
      <span class="hb-status" id="hbStatus-{idsuffix}"><span class="dot"></span><span class="t">Hours</span></span>
    </div>
    <div class="hb-rows">
{chr(10).join(rows)}
    </div>
  </div>'''


def _fmt(m):
    h, mm = divmod(m, 60)
    ap = 'AM' if h < 12 else 'PM'
    h12 = 12 if h % 12 == 0 else h % 12
    return f"{h12}:{mm:02d} {ap}"


def footer():
    # Logo + NAP + live hours. (An "Explore" link column was added here briefly and removed —
    # it was never asked for, and it shipped unstyled.)
    return f'''
<footer class="f">
  <div class="wrap g">
    <div class="mk"><picture><source srcset="assets/cvvc-logo.webp" type="image/webp"><img src="assets/cvvc-logo.png" alt=""></picture></div>
{hours_block("footer")}
    <address class="nap">
      <div class="nap-name">Cumberland Valley Veterinary Clinic &amp; Pet Resort</div>
      <a class="nap-addr" href="{MAPS_URL}" target="_blank" rel="noopener">
        <i class="fa-solid fa-location-dot" aria-hidden="true"></i>
        <span>{ADDRESS_HTML}</span>
      </a>
      <a class="nap-tel telinline" href="{TEL_HREF}" aria-label="Call Cumberland Valley at {TEL_DISPLAY}">
        <i class="fa-solid fa-phone" aria-hidden="true"></i> {TEL_DISPLAY}
      </a>
    </address>
  </div>
</footer>
'''

# The hours widget + nav scroll + drawer. Shared by every page.
def script():
    rows = ",\n      ".join(
        "{{d:'{}', o:{}, c:{}}}".format(d, 'null' if o is None else o, 'null' if c is None else c)
        for d, o, c in HOURS
    )
    return '''
<script>
(function(){
  const nav=document.getElementById('nav');
  if(nav){
    const onScroll=()=>nav.classList.toggle('solid',window.scrollY>60);
    onScroll(); window.addEventListener('scroll',onScroll,{passive:true});
  }

  /* ---- desktop submenu (About > Team) ----
     CSS handles hover and focus-within. This adds explicit click/Esc control so the menu is
     operable by keyboard and on touch, where :hover never fires. */
  (function(){
    const subs=document.querySelectorAll('nav .links .has-sub');
    if(!subs.length) return;
    /* NOTE: must match BOTH trigger shapes — '.subtoggle' (chevron beside a real link) and
       '.subtoggle-main' (label-only parent, e.g. About). Matching only the former left the
       label-only trigger stuck at aria-expanded="true" after closing. */
    const closeAll=except=>subs.forEach(s=>{
      if(s===except) return;
      s.classList.remove('open');
      s.querySelectorAll(':scope > .subtoggle, :scope > .subtoggle-main, :scope > a[aria-haspopup]')
       .forEach(el=>el.setAttribute('aria-expanded','false'));
    });
    subs.forEach(s=>{
      // either a chevron next to a real link, or a label-only <button> trigger
      const btn=s.querySelector(':scope > .subtoggle, :scope > .subtoggle-main');
      const trig=s.querySelector(':scope > a[aria-haspopup]');
      if(!btn) return;
      btn.addEventListener('click',e=>{
        e.preventDefault(); e.stopPropagation();
        const open=!s.classList.contains('open');
        closeAll(s);
        s.classList.toggle('open',open);
        btn.setAttribute('aria-expanded',open?'true':'false');
        if(trig) trig.setAttribute('aria-expanded',open?'true':'false');
      });
    });
    document.addEventListener('click',e=>{ if(!e.target.closest('.has-sub')) closeAll(null); });
    document.addEventListener('keydown',e=>{
      if(e.key!=='Escape') return;
      const open=document.querySelector('nav .links .has-sub.open');
      if(!open) return;
      const b=open.querySelector(':scope > .subtoggle, :scope > .subtoggle-main');
      closeAll(null);
      if(b) b.focus();     /* focus returns to the trigger; it will NOT re-open (no :focus-within) */
    });
    /* Tabbing out of the group closes it — otherwise the panel hangs open behind the rest of the nav. */
    subs.forEach(s=>{
      s.addEventListener('focusout',e=>{
        if(!s.contains(e.relatedTarget)) {
          s.classList.remove('open');
          s.querySelectorAll(':scope > .subtoggle, :scope > .subtoggle-main, :scope > a[aria-haspopup]')
           .forEach(el=>el.setAttribute('aria-expanded','false'));
        }
      });
    });
  })();

  /* ---- mobile drawer ---- */
  (function(){
    const t=document.getElementById('navToggle'), d=document.getElementById('navDrawer');
    if(!t||!d) return;
    t.addEventListener('click',()=>{
      const open=d.classList.toggle('open');
      t.setAttribute('aria-expanded',open?'true':'false');
      t.setAttribute('aria-label',open?'Close menu':'Open menu');
      t.querySelector('i').className=open?'fa-solid fa-xmark':'fa-solid fa-bars';
    });
    /* Esc closes and returns focus to the button — keyboard users must not get trapped. */
    document.addEventListener('keydown',e=>{
      if(e.key==='Escape'&&d.classList.contains('open')){ t.click(); t.focus(); }
    });
  })();

  /* ---- open/closed widget ----
     CONFIRMED HOURS (client-supplied 2026-07-15). */
  (function(){
    const HOURS=[
      ''' + rows + '''
    ];
    const wrap=document.getElementById('status'), btn=document.getElementById('statusBtn'),
          dot=document.getElementById('statusDot'), txt=document.getElementById('statusText'),
          rows=document.getElementById('hoursRows');
    if(!wrap) return;
    const fmt=m=>{const h=Math.floor(m/60),mm=m%60,ap=h>=12?'PM':'AM',h12=h%12===0?12:h%12;
      return h12+(mm?':'+String(mm).padStart(2,'0'):'')+' '+ap;};
    /* Pinned to the CLINIC's clock, not the visitor's. Someone checking from Denver at 4 PM
       must see "Closed" — Hagerstown is already at 6 PM. */
    const clinicNow=()=>{
      try{ return new Date(new Date().toLocaleString('en-US',{timeZone:'America/New_York'})); }
      catch(e){ return new Date(); }
    };
    const now=clinicNow(), day=now.getDay(), mins=now.getHours()*60+now.getMinutes();
    const t=HOURS[day];
    let isOpen=false;
    if(t.o!==null && mins>=t.o && mins<t.c) isOpen=true;
    if(isOpen){
      dot.className='dot on';
      const left=t.c-mins;
      txt.textContent = left<=60 ? 'Open · closes in '+left+' min' : 'Open now · until '+fmt(t.c);
    }else{
      dot.className='dot off';
      let n=day, hops=0, nx=null;
      while(hops<7){ n=(n+1)%7; hops++; if(HOURS[n].o!==null){nx=HOURS[n];break;} }
      if(t.o!==null && mins<t.o) txt.textContent='Closed · opens '+fmt(t.o);
      else if(nx) txt.textContent='Closed · opens '+nx.d.slice(0,3)+' '+fmt(nx.o);
      else txt.textContent='Closed';
    }
    rows.innerHTML=HOURS.map((h,i)=>
      '<div class="hrow'+(i===day?' today':'')+'"><span>'+h.d+'</span><span>'+
      (h.o===null?'Closed':fmt(h.o)+' – '+fmt(h.c))+'</span></div>').join('');
    btn.addEventListener('click',()=>{
      const open=wrap.classList.toggle('open');
      btn.setAttribute('aria-expanded',open?'true':'false');
    });
    document.addEventListener('click',e=>{
      if(!wrap.contains(e.target)&&wrap.classList.contains('open')){
        wrap.classList.remove('open'); btn.setAttribute('aria-expanded','false');
      }
    });
    document.addEventListener('keydown',e=>{
      if(e.key==='Escape'&&wrap.classList.contains('open')){
        wrap.classList.remove('open'); btn.setAttribute('aria-expanded','false'); btn.focus();
      }
    });
  })();

  /* ---- standalone hours blocks (footer / contact page) ----
     Driven by the same HOURS + clinic-clock logic as the header widget. */
  (function(){
    const boxes=document.querySelectorAll('.hoursbox');
    if(!boxes.length) return;
    const HOURS=[
      ''' + rows + '''
    ];
    const fmt=m=>{const h=Math.floor(m/60),mm=m%60,ap=h>=12?'PM':'AM',h12=h%12===0?12:h%12;
      return h12+(mm?':'+String(mm).padStart(2,'0'):'')+' '+ap;};
    const clinicNow=()=>{
      try{ return new Date(new Date().toLocaleString('en-US',{timeZone:'America/New_York'})); }
      catch(e){ return new Date(); }
    };
    const now=clinicNow(), day=now.getDay(), mins=now.getHours()*60+now.getMinutes();
    const t=HOURS[day];
    let isOpen = t.o!==null && mins>=t.o && mins<t.c;
    let label;
    if(isOpen){
      const left=t.c-mins;
      label = left<=60 ? 'Open · closes in '+left+' min' : 'Open now · until '+fmt(t.c);
    }else{
      let n=day,hops=0,nx=null;
      while(hops<7){ n=(n+1)%7; hops++; if(HOURS[n].o!==null){nx=HOURS[n];break;} }
      if(t.o!==null && mins<t.o) label='Closed · opens '+fmt(t.o);
      else if(nx) label='Closed · opens '+nx.d.slice(0,3)+' '+fmt(nx.o);
      else label='Closed';
    }
    boxes.forEach(box=>{
      const st=box.querySelector('.hb-status');
      if(st){
        st.classList.add(isOpen?'on':'off');
        st.querySelector('.t').textContent=label;
      }
      /* rows are day RANGES now — highlight the range that contains today */
      box.querySelectorAll('.hrow').forEach(r=>{
        const days=(r.dataset.days||'').split(',');
        if(days.indexOf(HOURS[day].d)>-1) r.classList.add('today');
      });
    });
  })();

  /* ---- bio sheets (D3 · adaptive sheet) ----
     showModal() gives focus trapping, Esc and an inert background for free. */
  (function(){
    const triggers=document.querySelectorAll('[data-bio]');
    if(!triggers.length) return;
    triggers.forEach(b=>{
      const dlg=document.getElementById(b.dataset.bio);
      if(!dlg) return;
      b.addEventListener('click',()=>{
        dlg.showModal();
        dlg._trigger=b;
        const h=dlg.querySelector('h3');
        if(h) h.focus({preventScroll:true});   /* land on the name, not the close button */
      });
    });
    document.querySelectorAll('dialog.biosheet').forEach(dlg=>{
      const x=dlg.querySelector('.bs-x');
      if(x) x.addEventListener('click',()=>dlg.close());
      /* the backdrop is the dialog element itself — click outside the panel to dismiss */
      dlg.addEventListener('click',e=>{ if(e.target===dlg) dlg.close(); });
      dlg.addEventListener('close',()=>{ if(dlg._trigger) dlg._trigger.focus(); });
    });
  })();

  /* ---- parallax stone texture ----
     Same handler as the homepage: drift .whobg as its section crosses the viewport.
     rAF-throttled, and skipped entirely under prefers-reduced-motion. */
  (function(){
    /* resolve the SECTION explicitly — .whobg's parent is now .texclip (the clipping wrapper),
       and relying on parentElement would silently measure the wrong box if that nesting changes */
    const layers=[...document.querySelectorAll('.whobg')].map(bg=>({bg,sec:bg.closest('section')||bg.parentElement}));
    if(!layers.length) return;
    if(window.matchMedia('(prefers-reduced-motion: reduce)').matches) return;
    const DRIFT=220;
    let ticking=false;
    const update=()=>{
      const vh=window.innerHeight;
      layers.forEach(({bg,sec})=>{
        const r=sec.getBoundingClientRect();
        if(r.bottom>0&&r.top<vh){
          const p=(vh-r.top)/(vh+r.height);
          bg.style.transform='translate3d(0,'+((p-.5)*DRIFT).toFixed(1)+'px,0)';
        }
      });
      ticking=false;
    };
    const onP=()=>{if(!ticking){ticking=true;requestAnimationFrame(update);}};
    update();
    window.addEventListener('scroll',onP,{passive:true});
    window.addEventListener('resize',onP);
  })();

  /* ---- scroll reveals ---- */
  const rv=document.querySelectorAll('.rv');
  if(rv.length){
    if(window.matchMedia('(prefers-reduced-motion: reduce)').matches){
      rv.forEach(el=>el.classList.add('in'));
    }else{
      const io=new IntersectionObserver(es=>es.forEach(e=>{
        if(e.isIntersecting){ e.target.classList.add('in'); io.unobserve(e.target); }
      }),{threshold:.16,rootMargin:'0px 0px -8% 0px'});
      rv.forEach(el=>io.observe(el));
    }
  }
})();
</script>
</body>
</html>
'''
