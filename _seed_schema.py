#!/usr/bin/env python3
# Generates sections-schema.json - drives the /admin editor. Each section has a dot-path into content.json.
import json, pathlib
ROOT = pathlib.Path("/Users/larsbeurskens/Documents/stadium8-site")

def tx(id, label, **kw): return {"id": id, "type": "text", "label": label, **kw}
def ht(id, label, **kw): return {"id": id, "type": "textarea_html", "label": label, **kw}
def bi(base, label, type="text", **kw):
    f = ht if type == "textarea_html" else tx
    return [f(base+"_en", label+" (EN)", **kw), f(base+"_es", label+" (ES)", **kw)]
def sec(id, path, label, fields): return {"id": id, "path": path, "label": label, "fields": fields}

SCHEMA = {"version": 1, "groups": []}

SCHEMA["groups"].append({"id": "global", "label": "Global · brand & contact", "sections": [
  sec("brand", "brand", "Brand & contact details", [
    tx("phone", "Phone"), tx("whatsapp", "WhatsApp link (wa.me URL)"), tx("email", "Email"),
    tx("instagram", "Instagram URL"), tx("facebook", "Facebook URL"), tx("map", "Google Maps embed URL"),
    ht("address_html", "Address (use <br> for line break)"),
    tx("hours_en", "Opening hours line (EN)"), tx("hours_es", "Opening hours line (ES)"),
  ]),
  sec("nav", "nav", "Navigation labels", [
    *bi("field", "Field nav label"), *bi("gym", "Gym nav label"), *bi("classes", "Classes nav label"),
    *bi("hours", "Hours nav label"), *bi("book", "Book button label"),
  ]),
  sec("book", "shared.book", "Booking CTA block (field page)", [
    *bi("kicker", "Kicker"), *bi("h3", "Heading"), *bi("p", "Paragraph", "textarea_html"),
  ]),
  sec("smoothie", "shared.smoothie", "Sports bar band", [
    *bi("eyebrow", "Eyebrow"), *bi("h2", "Heading"), *bi("p", "Paragraph", "textarea_html"),
  ]),
  sec("contact", "shared.contact", "Contact block labels", [
    *bi("hours_label", "Hours label"), *bi("find_label", "Find-us label"), *bi("contact_label", "Contact label"),
  ]),
]})

SCHEMA["groups"].append({"id": "home", "label": "Home page", "sections": [
  sec("home_hero", "home.hero", "Hero", [
    *bi("eyebrow", "Eyebrow"), *bi("h1", "Headline (use <span> for accent)", "textarea_html"),
    *bi("lead", "Lead paragraph", "textarea_html"), *bi("cta1", "Button 1 label"), *bi("cta2", "Button 2 label"),
  ]),
  sec("home_pick", "home.pick", "\"Pick your game\" cards", [
    *bi("kicker", "Kicker"), *bi("h2", "Heading"), *bi("p", "Intro paragraph", "textarea_html"),
    {"id": "cards", "type": "list", "label": "Cards", "item_label": "Card", "item_fields": [
      {"id": "feature", "type": "bool", "label": "Featured (large) card"},
      tx("href_en", "Link (EN)"), tx("href_es", "Link (ES)"),
      *bi("tag", "Tag"), *bi("h", "Title"), *bi("p", "Text", "textarea_html"), *bi("go", "Link label"),
    ]},
  ]),
  sec("home_facility", "home.facility", "Facility section", [
    *bi("kicker", "Kicker"), *bi("h2", "Heading"), *bi("p", "Paragraph", "textarea_html"),
    {"id": "items_en", "type": "list_text", "label": "Bullet points (EN)"},
    {"id": "items_es", "type": "list_text", "label": "Bullet points (ES)"},
    *bi("btn", "Button label"),
  ]),
  sec("home_classes_head", "home.classes_head", "Classes section header", [
    *bi("kicker", "Kicker"), *bi("h2", "Heading"), *bi("p", "Paragraph", "textarea_html"),
  ]),
  sec("home_visit", "home.visit", "Visit section header", [*bi("kicker", "Kicker"), *bi("h2", "Heading")]),
]})

SCHEMA["groups"].append({"id": "field", "label": "Field / Cancha page", "sections": [
  sec("field_hero", "field", "Hero + booking section", [
    *bi("eyebrow", "Eyebrow"), *bi("h1", "Headline (use <span>)", "textarea_html"), *bi("lead", "Lead", "textarea_html"),
    *bi("whatbook_kicker", "\"What you can book\" kicker"), *bi("whatbook_h2", "\"What you can book\" heading"),
    {"id": "cards", "type": "list", "label": "Booking cards", "item_label": "Card", "item_fields": [
      *bi("h", "Title"), *bi("p", "Text", "textarea_html")]},
    *bi("footnote", "Footnote (before Hours link)", "textarea_html"),
  ]),
]})

SCHEMA["groups"].append({"id": "gym", "label": "Gym page", "sections": [
  sec("gym_hero", "gym", "Hero", [*bi("eyebrow", "Eyebrow"), *bi("h1", "Headline (use <span>)", "textarea_html"), *bi("lead", "Lead", "textarea_html")]),
  sec("gym_main", "gym", "The gym block", [
    *bi("gym_kicker", "Kicker"), *bi("gym_h2", "Heading"), *bi("gym_p", "Paragraph", "textarea_html"),
    {"id": "gym_items_en", "type": "list_text", "label": "Bullets (EN)"}, {"id": "gym_items_es", "type": "list_text", "label": "Bullets (ES)"},
    *bi("gym_btn", "Button label"), *bi("gym_imgslot", "Image-slot placeholder text"),
  ]),
  sec("gym_hybrid", "gym", "Hybrid Training block", [
    *bi("hybrid_kicker", "Kicker"), *bi("hybrid_h2", "Heading"), *bi("hybrid_p", "Paragraph", "textarea_html"),
    {"id": "hybrid_items_en", "type": "list_text", "label": "Bullets (EN)"}, {"id": "hybrid_items_es", "type": "list_text", "label": "Bullets (ES)"},
    *bi("hybrid_btn", "Button label"),
  ]),
  sec("gym_pt", "gym", "Personal training block", [
    *bi("pt_kicker", "Kicker"), *bi("pt_h2", "Heading"), *bi("pt_lead", "Lead", "textarea_html"),
    *bi("pt_body", "Body", "textarea_html"), *bi("pt_wa_label", "WhatsApp button label"), *bi("pt_link", "Details link label"),
  ]),
]})

SCHEMA["groups"].append({"id": "classes_page", "label": "Classes page", "sections": [
  sec("classes_hero", "classes_page", "Hero + timetable", [
    *bi("eyebrow", "Eyebrow"), *bi("h1", "Headline (use <span>)", "textarea_html"), *bi("lead", "Lead", "textarea_html"),
    *bi("tt_kicker", "Timetable kicker"), *bi("tt_h2", "Timetable heading"), *bi("tt_p", "Timetable intro", "textarea_html"),
    {"id": "tt_items_en", "type": "list_text", "label": "Timetable lines (EN)"}, {"id": "tt_items_es", "type": "list_text", "label": "Timetable lines (ES)"},
    *bi("reserve_note", "Reserve note (before WhatsApp link)"),
  ]),
]})

SCHEMA["groups"].append({"id": "hours", "label": "Hours & fees page", "sections": [
  sec("hours_hero", "hours", "Hero + fees", [
    *bi("eyebrow", "Eyebrow"), *bi("h1", "Headline (use <span>)", "textarea_html"), *bi("lead", "Lead", "textarea_html"),
    *bi("fees_kicker", "Fees kicker"), *bi("fees_h2", "Fees heading"), *bi("caption", "Table caption"),
    {"id": "rows", "type": "list", "label": "Fee rows", "item_label": "Row", "item_fields": [
      *bi("a", "Item"), *bi("b", "Detail"), *bi("c", "Price")]},
    *bi("note", "Note under table", "textarea_html"),
    *bi("visit_kicker", "Visit kicker"), *bi("visit_h2", "Visit heading"),
  ]),
]})

SCHEMA["groups"].append({"id": "class_list", "label": "Classes (detail pages)", "sections": [
  {"id": "classes", "path": "classes", "label": "Class detail pages", "type": "list_root",
   "item_label": "Class", "summary_field": "en", "item_fields": [
     tx("en", "Name (EN)"), tx("es", "Name (ES)"),
     *bi("tag", "Tagline"), *bi("desc", "Description", "textarea_html"), *bi("sched", "Schedule"),
     tx("inst", "Instructor"), *bi("level", "Level"), *bi("price", "Price"),
     tx("wa", "WhatsApp link"), tx("wal_en", "WhatsApp label (EN)"), tx("wal_es", "WhatsApp label (ES)"),
     tx("img", "Image filename (assets/img/)"), tx("slug_en", "URL slug (EN)"), tx("slug_es", "URL slug (ES)"),
   ]},
]})

(ROOT / "sections-schema.json").write_text(json.dumps(SCHEMA, ensure_ascii=False, indent=2), encoding="utf-8")
groups = SCHEMA["groups"]
print("sections-schema.json written:", (ROOT/"sections-schema.json").stat().st_size, "bytes")
print("groups:", [g["id"] for g in groups])
print("total sections:", sum(len(g["sections"]) for g in groups))
