from openpyxl import load_workbook
from itertools import product
from typing import Dict, List, Tuple, Any, Optional
from rules.zodiac_rules import check_horse_year_char
from config import (
    FIRST_CHAR, DESTINY_MEANINGS, PATTERN_MEANINGS,
    REQUESTED_COMBOS, PATTERN_TOTAL_FILTERS
)

def stroke_to_element(strokes: int) -> str:
    last = strokes % 10
    if last in (1, 2):
        return "木"
    if last in (3, 4):
        return "火"
    if last in (5, 6):
        return "土"
    if last in (7, 8):
        return "金"
    return "水"

def compute_five_grids(first: int, second: int, third: int) -> Dict[str, Tuple[int, str]]:
    tian = first + 1
    ren = first + second
    di = second + third
    zong = first + second + third  # NO +1
    return {
        "天格": (tian, stroke_to_element(tian)),
        "人格": (ren, stroke_to_element(ren)),
        "地格": (di, stroke_to_element(di)),
        "總格": (zong, stroke_to_element(zong)),
    }

def compute_pattern_elements(first: int, second: int, third: int) -> Dict[str, Any]:
    A = first + 1
    B = first + second
    C = second + third
    return {
        "calc_text": (
            f"{first}+1={A}({stroke_to_element(A)}) · "
            f"{first}+{second}={B}({stroke_to_element(B)}) · "
            f"{second}+{third}={C}({stroke_to_element(C)})"
        ),
        "elements": stroke_to_element(A) + stroke_to_element(B) + stroke_to_element(C),
        "A": A, "B": B, "C": C
    }

def allowed_destiny_total(pattern_key: str, destiny_total: int) -> bool:
    allowed = PATTERN_TOTAL_FILTERS.get(pattern_key)
    return True if not allowed else destiny_total in allowed

def load_db_raw(excel_path: str):
    """
    Raw loader (NO streamlit caching here).
    Excel columns:
      row[0]=char
      row[1]=pinyin
      row[2]=strokes
      row[3]=element
      row[4]=horse_rule (NEW)
      row[5]=EN meaning  (shifted)
      row[6]=ZH meaning  (shifted)
    Return: db, by_strokes, by_char
    """
    wb = load_workbook(excel_path)
    ws = wb.active

    db = []
    for row in ws.iter_rows(min_row=1, values_only=True):
        try:
            char = row[0]
            pinyin = row[1]
            strokes = int(row[2])
            element = row[3]

            horse_rule = row[4] if len(row) > 4 else ""       
            meaning_en = row[5] if len(row) > 5 else ""         
            meaning_zh = row[6] if len(row) > 6 else ""          

            if char and pinyin and strokes and element is not None:
                db.append({
                    "char": char,
                    "pinyin": pinyin,
                    "strokes": strokes,
                    "element": element,
                    "horse_rule": horse_rule or "",           
                    "meaning_en": meaning_en or "",
                    "meaning_zh": meaning_zh or ""
                })
        except:
            continue

    by_strokes = {}
    by_char = {}
    for c in db:
        by_strokes.setdefault(c["strokes"], []).append(c)
        by_char[c["char"]] = c

    return db, by_strokes, by_char

def make_row(requested_pattern_key: str, second: dict, third: dict, by_char: dict) -> Optional[dict]:
    first = FIRST_CHAR["strokes"]
    s2 = second["strokes"]
    s3 = third["strokes"]

    destiny_total = first + s2 + s3  # NO +1
    if not allowed_destiny_total(requested_pattern_key, destiny_total):
        return None

    pat = compute_pattern_elements(first, s2, s3)
    computed_pattern = pat["elements"]

    # STRICT pattern match
    if computed_pattern != requested_pattern_key:
        return None

    name = FIRST_CHAR["char"] + second["char"] + third["char"]
    pinyin = f"{FIRST_CHAR['pinyin']} {second['pinyin']} {third['pinyin']}"

    five_grids = compute_five_grids(first, s2, s3)

    first_info = by_char.get(FIRST_CHAR["char"], {
        "char": FIRST_CHAR["char"],
        "pinyin": FIRST_CHAR["pinyin"],
        "strokes": FIRST_CHAR["strokes"],
        "element": FIRST_CHAR["element"],
        "horse_rule": "",
        "meaning_en": "",
        "meaning_zh": ""
    })

    char_details = [first_info, second, third]
    zodiac_checks = []

    for ch in char_details:
        res = check_horse_year_char(ch.get("horse_rule", ""))

        zodiac_checks.append({
            "char": ch.get("char", ""),
            "status": res["status"],
            "matched": res["matched"],
        })

    return {
        "PatternRequested": requested_pattern_key,
        "PatternComputed": computed_pattern,
        "Name": name,
        "Pinyin": pinyin,
        "FiveGrids": five_grids,
        "PatternCalc": pat["calc_text"],
        "DestinyTotal": destiny_total,
        "DestinyElement": stroke_to_element(destiny_total),
        "DestinyMeaning_EN": DESTINY_MEANINGS.get(destiny_total, {}).get("en", "Not defined."),
        "DestinyMeaning_ZH": DESTINY_MEANINGS.get(destiny_total, {}).get("zh", "（未定義）"),
        "PatternMeaning_EN": PATTERN_MEANINGS.get(computed_pattern, {}).get("en", ""),
        "PatternMeaning_ZH": PATTERN_MEANINGS.get(computed_pattern, {}).get("zh", ""),
        "CharDetails": [first_info, second, third],
        "ZodiacHorseCheck": zodiac_checks,
    }

def generate_rows(by_strokes: dict, by_char: dict, selected_patterns: List[str]) -> List[dict]:
    rows = []
    for pattern_key in selected_patterns:
        for s2, s3 in REQUESTED_COMBOS.get(pattern_key, []):
            seconds = by_strokes.get(s2, [])
            thirds = by_strokes.get(s3, [])
            if not seconds or not thirds:
                continue
            for second, third in product(seconds, thirds):
                r = make_row(pattern_key, second, third, by_char)
                if r:
                    rows.append(r)
    return rows
