"""Wikidata (CC0) va Wikimedia ma'lumotlarini yig'ish — o'z kompyuteringizda ishga tushiring.

Bulut muhitidan Wikimedia serverlari yopiq, shu sababli bu skript alohida.
Faqat standart kutubxona kerak (Python 3.9+).

    python fetch_wikidata.py            # hammasi
    python fetch_wikidata.py polities   # faqat davlatlar nomlari
    python fetch_wikidata.py events     # tarixiy voqealar
    python fetch_wikidata.py people     # shaxslar

Natija: data/ papkasiga JSON fayllar.
"""
import json, os, sys, time, urllib.parse, urllib.request

LANGS = ["uz", "ru", "en", "kk", "ky", "tg", "tr", "uz-cyrl"]   # yangi til qo'shish: shu ro'yxatga
UA = "HamzamonDataBot/0.1 (educational atlas; contact: your-email@example.com)"
SPARQL = "https://query.wikidata.org/sparql"
API = "https://www.wikidata.org/w/api.php"
HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "..", "data", "data")


def get(url, params):
    req = urllib.request.Request(url + "?" + urllib.parse.urlencode(params), headers={"User-Agent": UA})
    for attempt in range(5):
        try:
            with urllib.request.urlopen(req, timeout=120) as r:
                return json.load(r)
        except Exception as e:  # 429/timeouts -> kutib qayta urinish
            print("  retry", attempt + 1, e); time.sleep(5 * (attempt + 1))
    raise RuntimeError("Wikidata javob bermadi")


def sparql(q):
    return get(SPARQL, {"query": q, "format": "json"})["results"]["bindings"]


def val(b, k):
    return b[k]["value"] if k in b else None


# ---------- 1. Davlatlar (Cliopatria QID'lari) uchun ko'p tilli nomlar, poytaxt, rasm ----------
def polities():
    pol = json.load(open(os.path.join(DATA, "polities.json"), encoding="utf-8"))
    qids = sorted({p["qid"] for p in pol if p["qid"]})
    out = {}
    for i in range(0, len(qids), 50):
        chunk = qids[i:i + 50]
        r = get(API, {"action": "wbgetentities", "ids": "|".join(chunk), "format": "json",
                      "props": "labels|descriptions|sitelinks|claims",
                      "languages": "|".join(LANGS),
                      "sitefilter": "|".join(l.replace("-", "_") + "wiki" for l in LANGS[:7])})
        for q, e in r.get("entities", {}).items():
            cl = e.get("claims", {})
            def first(pid):
                try: return cl[pid][0]["mainsnak"]["datavalue"]["value"]
                except (KeyError, IndexError): return None
            img = first("P18"); cap = first("P36")
            out[q] = {"label": {l: v["value"] for l, v in e.get("labels", {}).items()},
                      "desc": {l: v["value"] for l, v in e.get("descriptions", {}).items()},
                      "wiki": {s[:-4]: v["title"] for s, v in e.get("sitelinks", {}).items()},
                      "image": img, "capital": cap["id"] if isinstance(cap, dict) else None}
        print(f"polities {min(i + 50, len(qids))}/{len(qids)}"); time.sleep(1)
    json.dump(out, open(os.path.join(DATA, "polities_i18n.json"), "w", encoding="utf-8"), ensure_ascii=False)


# ---------- 2. Tarixiy voqealar: sana + koordinata bor, ko'p tilda maqolasi bor (mashhurlik filtri) ----------
EVENTS_Q = """
SELECT ?e ?date ?coord ?img (COUNT(DISTINCT ?sl) AS ?links) WHERE {
  VALUES ?cls { wd:Q1190554 wd:Q178561 wd:Q645883 wd:Q131569 wd:Q3024240 wd:Q124734 wd:Q7944 wd:Q1656682 }
  ?e wdt:P31/wdt:P279* ?cls .
  ?e wdt:P585|wdt:P580 ?date .
  ?e wdt:P625|wdt:P276/wdt:P625 ?coord .
  OPTIONAL { ?e wdt:P18 ?img }
  ?sl schema:about ?e ; schema:isPartOf/wikibase:wikiGroup "wikipedia" .
} GROUP BY ?e ?date ?coord ?img HAVING (COUNT(DISTINCT ?sl) >= 25) LIMIT 6000
"""

# ---------- 3. Shaxslar: tug'ilgan/vafot yili, tug'ilgan joy koordinatasi, mashhurlik ----------
PEOPLE_Q = """
SELECT ?p ?b ?d ?coord ?img ?links WHERE {
  ?p wdt:P31 wd:Q5 ; wikibase:sitelinks ?links .
  FILTER(?links >= 70)
  ?p wdt:P569 ?b .
  OPTIONAL { ?p wdt:P570 ?d }
  OPTIONAL { ?p wdt:P19/wdt:P625 ?coord }
  OPTIONAL { ?p wdt:P18 ?img }
  FILTER(YEAR(?b) < 1960)
} LIMIT 8000
"""

# Markaziy Osiyo shaxslari uchun alohida, past mashhurlik chegarasi bilan
CA_PEOPLE_Q = """
SELECT DISTINCT ?p ?b ?d ?coord ?img ?links WHERE {
  VALUES ?country { wd:Q265 wd:Q232 wd:Q813 wd:Q863 wd:Q874 wd:Q889 wd:Q794 }
  ?p wdt:P31 wd:Q5 ; wikibase:sitelinks ?links ; wdt:P19 ?place .
  ?place wdt:P17 ?country ; wdt:P625 ?coord .
  FILTER(?links >= 15)
  ?p wdt:P569 ?b . OPTIONAL { ?p wdt:P570 ?d } OPTIONAL { ?p wdt:P18 ?img }
  FILTER(YEAR(?b) < 1960)
} LIMIT 3000
"""


def labels_for(qids):
    out = {}
    qids = sorted(set(qids))
    for i in range(0, len(qids), 50):
        r = get(API, {"action": "wbgetentities", "ids": "|".join(qids[i:i + 50]), "format": "json",
                      "props": "labels|descriptions|sitelinks", "languages": "|".join(LANGS),
                      "sitefilter": "uzwiki|ruwiki|enwiki"})
        for q, e in r.get("entities", {}).items():
            out[q] = {"label": {l: v["value"] for l, v in e.get("labels", {}).items()},
                      "desc": {l: v["value"] for l, v in e.get("descriptions", {}).items()},
                      "wiki": {s[:-4]: v["title"] for s, v in e.get("sitelinks", {}).items()}}
        print(f"  labels {min(i + 50, len(qids))}/{len(qids)}"); time.sleep(1)
    return out


def point(c):
    if not c: return None
    lon, lat = c.replace("Point(", "").rstrip(")").split()[:2]
    return [round(float(lon), 3), round(float(lat), 3)]


def year(d):
    if not d: return None
    neg = d.startswith("-"); y = int(d.lstrip("-+").split("-")[0])
    return -y if neg else y


def events():
    rows = sparql(EVENTS_Q); seen = {}
    for b in rows:
        q = val(b, "e").rsplit("/", 1)[1]
        seen.setdefault(q, {"qid": q, "year": year(val(b, "date")), "ll": point(val(b, "coord")),
                            "image": val(b, "img"), "links": int(val(b, "links"))})
    lab = labels_for(seen)
    for q, e in seen.items(): e.update(lab.get(q, {}))
    json.dump(sorted(seen.values(), key=lambda e: e["year"] or 0),
              open(os.path.join(DATA, "events.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print(len(seen), "events")


def people():
    seen = {}
    for qtext in (PEOPLE_Q, CA_PEOPLE_Q):
        for b in sparql(qtext):
            q = val(b, "p").rsplit("/", 1)[1]
            seen.setdefault(q, {"qid": q, "born": year(val(b, "b")), "died": year(val(b, "d")),
                                "ll": point(val(b, "coord")), "image": val(b, "img"),
                                "links": int(val(b, "links"))})
    lab = labels_for(seen)
    for q, e in seen.items(): e.update(lab.get(q, {}))
    json.dump(sorted(seen.values(), key=lambda e: e["born"] or 0),
              open(os.path.join(DATA, "people.json"), "w", encoding="utf-8"), ensure_ascii=False)
    print(len(seen), "people")


if __name__ == "__main__":
    what = sys.argv[1:] or ["polities", "events", "people"]
    for w in what: globals()[w]()
