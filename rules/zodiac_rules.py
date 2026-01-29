HORSE_YEAR_RULE = {
    "zodiac": "馬",
    "name": "Horse",
    "auspicious": [
        "艹", "金", "禾", "木", "玉", "米",
        "虫", "豆", "月", "亻", "扌", "土"
    ],
    "inauspicious": [
        "そ", "火", "田", "日", "車",
        "刀", "力", "石", "馬", "酉"
    ]
}

def check_horse_year_name(char: str) -> dict:
    """
    Check a single character against Horse-year rules.
    Returns: {status: '吉' | '凶' | 'neutral', matched: component or None}
    """
    for comp in HORSE_YEAR_RULE["auspicious"]:
        if comp in char:
            return {"status": "吉", "matched": comp}

    for comp in HORSE_YEAR_RULE["inauspicious"]:
        if comp in char:
            return {"status": "凶", "matched": comp}

    return {"status": "neutral", "matched": None}
