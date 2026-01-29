from openpyxl import load_workbook
from itertools import product

# -----------------------------
# CONFIG
# -----------------------------
EXCEL_PATH = "Chinese Characters.xlsx"

FIRST_CHAR = {
    "char": "洪",
    "pinyin": "hóng",
    "element": "木",
    "strokes": 10
}

DESTINY_MEANINGS = {
    16: "（吉）能夠克己助人而敦厚雅量，安富會榮而福壽雙全。女性則能益夫興家而子孫榮昌，並且賢淑而理家有方。",
    25: "（吉）能得天時與地利，但難以得人和，學識豐富而精神活潑，有領導的能力，若能善用人才則大可成功。至於女性則很有才氣，並且溫和賢淑而有感情。",
    31: "（吉）能夠腳踏實地而智勇雙全，性情溫和而寬宏大量，貴人明現。",
    41: "（吉）有才能也有理智，前程似錦，有官運與財運。",
    45: "（吉）做事一帆風順，智勇雙全必能有所成就。女性則不要虛榮則吉，可助夫益子而使家業興隆。"
}

# Five-element pattern meanings (your text)
PATTERN_MEANINGS = {
    "木木木": {
        "en": "The foundation is stable. The matters you seek can largely be fulfilled as you wish. "
              "The family business will prosper, and both body and mind will remain sound. "
              "With proper care and maintenance, one can enjoy a long life.",
        "zh": "基礎安定，所求之事頗能如願，家業興隆⽽⼼身健全，保養得宜則能長壽"
    },
    "木木土": {
        "en": "With a steady and composed temperament, life circumstances are firm and well-established. "
              "Body and mind remain healthy, bringing lasting happiness and longevity; be forgiving in dealings with others.",
        "zh": "性情能夠穩健，境遇也很堅固，身⼼健康⽽幸福長壽。與⼈相處要寬恕之道"
    },
    "木火水": {
        "en": "Destined to receive support from both superiors and subordinates, enabling steady growth and advancement. "
              "With such harmony and assistance, happiness and longevity are assured.",
        "zh": "能得到上下的幫助⽽發展，幸福長壽"
    },
    "木火土": {
        "en": "With guidance and introductions from elders, one can grow and achieve success. Warm and sincere to others, "
              "especially kind and approachable to those below; enjoys popularity and goodwill—thus happiness and longevity.",
        "zh": "受長輩的引進⽽發展成功，對⼈熱情⽽對下更親切⽽有⼈緣，因此長壽幸福。"
    },
    "木土火": {
        "en": "Blessed with strong interpersonal harmony; a sound foundational fortune supports successful growth and advancement.",
        "zh": "有⼈緣，基礎運健全，能成功發展"
    }
}

# Stroke-combo requests (you can add more tuples anytime)
# Format: PATTERN -> list of (second_strokes, third_strokes)
REQUESTED_COMBOS = {
    "木木木": [(11,10), (1,20), (11,20), (21,10)], 
    "木木土": [(21, 14), (1, 5), (11, 24)],
    "木火土": [(13, 12)],
    # "木火水": [(?, ?)],
    # "木土火": [(?, ?)],
}
PATTERN_TOTAL_FILTERS = {
    "木木木": {31, 41},
    "木木土": {16, 45},
    "木火土": {25}
}
# -----------------------------
# LOAD EXCEL DATABASE
# Expected columns:
# row[0] = character, row[1] = pinyin, row[2] = strokes, row[3] = element
# -----------------------------
wb = load_workbook(EXCEL_PATH)
ws = wb.active

db = []
for row in ws.iter_rows(min_row=1, values_only=True):
    try:
        char = row[0]
        pinyin = row[1]
        strokes = int(row[2])          
        element = row[3]
        if char and pinyin and element:
            db.append({
                "char": char,
                "pinyin": pinyin,
                "strokes": strokes,
                "element": element
            })
    except:
        continue

# Index by (element, strokes) for fast lookup
by_elem_strokes = {}
for c in db:
    key = (c["element"], c["strokes"])
    by_elem_strokes.setdefault(key, []).append(c)

# Also group by element if you ever want "generate all"
by_element = {}
for c in db:
    by_element.setdefault(c["element"], []).append(c)

def print_combo(name, pinyin, breakdown, total, pattern_key):
    strokes_text = " + ".join(f"{s}({ch})" for ch, s in breakdown)

    print(f"Pattern: {pattern_key}")
    print(f"Name: {name}")
    print(f"Pinyin: {pinyin}")
    print(f"Total Strokes 筆畫: {strokes_text} = {total}")

    # Pattern meaning (EN + ZH)
    pm = PATTERN_MEANINGS.get(pattern_key)
    if pm:
        print(f"Pattern Meaning (EN): {pm['en']}")
        print(f"Pattern Meaning (ZH): {pm['zh']}")

    # Total-strokes numerology meaning (by total)
    ds = DESTINY_MEANINGS.get(total)
    if ds:
        print(f"Total-Strokes Numerology 數理({total}): {ds}")
    else:
        print(f"Total-Strokes Numerology 數理({total}): （未定義）")

    print("-" * 110)

def allowed_total(pattern_key, total):
    """Apply per-pattern total-strokes filter if present; otherwise allow all totals."""
    allowed = PATTERN_TOTAL_FILTERS.get(pattern_key)
    if not allowed:
        return True
    return total in allowed

def generate_for_pattern(pattern_key, tuples_list):
    """
    pattern_key like '木木土':
    FIRST is always 木 (洪),
    second element = pattern_key[1],
    third element  = pattern_key[2]
    """
    second_elem = pattern_key[1]
    third_elem  = pattern_key[2]

    # If tuples_list is empty: generate ALL combos for those elements (can be huge!)
    if not tuples_list:
        seconds = by_element.get(second_elem, [])
        thirds  = by_element.get(third_elem, [])
        for second, third in product(seconds, thirds):
            total = FIRST_CHAR["strokes"] + second["strokes"] + third["strokes"]
            if not allowed_total(pattern_key, total):
                continue

            name = FIRST_CHAR["char"] + second["char"] + third["char"]
            pinyin = f"{FIRST_CHAR['pinyin']} {second['pinyin']} {third['pinyin']}"
            breakdown = [(FIRST_CHAR["char"], FIRST_CHAR["strokes"]),
                         (second["char"], second["strokes"]),
                         (third["char"], third["strokes"])]
            print_combo(name, pinyin, breakdown, total, pattern_key)
        return

    # Otherwise: generate only the requested (second_strokes, third_strokes)
    for s2, s3 in tuples_list:
        seconds = by_elem_strokes.get((second_elem, s2), [])
        thirds  = by_elem_strokes.get((third_elem,  s3), [])

        if not seconds or not thirds:
            print(f"[WARN] No match in Excel for {pattern_key} with strokes ({FIRST_CHAR['strokes']}, {s2}, {s3})")
            continue

        for second, third in product(seconds, thirds):
            total = FIRST_CHAR["strokes"] + second["strokes"] + third["strokes"]
            if not allowed_total(pattern_key, total):
                continue

            name = FIRST_CHAR["char"] + second["char"] + third["char"]
            pinyin = f"{FIRST_CHAR['pinyin']} {second['pinyin']} {third['pinyin']}"
            breakdown = [(FIRST_CHAR["char"], FIRST_CHAR["strokes"]),
                         (second["char"], second["strokes"]),
                         (third["char"], third["strokes"])]
            print_combo(name, pinyin, breakdown, total, pattern_key)

# -----------------------------
# RUN: generate your requested combinations + per-pattern total filters
# -----------------------------
for pattern, tuples_list in REQUESTED_COMBOS.items():
    # sanity: all patterns must start with 木 because 洪 is 木
    if not pattern.startswith("木") or len(pattern) != 3:
        print(f"[SKIP] invalid pattern key: {pattern}")
        continue
    generate_for_pattern(pattern, tuples_list)