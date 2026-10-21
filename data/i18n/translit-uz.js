// O'zbek lotin ⇄ kirill transliteratsiyasi (Hamzamon, MIT)
// latinToCyr("O'zbekiston") -> "Ўзбекистон";  cyrToLatin("Самарқанд") -> "Samarqand"

const L2C_MULTI = [
  ["O‘", "Ў"], ["o‘", "ў"], ["G‘", "Ғ"], ["g‘", "ғ"],
  ["Oʻ", "Ў"], ["oʻ", "ў"], ["Gʻ", "Ғ"], ["gʻ", "ғ"],
  ["O'", "Ў"], ["o'", "ў"], ["G'", "Ғ"], ["g'", "ғ"],
  ["Sh", "Ш"], ["sh", "ш"], ["SH", "Ш"], ["Ch", "Ч"], ["ch", "ч"], ["CH", "Ч"],
  ["Yo", "Ё"], ["yo", "ё"], ["YO", "Ё"], ["Yu", "Ю"], ["yu", "ю"], ["YU", "Ю"],
  ["Ya", "Я"], ["ya", "я"], ["YA", "Я"], ["Ye", "Е"], ["ye", "е"], ["YE", "Е"],
  ["Ts", "Ц"], ["ts", "ц"],
];
const L2C = {
  a: "а", b: "б", d: "д", e: "е", f: "ф", g: "г", h: "ҳ", i: "и", j: "ж", k: "к", l: "л",
  m: "м", n: "н", o: "о", p: "п", q: "қ", r: "р", s: "с", t: "т", u: "у", v: "в", x: "х",
  y: "й", z: "з", "'": "ъ", "’": "ъ", "ʼ": "ъ",
};
const C2L = {
  а: "a", б: "b", в: "v", г: "g", ғ: "g‘", д: "d", е: "e", ё: "yo", ж: "j", з: "z", и: "i",
  й: "y", к: "k", қ: "q", л: "l", м: "m", н: "n", о: "o", п: "p", р: "r", с: "s", т: "t",
  у: "u", ў: "o‘", ф: "f", х: "x", ҳ: "h", ц: "ts", ч: "ch", ш: "sh", щ: "sh", ъ: "’",
  ь: "", ы: "i", э: "e", ю: "yu", я: "ya",
};

function caseLike(src, out) {
  if (src === src.toLowerCase()) return out;
  return out.charAt(0).toUpperCase() + out.slice(1);
}

export function latinToCyr(text) {
  let s = text;
  // so'z boshidagi "e" -> "э"
  s = s.replace(/(^|[^A-Za-zʻ‘'’])([Ee])/g, (m, p, e) => p + (e === "E" ? "Э" : "э"));
  for (const [a, b] of L2C_MULTI) s = s.split(a).join(b);
  return s.replace(/[A-Za-z'’ʼ]/g, (ch) => {
    const low = L2C[ch.toLowerCase()];
    if (low === undefined) return ch;
    return ch === ch.toLowerCase() ? low : low.toUpperCase();
  });
}

export function cyrToLatin(text) {
  // so'z boshidagi "е" -> "ye"
  let s = text.replace(/(^|[^\u0400-\u04FF])([еЕ])/g, (m, p, e) => p + (e === "Е" ? "Ye" : "ye"));
  return s.replace(/[\u0400-\u04FF]/g, (m) => {
    const low = C2L[m.toLowerCase()];
    if (low === undefined) return m;
    return m === m.toLowerCase() ? low : caseLike(m, low);
  });
}

// Til zanjiri: tanlangan til yo'q bo'lsa keyingisiga o'tadi
export const FALLBACK = { uz: ["uz", "uz-cyrl", "ru", "en"], "uz-cyrl": ["uz-cyrl", "uz", "ru", "en"],
  ru: ["ru", "en"], en: ["en", "ru"], kk: ["kk", "ru", "en"], ky: ["ky", "ru", "en"],
  tg: ["tg", "ru", "en"], tr: ["tr", "en"] };

export function pick(labels, lang) {
  for (const l of FALLBACK[lang] || [lang, "en"]) {
    if (labels?.[l]) return { text: labels[l], lang: l };
    if (l === "uz-cyrl" && labels?.uz) return { text: latinToCyr(labels.uz), lang: l };
    if (l === "uz" && labels?.["uz-cyrl"]) return { text: cyrToLatin(labels["uz-cyrl"]), lang: l };
  }
  return { text: "", lang: null };
}
