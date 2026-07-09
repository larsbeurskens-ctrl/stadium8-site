#!/usr/bin/env python3
# Stadium 8 multi-page static site generator (EN + ES). Content-driven: all copy lives in content.json.
import pathlib, re, json

ROOT = pathlib.Path(__file__).resolve().parent
SITE = "https://stadium8.com"
CSSV = "5"

C = json.loads((ROOT / "content.json").read_text(encoding="utf-8"))
B = C["brand"]
PHONE = B["phone"]; WA = B["whatsapp"]; EMAIL = B["email"]; IG = B["instagram"]; FB = B["facebook"]; MAP = B["map"]; ADDR = B["address_html"]

NAV = {
  "en": [("field",C["nav"]["field_en"],"/field/"),("gym",C["nav"]["gym_en"],"/gym/"),
         ("classes",C["nav"]["classes_en"],"/classes/"),("hours",C["nav"]["hours_en"],"/hours/")],
  "es": [("field",C["nav"]["field_es"],"/es/cancha/"),("gym",C["nav"]["gym_es"],"/es/gimnasio/"),
         ("classes",C["nav"]["classes_es"],"/es/clases/"),("hours",C["nav"]["hours_es"],"/es/horarios/")],
}
BOOK = {"en":("/field/#book",C["nav"]["book_en"]),"es":("/es/cancha/#book",C["nav"]["book_es"])}
HOME = {"en":"/","es":"/es/"}
LINKS = {
  "en": {"book":"/field/#book","field":"/field/","gym":"/gym/","classes":"/classes/","hours":"/hours/"},
  "es": {"book":"/es/cancha/#book","field":"/es/cancha/","gym":"/es/gimnasio/","classes":"/es/clases/","hours":"/es/horarios/"},
}

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
    drawer += f'<div class="lang" style="padding:14px 0 2px;font-size:.95rem">{langtog}</div>'
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

def wa_number(wa_link):
    m = re.search(r"wa\.me/506(\d{8})", wa_link or "")
    return f"+506 {m.group(1)[:4]} {m.group(1)[4:]}" if m else ""

def wa_cta_label(inst, lang):
    first = re.split(r"\s*[-,]\s*", (inst or "").strip())[0].strip()
    if not first or re.search(r"studio|team|center|centre|wellness|stadium", first, re.I):
        return "WhatsApp to reserve" if lang=="en" else "WhatsApp para reservar"
    return "WhatsApp " + first.split()[0]

# ====================== SHARED CONTENT BLOCKS ======================
# Cal.com inline embed for the cancha booking (plain string: JS braces must not be f-string-interpolated)
CAL_EMBED = '''<div style="width:100%;min-height:660px;overflow:auto;border-radius:14px;background:#fff;padding:4px" id="cal-cancha"></div>
<script type="text/javascript">
(function (C, A, L) { let p = function (a, ar) { a.q.push(ar); }; let d = C.document; C.Cal = C.Cal || function () { let cal = C.Cal; let ar = arguments; if (!cal.loaded) { cal.ns = {}; cal.q = cal.q || []; d.head.appendChild(d.createElement("script")).src = A; cal.loaded = true; } if (ar[0] === L) { const api = function () { p(api, arguments); }; const namespace = ar[1]; api.q = api.q || []; if (typeof namespace === "string") { cal.ns[namespace] = cal.ns[namespace] || api; p(cal.ns[namespace], ar); p(cal, ["initNamespace", namespace]); } else p(cal, ar); return; } p(cal, ar); }; })(window, "https://app.cal.com/embed/embed.js", "init");
Cal("init", "cancha", { origin: "https://cal.com" });
Cal.ns.cancha("inline", { elementOrSelector: "#cal-cancha", config: { layout: "month_view" }, calLink: "stadium8/cancha" });
Cal.ns.cancha("ui", { hideEventTypeDetails: false, layout: "month_view", cssVarsPerTheme: { light: { "cal-brand": "#F5B400" } } });
</script>'''

def book_block(lang, embed=False):
    s = C["shared"]["book"]; L = lang
    msg = (f'Prefer to message us? <a class="yellow" href="{WA}" style="font-weight:700">WhatsApp us &rarr;</a>' if lang=="en"
      else f'¿Mejor por mensaje? <a class="yellow" href="{WA}" style="font-weight:700">Escribinos por WhatsApp &rarr;</a>')
    bhref, blabel = BOOK[L]
    if embed:
        inner = CAL_EMBED
    else:
        inner = f'<a href="{bhref}" class="btn btn-y" style="margin-top:.2rem">{blabel} &rarr;</a>'
    return f'''<section class="book-sec" id="book">
  <div class="wrap">
    <div class="bookbox">
      <span class="kicker">{s["kicker_"+L]}</span>
      <h3>{s["h3_"+L]}</h3>
      <p>{s["p_"+L]}</p>
      {inner}
      <p style="margin-top:1.4rem">{msg}</p>
    </div>
  </div>
</section>'''

def smoothie_band(lang):
    s = C["shared"]["smoothie"]; L = lang
    return f'''<section class="smoothie" id="smoothie">
  <div class="wrap">
    <div><span style="font-weight:700;letter-spacing:.14em;text-transform:uppercase;font-size:.8rem">{s["eyebrow_"+L]}</span><h2>{s["h2_"+L]}</h2></div>
    <p>{s["p_"+L]}</p>
  </div>
</section>'''

def contact_block(lang):
    s = C["shared"]["contact"]; L = lang; hours = B["hours_"+L]
    if lang=="en":
        return f'''<div class="contact">
  <div class="info">
    <p class="lbl">{s["hours_label_en"]}</p>
    <p>{hours}</p>
    <p class="lbl" style="margin-top:1.4rem">{s["find_label_en"]}</p>
    <p>{ADDR}</p>
    <p class="lbl">{s["contact_label_en"]}</p>
    <p><a href="{WA}">WhatsApp / call: {PHONE}</a></p>
    <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <div class="socials"><a href="{IG}" aria-label="Instagram">IG</a><a href="{FB}" aria-label="Facebook">FB</a></div>
  </div>
  <div class="mapbox"><iframe loading="lazy" title="Stadium 8 location map" src="{MAP}"></iframe></div>
</div>'''
    return f'''<div class="contact">
  <div class="info">
    <p class="lbl">{s["hours_label_es"]}</p>
    <p>{hours}</p>
    <p class="lbl" style="margin-top:1.4rem">{s["find_label_es"]}</p>
    <p>{ADDR}</p>
    <p class="lbl">{s["contact_label_es"]}</p>
    <p><a href="{WA}">WhatsApp / llamadas: {PHONE}</a></p>
    <p><a href="mailto:{EMAIL}">{EMAIL}</a></p>
    <div class="socials"><a href="{IG}" aria-label="Instagram">IG</a><a href="{FB}" aria-label="Facebook">FB</a></div>
  </div>
  <div class="mapbox"><iframe loading="lazy" title="Mapa de ubicación de Stadium 8" src="{MAP}"></iframe></div>
</div>'''

# ====================== CLASSES ======================
CLASSES = C["classes"]

def class_detail(c, lang):
    name = c[lang]; tag = c["tag_"+lang]
    T = C["class_labels"][lang]
    back = LINKS[lang]["classes"]; back_label = T["back"]
    desc=c["desc_"+lang]; sched=c["sched_"+lang]; inst=c["inst"]; level=c["level_"+lang]; price=c["price_"+lang]
    wa=c["wa"]; wal=c["wal_"+lang]; wal_clean=wa_cta_label(c.get("inst",""), lang); wa_num=wa_number(wa)
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
      <a href="{wa}" class="btn btn-y" style="margin-top:1.6rem">{wal_clean} &rarr;</a>
      <p style="color:var(--muted);font-size:.85rem;margin-top:.9rem">{wa_num}</p>
      <p style="color:var(--muted);font-size:.9rem;margin-top:.6rem">{T["note"]}</p>
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

def class_chips(lang):
    more = "Learn more &rarr;" if lang=="en" else "Ver más &rarr;"
    base = LINKS[lang]["classes"]
    return "".join(f'<a class="classcard" href="{base}{c["slug_"+lang]}/"><h4>{c[lang]}</h4><p>{c["tag_"+lang]}</p><span class="go">{more}</span></a>' for c in CLASSES)

# ====================== PAGE BODIES (content-driven, EN + ES) ======================
def feat_lis(items):
    return "\n" + "\n".join(f'        <li>{x}</li>' for x in items) + "\n      "

def home(lang):
    H = C["home"]; hero = H["hero"]; L = lang
    cardhtml = ""
    for cd in H["pick"]["cards"]:
        feat = " feature" if cd["feature"] else ""
        cardhtml += f'<a class="card{feat}" href="{cd["href_"+L]}"><span class="tag">{cd["tag_"+L]}</span><div><h3>{cd["h_"+L]}</h3><p>{cd["p_"+L]}</p></div><span class="go">{cd["go_"+L]}</span></a>'
    chips = class_chips(lang)
    fac = H["facility"]; pick = H["pick"]; ch = H["classes_head"]; vis = H["visit"]
    return f'''<section class="hero">
  <video class="hero-video" autoplay muted loop playsinline preload="auto" poster="/assets/img/stadium8-hero-poster.jpg"><source src="/assets/video/stadium8-hero.mp4" type="video/mp4"></video>
  <span class="eight">8</span>
  <div class="wrap hero-inner">
    <span class="eyebrow">{hero["eyebrow_"+L]}</span>
    <h1>{hero["h1_"+L]}</h1>
    <p class="lead">{hero["lead_"+L]}</p>
    <div class="cta"><a href="{LINKS[L]["book"]}" class="btn btn-y">{hero["cta1_"+L]}</a><a href="{LINKS[L]["classes"]}" class="btn btn-o">{hero["cta2_"+L]}</a></div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-head"><span class="kicker">{pick["kicker_"+L]}</span><h2>{pick["h2_"+L]}</h2><p>{pick["p_"+L]}</p></div>
    <div class="cards">{cardhtml}</div>
  </div>
</section>
<section style="background:#0E0E0E">
  <div class="wrap split">
    <div>
      <span class="kicker">{fac["kicker_"+L]}</span>
      <h2 style="font-size:clamp(2rem,4.5vw,3.1rem);color:#fff;margin:.4rem 0 .8rem">{fac["h2_"+L]}</h2>
      <p style="color:var(--muted)">{fac["p_"+L]}</p>
      <ul class="feat-list">{feat_lis(fac["items_"+L])}</ul>
      <a href="{LINKS[L]["gym"]}" class="btn btn-y" style="margin-top:1.6rem">{fac["btn_"+L]}</a>
    </div>
    {facility_img(lang)}
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-head"><span class="kicker">{ch["kicker_"+L]}</span><h2>{ch["h2_"+L]}</h2><p>{ch["p_"+L]}</p></div>
    <div class="classgrid">{chips}</div>
  </div>
</section>
{book_block(lang)}
{smoothie_band(lang)}
<section>
  <div class="wrap">
    <div class="sec-head"><span class="kicker">{vis["kicker_"+L]}</span><h2>{vis["h2_"+L]}</h2></div>
    {contact_block(lang)}
  </div>
</section>'''

def field(lang):
    F = C["field"]; L = lang
    ch = "".join(f'<div class="card"><div><h3>{cd["h_"+L]}</h3><p>{cd["p_"+L]}</p></div></div>' for cd in F["cards"])
    hours_link = LINKS[L]["hours"]; hours_label = "Hours &amp; fees" if lang=="en" else "Horarios y precios"
    return f'''<section class="subhero has-video">
  <video class="subhero-video" autoplay muted loop playsinline preload="auto" poster="/assets/img/stadium8-hero-poster.jpg"><source src="/assets/video/stadium8-hero.mp4" type="video/mp4"></video>
  <span class="eight">8</span>
  <div class="wrap subhero-inner">
    <span class="eyebrow">{F["eyebrow_"+L]}</span>
    <h1>{F["h1_"+L]}</h1>
    <p class="lead">{F["lead_"+L]}</p>
  </div>
</section>
{book_block(lang, embed=True)}
<section>
  <div class="wrap">
    <div class="sec-head"><span class="kicker">{F["whatbook_kicker_"+L]}</span><h2>{F["whatbook_h2_"+L]}</h2></div>
    <div class="cards">{ch}</div>
    <p style="color:var(--muted);margin-top:1.6rem">{F["footnote_"+L]}<a class="yellow" href="{hours_link}">{hours_label}</a>.</p>
  </div>
</section>'''

def gym(lang):
    G = C["gym"]; L = lang
    hyb = next(c for c in CLASSES if c["key"]=="hybrid"); pt = next(c for c in CLASSES if c["key"]=="pt")
    hybrid_link = LINKS[L]["classes"] + hyb["slug_"+L] + "/"
    pt_link_href = LINKS[L]["classes"] + pt["slug_"+L] + "/"
    noe_alt = "Hybrid Training with Noe - Samara Workout" if lang=="en" else "Entrenamiento Híbrido con Noe - Samara Workout"
    return f'''<section class="subhero has-photo">
  <img class="subhero-photo" src="/assets/img/gym-stadium8.jpg" alt="{G["h1_"+L]}" />
  <span class="eight">8</span>
  <div class="wrap subhero-inner">
    <span class="eyebrow">{G["eyebrow_"+L]}</span>
    <h1>{G["h1_"+L]}</h1>
    <p class="lead">{G["lead_"+L]}</p>
  </div>
</section>
<section>
  <div class="wrap split">
    <div>
      <span class="kicker">{G["gym_kicker_"+L]}</span>
      <h2 style="font-size:clamp(2rem,4.5vw,3.1rem);color:#fff;margin:.4rem 0 .8rem">{G["gym_h2_"+L]}</h2>
      <p style="color:var(--muted)">{G["gym_p_"+L]}</p>
      <ul class="feat-list">{feat_lis(G["gym_items_"+L])}</ul>
      <a href="{LINKS[L]["hours"]}" class="btn btn-y" style="margin-top:1.6rem">{G["gym_btn_"+L]}</a>
    </div>
    <div class="imgslot" style="padding:0;overflow:hidden"><img src="/assets/img/gym-stadium8.jpg" alt="{G["gym_h2_"+L]}" loading="lazy" style="width:100%;height:100%;object-fit:cover;display:block" /></div>
  </div>
</section>
<section style="background:#0E0E0E">
  <div class="wrap split">
    <div>
      <span class="kicker">{G["hybrid_kicker_"+L]}</span>
      <h2 style="font-size:clamp(2rem,4.5vw,3.1rem);color:#fff;margin:.4rem 0 .8rem">{G["hybrid_h2_"+L]}</h2>
      <p style="color:var(--muted)">{G["hybrid_p_"+L]}</p>
      <ul class="feat-list">{feat_lis(G["hybrid_items_"+L])}</ul>
      <a href="{hybrid_link}" class="btn btn-y" style="margin-top:1.6rem">{G["hybrid_btn_"+L]}</a>
    </div>
    <div class="imgslot" style="padding:0;overflow:hidden"><img src="/assets/img/noe%20workout%201.png" alt="{noe_alt}" loading="lazy" style="width:100%;height:100%;object-fit:contain;background:#0B0B0B;display:block" /></div>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-head"><span class="kicker">{G["pt_kicker_"+L]}</span><h2>{G["pt_h2_"+L]}</h2><p>{G["pt_lead_"+L]}</p></div>
    <p style="color:var(--muted);max-width:640px">{G["pt_body_"+L]}</p>
    <a href="https://wa.me/50683423808" class="btn btn-y" style="margin-top:1.4rem">WhatsApp Jeffry &rarr;</a>
    <a href="{pt_link_href}" style="display:inline-block;margin:1.4rem 0 0 1rem;color:var(--yellow);font-weight:700">{G["pt_link_"+L]}</a>
    <p style="color:var(--muted);font-size:.85rem;margin-top:.9rem">+506 8342 3808</p>
  </div>
</section>'''

def classes_page(lang):
    P = C["classes_page"]; L = lang
    chips = class_chips(lang); tt = feat_lis(P["tt_items_"+L])
    return f'''<section class="subhero">
  <span class="eight">8</span>
  <div class="wrap subhero-inner">
    <span class="eyebrow">{P["eyebrow_"+L]}</span>
    <h1>{P["h1_"+L]}</h1>
    <p class="lead">{P["lead_"+L]}</p>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="classgrid">{chips}</div>
    <div class="sec-head" style="margin-top:3rem"><span class="kicker">{P["tt_kicker_"+L]}</span><h2>{P["tt_h2_"+L]}</h2></div>
    <p style="color:var(--muted)">{P["tt_p_"+L]}</p>
    <ul class="feat-list" style="margin-top:1rem">{tt}</ul>
    <p style="color:var(--muted);margin-top:1rem">{P["reserve_note_"+L]} <a class="yellow" href="{WA}" style="font-weight:700">{"WhatsApp us" if lang=="en" else "Escribinos por WhatsApp"} &rarr;</a></p>
  </div>
</section>'''

def hours(lang):
    Hh = C["hours"]; L = lang
    tr = "".join(f'<tr><td>{r["a_"+L]}</td><td style="color:var(--muted)">{r["b_"+L]}</td><td class="amt">{r["c_"+L]}</td></tr>' for r in Hh["rows"])
    return f'''<section class="subhero">
  <span class="eight">8</span>
  <div class="wrap subhero-inner">
    <span class="eyebrow">{Hh["eyebrow_"+L]}</span>
    <h1>{Hh["h1_"+L]}</h1>
    <p class="lead">{Hh["lead_"+L]}</p>
  </div>
</section>
<section>
  <div class="wrap">
    <div class="sec-head"><span class="kicker">{Hh["fees_kicker_"+L]}</span><h2>{Hh["fees_h2_"+L]}</h2></div>
    <table class="ptable"><caption>{Hh["caption_"+L]}</caption><tbody>{tr}</tbody></table>
    <p style="color:var(--muted);margin-top:1.2rem">{Hh["note_"+L]}</p>
  </div>
</section>
<section style="background:#0E0E0E">
  <div class="wrap">
    <div class="sec-head"><span class="kicker">{Hh["visit_kicker_"+L]}</span><h2>{Hh["visit_h2_"+L]}</h2></div>
    {contact_block(lang)}
  </div>
</section>'''
print("page bodies loaded")

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
   "Samara's home of sport. Rent the football field, train in the full gym, join a class, or book a birthday party. Stadium 8 Sport Center, Samara, Guanacaste.", home("en"), SCHEMA),
  ("/es/", "/", "es", "", "Stadium 8 Sport Center | Sámara, Costa Rica",
   "La casa del deporte en Sámara. Alquilá la cancha de fútbol, entrená en el gimnasio, metete a una clase o reservá un cumpleaños. Stadium 8 Sport Center, Sámara, Guanacaste.", home("es"), SCHEMA),
  ("/field/", "/es/cancha/", "en", "field", "Book the field | Stadium 8 Samara",
   "Book Stadium 8's football field, open-court sports or a birthday party in Samara. Pick your time, pay cash on the day.", field("en"), ""),
  ("/es/cancha/", "/field/", "es", "field", "Reservá la cancha | Stadium 8 Sámara",
   "Reservá la cancha de fútbol, deportes de cancha o un cumpleaños en Stadium 8, Sámara. Elegí tu hora, pagás en efectivo.", field("es"), ""),
  ("/gym/", "/es/gimnasio/", "en", "gym", "Gym &amp; training | Stadium 8 Samara",
   "Full gym and personal training at Stadium 8 Samara - free weights, machines, cardio, and coaching for kids and adults.", gym("en"), ""),
  ("/es/gimnasio/", "/gym/", "es", "gym", "Gimnasio y entreno | Stadium 8 Sámara",
   "Gimnasio completo y entrenamiento personal en Stadium 8 Sámara - pesas, máquinas, cardio y coaching para niños y adultos.", gym("es"), ""),
  ("/classes/", "/es/clases/", "en", "classes", "Classes | Stadium 8 Samara",
   "Hybrid training, martial arts, pilates, spinning and personal training at Stadium 8 Samara. Every class has its own page - message us to reserve.", classes_page("en"), ""),
  ("/es/clases/", "/classes/", "es", "classes", "Clases | Stadium 8 Sámara",
   "Entrenamiento híbrido, artes marciales, pilates, spinning y entrenamiento personal en Stadium 8 Sámara. Cada clase tiene su página - escribinos para reservar.", classes_page("es"), ""),
  ("/hours/", "/es/horarios/", "en", "hours", "Hours &amp; fees | Stadium 8 Samara",
   "Opening hours, prices and how to find Stadium 8 Sport Center in Samara, Guanacaste, Costa Rica.", hours("en"), ""),
  ("/es/horarios/", "/hours/", "es", "hours", "Horarios y precios | Stadium 8 Sámara",
   "Horario, precios y cómo encontrar Stadium 8 Sport Center en Sámara, Guanacaste, Costa Rica.", hours("es"), ""),
]

for c in CLASSES:
    en_p=f"/classes/{c['slug_en']}/"; es_p=f"/es/clases/{c['slug_es']}/"
    pages.append((en_p, es_p, "en", "classes", f"{c['en']} class | Stadium 8 Samara", c["tag_en"], class_detail(c,"en"), ""))
    pages.append((es_p, en_p, "es", "classes", f"Clase de {c['es']} | Stadium 8 Sámara", c["tag_es"], class_detail(c,"es"), ""))

written=[]
for path,alt,lang,active,title,desc,body,schema in pages:
    written.append(render(path,alt,lang,active,title,desc,body,schema))

print(f"\n{len(written)} pages generated:")
for w in written: print("  ", w)
