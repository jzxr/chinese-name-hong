from openpyxl import load_workbook
from itertools import product

# -----------------------------
# CONFIG
# -----------------------------
EXCEL_PATH = "Chinese Characters.xlsx"

FIRST_CHAR = {
    "char": "洪",
    "pinyin": "hóng",   # set surname pinyin here (or load from Excel if you prefer)
    "element": "木",
    "strokes": 10
}

DESTINY_MEANINGS = {
    31: "（吉）能夠腳踏實地而智勇雙全，性情溫和而寬宏大量，貴人明現。",
    41: "（吉）有才能也有理智，前程似錦，有官運與財運。"
}

TARGET_TOTALS = {31, 41}

# -----------------------------
# LOAD EXCEL DATABASE
# -----------------------------
wb = load_workbook(EXCEL_PATH)
ws = wb.active

characters = []

# Your columns (based on your code):
# row[0] = character
# row[1] = pinyin  
# row[2] = strokes
# row[3] = element

for row in ws.iter_rows(min_row=1, values_only=True):
    try:
        char = row[0]
        pinyin = row[1]            
        strokes = int(row[2])
        element = row[3]
        if char and element and pinyin:
            characters.append({
                "char": char,
                "pinyin": pinyin, 
                "element": element,
                "strokes": strokes
            })
    except:
        continue

# -----------------------------
# FILTER 木 ELEMENT
# -----------------------------
wood_chars = [c for c in characters if c["element"] == "木"]

# -----------------------------
# GENERATE 木木木 COMBINATIONS
# Only keep totals 31 or 41
# -----------------------------
results = []

for second, third in product(wood_chars, repeat=2):
    total_strokes = FIRST_CHAR["strokes"] + second["strokes"] + third["strokes"]

    # Filter totals to only 31 and 41
    if total_strokes not in TARGET_TOTALS:
        continue

    results.append({
        "name": FIRST_CHAR["char"] + second["char"] + third["char"],
        "pinyin": f"{FIRST_CHAR['pinyin']} {second['pinyin']} {third['pinyin']}",  # NEW
        "breakdown": [
            (FIRST_CHAR["char"], FIRST_CHAR["strokes"]),
            (second["char"], second["strokes"]),
            (third["char"], third["strokes"])
        ],
        "total": total_strokes,
        "meaning": DESTINY_MEANINGS[total_strokes]
    })

# -----------------------------
# DISPLAY RESULTS
# -----------------------------
print(f"TOTAL 木木木 NAMES (only 31 or 41 strokes): {len(results)}\n")

for r in results:
    strokes_text = " + ".join(f"{c[1]}({c[0]})" for c in r["breakdown"])
    print(f"Name: {r['name']}")
    print(f"Pinyin: {r['pinyin']}")
    print(f"Total Strokes 筆畫: {strokes_text} = {r['total']}")
    print(f"The meaning of total strokes 數理: {r['meaning']}")
    print("-" * 80)
