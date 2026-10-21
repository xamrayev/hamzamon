"""Hamzamon: shaxslar portretlari va voqea rasmlarini Wikimedia Commons'dan yuklash.

O'z kompyuteringizda ishga tushiring (Python 3.9+, faqat standart kutubxona):

    python fetch_images.py

Nima qiladi:
  1. wiki_titles.json dagi har bir maqola uchun Vikipediyaning asosiy rasmini topadi.
  2. Commons'dan muallif va litsenziyani oladi. Faqat erkin litsenziyalar qabul qilinadi
     (Public domain, CC0, CC BY, CC BY-SA). Boshqasi o'tkazib yuboriladi.
  3. 360 px kenglikdagi kichik nusxani images/<id>.jpg ga saqlaydi.
  4. images/credits.json ga muallif, litsenziya va manba havolasini yozadi.

Tayyor bo'lgach images/ papkasini menga yuboring — saytga qo'shaman.
"""
import json, os, re, time, urllib.parse, urllib.request

UA = "HamzamonImageBot/0.1 (educational history atlas)"
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "images")
WIDTH = 360
# Har bir rasm orasidagi tanaffus (soniya). 429 (Too Many Requests) kelsa, HZ_DELAY=2 qilib qayta ishga tushiring.
DELAY = float(os.environ.get("HZ_DELAY", "0.5"))
# Erkin litsenziyalar: ijodkor ko‘rsatilsa, tijorat maqsadida ham ishlatish mumkin bo‘lganlari.
FREE = re.compile(r"^(public domain|pd|cc0|cc pdm|no restrictions|attribution|copyrighted free use|ogl|kogl|godl|gfdl|cc[- ]by(?:-sa)?(?:[- ]\d\.\d)?|cc by(?:-sa)? \d\.\d)", re.I)


def api(url, params):
    q = url + "?" + urllib.parse.urlencode({**params, "format": "json", "formatversion": 2})
    req = urllib.request.Request(q, headers={"User-Agent": UA})
    for i in range(4):
        try:
            with urllib.request.urlopen(req, timeout=60) as r:
                return json.load(r)
        except Exception as e:
            print("   retry", e); time.sleep(3 * (i + 1))
    return {}


def strip_html(s):
    return re.sub(r"<[^>]+>", "", s or "").strip()


def main_image(title):
    r = api("https://en.wikipedia.org/w/api.php", {"action": "query", "titles": title, "redirects": 1,
                                                   "prop": "pageimages|pageprops", "piprop": "name"})
    pages = r.get("query", {}).get("pages", [])
    if not pages or "pageimage" not in pages[0]:
        return None, None
    return pages[0]["pageimage"], pages[0].get("pageprops", {}).get("wikibase_item")


def commons_info(filename):
    r = api("https://commons.wikimedia.org/w/api.php", {"action": "query", "titles": "File:" + filename,
                                                        "prop": "imageinfo", "iiprop": "url|extmetadata",
                                                        "iiurlwidth": WIDTH})
    pages = r.get("query", {}).get("pages", [])
    if not pages or "imageinfo" not in pages[0]:
        return None
    ii = pages[0]["imageinfo"][0]; md = ii.get("extmetadata", {})
    lic = strip_html(md.get("LicenseShortName", {}).get("value"))
    return {"thumb": ii.get("thumburl"), "page": ii.get("descriptionurl"), "license": lic,
            "author": strip_html(md.get("Artist", {}).get("value"))[:120] or "Unknown"}


def save(credits):
    json.dump(credits, open(os.path.join(OUT, "credits.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)


def run():
    os.makedirs(OUT, exist_ok=True)
    titles = json.load(open(os.path.join(HERE, "wiki_titles.json"), encoding="utf-8"))
    # Avval yuklangani qayta yuklanmaydi: skriptni istalgan payt to'xtatib, qaytadan ishga tushirish mumkin.
    cpath = os.path.join(OUT, "credits.json")
    credits = json.load(open(cpath, encoding="utf-8")) if os.path.exists(cpath) else {}
    for kind in ("people", "events"):
        for hid, title in titles[kind].items():
            key = ("p:" if kind == "people" else "e:") + hid
            done = credits.get(key)
            if done and os.path.exists(os.path.join(OUT, done["file"])):
                continue
            print(key, "←", title)
            fname, qid = main_image(title)
            if not fname:
                print("   rasm yo'q"); continue
            info = commons_info(fname)
            if not info or not info["thumb"]:
                print("   Commons'da topilmadi"); continue
            if not FREE.match(info["license"]):
                print("   litsenziya mos emas:", info["license"]); continue
            ext = ".png" if info["thumb"].lower().endswith(".png") else ".jpg"
            path = os.path.join(OUT, key.replace(":", "_") + ext)
            req = urllib.request.Request(info["thumb"], headers={"User-Agent": UA})
            with urllib.request.urlopen(req, timeout=60) as r, open(path, "wb") as f:
                f.write(r.read())
            credits[key] = {"file": os.path.basename(path), "author": info["author"], "license": info["license"],
                            "source": info["page"], "qid": qid}
            save(credits)
            time.sleep(DELAY)
    save(credits)
    print("\nTayyor:", len(credits), "ta rasm →", OUT)


if __name__ == "__main__":
    run()
