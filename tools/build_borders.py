"""Cliopatria (Seshat, CC BY 4.0) -> yillar bo'yicha chegara kesimlari + davlatlar indeksi.

Ishlatish:  python3 -I scripts/build_borders.py raw/cliopatria/cliopatria_polities_only_v021.geojson build
Natija:     build/borders/raw/<yil>.geojson  (keyin mapshaper bilan soddalashtiriladi)
            build/data/polities.json
"""
import json, os, sys

src, out = sys.argv[1], sys.argv[2]

# Kesim yillari: qadimda siyrak, zamonaviyga yaqin zichroq
YEARS = (list(range(-3400, 1500, 100)) + list(range(1500, 1800, 50))
         + list(range(1800, 1900, 25)) + list(range(1900, 2021, 10)) + [2024])

feats = [f for f in json.load(open(src, encoding="utf-8"))["features"]
         if f["properties"]["Type"] == "POLITY" and f["geometry"]]

os.makedirs(f"{out}/borders/raw", exist_ok=True)
os.makedirs(f"{out}/data", exist_ok=True)

slices = []
for y in YEARS:
    sel = [f for f in feats if f["properties"]["FromYear"] <= y <= f["properties"]["ToYear"]]
    fc = {"type": "FeatureCollection", "features": [{
        "type": "Feature",
        "properties": {"n": f["properties"]["Name"], "q": f["properties"]["Wikidata"] or None},
        "geometry": f["geometry"]} for f in sel]}
    json.dump(fc, open(f"{out}/borders/raw/{y}.geojson", "w", encoding="utf-8"), ensure_ascii=False)
    slices.append({"year": y, "count": len(sel)})


def centroid(geom):
    rings = [geom["coordinates"][0]] if geom["type"] == "Polygon" else [p[0] for p in geom["coordinates"]]
    ring = max(rings, key=len)
    return [round(sum(c[0] for c in ring) / len(ring), 3), round(sum(c[1] for c in ring) / len(ring), 3)]


# Davlatlar indeksi: nom bo'yicha birlashtiriladi
idx = {}
for f in feats:
    p = f["properties"]
    e = idx.setdefault(p["Name"], {"name": p["Name"], "qid": p["Wikidata"] or None,
                                   "wiki_en": p["Wikipedia"] or None, "from": p["FromYear"],
                                   "to": p["ToYear"], "max_area_km2": 0, "center": None,
                                   "member_of": p["MemberOf"] or None})
    e["from"] = min(e["from"], p["FromYear"]); e["to"] = max(e["to"], p["ToYear"])
    if p["Area"] and p["Area"] > e["max_area_km2"]:
        e["max_area_km2"] = round(p["Area"]); e["center"] = centroid(f["geometry"])

pol = sorted(idx.values(), key=lambda e: (e["from"], e["name"]))
for i, e in enumerate(pol):
    e["id"] = i
json.dump(pol, open(f"{out}/data/polities.json", "w", encoding="utf-8"), ensure_ascii=False, indent=0)
json.dump(slices, open(f"{out}/borders/index.json", "w"), indent=0)
print(len(pol), "polities;", len(slices), "slices")
