import base64, io, os
from PIL import Image

A = "assets"

def b64(path, mime):
    with open(path, "rb") as f:
        return "data:%s;base64,%s" % (mime, base64.b64encode(f.read()).decode())

def b64_png_resized(path, w):
    im = Image.open(path).convert("RGBA")
    if im.width > w:
        im = im.resize((w, round(im.height * w / im.width)), Image.LANCZOS)
    buf = io.BytesIO(); im.save(buf, "PNG", optimize=True)
    return "data:image/png;base64," + base64.b64encode(buf.getvalue()).decode()

LOGO  = b64_png_resized(f"{A}/logo.png", 1200)
GIF   = b64(f"{A}/logo.gif", "image/gif")
HOF   = b64_png_resized(f"{A}/halloffame.png", 1100)
ALBUM = b64_png_resized(f"{A}/album.png", 400)

AUDIO_PATH = f"{A}/music.mp3"
AUDIO_SRC = b64(AUDIO_PATH, "audio/mpeg") if os.path.exists(AUDIO_PATH) else "assets/music.mp3"
TRACK_TITLE = "7118 - OST"

members = [
    {"name": "wez",    "user": "ecstsy_1.",           "id": "1336380647253475341",
     "avatar": b64_png_resized(f"{A}/wez.png", 256),    "deco": None},
    {"name": "pownzi", "user": "cinepownz",           "id": "1320410416333066283",
     "avatar": b64_png_resized(f"{A}/pownzi.png", 256), "deco": b64(f"{A}/deco_pownzi.png","image/png")},
    {"name": "Seko",   "user": "drippedinheartbreak", "id": "1257391429165252759",
     "avatar": b64_png_resized(f"{A}/seko.png", 256),   "deco": b64(f"{A}/deco_seko.png","image/png")},
]

cards = []
for i, m in enumerate(members):
    deco = f'<img class="deco" src="{m["deco"]}" alt="">' if m["deco"] else ""
    pcls = "pfp" if m["deco"] else "pfp plain"
    cards.append(f'''
      <a class="card reveal" style="--d:{i*.12+.15}s" href="#" title="@{m['user']}">
        <div class="{pcls}">
          <img class="av" src="{m['avatar']}" alt="{m['name']}">
          {deco}
        </div>
        <div class="name">{m['name']}</div>
        <div class="tag">@{m['user']}</div>
      </a>''')

html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>7118</title>
<style>
  *{{box-sizing:border-box;margin:0;padding:0}}
  html{{
    scroll-behavior:auto;
    scroll-snap-type:none;
    overflow-y:auto;
    scrollbar-width:none;
    -ms-overflow-style:none;
  }}
  html::-webkit-scrollbar,body::-webkit-scrollbar{{width:0;height:0;display:none}}
  html,body{{height:100%}}
  body{{
    background:#000;color:#e8d9ff;
    font-family:"Segoe UI",Inter,system-ui,-apple-system,sans-serif;
    text-align:center;overflow-x:hidden;
  }}
  body::before{{
    content:"";position:fixed;inset:0;pointer-events:none;z-index:0;
    background:radial-gradient(ellipse 900px 520px at 50% 6%,rgba(150,40,255,.2),transparent 70%);
  }}

  /* ---------- SNAP SECTIONS ---------- */
  section{{
    min-height:100vh;position:relative;z-index:1;
    display:flex;flex-direction:column;align-items:center;justify-content:center;
    padding:70px 20px;
  }}
  .inner{{width:100%;max-width:1000px;margin:0 auto}}

  /* velocity: whole section leans/blurs with scroll speed */
  .vel{{
    transform:translateY(var(--vy,0px)) skewY(var(--vs,0deg)) scale(var(--vz,1));
    filter:blur(var(--vb,0px));
    will-change:transform,filter;
  }}

  /* reveal on enter */
  .reveal{{opacity:0;transform:translateY(46px);transition:opacity .8s cubic-bezier(.2,.7,.2,1) var(--d,0s),transform .8s cubic-bezier(.2,.7,.2,1) var(--d,0s)}}
  section.on .reveal{{opacity:1;transform:none}}

  /* ---------- ENTER GATE ---------- */
  #gate{{
    position:fixed;inset:0;z-index:99;background:#000;
    display:flex;align-items:center;justify-content:center;flex-direction:column;gap:22px;
    cursor:pointer;transition:opacity .7s ease;
  }}
  #gate.hide{{opacity:0;pointer-events:none}}
  #gate img{{width:110px;filter:drop-shadow(0 0 22px rgba(170,60,255,.9));animation:float 3.6s ease-in-out infinite}}
  #gate span{{font-size:13px;letter-spacing:.5em;text-transform:uppercase;color:#fff;text-shadow:0 0 14px rgba(170,60,255,.95);animation:pulse 2s ease-in-out infinite}}
  @keyframes pulse{{0%,100%{{opacity:.45}}50%{{opacity:1}}}}

  /* ---------- HERO ---------- */
  .hero img{{
    width:100%;max-width:820px;height:auto;display:block;margin:0 auto;
    animation:breathe 5s ease-in-out infinite;
  }}
  @keyframes breathe{{
    0%,100%{{filter:drop-shadow(0 0 34px rgba(160,50,255,.45)) drop-shadow(0 0 80px rgba(120,0,255,.28))}}
    50%{{filter:drop-shadow(0 0 55px rgba(185,80,255,.75)) drop-shadow(0 0 120px rgba(140,0,255,.45))}}
  }}
  @keyframes float{{0%,100%{{transform:translateY(0)}}50%{{transform:translateY(-8px)}}}}

  /* small gif under the logo (decorative) */
  .sigil-plain img{{
    width:104px;height:auto;display:block;margin:-4px auto 0;
    filter:drop-shadow(0 0 18px rgba(170,60,255,.8));
    animation:float 3.6s ease-in-out infinite;
  }}
  /* small gif = INFO trigger (section 3) */
  .sigil{{margin:0 auto;background:none;border:0;padding:0;cursor:pointer;display:block}}
  .sigil img{{
    width:150px;height:auto;display:block;margin:0 auto;
    filter:drop-shadow(0 0 26px rgba(170,60,255,.85));
    animation:float 3.6s ease-in-out infinite;
    transition:transform .3s cubic-bezier(.2,.7,.2,1),filter .3s ease;
  }}
  .sigil:hover img{{transform:scale(1.14);filter:drop-shadow(0 0 46px rgba(210,120,255,1))}}
  .sigil:active img{{transform:scale(.97)}}
  .sigil .hint{{
    display:block;margin-top:16px;font-size:9.5px;letter-spacing:.46em;text-transform:uppercase;
    color:#9b78c9;text-shadow:0 0 12px rgba(150,40,255,.7);
    animation:pulse 2.4s ease-in-out infinite;
  }}

  .rule{{width:min(560px,80%);height:1px;margin:24px auto 0;background:linear-gradient(90deg,transparent,rgba(170,70,255,.75),transparent);box-shadow:0 0 14px rgba(160,50,255,.6)}}

  /* ---------- HALL OF FAME ---------- */
  .hof img{{
    width:100%;max-width:560px;height:auto;display:block;margin:0 auto 34px;
    mix-blend-mode:screen;animation:hofglow 4.5s ease-in-out infinite;
  }}
  @keyframes hofglow{{0%,100%{{filter:drop-shadow(0 0 18px rgba(150,40,255,.45))}}50%{{filter:drop-shadow(0 0 40px rgba(190,90,255,.85))}}}}

  .grid{{display:flex;flex-wrap:wrap;justify-content:center;gap:46px 70px}}
  .card{{text-decoration:none;color:inherit;display:block}}
  .card:hover{{transform:translateY(-8px) scale(1.04)}}
  .pfp{{position:relative;width:150px;height:150px;margin:0 auto}}
  .av{{
    position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);
    width:78%;height:78%;border-radius:50%;object-fit:cover;display:block;
    border:2px solid rgba(175,80,255,.55);
    box-shadow:0 0 22px rgba(150,40,255,.65),inset 0 0 20px rgba(0,0,0,.8);
    transition:box-shadow .25s ease,border-color .25s ease;
  }}
  .card:hover .av{{box-shadow:0 0 38px rgba(190,90,255,.95),0 0 70px rgba(130,0,255,.55);border-color:#c07bff}}
  .deco{{position:absolute;top:0;left:0;width:100%;height:100%;pointer-events:none}}
  .name{{margin-top:16px;font-size:17px;font-weight:700;letter-spacing:.16em;text-transform:uppercase;color:#fff;text-shadow:0 0 12px rgba(170,60,255,.85)}}
  .tag{{margin-top:4px;font-size:12px;letter-spacing:.06em;color:#9b78c9}}

  /* ---------- SECTION 2 : PLAYER ---------- */
  .stitle{{
    font-size:11px;letter-spacing:.5em;text-transform:uppercase;color:#a683d6;
    margin-bottom:26px;text-shadow:0 0 12px rgba(150,40,255,.6);
  }}
  #player{{
    margin:0 auto;width:min(470px,94vw);display:flex;align-items:center;gap:14px;
    padding:13px 16px;border-radius:16px;
    background:rgba(12,4,22,.82);backdrop-filter:blur(10px);
    border:1px solid rgba(160,60,255,.4);
    box-shadow:0 0 30px rgba(120,0,255,.35),inset 0 0 22px rgba(90,0,180,.22);
  }}
  #art{{
    flex:none;width:58px;height:58px;border-radius:10px;object-fit:cover;display:block;
    border:1px solid rgba(180,90,255,.55);
    box-shadow:0 0 16px rgba(150,40,255,.6);
    transition:transform .3s ease,box-shadow .3s ease;
  }}
  #player.playing #art{{animation:artpulse 2.6s ease-in-out infinite}}
  @keyframes artpulse{{
    0%,100%{{box-shadow:0 0 14px rgba(150,40,255,.55);transform:scale(1)}}
    50%{{box-shadow:0 0 30px rgba(200,110,255,.95);transform:scale(1.045)}}
  }}
  #pp{{
    flex:none;width:38px;height:38px;padding:0;border-radius:50%;cursor:pointer;
    background:rgba(150,50,255,.16);border:1px solid rgba(180,90,255,.6);
    display:flex;align-items:center;justify-content:center;
    box-shadow:0 0 14px rgba(150,40,255,.45);transition:.2s;
  }}
  #pp:hover{{background:rgba(170,70,255,.32);box-shadow:0 0 24px rgba(190,90,255,.85);transform:scale(1.06)}}
  #pp:active{{transform:scale(.94)}}
  #pp svg{{width:15px;height:15px;fill:#efe0ff;display:block;filter:drop-shadow(0 0 6px rgba(200,120,255,.9))}}
  #pp .ico-pause{{display:none}}
  #pp.playing .ico-play{{display:none}}
  #pp.playing .ico-pause{{display:block}}
  .mid{{flex:1;min-width:0;text-align:left}}
  .ttl{{
    font-size:11px;letter-spacing:.24em;text-transform:uppercase;color:#d3b6ff;font-weight:600;
    white-space:nowrap;overflow:hidden;text-overflow:ellipsis;margin-bottom:7px;
    text-shadow:0 0 12px rgba(160,50,255,.75);
  }}
  .bar{{position:relative;height:5px;border-radius:4px;overflow:hidden;background:rgba(255,255,255,.09);pointer-events:none;user-select:none}}
  #fill{{position:absolute;inset:0 auto 0 0;width:0%;border-radius:4px;background:linear-gradient(90deg,#7a1bd6,#c46bff);box-shadow:0 0 12px rgba(180,80,255,.9)}}
  .times{{display:flex;justify-content:space-between;font-size:9.5px;color:#8f6cbf;margin-top:5px;letter-spacing:.08em}}
  .vol{{flex:none;display:flex;align-items:center;gap:7px}}
  .vol svg{{width:15px;height:15px;fill:#b691e8;filter:drop-shadow(0 0 6px rgba(160,60,255,.7))}}
  #vol{{
    -webkit-appearance:none;appearance:none;width:78px;height:4px;border-radius:4px;cursor:pointer;
    background:linear-gradient(90deg,#a63cff var(--v,70%),rgba(255,255,255,.12) var(--v,70%));
    box-shadow:0 0 10px rgba(150,40,255,.4);
  }}
  #vol::-webkit-slider-thumb{{-webkit-appearance:none;width:12px;height:12px;border-radius:50%;background:#e2c8ff;box-shadow:0 0 10px rgba(200,120,255,1);cursor:pointer}}
  #vol::-moz-range-thumb{{width:12px;height:12px;border:0;border-radius:50%;background:#e2c8ff;box-shadow:0 0 10px rgba(200,120,255,1)}}

  /* ---------- SCROLL CUE ---------- */
  .cue{{
    position:absolute;bottom:22px;left:50%;transform:translateX(-50%);
    font-size:9px;letter-spacing:.42em;text-transform:uppercase;color:#6f549b;
    animation:pulse 2.4s ease-in-out infinite;
  }}
  footer{{margin-top:44px;font-size:11px;letter-spacing:.34em;text-transform:uppercase;color:#7d5aa8;text-shadow:0 0 10px rgba(120,0,255,.5)}}

  /* ---------- INFO MODAL ---------- */
  #ov{{
    position:fixed;inset:0;z-index:200;display:flex;align-items:center;justify-content:center;
    padding:24px;background:rgba(2,0,6,.86);backdrop-filter:blur(9px);
    opacity:0;pointer-events:none;transition:opacity .35s ease;
  }}
  #ov.show{{opacity:1;pointer-events:auto}}
  .modal{{
    position:relative;width:min(620px,100%);max-height:84vh;overflow-y:auto;
    padding:40px 38px 34px;border-radius:18px;text-align:left;
    background:linear-gradient(170deg,rgba(24,7,42,.96),rgba(7,2,14,.98));
    border:1px solid rgba(170,70,255,.45);
    box-shadow:0 0 60px rgba(120,0,255,.45),inset 0 0 40px rgba(80,0,170,.28);
    transform:translateY(40px) scale(.9);opacity:0;
    transition:transform .55s cubic-bezier(.16,1,.3,1),opacity .45s ease;
  }}
  #ov.show .modal{{transform:none;opacity:1}}
  .modal::-webkit-scrollbar{{width:6px}}
  .modal::-webkit-scrollbar-thumb{{background:rgba(160,60,255,.5);border-radius:4px}}
  .modal h3{{
    font-size:15px;letter-spacing:.52em;text-transform:uppercase;color:#fff;text-align:center;
    text-shadow:0 0 16px rgba(170,60,255,1);margin-bottom:8px;
  }}
  .modal .mrule{{height:1px;margin:0 0 24px;background:linear-gradient(90deg,transparent,rgba(170,70,255,.8),transparent)}}
  .modal p{{font-size:13.5px;line-height:1.95;color:#c3aade;margin-bottom:15px}}
  .modal strong{{color:#fff;text-shadow:0 0 10px rgba(170,60,255,.7)}}
  .modal .sig{{margin-top:24px;text-align:center;font-size:12px;letter-spacing:.42em;text-transform:uppercase;color:#fff;text-shadow:0 0 14px rgba(170,60,255,.9)}}
  .modal .motto{{margin-top:8px;text-align:center;font-size:10px;letter-spacing:.34em;text-transform:uppercase;color:#9b78c9}}
  #x{{
    position:absolute;top:14px;right:16px;width:30px;height:30px;border-radius:50%;cursor:pointer;
    background:rgba(150,50,255,.14);border:1px solid rgba(180,90,255,.5);color:#e0c9ff;font-size:15px;line-height:1;
    display:flex;align-items:center;justify-content:center;transition:.2s;
  }}
  #x:hover{{background:rgba(180,80,255,.34);box-shadow:0 0 16px rgba(190,90,255,.8)}}

  /* ---------- RIGHT SIDE SECTION NAV ---------- */
  #pageNav{{position:fixed;right:24px;top:50%;transform:translateY(-50%);z-index:120;display:flex;flex-direction:column;align-items:center;gap:15px;padding:0;border:0;border-radius:0;background:transparent;backdrop-filter:none;box-shadow:none;opacity:.92}}
  #pageNav::before{{display:none}}
  .pageDot{{width:7px;height:7px;border-radius:50%;padding:0;border:0;background:rgba(255,255,255,.2);cursor:pointer;position:relative;transition:transform .32s ease,box-shadow .32s ease,background .32s ease}}
  .pageDot::after{{display:none}}
  .pageDot:hover{{transform:scale(1.28);background:rgba(255,255,255,.48)}}
  .pageDot.active{{transform:scale(1.5);background:#eadbff;box-shadow:0 0 10px rgba(205,130,255,.95),0 0 24px rgba(144,50,255,.62)}}
  .pageDot:focus-visible{{outline:none}}
  body.velocity-active::after{{content:"";position:fixed;inset:-20%;pointer-events:none;z-index:2;opacity:var(--trail-opacity,0);background:repeating-linear-gradient(to bottom,rgba(190,100,255,0) 0 10px,rgba(190,100,255,.04) 11px 12px,rgba(190,100,255,0) 13px 30px);transform:translateY(var(--trail-y,0px));filter:blur(1px);mix-blend-mode:screen}}
  @media(max-width:720px){{#pageNav{{right:12px;gap:12px}}.pageDot{{width:6px;height:6px}}}}
  /* ---------- PLAYER ---------- */

  @media(max-width:520px){{
    .grid{{gap:32px}}
    .pfp{{width:118px;height:118px}}
    .sigil img{{width:88px}}
    #vol{{width:52px}}
    #art{{width:48px;height:48px}}
    .modal{{padding:34px 22px 26px}}
  }}
  @media(prefers-reduced-motion:reduce){{
    .vel{{transform:none!important;filter:none!important}}
  }}
</style>
</head>
<body>

  <div id="gate"><img src="{GIF}" alt=""><span>click to enter</span></div>

  <nav id="pageNav" aria-label="Section navigation">
    <button class="pageDot active" type="button" aria-label="Hall of Fame" data-target="s1"></button>
    <button class="pageDot" type="button" aria-label="Music player" data-target="s2"></button>
    <button class="pageDot" type="button" aria-label="About" data-target="s3"></button>
  </nav>

  <!-- ============ 1 : HALL OF FAME ============ -->
  <section id="s1">
    <div class="inner vel">
      <div class="hero reveal"><img src="{LOGO}" alt="7118"></div>

      <div class="sigil-plain reveal" style="--d:.1s"><img src="{GIF}" alt=""></div>
      <div class="rule reveal" style="--d:.15s"></div>
      <div class="hof reveal" style="--d:.2s"><img src="{HOF}" alt="Hall of Fame"></div>
      <div class="grid">{''.join(cards)}</div>
    </div>
    <div class="cue">scroll</div>
  </section>

  <!-- ============ 2 : PLAYER ============ -->
  <section id="s2">
    <div class="inner vel">
      <div class="stitle reveal">music player</div>

      <audio id="au" src="{AUDIO_SRC}" loop preload="auto"></audio>

      <div id="player" class="reveal" style="--d:.1s">
        <img id="art" src="{ALBUM}" alt="cover">
        <button id="pp" type="button" aria-label="Play">
          <svg class="ico-play" viewBox="0 0 24 24"><path d="M8 5.5v13a1 1 0 0 0 1.54.84l10-6.5a1 1 0 0 0 0-1.68l-10-6.5A1 1 0 0 0 8 5.5z"/></svg>
          <svg class="ico-pause" viewBox="0 0 24 24"><path d="M6 4h4v16H6zM14 4h4v16h-4z"/></svg>
        </button>
        <div class="mid">
          <div class="ttl">{TRACK_TITLE}</div>
          <div class="bar"><div id="fill"></div></div>
          <div class="times"><span id="cur">0:00</span><span id="dur">0:00</span></div>
        </div>
        <div class="vol">
          <svg viewBox="0 0 24 24"><path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3a4.5 4.5 0 0 0-2.5-4v8a4.5 4.5 0 0 0 2.5-4zM14 3v2a7 7 0 0 1 0 14v2a9 9 0 0 0 0-18z"/></svg>
          <input id="vol" type="range" min="0" max="100" value="70">
        </div>
      </div>
</div>

    </div>
    <div class="cue">scroll</div>
  </section>

  <!-- ============ 3 : INFO ============ -->
  <section id="s3">
    <div class="inner vel">
      <button class="sigil reveal" id="infoBtn" type="button" aria-label="Open info">
        <img src="{GIF}" alt="">
        <span class="hint">press for info</span>
      </button>
      <footer class="reveal" style="--d:.25s">7118</footer>
    </div>
  </section>

  <!-- ============ INFO ============ -->
  <div id="ov">
    <div class="modal">
      <button id="x" type="button" aria-label="Close">&#10005;</button>
      <h3>Info</h3>
      <div class="mrule"></div>
      <p><strong>7118</strong> is a private digital crew focused on monitoring, documenting, and addressing activity that goes against <strong>Discord&rsquo;s Terms of Service and Community Guidelines</strong>.</p>
      <p>The crew conducts internal investigations into reported incidents, reviews available information, and documents activity involving <strong>harassment, scams, impersonation, malicious behavior, threats, abuse, and other violations</strong> within online communities.</p>
      <p>7118 operates independently as a crew and is <strong>not affiliated with Discord, the NBI, police, or any government law-enforcement agency</strong>.</p>
      <p>When necessary, documented information may be brought to the appropriate platform or authority for review.</p>
      <div class="sig">7118 &mdash; Crew</div>
      <div class="motto">Watch &bull; Document &bull; Stand on Business</div>
    </div>
  </div>

<script src="https://unpkg.com/lenis@1.3.26/dist/lenis.min.js"></script>
<script>
(function(){{
  /* ---------- reveal on section enter ---------- */
  var secs=[].slice.call(document.querySelectorAll('section'));
  var io=new IntersectionObserver(function(es){{
    es.forEach(function(e){{ if(e.isIntersecting) e.target.classList.add('on'); }});
  }},{{threshold:.25}});
  secs.forEach(function(s){{ io.observe(s); }});

  /* ---------- Lenis smooth momentum scroll ---------- */
  var vels = [].slice.call(document.querySelectorAll('.vel'));
  var reduce = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
  var lenis = null;

  function applyVelocity(v){{
    for(var i=0;i<vels.length;i++){{
      var el = vels[i], st = el.style;
      st.setProperty('--vy', (-v * 0.035).toFixed(2) + 'px');
      st.setProperty('--vs', (v * 0.012).toFixed(3) + 'deg');
      st.setProperty('--vz', (1 - Math.min(Math.abs(v) * 0.00022, 0.012)).toFixed(4));
      st.setProperty('--vb', Math.min(Math.abs(v) * 0.008, 0.9).toFixed(2) + 'px');
    }}
    document.body.style.setProperty('--trail-opacity', Math.min(Math.abs(v) * 0.0025, .12).toFixed(3));
    document.body.classList.toggle('velocity-active', Math.abs(v) > 0.9);
  }}

  if(!reduce && window.Lenis){{
    lenis = new Lenis({{
      lerp: 0.085,
      duration: 1.15,
      smoothWheel: true,
      syncTouch: true,
      autoRaf: true,
      anchors: true,
      allowNestedScroll: true,
      naiveDimensions: true,
      stopInertiaOnNavigate: true
    }});
    lenis.on('scroll', function(e){{
      applyVelocity(e.velocity || 0);
      updateActiveFromY(typeof e.animatedScroll === 'number' ? e.animatedScroll : (window.scrollY || 0));
    }});
  }}

  /* ---------- page nav + active section ---------- */
  var dots=[].slice.call(document.querySelectorAll('.pageDot'));
  var activeIndex=-1;
  function setActiveIndex(i){{
    if(i<0 || i>=dots.length || i===activeIndex) return;
    activeIndex=i;
    for(var di=0;di<dots.length;di++){{
      var on=di===i;
      dots[di].classList.toggle('active',on);
      dots[di].setAttribute('aria-current',on?'page':'false');
    }}
  }}
  function updateActiveFromY(y){{
    var viewportCenter=y + window.innerHeight/2;
    var best=0, bestDist=Infinity;
    for(var si=0;si<secs.length;si++){{
      var center=secs[si].offsetTop + secs[si].offsetHeight/2;
      var d=Math.abs(center-viewportCenter);
      if(d<bestDist){{bestDist=d;best=si;}}
    }}
    setActiveIndex(best);
  }}
  dots.forEach(function(dot,idx){{dot.addEventListener('click',function(){{
    var target=document.getElementById(dot.getAttribute('data-target'));
    if(!target)return;
    setActiveIndex(idx);
    if(lenis){{
      lenis.scrollTo(target,{{duration:1.25,lock:true,force:true,immediate:false}});
    }} else {{
      target.scrollIntoView({{behavior:'smooth',block:'start'}});
    }}
  }});}});
  updateActiveFromY(window.scrollY || 0);
  window.addEventListener('scroll',function(){{ updateActiveFromY(window.scrollY || 0); }},{{passive:true}});

  /* ---------- audio ---------- */
  var au=document.getElementById('au'), pp=document.getElementById('pp'),
      fill=document.getElementById('fill'), cur=document.getElementById('cur'),
      dur=document.getElementById('dur'), vol=document.getElementById('vol'),
      gate=document.getElementById('gate'), pl=document.getElementById('player');

  au.volume=0.7; vol.style.setProperty('--v','70%');
  function fmt(s){{ if(!isFinite(s))return '0:00'; s=Math.floor(s);
    return Math.floor(s/60)+':'+('0'+(s%60)).slice(-2); }}

  au.addEventListener('loadedmetadata',function(){{ dur.textContent=fmt(au.duration); }});
  au.addEventListener('timeupdate',function(){{
    if(au.duration) fill.style.width=(au.currentTime/au.duration*100)+'%';
    cur.textContent=fmt(au.currentTime);
  }});
  au.addEventListener('play', function(){{ pp.classList.add('playing');    pl.classList.add('playing');    pp.setAttribute('aria-label','Pause'); }});
  au.addEventListener('pause',function(){{ pp.classList.remove('playing'); pl.classList.remove('playing'); pp.setAttribute('aria-label','Play'); }});
  au.addEventListener('ended',function(){{ pp.classList.remove('playing'); pl.classList.remove('playing'); }});

  pp.addEventListener('click',function(e){{
    e.preventDefault(); e.stopPropagation();
    if(au.paused){{ var p=au.play(); if(p&&p.catch) p.catch(function(){{}}); }} else {{ au.pause(); }}
  }});
  vol.addEventListener('input',function(){{
    au.volume=vol.value/100; vol.style.setProperty('--v',vol.value+'%');
  }});

  /* unskippable */
  var lastT=0;
  au.addEventListener('timeupdate',function(){{ lastT=au.currentTime; }});
  au.addEventListener('seeking',function(){{
    if(Math.abs(au.currentTime-lastT)>1.2) au.currentTime=lastT;
  }});

  /* ---------- gate ---------- */
  gate.addEventListener('click',function(){{
    var p=au.play(); if(p&&p.catch) p.catch(function(){{}});
    gate.classList.add('hide');
    setTimeout(function(){{ gate.remove(); }},800);
  }});

  /* ---------- info modal ---------- */
  var ov=document.getElementById('ov');
  function open(){{ ov.classList.add('show'); }}
  function close(){{ ov.classList.remove('show'); }}
  document.getElementById('infoBtn').addEventListener('click',open);
  document.getElementById('x').addEventListener('click',close);
  ov.addEventListener('click',function(e){{ if(e.target===ov) close(); }});
  document.addEventListener('keydown',function(e){{ if(e.key==='Escape') close(); }});
}})();
</script>
</body>
</html>
'''

with open("index.html", "w") as f:
    f.write(html)
print("bytes:", os.path.getsize("index.html"), "| audio embedded:", os.path.exists(AUDIO_PATH))
