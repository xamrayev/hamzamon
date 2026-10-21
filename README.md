# Hamzamon — dunyo tarixi O‘zbekiston nigohida

Loyiha muallifi: **Xamrayeva Diana** · Dasturchi: **Xamrayev Xurshidbek** · Ko‘magida: **Nazar AI** (nazarai.uz)

## Tarkib

| Papka | Nima |
|---|---|
| `site/` | Tayyor sayt: `index.html`, kontent (`content.js`, `content2.js`, `content3.js`), chegaralar (`b/`), quruqlik va O‘zbekiston chegarasi |
| `data/` | To‘liq ochiq ma'lumotlar: Cliopatria chegaralari, historical-basemaps foni va joylari, Natural Earth, i18n, litsenziyalar |
| `tools/` | Skriptlar: `build_borders.py` (chegaralarni kesish), `fetch_wikidata.py` (Wikidata nomlari, voqealar, shaxslar), `fetch_images.py` (Commons portretlari) |

## Saytni ishga tushirish

Sayt fayllarni `fetch` orqali yuklaydi, shuning uchun uni to‘g‘ridan-to‘g‘ri ikki marta bosib emas, kichik server orqali oching:

```
cd site
python -m http.server 8000
```

Keyin brauzerda: http://localhost:8000

Hosting uchun `site/` papkasini istalgan statik hostingga (Cloudflare Pages, GitHub Pages, Netlify) yuklash kifoya.

## Rasmlar qo‘shish

```
cd tools
python fetch_images.py
```

Hosil bo‘lgan `images/` papkasini `site/images/` ga ko‘chiring — portretlar va rasmlar avtomatik paydo bo‘ladi.

## Wikidata ma'lumotlari

`tools/fetch_wikidata.py` ni `data/` papkasi yonida ishga tushiring (`data/data/polities.json` dan o‘qiydi). Yangi til uchun skriptdagi `LANGS` ro‘yxatiga kod qo‘shing.

## Yangi til qo‘shish (saytda)

`site/index.html` ichida `LANGS` ro‘yxatiga qator va `STR` lug‘atiga tarjimalar qo‘shing; kontentdagi `{uz, ru, en}` maydonlariga yangi til kalitini yozing. Tarjima bo‘lmasa, keyingi til ko‘rsatiladi.

## Manbalar va litsenziyalar

- Chegaralar: Cliopatria (Seshat Global History Databank), CC BY 4.0
- Fon va tarixiy joylar: historical-basemaps (André Ourednik), GPL-3.0
- Quruqlik va zamonaviy chegaralar: Natural Earth, public domain
- Nomlar, sanalar: Wikidata (CC0); rasmlar: Wikimedia Commons (har biriga alohida)
- Matnlar va kod: Hamzamon
