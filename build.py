#!/usr/bin/env python3
# Stadium 8 multi-page static site generator (EN + ES). Shared chrome + per-page bodies.
import pathlib, html as _h

ROOT = pathlib.Path("/Users/larsbeurskens/Documents/stadium8-site")
SITE = "https://stadium8.com"
CSSV = "5"

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
      <p>Choose football, open-court sports or a birthday party, pick your time and you're set. Pay cash on the day - no card needed.</p>
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
      <p>Elegí fútbol, deportes de cancha o un cumpleaños, escogé tu hora y listo. Pagás en efectivo el mismo día - sin tarjeta.</p>
      <div class="cal-placeholder">El calendario de reservas carga acá una vez que el Google Calendar de Stadium 8 (stadiumcr@gmail.com) esté conectado a Cal.com.<br />Llega en el próximo paso del build.</div>
      <p style="margin-top:1.4rem">¿Mejor por mensaje? <a class="yellow" href="{WA}" style="font-weight:700">WhatsApp {PHONE} &rarr;</a></p>
    </div>
  </div>
</section>'''

def smoothie_band(lang):
    if lang=="en":
        return f'''<section class="smoothie" id="smoothie">
  <div class="wrap">
    <div><span style="font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:.8rem">Watch. Refuel. Repeat.</span><h2>The sports bar</h2></div>
    <p>Live football on the big screen, cold drinks and snacks. Beer ₡1,500 · Powerade ₡1,500 · Water ₡1,000 · Fresco ₡1,000. Fast food coming soon.</p>
  </div>
</section>'''
    return f'''<section class="smoothie" id="smoothie">
  <div class="wrap">
    <div><span style="font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:.8rem">Mirá. Recargá. Repetí.</span><h2>El bar deportivo</h2></div>
    <p>Fútbol en vivo en pantalla grande, bebidas frías y algo para picar. Cerveza ₡1.500 · Powerade ₡1.500 · Agua ₡1.000 · Fresco ₡1.000. Comida rápida muy pronto.</p>
  </div>
</section>'''

def contact_block(lang):
    if lang=="en":
        return f'''<div class="contact">
  <div class="info">
    <p class="lbl">Opening hours</p>
    <p>Mon-Fri 7am-8pm · Sat 7am-3pm · Sun closed</p>
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
    <p>Lun-Vie 7am-8pm · Sáb 7am-3pm · Dom cerrado</p>
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
  {"key":"hybrid","img":"noe workout 1.png","slug_en":"hybrid-training","slug_es":"entrenamiento-hibrido","en":"Hybrid Training","es":"Entrenamiento Híbrido",
   "tag_en":"Strength + cardio. Build muscle and endurance in one session.","tag_es":"Fuerza + cardio. Músculo y resistencia en una sola sesión.",
   "desc_en":"Strength and cardio in one program, so you never have to choose between being strong and having endurance. Every session is different (zero boredom): you build real muscle and strength, improve your stamina, burn fat faster and perform better both in the gym and outside it. Run by Samara Workout with coach Noe.",
   "desc_es":"Fuerza y cardio en un solo programa, para que no tengás que elegir entre ser fuerte o tener resistencia. Cada sesión es diferente (cero aburrimiento): ganás músculo y fuerza real, mejorás tu resistencia, quemás grasa más rápido y rendís mejor dentro y fuera del gym. A cargo de Samara Workout con el entrenador Noe.",
   "sched_en":"Mon-Fri 7am &amp; 8pm · Sat 7am &amp; 3pm · Extra 6am on Mon/Wed/Fri","sched_es":"Lun-Vie 7am y 8pm · Sáb 7am y 3pm · Extra 6am Lun/Mié/Vie",
   "inst":"Noe - Samara Workout","level_en":"All levels","level_es":"Todos los niveles",
   "price_en":"₡25,000 / month · ₡10,000 / week · ₡3,000 / day","price_es":"₡25.000 / mes · ₡10.000 / semana · ₡3.000 / día",
   "wa":WA,"wal_en":f"WhatsApp to reserve {PHONE}","wal_es":f"WhatsApp para reservar {PHONE}"},

  {"key":"martial","img":"martialart 2.png","slug_en":"martial-arts","slug_es":"artes-marciales","en":"Martial Arts","es":"Artes Marciales",
   "tag_en":"Brazilian Jiu-Jitsu &amp; MMA for adults, teens and kids.","tag_es":"Jiu-Jitsu Brasileño y MMA para adultos, jóvenes y niños.",
   "desc_en":"Grappling and striking with Pura Vida Martial Arts: Brazilian Jiu-Jitsu (Gi and No-Gi) and MMA. Adults, teenagers and kids, all levels welcome. Train hard, stay humble, live Pura Vida - all levels, all goals, one family.",
   "desc_es":"Grappling y striking con Pura Vida Martial Arts: Jiu-Jitsu Brasileño (con Gi y sin Gi) y MMA. Adultos, jóvenes y niños, todos los niveles bienvenidos. Entrená duro, mantené la humildad, viví la pura vida - todos los niveles, todas las metas, una sola familia.",
   "sched_en":"Adults BJJ: Mon/Wed/Fri 10-11am &amp; 5-6pm, Tue/Thu 9:30-10:30am &amp; 5-6pm · Kids: Mon&amp;Wed / Tue&amp;Thu 3:30-4:30pm, Sat 10:15-11:15am","sched_es":"BJJ adultos: Lun/Mié/Vie 10-11am y 5-6pm, Mar/Jue 9:30-10:30am y 5-6pm · Niños: Lun y Mié / Mar y Jue 3:30-4:30pm, Sáb 10:15-11:15am",
   "inst":"Oli - Pura Vida Martial Arts","level_en":"All levels · adults, teens &amp; kids","level_es":"Todos los niveles · adultos, jóvenes y niños",
   "price_en":"Ask Oli for class prices","price_es":"Consultá los precios con Oli",
   "wa":"https://wa.me/50686162810","wal_en":"WhatsApp Oli +506 8616 2810","wal_es":"WhatsApp Oli +506 8616 2810"},

  {"key":"pilates","img":"pilates.jpg","slug_en":"pilates-reformer","slug_es":"pilates-reformer","en":"Pilates Reformer","es":"Pilates Reformer",
   "tag_en":"Low-impact, fast results. Posture, core and flexibility.","tag_es":"Bajo impacto, resultados rápidos. Postura, core y flexibilidad.",
   "desc_en":"Personalized Reformer Pilates on 2 beds plus a Wunda chair, in small groups of up to 3 and adapted to every level. Low impact with fast results: improve your posture and ease chronic pain by strengthening the core, gain flexibility, sharpen concentration and coordination, and use the breath as part of every movement.",
   "desc_es":"Pilates Reformer personalizado en 2 camas más una silla Wunda, en grupos pequeños de máximo 3 y adaptado a todos los niveles. Bajo impacto con resultados rápidos: mejorá tu postura y eliminá dolores crónicos fortaleciendo el core, ganá flexibilidad, trabajá la concentración y la coordinación, y usá la respiración como parte del movimiento.",
   "sched_en":"Mon-Fri 8am-5pm","sched_es":"Lun-Vie 8am-5pm",
   "inst":"Wellness studio","level_en":"All levels · max 3 per class","level_es":"Todos los niveles · máx. 3 por clase",
   "price_en":"Ask for class prices","price_es":"Consultá los precios",
   "wa":WA,"wal_en":f"WhatsApp to reserve {PHONE}","wal_es":f"WhatsApp para reservar {PHONE}"},

  {"key":"spinning","img":"spinning.jpg","slug_en":"spinning","slug_es":"spinning","en":"Spinning","es":"Spinning",
   "tag_en":"Intense cardio on the bike. Low impact, big burn.","tag_es":"Cardio intenso en la bici. Bajo impacto, gran quema.",
   "desc_en":"Personalized spinning on 5 bikes, in small groups of up to 5 and open to every level. Burn calories and build endurance with intense cardiovascular training: tone legs and glutes, release endorphins and use your breath to guide the movement, all in a low-impact session.",
   "desc_es":"Spinning personalizado en 5 bicicletas, en grupos pequeños de máximo 5 y para todos los niveles. Quemá calorías y mejorá tu resistencia con entrenamiento cardiovascular intenso: tonificá piernas y glúteos, liberá endorfinas y usá la respiración para guiar el movimiento, todo en una sesión de bajo impacto.",
   "sched_en":"Selected days 4:30-5:30pm &amp; 5:30-6:30pm","sched_es":"Días seleccionados 4:30-5:30pm y 5:30-6:30pm",
   "inst":"Wellness studio","level_en":"All levels · max 5 per class","level_es":"Todos los niveles · máx. 5 por clase",
   "price_en":"Ask for class prices","price_es":"Consultá los precios",
   "wa":WA,"wal_en":f"WhatsApp to reserve {PHONE}","wal_es":f"WhatsApp para reservar {PHONE}"},

  {"key":"aerial","img":"silk areal.jpeg","slug_en":"aerial-silk","slug_es":"acrobacia-aerea","en":"Aerial Silk","es":"Acrobacia Aérea",
   "tag_en":"Strength, grace and confidence on the silks.","tag_es":"Fuerza, gracia y confianza en las telas.",
   "desc_en":"Climb, wrap and pose on the aerial silks - a full-body workout that builds strength, flexibility and body awareness while you learn to move with control and grace. Open to adults and kids. Coached by Celeste.",
   "desc_es":"Subí, envolvete y posá en las telas aéreas - un trabajo de cuerpo completo que desarrolla fuerza, flexibilidad y conciencia corporal mientras aprendés a moverte con control y gracia. Para adultos y niños. A cargo de la coach Celeste.",
   "sched_en":"Tue &amp; Thu 3:30pm (kids classes too)","sched_es":"Mar y Jue 3:30pm (también para niños)",
   "inst":"Celeste","level_en":"All levels · kids &amp; adults","level_es":"Todos los niveles · niños y adultos",
   "price_en":"₡6,000 / class · ₡20,000 / month","price_es":"₡6.000 / clase · ₡20.000 / mes",
   "wa":"https://wa.me/50687494771","wal_en":"WhatsApp Celeste +506 8749 4771","wal_es":"WhatsApp Celeste +506 8749 4771"},

  {"key":"pt","img":"personal trainer 1.png","slug_en":"personal-training","slug_es":"entrenamiento-personal","en":"Personal Training","es":"Entrenamiento Personal",
   "tag_en":"One-on-one coaching built around your goals.","tag_es":"Entrenamiento uno a uno según tus metas.",
   "desc_en":"One-on-one coaching with Jeffry Z., a certified personal trainer and Human Movement Sciences (Physical Education) student. Whether it's weight loss, muscle gain or simply better health, you get a plan tailored to you: customized workout plans, one-on-one sessions and online coaching. Book a free consultation to start.",
   "desc_es":"Entrenamiento uno a uno con Jeffry Z., entrenador personal certificado y estudiante de Ciencias del Movimiento Humano (Educación Física). Ya sea bajar de peso, ganar músculo o simplemente estar más sano, recibís un plan hecho para vos: rutinas personalizadas, sesiones uno a uno y coaching en línea. Reservá una consulta gratis para empezar.",
   "sched_en":"By appointment","sched_es":"Con cita previa",
   "inst":"Jeffry Z. - certified trainer","level_en":"All levels · kids &amp; adults","level_es":"Todos los niveles · niños y adultos",
   "price_en":"Free first consultation · ask for session rates","price_es":"Primera consulta gratis · consultá las tarifas",
   "wa":"https://wa.me/50683423808","wal_en":"WhatsApp Jeffry +506 8342 3808","wal_es":"WhatsApp Jeffry +506 8342 3808"},
]

def class_detail(c, lang):
    name = c[lang]; tag = c["tag_"+lang]
    if lang=="en":
        back="/classes/"; back_label="All classes"
        T={"eyebrow":"Class","about":"About the class","details":"Details","sched":"Schedule","inst":"Instructor","level":"Level","price":"Price",
           "note":"Classes are reserved by message - no online booking needed. Times can change; the trainer can update this anytime."}
    else:
        back="/es/clases/"; back_label="Todas las clases"
        T={"eyebrow":"Clase","about":"Sobre la clase","details":"Detalles","sched":"Horario","inst":"Instructor","level":"Nivel","price":"Precio",
           "note":"Las clases se reservan por mensaje - sin reserva en línea. Los horarios pueden cambiar; el entrenador lo puede actualizar cuando quiera."}
    desc=c["desc_"+lang]; sched=c["sched_"+lang]; inst=c["inst"]; level=c["level_"+lang]; price=c["price_"+lang]
    wa=c["wa"]; wal=c["wal_"+lang]
    _img=c.get("img","")
    img_html = (f'<img src="/assets/img/{_img.replace(" ","%20")}" alt="{name}" loading="lazy" style="width:100%;max-height:460px;object-fit:contain;background:#0E0E0E;border-radius:14px;display:block;margin-bottom:1.4rem;border:1px solid rgba(255,255,255,.08)" />' if (_img and (ROOT/"assets/img"/_img).exists()) else "")
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
      {img_html}
      <span class="kicker">{T["about"]}</span>
      <h2 style="color:#fff;font-size:clamp(1.7rem,3.5vw,2.4rem);margin:.4rem 0 1rem">{name}</h2>
      <p>{desc}</p>
      <a href="{wa}" class="btn btn-y" style="margin-top:1.6rem">{wal} &rarr;</a>
      <p style="color:var(--muted);font-size:.9rem;margin-top:1rem">{T["note"]}</p>
    </div>
    <div class="detail-card">
      <span class="kicker">{T["details"]}</span>
      <div class="row" style="margin-top:.6rem"><div class="lbl">{T["sched"]}</div><div class="val">{sched}</div></div>
      <div class="row"><div class="lbl">{T["inst"]}</div><div class="val">{inst}</div></div>
      <div class="row"><div class="lbl">{T["level"]}</div><div class="val">{level}</div></div>
      <div class="row"><div class="lbl">{T["price"]}</div><div class="val">{price}</div></div>
      <a href="{back}" style="display:inline-block;margin-top:1.2rem;color:var(--yellow);font-weight:700;font-size:.9rem">&larr; {back_label}</a>
    </div>
  </div>
</section>'''
print("blocks loaded")

def _img_exists(fn):
    return bool(fn) and (ROOT / "assets/img" / fn).exists()

def facility_img(lang):
    if _img_exists("stadium8-hero-poster.jpg"):
        alt = "Stadium 8 Sport Center" if lang=="en" else "Stadium 8 Sport Center"
        return f'<div class="imgslot" style="padding:0;overflow:hidden"><img src="/assets/img/stadium8-hero-poster.jpg" alt="{alt}" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block" /></div>'
    return '<div class="imgslot">[ Photo slot - assets/img/stadium8-hero-poster.jpg ]</div>' if lang=="en" else '<div class="imgslot">[ Espacio para foto ]</div>'

# ====================== EN BODIES ======================
def home_en():
    cards = [
      ("feature","Book online","Field &amp; courts","Football 5, open-court sports and birthday parties. Reserve in seconds.","Book the field &rarr;","/field/#book"),
      ("","Open daily","Full gym","Free weights, machines and cardio. Drop in or train with a coach.","More &rarr;","/gym/"),
      ("","All levels","Group classes","Hybrid training, martial arts, pilates and spinning with Samara's own coaches.","See the classes &rarr;","/classes/"),
      ("","One on one","Personal training","Custom programmes for kids and adults, built around your goals.","More &rarr;","/gym/"),
      ("","Parties","Birthday parties","The field, the space and the energy. We host, you celebrate.","Enquire &rarr;","/field/#book"),
      ("","Watch the match","Sports bar","Live football, cold drinks and snacks. Fast food coming soon.","More &rarr;","#smoothie"),
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
        <li>Group classes: hybrid training, martial arts, pilates, spinning, aerial silk</li>
        <li>Personal training for kids and adults</li>
        <li>A sports bar to refuel and watch the match</li>
      </ul>
      <a href="/gym/" class="btn btn-y" style="margin-top:1.6rem">Explore the gym &rarr;</a>
    </div>
    {facility_img("en")}
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
    cards=[("Football 5","Five-a-side (5v5) for men, women and kids. ₡10,000 per team or ₡20,000 per hour. Reserve on WhatsApp, plan online and find a match."),
           ("Open-court sports","Volleyball, badminton, handball, ultimate frisbee, athletics, foot-tennis or free court time. ₡2,000 per person."),
           ("Birthdays &amp; events","Birthday parties and private events - the field, the space and the energy. Price depends on the event.")]
    ch="".join(f'<div class="card"><div><h3>{h}</h3><p>{p}</p></div></div>' for h,p in cards)
    return f'''<section class="subhero has-video">
  <video class="subhero-video" autoplay muted loop playsinline preload="auto" poster="/assets/img/stadium8-hero-poster.jpg"><source src="/assets/video/stadium8-hero.mp4" type="video/mp4"></video>
  <span class="eight">8</span>
  <div class="wrap subhero-inner">
    <span class="eyebrow">Reserve online</span>
    <h1>Field &amp; <span>courts</span></h1>
    <p class="lead">Book the football field, open-court sports or a birthday - pick your time and pay cash on the day.</p>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-head"><span class="kicker">What you can book</span><h2>One pitch, every game</h2></div>
    <div class="cards" style="grid-template-columns:repeat(3,1fr)">{ch}</div>
    <p style="color:var(--muted);margin-top:1.6rem">Football 5: ₡10,000/team or ₡20,000/hour · Open-court sports: ₡2,000/person · Birthdays &amp; events: price on request. Full list on <a class="yellow" href="/hours/">Hours &amp; fees</a>.</p>
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
  <div class="wrap split">
    <div>
      <span class="kicker">Train with Noe</span>
      <h2 style="font-size:clamp(2rem,4.5vw,3.1rem);color:#fff;margin:.4rem 0 .8rem">Hybrid Training</h2>
      <p style="color:var(--muted)">Strength and cardio in one program with Samara Workout. Build real muscle and endurance, burn fat and perform better - and every session is different. All levels welcome.</p>
      <ul class="feat-list">
        <li>Mon-Fri 7am &amp; 8pm, Sat 7am &amp; 3pm (extra 6am Mon/Wed/Fri)</li>
        <li>₡25,000 / month · ₡10,000 / week · ₡3,000 / day</li>
        <li>Coach Noe · all levels</li>
      </ul>
      <a href="/classes/hybrid-training/" class="btn btn-y" style="margin-top:1.6rem">Hybrid Training details &rarr;</a>
    </div>
    <div class="imgslot" style="padding:0;overflow:hidden"><img src="/assets/img/noe%20workout%201.png" alt="Hybrid Training with Noe - Samara Workout" loading="lazy" style="width:100%;height:100%;object-fit:contain;background:#0B0B0B;display:block" /></div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-head"><span class="kicker">One on one</span><h2>Personal training</h2><p>Custom programmes for kids and adults, built around your goals.</p></div>
    <p style="color:var(--muted);max-width:640px">One-on-one coaching with Jeffry Z., a certified personal trainer and Human Movement Sciences student. Customized workout plans, one-on-one sessions and online coaching - for weight loss, muscle gain or just better health. Your first consultation is free.</p>
    <a href="https://wa.me/50683423808" class="btn btn-y" style="margin-top:1.4rem">WhatsApp Jeffry +506 8342 3808 &rarr;</a>
    <a href="/classes/personal-training/" style="display:inline-block;margin:1.4rem 0 0 1rem;color:var(--yellow);font-weight:700">Personal training details &rarr;</a>
  </div>
</section>'''

def classes_en():
    chips="".join(f'<a class="classcard" href="/classes/{c["slug_en"]}/"><h4>{c["en"]}</h4><p>{c["tag_en"]}</p><span class="go">Learn more &rarr;</span></a>' for c in CLASSES)
    return f'''<section class="subhero">
  <span class="eight">8</span>
  <div class="wrap subhero-inner">
    <span class="eyebrow">Move with us</span>
    <h1>Classes for every <span>level</span></h1>
    <p class="lead">Hybrid training, martial arts, pilates, spinning, aerial silk and personal training with Samara's own coaches. Tap a class for the details - message us to reserve.</p>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="classgrid">{chips}</div>
    <div class="sec-head" style="margin-top:3rem"><span class="kicker">Timetable</span><h2>Weekly schedule</h2></div>
    <p style="color:var(--muted)">Each class keeps its own times - open a class above for the full schedule. Quick guide:</p>
    <ul class="feat-list" style="margin-top:1rem">
      <li>Hybrid Training - Mon-Fri 7am &amp; 8pm, Sat 7am &amp; 3pm (extra 6am Mon/Wed/Fri)</li>
      <li>Martial Arts - adults &amp; kids, mornings &amp; evenings (BJJ &amp; MMA)</li>
      <li>Pilates Reformer - Mon-Fri 8am-5pm</li>
      <li>Spinning - selected afternoons 4:30 &amp; 5:30pm</li>
      <li>Aerial Silk - Tue &amp; Thu 3:30pm (kids too)</li>
      <li>Personal Training - by appointment</li>
    </ul>
    <p style="color:var(--muted);margin-top:1rem">Classes are reserved by message. <a class="yellow" href="{WA}" style="font-weight:700">WhatsApp {PHONE} &rarr;</a></p>
  </div>
</section>'''

def hours_en():
    rows=[("Football 5","per team / per hour","₡10,000 / ₡20,000"),
          ("Open-court sports","volleyball, badminton, handball, ultimate, athletics, foot-tennis","₡2,000 / person"),
          ("Hybrid Training","month / week / day","₡25,000 / ₡10,000 / ₡3,000"),
          ("Other classes","pilates, spinning, martial arts, personal training","Ask the trainer"),
          ("Birthdays &amp; events","private events","Price on request"),
          ("Sports bar","beer / Powerade / water / fresco","₡1,500 / ₡1,500 / ₡1,000 / ₡1,000")]
    tr="".join(f'<tr><td>{a}</td><td style="color:var(--muted)">{b}</td><td class="amt">{c}</td></tr>' for a,b,c in rows)
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
    <table class="ptable"><caption>Prices in colones (₡)</caption><tbody>{tr}</tbody></table>
    <p style="color:var(--muted);margin-top:1.2rem">Class prices for pilates, spinning, martial arts and personal training are set by each trainer - just ask on WhatsApp. Gym drop-in rates coming soon.</p>
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
      ("feature","Reservá en línea","Cancha","Fútbol 5, deportes de cancha y cumpleaños. Reservá tu espacio en segundos.","Reservá la cancha &rarr;","/es/cancha/#book"),
      ("","Abierto a diario","Gimnasio","Pesas libres, máquinas y cardio. Entrá por el día o entrená con coach.","Más &rarr;","/es/gimnasio/"),
      ("","Todos los niveles","Clases grupales","Entrenamiento híbrido, artes marciales, pilates y spinning con los coaches de Sámara.","Ver las clases &rarr;","/es/clases/"),
      ("","Uno a uno","Entrenamiento personal","Programas a medida para niños y adultos, según tus objetivos.","Más &rarr;","/es/gimnasio/"),
      ("","Fiestas","Cumpleaños","La cancha, el espacio y la energía. Nosotros recibimos, vos celebrás.","Consultá &rarr;","/es/cancha/#book"),
      ("","Mirá el partido","Bar deportivo","Fútbol en vivo, bebidas frías y algo para picar. Comida rápida muy pronto.","Más &rarr;","#smoothie"),
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
        <li>Clases grupales: entrenamiento híbrido, artes marciales, pilates, spinning, acrobacia aérea</li>
        <li>Entrenamiento personal para niños y adultos</li>
        <li>Un bar deportivo para recargar y ver el partido</li>
      </ul>
      <a href="/es/gimnasio/" class="btn btn-y" style="margin-top:1.6rem">Conocé el gimnasio &rarr;</a>
    </div>
    {facility_img("es")}
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
    cards=[("Fútbol 5","Cinco contra cinco (5v5) para hombres, mujeres y niños. ₡10.000 por equipo o ₡20.000 por hora. Reservá por WhatsApp, planeá en línea y buscá reto."),
           ("Deportes de cancha","Voleibol, bádminton, handball, ultimate frisbee, atletismo, fútbol-tenis o cancha libre. ₡2.000 por persona."),
           ("Cumpleaños y eventos","Cumpleaños y eventos privados - la cancha, el espacio y la energía. El precio depende del evento.")]
    ch="".join(f'<div class="card"><div><h3>{h}</h3><p>{p}</p></div></div>' for h,p in cards)
    return f'''<section class="subhero has-video">
  <video class="subhero-video" autoplay muted loop playsinline preload="auto" poster="/assets/img/stadium8-hero-poster.jpg"><source src="/assets/video/stadium8-hero.mp4" type="video/mp4"></video>
  <span class="eight">8</span>
  <div class="wrap subhero-inner">
    <span class="eyebrow">Reservá en línea</span>
    <h1><span>Cancha</span> y canchas</h1>
    <p class="lead">Reservá la cancha de fútbol, deportes de cancha o un cumpleaños - elegí tu hora y pagás en efectivo el mismo día.</p>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-head"><span class="kicker">Qué podés reservar</span><h2>Una cancha, todos los juegos</h2></div>
    <div class="cards" style="grid-template-columns:repeat(3,1fr)">{ch}</div>
    <p style="color:var(--muted);margin-top:1.6rem">Fútbol 5: ₡10.000/equipo o ₡20.000/hora · Deportes de cancha: ₡2.000/persona · Cumpleaños y eventos: precio a consultar. Lista completa en <a class="yellow" href="/es/horarios/">Horarios y precios</a>.</p>
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
  <div class="wrap split">
    <div>
      <span class="kicker">Entrená con Noe</span>
      <h2 style="font-size:clamp(2rem,4.5vw,3.1rem);color:#fff;margin:.4rem 0 .8rem">Entrenamiento Híbrido</h2>
      <p style="color:var(--muted)">Fuerza y cardio en un solo programa con Samara Workout. Ganá músculo y resistencia real, quemá grasa y rendí mejor - y cada sesión es diferente. Todos los niveles.</p>
      <ul class="feat-list">
        <li>Lun-Vie 7am y 8pm, Sáb 7am y 3pm (extra 6am Lun/Mié/Vie)</li>
        <li>₡25.000 / mes · ₡10.000 / semana · ₡3.000 / día</li>
        <li>Coach Noe · todos los niveles</li>
      </ul>
      <a href="/es/clases/entrenamiento-hibrido/" class="btn btn-y" style="margin-top:1.6rem">Ver Entrenamiento Híbrido &rarr;</a>
    </div>
    <div class="imgslot" style="padding:0;overflow:hidden"><img src="/assets/img/noe%20workout%201.png" alt="Entrenamiento Híbrido con Noe - Samara Workout" loading="lazy" style="width:100%;height:100%;object-fit:contain;background:#0B0B0B;display:block" /></div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-head"><span class="kicker">Uno a uno</span><h2>Entrenamiento personal</h2><p>Programas a medida para niños y adultos, según tus objetivos.</p></div>
    <p style="color:var(--muted);max-width:640px">Entrenamiento uno a uno con Jeffry Z., entrenador personal certificado y estudiante de Ciencias del Movimiento Humano. Rutinas personalizadas, sesiones uno a uno y coaching en línea - para bajar de peso, ganar músculo o simplemente estar más sano. La primera consulta es gratis.</p>
    <a href="https://wa.me/50683423808" class="btn btn-y" style="margin-top:1.4rem">WhatsApp Jeffry +506 8342 3808 &rarr;</a>
    <a href="/es/clases/entrenamiento-personal/" style="display:inline-block;margin:1.4rem 0 0 1rem;color:var(--yellow);font-weight:700">Ver entrenamiento personal &rarr;</a>
  </div>
</section>'''

def classes_es():
    chips="".join(f'<a class="classcard" href="/es/clases/{c["slug_es"]}/"><h4>{c["es"]}</h4><p>{c["tag_es"]}</p><span class="go">Ver más &rarr;</span></a>' for c in CLASSES)
    return f'''<section class="subhero">
  <span class="eight">8</span>
  <div class="wrap subhero-inner">
    <span class="eyebrow">Movete con nosotros</span>
    <h1>Clases para todos los <span>niveles</span></h1>
    <p class="lead">Entrenamiento híbrido, artes marciales, pilates, spinning, acrobacia aérea y entrenamiento personal con los coaches de Sámara. Tocá una clase para ver los detalles - escribinos para reservar.</p>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="classgrid">{chips}</div>
    <div class="sec-head" style="margin-top:3rem"><span class="kicker">Horario</span><h2>Programa semanal</h2></div>
    <p style="color:var(--muted)">Cada clase tiene su propio horario - abrí una clase arriba para verlo completo. Guía rápida:</p>
    <ul class="feat-list" style="margin-top:1rem">
      <li>Entrenamiento Híbrido - Lun-Vie 7am y 8pm, Sáb 7am y 3pm (extra 6am Lun/Mié/Vie)</li>
      <li>Artes Marciales - adultos y niños, mañanas y tardes (BJJ y MMA)</li>
      <li>Pilates Reformer - Lun-Vie 8am-5pm</li>
      <li>Spinning - tardes seleccionadas 4:30 y 5:30pm</li>
      <li>Acrobacia Aérea - Mar y Jue 3:30pm (también niños)</li>
      <li>Entrenamiento Personal - con cita previa</li>
    </ul>
    <p style="color:var(--muted);margin-top:1rem">Las clases se reservan por mensaje. <a class="yellow" href="{WA}" style="font-weight:700">WhatsApp {PHONE} &rarr;</a></p>
  </div>
</section>'''

def hours_es():
    rows=[("Fútbol 5","por equipo / por hora","₡10.000 / ₡20.000"),
          ("Deportes de cancha","voleibol, bádminton, handball, ultimate, atletismo, fútbol-tenis","₡2.000 / persona"),
          ("Entrenamiento Híbrido","mes / semana / día","₡25.000 / ₡10.000 / ₡3.000"),
          ("Otras clases","pilates, spinning, artes marciales, entreno personal","Consultá al entrenador"),
          ("Cumpleaños y eventos","eventos privados","Precio a consultar"),
          ("Bar deportivo","cerveza / Powerade / agua / fresco","₡1.500 / ₡1.500 / ₡1.000 / ₡1.000")]
    tr="".join(f'<tr><td>{a}</td><td style="color:var(--muted)">{b}</td><td class="amt">{c}</td></tr>' for a,b,c in rows)
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
    <table class="ptable"><caption>Precios en colones (₡)</caption><tbody>{tr}</tbody></table>
    <p style="color:var(--muted);margin-top:1.2rem">Los precios de pilates, spinning, artes marciales y entrenamiento personal los pone cada entrenador - consultá por WhatsApp. Tarifas del gimnasio por día muy pronto.</p>
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
   "Book Stadium 8's football field, open-court sports or a birthday party in Samara. Pick your time, pay cash on the day.", field_en(), ""),
  ("/es/cancha/", "/field/", "es", "field", "Reservá la cancha | Stadium 8 Sámara",
   "Reservá la cancha de fútbol, deportes de cancha o un cumpleaños en Stadium 8, Sámara. Elegí tu hora, pagás en efectivo.", field_es(), ""),
  ("/gym/", "/es/gimnasio/", "en", "gym", "Gym &amp; training | Stadium 8 Samara",
   "Full gym and personal training at Stadium 8 Samara - free weights, machines, cardio, and coaching for kids and adults.", gym_en(), ""),
  ("/es/gimnasio/", "/gym/", "es", "gym", "Gimnasio y entreno | Stadium 8 Sámara",
   "Gimnasio completo y entrenamiento personal en Stadium 8 Sámara - pesas, máquinas, cardio y coaching para niños y adultos.", gym_es(), ""),
  ("/classes/", "/es/clases/", "en", "classes", "Classes | Stadium 8 Samara",
   "Hybrid training, martial arts, pilates, spinning and personal training at Stadium 8 Samara. Every class has its own page - message us to reserve.", classes_en(), ""),
  ("/es/clases/", "/classes/", "es", "classes", "Clases | Stadium 8 Sámara",
   "Entrenamiento híbrido, artes marciales, pilates, spinning y entrenamiento personal en Stadium 8 Sámara. Cada clase tiene su página - escribinos para reservar.", classes_es(), ""),
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
