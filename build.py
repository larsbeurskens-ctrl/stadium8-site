#!/usr/bin/env python3
# Stadium 8 multi-page static site generator (EN + ES). Shared chrome + per-page bodies.
import pathlib, html as _h

ROOT = pathlib.Path("/Users/larsbeurskens/Documents/stadium8-site")
SITE = "https://stadium8.com"
CSSV = "3"

# ---- brand / contact ----
PHONE = "+506 8636 4357"
WA = "https://wa.me/50686364357"
EMAIL = "stadium8sportcenter@gmail.com"
IG = "https://www.instagram.com/stadium.8"
FB = "https://www.facebook.com/stadium8samara/"
MAP = "https://www.google.com/maps?q=Stadium%208%20Sport%20Center%20Samara%20Costa%20Rica&output=embed"
ADDR = "600m West of Super Iguana Verde,<br>Route 160, Samara, Guanacaste, Costa Rica"

NAV = {
  "en": [("field","Field &amp; courts","/field/"),("gym","Gym &amp; training","/gym/"),
         ("classes","Classes","/classes/"),("hours","Hours &amp; fees","/hours/")],
  "es": [("field","Cancha","/es/cancha/"),("gym","Gimnasio","/es/gimnasio/"),
         ("classes","Clases","/es/clases/"),("hours","Horarios","/es/horarios/")],
}
BOOK = {"en":("/field/#book","Book the field"),"es":("/es/cancha/#book","Reservar la cancha")}
HOME = {"en":"/","es":"/es/"}

def head(title, desc, path, lang, alt_path, schema=""):
    canon = SITE + path
    en_alt = path if lang=="en" else alt_path
    es_alt = path if lang=="es" else alt_path
    return f'''<!DOCTYPE html>
<html lang="{lang}">
<head>
<meta charset="UTF-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>{title}</title>
<meta name="description" content="{desc}" />
<link rel="canonical" href="{canon}" />
<link rel="alternate" hreflang="en" href="{SITE}{en_alt}" />
<link rel="alternate" hreflang="es" href="{SITE}{es_alt}" />
<link rel="alternate" hreflang="x-default" href="{SITE}{en_alt}" />
<link rel="icon" href="/assets/img/logo.png" />
<link rel="apple-touch-icon" href="/assets/img/logo.png" />
<meta property="og:title" content="{title}" />
<meta property="og:description" content="{desc}" />
<meta property="og:type" content="website" />
<meta property="og:url" content="{canon}" />
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link href="https://fonts.googleapis.com/css2?family=Anton&family=Inter:wght@400;500;600;700;800&display=swap" rel="stylesheet" />
<link rel="stylesheet" href="/assets/css/style.css?v={CSSV}" />
{schema}</head>
<body>'''

def nav(active, lang, alt_path, path):
    items = ""
    for key,label,href in NAV[lang]:
        cls = ' class="active"' if key==active else ""
        items += f'<a href="{href}"{cls}>{label}</a>'
    bhref,blabel = BOOK[lang]
    if lang=="en":
        langtog = f'<a class="on" href="{path}">EN</a>/<a href="{alt_path}">ES</a>'
    else:
        langtog = f'<a href="{alt_path}">EN</a>/<a class="on" href="{path}">ES</a>'
    drawer = "".join(f'<a href="{href}" style="display:block;padding:10px 0">{label}</a>' for _,label,href in NAV[lang])
    drawer += f'<a href="{bhref}" style="display:block;padding:10px 0;color:var(--yellow);font-weight:700">{blabel}</a>'
    return f'''<header>
  <div class="wrap">
    <nav>
      <a class="brand" href="{HOME[lang]}"><img src="/assets/img/logo.png" alt="Stadium 8 Sport Center logo" /> Stadium <b>8</b></a>
      <div class="navlinks">
        {items}
        <a href="{bhref}" class="btn btn-y" style="padding:.6rem 1.1rem">{blabel}</a>
        <span class="lang">{langtog}</span>
      </div>
      <button class="menubtn" aria-label="Menu" onclick="var m=document.getElementById('m');m.style.display=m.style.display==='block'?'none':'block'">&#9776;</button>
    </nav>
  </div>
  <div id="m" style="display:none;border-top:1px solid var(--line);padding:14px 22px">
    {drawer}
  </div>
</header>'''

def footer(lang):
    built = "Built by Pulpería Studio" if lang=="en" else "Hecho por Pulpería Studio"
    return f'''<footer>
  <div class="wrap">
    <span>&copy; <span id="yr"></span> Stadium 8 Sport Center &middot; Samara, Costa Rica</span>
    <span>{built}</span>
  </div>
</footer>
<script>
document.getElementById('yr').textContent=new Date().getFullYear();
document.querySelectorAll('#m a').forEach(function(a){{a.addEventListener('click',function(){{document.getElementById('m').style.display='none';}});}});
</script>
</body>
</html>'''

def render(path, alt_path, lang, active, title, desc, body, schema=""):
    doc = head(title,desc,path,lang,alt_path,schema) + "\n" + nav(active,lang,alt_path,path) + "\n" + body + "\n" + footer(lang)
    rel = (path.strip("/") + "/index.html") if path != "/" else "index.html"
    if path == "/es/": rel = "es/index.html"
    out = ROOT / rel
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(doc, encoding="utf-8")
    return rel

print("chrome loaded")

# ====================== SHARED CONTENT BLOCKS ======================
def book_block(lang):
    if lang=="en":
        return f'''<section class="book-sec" id="book">
  <div class="wrap">
    <div class="bookbox">
      <span class="kicker">Reserve online</span>
      <h3>Book the field</h3>
      <p>Choose football, badminton or a birthday party, pick your time and you're set. Pay cash on the day - no card needed.</p>
      <div class="cal-placeholder">Booking calendar loads here once the Stadium 8 Google Calendar (stadiumcr@gmail.com) is connected to Cal.com.<br />Coming in the next build step.</div>
      <p style="margin-top:1.4rem">Prefer to message us? <a class="yellow" href="{WA}" style="font-weight:700">WhatsApp {PHONE} &rarr;</a></p>
    </div>
  </div>
</section>'''
    return f'''<section class="book-sec" id="book">
  <div class="wrap">
    <div class="bookbox">
      <span class="kicker">Reservá en línea</span>
      <h3>Reservá la cancha</h3>
      <p>Elegí fútbol, bádminton o una fiesta de cumpleaños, escogé tu hora y listo. Pagás en efectivo el mismo día - sin tarjeta.</p>
      <div class="cal-placeholder">El calendario de reservas carga acá una vez que el Google Calendar de Stadium 8 (stadiumcr@gmail.com) esté conectado a Cal.com.<br />Llega en el próximo paso del build.</div>
      <p style="margin-top:1.4rem">¿Mejor por mensaje? <a class="yellow" href="{WA}" style="font-weight:700">WhatsApp {PHONE} &rarr;</a></p>
    </div>
  </div>
</section>'''

def smoothie_band(lang):
    if lang=="en":
        return f'''<section class="smoothie">
  <div class="wrap">
    <div><span style="font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:.8rem">Refresh. Refuel. Repeat.</span><h2>Visit the smoothie bar</h2></div>
    <p>Cold drinks always on. Stop by reception for a fresh smoothie before or after you train.</p>
  </div>
</section>'''
    return f'''<section class="smoothie">
  <div class="wrap">
    <div><span style="font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:.8rem">Refrescá. Recargá. Repetí.</span><h2>Pasá por el bar de batidos</h2></div>
    <p>Bebidas frías siempre listas. Pasá por recepción por un batido fresco antes o después de entrenar.</p>
  </div>
</section>'''

def contact_block(lang):
    if lang=="en":
        return f'''<div class="contact">
  <div class="info">
    <p class="lbl">Opening hours</p>
    <div class="ph"><b>To confirm.</b> Send us your daily opening hours and we'll drop them straight in.</div>
    <p class="lbl" style="margin-top:1.4rem">Find us</p>
    <p>{ADDR}</p>
    <p class="lbl">Contact</p>
    <p><a href="{WA}">WhatsApp / call: {PHONE}</a></p>
    <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <div class="socials"><a href="{IG}" aria-label="Instagram">IG</a><a href="{FB}" aria-label="Facebook">FB</a></div>
  </div>
  <div class="mapbox"><iframe loading="lazy" title="Stadium 8 location map" src="{MAP}"></iframe></div>
</div>'''
    return f'''<div class="contact">
  <div class="info">
    <p class="lbl">Horario</p>
    <div class="ph"><b>Por confirmar.</b> Mandanos tu horario diario y lo dejamos puesto al toque.</div>
    <p class="lbl" style="margin-top:1.4rem">Dónde estamos</p>
    <p>{ADDR}</p>
    <p class="lbl">Contacto</p>
    <p><a href="{WA}">WhatsApp / llamadas: {PHONE}</a></p>
    <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <div class="socials"><a href="{IG}" aria-label="Instagram">IG</a><a href="{FB}" aria-label="Facebook">FB</a></div>
  </div>
  <div class="mapbox"><iframe loading="lazy" title="Mapa de ubicación de Stadium 8" src="{MAP}"></iframe></div>
</div>'''

# ====================== CLASSES ======================
CLASSES = [
  {"key":"hiit","slug_en":"hiit","slug_es":"hiit","en":"HIIT","es":"HIIT",
   "tag_en":"High-intensity intervals to build strength and burn.","tag_es":"Intervalos de alta intensidad para fuerza y quema."},
  {"key":"boxing","slug_en":"boxing","slug_es":"boxeo","en":"Boxing","es":"Boxeo",
   "tag_en":"Technique, fitness and a serious sweat.","tag_es":"Técnica, estado físico y sudor del bueno."},
  {"key":"pilates","slug_en":"pilates","slug_es":"pilates","en":"Pilates","es":"Pilates",
   "tag_en":"Core, control and mobility, low impact.","tag_es":"Core, control y movilidad, bajo impacto."},
  {"key":"acroyoga","slug_en":"acroyoga","slug_es":"acroyoga","en":"Acroyoga","es":"Acroyoga",
   "tag_en":"Balance, trust and play with a partner.","tag_es":"Equilibrio, confianza y juego en pareja."},
]

def class_detail(c, lang):
    name = c[lang]; tag = c["tag_"+lang]
    if lang=="en":
        back="/classes/"; T={"eyebrow":"Group class","reserve":"Reserve your spot","about":"About the class",
            "ph_about":"A short description of this class goes here - what a session looks like, who it suits, and the vibe. Send us a couple of lines and we'll polish it.",
            "details":"Details","sched":"Schedule","inst":"Instructor","level":"Level","bring":"What to bring",
            "tbc":"To confirm","cta":f"Classes are reserved by message - no online booking needed.","wa":f"WhatsApp to reserve {PHONE}"}
    else:
        back="/es/clases/"; T={"eyebrow":"Clase grupal","reserve":"Reservá tu lugar","about":"Sobre la clase",
            "ph_about":"Acá va una descripción corta de la clase - cómo es una sesión, para quién es y la onda. Mandanos un par de líneas y la pulimos.",
            "details":"Detalles","sched":"Horario","inst":"Instructor","level":"Nivel","bring":"Qué traer",
            "tbc":"Por confirmar","cta":"Las clases se reservan por mensaje - sin reserva en línea.","wa":f"WhatsApp para reservar {PHONE}"}
    return f'''<section class="subhero">
  <span class="eight">8</span>
  <div class="wrap subhero-inner">
    <span class="eyebrow">{T["eyebrow"]}</span>
    <h1>{name}</h1>
    <p class="lead">{tag}</p>
  </div>
</section>
<section>
  <div class="wrap detail-grid">
    <div class="prose">
      <span class="kicker">{T["about"]}</span>
      <h2 style="color:#fff;font-size:clamp(1.7rem,3.5vw,2.4rem);margin:.4rem 0 1rem">{name}</h2>
      <p>{T["ph_about"]}</p>
      <div class="ph">Send us the class description, schedule and instructor and we'll fill this page in.</div>
      <a href="{WA}" class="btn btn-y" style="margin-top:1.6rem">{T["wa"]} &rarr;</a>
      <p style="color:var(--muted);font-size:.9rem;margin-top:1rem">{T["cta"]}</p>
    </div>
    <div class="detail-card">
      <span class="kicker">{T["details"]}</span>
      <div class="row" style="margin-top:.6rem"><div class="lbl">{T["sched"]}</div><div class="val">{T["tbc"]}</div></div>
      <div class="row"><div class="lbl">{T["inst"]}</div><div class="val">{T["tbc"]}</div></div>
      <div class="row"><div class="lbl">{T["level"]}</div><div class="val">{T["tbc"]}</div></div>
      <div class="row"><div class="lbl">{T["bring"]}</div><div class="val">{T["tbc"]}</div></div>
      <a href="{back}" style="display:inline-block;margin-top:1.2rem;color:var(--yellow);font-weight:700;font-size:.9rem">&larr; {"All classes" if lang=="en" else "Todas las clases"}</a>
    </div>
  </div>
</section>'''
print("blocks loaded")

# ====================== EN BODIES ======================
def home_en():
    cards = [
      ("feature","Book online","Field &amp; courts","Football, badminton and birthday parties. Reserve your slot in seconds.","Book the field &rarr;","/field/#book"),
      ("","Open daily","Full gym","Free weights, machines and cardio. Drop in or train with a coach.","More &rarr;","/gym/"),
      ("","All levels","Group classes","HIIT, boxing, pilates and acroyoga with Samara's best instructors.","See the timetable &rarr;","/classes/"),
      ("","One on one","Personal training","Custom programmes for kids and adults, built around your goals.","More &rarr;","/gym/"),
      ("","Parties","Birthday parties","The field, the space and the energy. We host, you celebrate.","Enquire &rarr;","/field/#book"),
      ("","Refuel","Smoothie bar","Cold drinks and fresh smoothies waiting at reception.","More &rarr;","#smoothie"),
    ]
    cardhtml=""
    for cls,tag,h,p,go,href in cards:
        c=" feature" if cls=="feature" else ""
        cardhtml+=f'<a class="card{c}" href="{href}"><span class="tag">{tag}</span><div><h3>{h}</h3><p>{p}</p></div><span class="go">{go}</span></a>'
    chips="".join(f'<a class="classcard" href="/classes/{c["slug_en"]}/"><h4>{c["en"]}</h4><p>{c["tag_en"]}</p><span class="go">Learn more &rarr;</span></a>' for c in CLASSES)
    return f'''<section class="hero">
  <video class="hero-video" autoplay muted loop playsinline preload="auto" poster="/assets/img/stadium8-hero-poster.jpg"><source src="/assets/video/stadium8-hero.mp4" type="video/mp4"></video>
  <span class="eight">8</span>
  <div class="wrap hero-inner">
    <span class="eyebrow">Samara &middot; Guanacaste &middot; Costa Rica</span>
    <h1>Samara's home of <span>sport</span>.</h1>
    <p class="lead">Rent the football field, train in the full gym, jump into a class, or throw a birthday the kids will not forget. One place, every way to move.</p>
    <div class="cta"><a href="/field/#book" class="btn btn-y">Book the field &rarr;</a><a href="/classes/" class="btn btn-o">See classes</a></div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-head"><span class="kicker">What's on</span><h2>Pick your game</h2><p>From a kickabout with friends to a full week of training - here's everything happening under one roof.</p></div>
    <div class="cards">{cardhtml}</div>
  </div>
</section>
<section style="background:#0E0E0E">
  <div class="wrap split">
    <div>
      <span class="kicker">The facility</span>
      <h2 style="font-size:clamp(2rem,4.5vw,3.1rem);color:#fff;margin:.4rem 0 .8rem">Everything you need to train</h2>
      <p style="color:var(--muted)">Samara's only full sports center. Lift in the gym, play on the pitch, take a class, or just relax with a game of bocce. Whatever your level, there's a place for you here.</p>
      <ul class="feat-list">
        <li>Full gym - free weights, machines and cardio</li>
        <li>Football field for matches, pick-up games and rentals</li>
        <li>Group classes: HIIT, boxing, pilates, acroyoga</li>
        <li>Personal training for kids and adults</li>
        <li>Bocce ball and a smoothie bar to refuel</li>
      </ul>
      <a href="/gym/" class="btn btn-y" style="margin-top:1.6rem">Explore the gym &rarr;</a>
    </div>
    <div class="imgslot">[ Photo slot - drop a gym / field shot here: assets/img/gym.jpg ]</div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-head"><span class="kicker">Move with us</span><h2>Classes for every level</h2><p>Each class has its own page with the schedule, the coach and what to bring. Tap to learn more - message us to reserve your spot.</p></div>
    <div class="classgrid">{chips}</div>
  </div>
</section>
{book_block("en")}
{smoothie_band("en")}
<section>
  <div class="wrap">
    <div class="sec-head"><span class="kicker">Plan your visit</span><h2>Hours &amp; where to find us</h2></div>
    {contact_block("en")}
  </div>
</section>'''

def field_en():
    cards=[("Football","Five-a-side, a full match or a kickabout. The pitch is yours by the hour."),
           ("Badminton","Nets up, rackets ready. Book a court for singles or doubles."),
           ("Birthday parties","The field, the space and the energy. We host, you celebrate.")]
    ch="".join(f'<div class="card"><div><h3>{h}</h3><p>{p}</p></div></div>' for h,p in cards)
    return f'''<section class="subhero">
  <span class="eight">8</span>
  <div class="wrap subhero-inner">
    <span class="eyebrow">Reserve online</span>
    <h1>Field &amp; <span>courts</span></h1>
    <p class="lead">Book the football field, a badminton court or a birthday party - pick your time and pay cash on the day.</p>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-head"><span class="kicker">What you can book</span><h2>One pitch, every game</h2></div>
    <div class="cards" style="grid-template-columns:repeat(3,1fr)">{ch}</div>
    <div class="ph" style="margin-top:1.6rem">Field rental rates and party packages live on <a class="yellow" href="/hours/">Hours &amp; fees</a> - send us the prices and we'll add them.</div>
  </div>
</section>
{book_block("en")}'''

def gym_en():
    return f'''<section class="subhero">
  <span class="eight">8</span>
  <div class="wrap subhero-inner">
    <span class="eyebrow">Open daily</span>
    <h1>Gym &amp; <span>training</span></h1>
    <p class="lead">A full gym, personal training for kids and adults, and the space to train however you like.</p>
  </div>
</section>
<section>
  <div class="wrap split">
    <div>
      <span class="kicker">The gym</span>
      <h2 style="font-size:clamp(2rem,4.5vw,3.1rem);color:#fff;margin:.4rem 0 .8rem">Lift, sweat, repeat</h2>
      <p style="color:var(--muted)">Free weights, machines and cardio under one roof. Drop in for a session or train with one of our coaches - whatever your level, there's room to work.</p>
      <ul class="feat-list">
        <li>Free weights and racks</li>
        <li>Resistance machines</li>
        <li>Cardio equipment</li>
        <li>Open daily - hours on the Hours &amp; fees page</li>
      </ul>
      <a href="/hours/" class="btn btn-y" style="margin-top:1.6rem">Hours &amp; drop-in rates &rarr;</a>
    </div>
    <div class="imgslot">[ Photo slot - gym interior: assets/img/gym.jpg ]</div>
  </div>
</section>
<section style="background:#0E0E0E">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">One on one</span><h2>Personal training</h2><p>Custom programmes for kids and adults, built around your goals.</p></div>
    <div class="ph">Send us the trainer details, session options and prices and we'll build this section out.</div>
    <a href="{WA}" class="btn btn-y" style="margin-top:1.4rem">Ask about training &rarr;</a>
  </div>
</section>'''

def classes_en():
    chips="".join(f'<a class="classcard" href="/classes/{c["slug_en"]}/"><h4>{c["en"]}</h4><p>{c["tag_en"]}</p><span class="go">Learn more &rarr;</span></a>' for c in CLASSES)
    return f'''<section class="subhero">
  <span class="eight">8</span>
  <div class="wrap subhero-inner">
    <span class="eyebrow">Move with us</span>
    <h1>Classes for every <span>level</span></h1>
    <p class="lead">HIIT, boxing, pilates and acroyoga with Samara's best instructors. Tap a class for the details - message us to reserve.</p>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="classgrid">{chips}</div>
    <div class="sec-head" style="margin-top:3rem"><span class="kicker">Timetable</span><h2>Weekly schedule</h2></div>
    <div class="ph">Send us the weekly class timetable and we'll lay it out here - day, time and instructor for each class.</div>
    <p style="color:var(--muted);margin-top:1rem">Classes are reserved by message. <a class="yellow" href="{WA}" style="font-weight:700">WhatsApp {PHONE} &rarr;</a></p>
  </div>
</section>'''

def hours_en():
    rows=[("Field rental","per hour"),("Gym drop-in","per visit"),("Class drop-in","per class"),("Personal training","per session"),("Birthday party","per package")]
    tr="".join(f'<tr><td>{a}</td><td style="color:var(--muted)">{b}</td><td class="amt">To confirm</td></tr>' for a,b in rows)
    return f'''<section class="subhero">
  <span class="eight">8</span>
  <div class="wrap subhero-inner">
    <span class="eyebrow">Plan your visit</span>
    <h1>Hours &amp; <span>fees</span></h1>
    <p class="lead">Everything you need to plan a visit - what it costs, when we're open and how to find us.</p>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-head"><span class="kicker">Fees</span><h2>What it costs</h2></div>
    <table class="ptable"><caption>Prices - to confirm</caption><tbody>{tr}</tbody></table>
    <div class="ph" style="margin-top:1.2rem">Send us your prices and we'll swap "To confirm" for the real numbers.</div>
  </div>
</section>
<section style="background:#0E0E0E">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">Plan your visit</span><h2>Hours &amp; where to find us</h2></div>
    {contact_block("en")}
  </div>
</section>'''
print("EN bodies loaded")

# ====================== ES BODIES ======================
def home_es():
    cards = [
      ("feature","Reservá en línea","Cancha","Fútbol, bádminton y fiestas de cumpleaños. Reservá tu espacio en segundos.","Reservá la cancha &rarr;","/es/cancha/#book"),
      ("","Abierto a diario","Gimnasio","Pesas libres, máquinas y cardio. Entrá por el día o entrená con coach.","Más &rarr;","/es/gimnasio/"),
      ("","Todos los niveles","Clases grupales","HIIT, boxeo, pilates y acroyoga con los mejores instructores de Sámara.","Ver el horario &rarr;","/es/clases/"),
      ("","Uno a uno","Entrenamiento personal","Programas a medida para niños y adultos, según tus objetivos.","Más &rarr;","/es/gimnasio/"),
      ("","Fiestas","Cumpleaños","La cancha, el espacio y la energía. Nosotros recibimos, vos celebrás.","Consultá &rarr;","/es/cancha/#book"),
      ("","Recargá","Bar de batidos","Bebidas frías y batidos frescos esperando en recepción.","Más &rarr;","#smoothie"),
    ]
    cardhtml=""
    for cls,tag,h,p,go,href in cards:
        c=" feature" if cls=="feature" else ""
        cardhtml+=f'<a class="card{c}" href="{href}"><span class="tag">{tag}</span><div><h3>{h}</h3><p>{p}</p></div><span class="go">{go}</span></a>'
    chips="".join(f'<a class="classcard" href="/es/clases/{c["slug_es"]}/"><h4>{c["es"]}</h4><p>{c["tag_es"]}</p><span class="go">Ver más &rarr;</span></a>' for c in CLASSES)
    return f'''<section class="hero">
  <video class="hero-video" autoplay muted loop playsinline preload="auto" poster="/assets/img/stadium8-hero-poster.jpg"><source src="/assets/video/stadium8-hero.mp4" type="video/mp4"></video>
  <span class="eight">8</span>
  <div class="wrap hero-inner">
    <span class="eyebrow">Sámara &middot; Guanacaste &middot; Costa Rica</span>
    <h1>La casa del <span>deporte</span> en Sámara.</h1>
    <p class="lead">Alquilá la cancha de fútbol, entrená en el gimnasio completo, metete a una clase o armá un cumpleaños que los chicos no van a olvidar. Un solo lugar, todas las formas de moverte.</p>
    <div class="cta"><a href="/es/cancha/#book" class="btn btn-y">Reservá la cancha &rarr;</a><a href="/es/clases/" class="btn btn-o">Ver clases</a></div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-head"><span class="kicker">Qué hay</span><h2>Elegí tu juego</h2><p>Desde un partidito con amigos hasta una semana completa de entrenamiento - acá está todo lo que pasa bajo un mismo techo.</p></div>
    <div class="cards">{cardhtml}</div>
  </div>
</section>
<section style="background:#0E0E0E">
  <div class="wrap split">
    <div>
      <span class="kicker">Las instalaciones</span>
      <h2 style="font-size:clamp(2rem,4.5vw,3.1rem);color:#fff;margin:.4rem 0 .8rem">Todo lo que necesitás para entrenar</h2>
      <p style="color:var(--muted)">El único centro deportivo completo de Sámara. Levantá en el gimnasio, jugá en la cancha, tomá una clase o relajate con un juego de bocce. Sea cual sea tu nivel, hay un lugar para vos acá.</p>
      <ul class="feat-list">
        <li>Gimnasio completo - pesas libres, máquinas y cardio</li>
        <li>Cancha de fútbol para partidos, mejengas y alquiler</li>
        <li>Clases grupales: HIIT, boxeo, pilates, acroyoga</li>
        <li>Entrenamiento personal para niños y adultos</li>
        <li>Bocce y un bar de batidos para recargar</li>
      </ul>
      <a href="/es/gimnasio/" class="btn btn-y" style="margin-top:1.6rem">Conocé el gimnasio &rarr;</a>
    </div>
    <div class="imgslot">[ Espacio para foto - poné una toma del gimnasio o la cancha: assets/img/gym.jpg ]</div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-head"><span class="kicker">Movete con nosotros</span><h2>Clases para todos los niveles</h2><p>Cada clase tiene su propia página con el horario, el coach y qué traer. Tocá para ver más - escribinos para reservar tu lugar.</p></div>
    <div class="classgrid">{chips}</div>
  </div>
</section>
{book_block("es")}
{smoothie_band("es")}
<section>
  <div class="wrap">
    <div class="sec-head"><span class="kicker">Planeá tu visita</span><h2>Horario y dónde encontrarnos</h2></div>
    {contact_block("es")}
  </div>
</section>'''

def field_es():
    cards=[("Fútbol","Cinco contra cinco, un partido completo o una mejenga. La cancha es tuya por hora."),
           ("Bádminton","Redes puestas, raquetas listas. Reservá una cancha para singles o dobles."),
           ("Cumpleaños","La cancha, el espacio y la energía. Nosotros recibimos, vos celebrás.")]
    ch="".join(f'<div class="card"><div><h3>{h}</h3><p>{p}</p></div></div>' for h,p in cards)
    return f'''<section class="subhero">
  <span class="eight">8</span>
  <div class="wrap subhero-inner">
    <span class="eyebrow">Reservá en línea</span>
    <h1><span>Cancha</span> y canchas</h1>
    <p class="lead">Reservá la cancha de fútbol, una cancha de bádminton o una fiesta de cumpleaños - elegí tu hora y pagás en efectivo el mismo día.</p>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-head"><span class="kicker">Qué podés reservar</span><h2>Una cancha, todos los juegos</h2></div>
    <div class="cards" style="grid-template-columns:repeat(3,1fr)">{ch}</div>
    <div class="ph" style="margin-top:1.6rem">Las tarifas de alquiler y los paquetes de cumpleaños viven en <a class="yellow" href="/es/horarios/">Horarios y precios</a> - mandanos los precios y los agregamos.</div>
  </div>
</section>
{book_block("es")}'''

def gym_es():
    return f'''<section class="subhero">
  <span class="eight">8</span>
  <div class="wrap subhero-inner">
    <span class="eyebrow">Abierto a diario</span>
    <h1><span>Gimnasio</span> y entreno</h1>
    <p class="lead">Un gimnasio completo, entrenamiento personal para niños y adultos, y el espacio para entrenar como más te guste.</p>
  </div>
</section>
<section>
  <div class="wrap split">
    <div>
      <span class="kicker">El gimnasio</span>
      <h2 style="font-size:clamp(2rem,4.5vw,3.1rem);color:#fff;margin:.4rem 0 .8rem">Levantá, sudá, repetí</h2>
      <p style="color:var(--muted)">Pesas libres, máquinas y cardio bajo un mismo techo. Entrá por una sesión o entrená con uno de nuestros coaches - sea cual sea tu nivel, hay espacio para trabajar.</p>
      <ul class="feat-list">
        <li>Pesas libres y racks</li>
        <li>Máquinas de resistencia</li>
        <li>Equipo de cardio</li>
        <li>Abierto a diario - horario en la página de Horarios y precios</li>
      </ul>
      <a href="/es/horarios/" class="btn btn-y" style="margin-top:1.6rem">Horario y tarifas &rarr;</a>
    </div>
    <div class="imgslot">[ Espacio para foto - interior del gimnasio: assets/img/gym.jpg ]</div>
  </div>
</section>
<section style="background:#0E0E0E">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">Uno a uno</span><h2>Entrenamiento personal</h2><p>Programas a medida para niños y adultos, según tus objetivos.</p></div>
    <div class="ph">Mandanos los datos del entrenador, las opciones de sesión y los precios y armamos esta sección.</div>
    <a href="{WA}" class="btn btn-y" style="margin-top:1.4rem">Consultá por entrenamiento &rarr;</a>
  </div>
</section>'''

def classes_es():
    chips="".join(f'<a class="classcard" href="/es/clases/{c["slug_es"]}/"><h4>{c["es"]}</h4><p>{c["tag_es"]}</p><span class="go">Ver más &rarr;</span></a>' for c in CLASSES)
    return f'''<section class="subhero">
  <span class="eight">8</span>
  <div class="wrap subhero-inner">
    <span class="eyebrow">Movete con nosotros</span>
    <h1>Clases para todos los <span>niveles</span></h1>
    <p class="lead">HIIT, boxeo, pilates y acroyoga con los mejores instructores de Sámara. Tocá una clase para ver los detalles - escribinos para reservar.</p>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="classgrid">{chips}</div>
    <div class="sec-head" style="margin-top:3rem"><span class="kicker">Horario</span><h2>Programa semanal</h2></div>
    <div class="ph">Mandanos el horario semanal de clases y lo dejamos acá - día, hora e instructor de cada clase.</div>
    <p style="color:var(--muted);margin-top:1rem">Las clases se reservan por mensaje. <a class="yellow" href="{WA}" style="font-weight:700">WhatsApp {PHONE} &rarr;</a></p>
  </div>
</section>'''

def hours_es():
    rows=[("Alquiler de cancha","por hora"),("Gimnasio por día","por visita"),("Clase suelta","por clase"),("Entrenamiento personal","por sesión"),("Fiesta de cumpleaños","por paquete")]
    tr="".join(f'<tr><td>{a}</td><td style="color:var(--muted)">{b}</td><td class="amt">Por confirmar</td></tr>' for a,b in rows)
    return f'''<section class="subhero">
  <span class="eight">8</span>
  <div class="wrap subhero-inner">
    <span class="eyebrow">Planeá tu visita</span>
    <h1><span>Horarios</span> y precios</h1>
    <p class="lead">Todo lo que necesitás para planear una visita - cuánto cuesta, cuándo abrimos y cómo encontrarnos.</p>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-head"><span class="kicker">Precios</span><h2>Cuánto cuesta</h2></div>
    <table class="ptable"><caption>Precios - por confirmar</caption><tbody>{tr}</tbody></table>
    <div class="ph" style="margin-top:1.2rem">Mandanos tus precios y cambiamos "Por confirmar" por los números reales.</div>
  </div>
</section>
<section style="background:#0E0E0E">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">Planeá tu visita</span><h2>Horario y dónde encontrarnos</h2></div>
    {contact_block("es")}
  </div>
</section>'''
print("ES bodies loaded")

# ====================== SCHEMA (home) ======================
SCHEMA = '''<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "SportsActivityLocation",
  "name": "Stadium 8 Sport Center",
  "description": "Multi-sport facility in Samara, Costa Rica - football field, full gym, group classes, personal training and birthday parties.",
  "image": "https://stadium8.com/assets/img/logo.png",
  "telephone": "+506 8636 4357",
  "email": "stadium8sportcenter@gmail.com",
  "url": "https://stadium8.com/",
  "address": {"@type": "PostalAddress","streetAddress": "600m West of Super Iguana Verde, Route 160","addressLocality": "Samara","addressRegion": "Guanacaste","addressCountry": "CR"},
  "sameAs": ["https://www.instagram.com/stadium.8","https://www.facebook.com/stadium8samara/"]
}
</script>
'''

# ====================== REGISTRY + BUILD ======================
pages = [
  ("/", "/es/", "en", "", "Stadium 8 Sport Center | Samara, Costa Rica",
   "Samara's home of sport. Rent the football field, train in the full gym, join a class, or book a birthday party. Stadium 8 Sport Center, Samara, Guanacaste.", home_en(), SCHEMA),
  ("/es/", "/", "es", "", "Stadium 8 Sport Center | Sámara, Costa Rica",
   "La casa del deporte en Sámara. Alquilá la cancha de fútbol, entrená en el gimnasio, metete a una clase o reservá un cumpleaños. Stadium 8 Sport Center, Sámara, Guanacaste.", home_es(), SCHEMA),
  ("/field/", "/es/cancha/", "en", "field", "Book the field | Stadium 8 Samara",
   "Book Stadium 8's football field, badminton courts or a birthday party in Samara. Pick your time, pay cash on the day.", field_en(), ""),
  ("/es/cancha/", "/field/", "es", "field", "Reservá la cancha | Stadium 8 Sámara",
   "Reservá la cancha de fútbol, las canchas de bádminton o un cumpleaños en Stadium 8, Sámara. Elegí tu hora, pagás en efectivo.", field_es(), ""),
  ("/gym/", "/es/gimnasio/", "en", "gym", "Gym &amp; training | Stadium 8 Samara",
   "Full gym and personal training at Stadium 8 Samara - free weights, machines, cardio, and coaching for kids and adults.", gym_en(), ""),
  ("/es/gimnasio/", "/gym/", "es", "gym", "Gimnasio y entreno | Stadium 8 Sámara",
   "Gimnasio completo y entrenamiento personal en Stadium 8 Sámara - pesas, máquinas, cardio y coaching para niños y adultos.", gym_es(), ""),
  ("/classes/", "/es/clases/", "en", "classes", "Classes | Stadium 8 Samara",
   "HIIT, boxing, pilates and acroyoga classes at Stadium 8 Samara. Every class has its own page - message us to reserve.", classes_en(), ""),
  ("/es/clases/", "/classes/", "es", "classes", "Clases | Stadium 8 Sámara",
   "Clases de HIIT, boxeo, pilates y acroyoga en Stadium 8 Sámara. Cada clase tiene su página - escribinos para reservar.", classes_es(), ""),
  ("/hours/", "/es/horarios/", "en", "hours", "Hours &amp; fees | Stadium 8 Samara",
   "Opening hours, prices and how to find Stadium 8 Sport Center in Samara, Guanacaste, Costa Rica.", hours_en(), ""),
  ("/es/horarios/", "/hours/", "es", "hours", "Horarios y precios | Stadium 8 Sámara",
   "Horario, precios y cómo encontrar Stadium 8 Sport Center en Sámara, Guanacaste, Costa Rica.", hours_es(), ""),
]

# class detail pages (EN + ES) from CLASSES
for c in CLASSES:
    en_p=f"/classes/{c['slug_en']}/"; es_p=f"/es/clases/{c['slug_es']}/"
    pages.append((en_p, es_p, "en", "classes", f"{c['en']} class | Stadium 8 Samara", c["tag_en"], class_detail(c,"en"), ""))
    pages.append((es_p, en_p, "es", "classes", f"Clase de {c['es']} | Stadium 8 Sámara", c["tag_es"], class_detail(c,"es"), ""))

written=[]
for path,alt,lang,active,title,desc,body,schema in pages:
    written.append(render(path,alt,lang,active,title,desc,body,schema))

print(f"\n{len(written)} pages generated:")
for w in written: print("  ", w)
