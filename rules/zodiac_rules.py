from typing import Dict, List

HORSE_YEAR_RULE = {
    "auspicious": {
        "艹", "金", "禾", "木", "玉", "米",
        "虫", "豆", "月", "亻", "扌", "土"
    },
    "inauspicious": {
        "氵", "火", "田", "日", "車",
        "刀", "力", "石", "馬", "酉"
    }
}


def _split_components(text: str) -> List[str]:
    """
    Supports: ， 、 , and trims whitespace
    Example: '艹，木，馬' → ['艹', '木', '馬']
    """
    if not text:
        return []

    normalized = (
        str(text)
        .replace("、", "，")
        .replace(",", "，")
        .strip()
    )

    return [p.strip() for p in normalized.split("，") if p.strip()]


def check_horse_year_char(horse_rule_text: str) -> Dict[str, str]:
    """
    Horse year naming rule:
    - 凶 overrides 吉
    - Input MUST be Excel row[4]
    """
    components = _split_components(horse_rule_text)

    # ❌ 凶 has absolute priority
    for c in components:
        if c in HORSE_YEAR_RULE["inauspicious"]:
            return {"status": "凶", "matched": c}

    # ✅ 吉 only if no 凶 found
    for c in components:
        if c in HORSE_YEAR_RULE["auspicious"]:
            return {"status": "吉", "matched": c}

    return {"status": "neutral", "matched": ""}
