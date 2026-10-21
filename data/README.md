# Hamzamon — ochiq ma'lumotlar to'plami

Panchronia'ning "Sources and licences" sahifasida ko'rsatilgan **ochiq manbalardan to'g'ridan-to'g'ri** yig'ilgan.
Panchronia'ning o'z matnlari, tanlovlari va faktlari bu yerda **yo'q** — ular mualliflik huquqi bilan himoyalangan.

## Tarkib

| Papka / fayl | Nima | Manba | Litsenziya |
|---|---|---|---|
| `borders/topo/<yil>.topojson` | 73 ta yil kesimi (mil. avv. 3400 — 2024), davlat chegaralari. Xususiyatlar: `n` — nom, `q` — Wikidata QID | Cliopatria v0.21 (Seshat Global History Databank) | CC BY 4.0 |
| `borders/index.json` | kesim yillari va har birida davlatlar soni | o'sha | CC BY 4.0 |
| `data/polities.json` | 1 587 davlat: nom, QID, en-Wikipedia, boshlanish/tugash yili, maks. maydon, markaz koordinatasi | o'sha | CC BY 4.0 |
| `background/<yil>.topojson` | 54 kesim (123 000 yil avval — 2010): xalqlar, madaniyatlar, qabilalar. `n` nom, `s` tobe, `p` tarkibi | historical-basemaps (André Ourednik) | **GPL-3.0** — hosila fayllar ham GPL-3.0 |
| `data/places.json` | 2 340 tarixiy shahar/joy: nom (en/ru/tr), QID, qachondan/qachongacha, koordinata | historical-basemaps | GPL-3.0 |
| `base/countries-50m.json`, `countries-110m.json`, `land-110m.json` | zamonaviy davlatlar va quruqlik (TopoJSON) | Natural Earth, world-atlas orqali | public domain (world-atlas: ISC) |
| `i18n/ui.json` | interfeys matnlari uz/ru/en (yangi til — yangi kalit) | o'zimizniki | MIT |
| `i18n/translit-uz.js` | o'zbek lotin ⇄ kirill + til zanjiri (`pick`) | o'zimizniki | MIT |
| `scripts/` | barcha qayta ishlash skriptlari | o'zimizniki | MIT |

Chegaralar 4 % gacha soddalashtirilgan (mapshaper, `keep-shapes`), fon 5 % gacha.

## Hali yig'ilmagan qism: Wikidata / Wikipedia / Commons

Bulut muhitidan Wikimedia serverlari yopiq. O'z kompyuteringizda ishga tushiring:

```
cd hamzamon
python scripts/fetch_wikidata.py
```

U `data/` ga yozadi:
- `polities_i18n.json` — 1 587 davlat nomi uz, uz-cyrl, ru, en, kk, ky, tg, tr tillarida; Wikipedia havolalari; rasm (P18); poytaxt (P36)
- `events.json` — sana va koordinatasi bor, 25+ Vikipediyada maqolasi bor voqealar (janglar, urushlar, inqiloblar, shartnomalar, ofatlar…)
- `people.json` — 70+ Vikipediyada maqolasi bor shaxslar + Markaziy Osiyoda tug'ilgan shaxslar (15+)

Yangi til qo'shish: skriptdagi `LANGS` ro'yxatiga kod qo'shing va qayta ishga tushiring.
Rasmlar ilovada to'g'ridan-to'g'ri Wikimedia Commons'dan yuklanadi, har birida muallif va litsenziya ko'rsatiladi.

## Atributsiya (saytda ko'rsatish shart)

- Borders: Cliopatria (Seshat Global History Databank), CC BY 4.0 — https://github.com/Seshat-Global-History-Databank/cliopatria
- Background & places: historical-basemaps by André Ourednik, GPL-3.0 — https://github.com/aourednik/historical-basemaps
- Base map: Natural Earth (public domain) via world-atlas
- Labels, dates, coordinates: Wikidata (CC0); summaries: Wikipedia (CC BY-SA 4.0); images: Wikimedia Commons (per image)
