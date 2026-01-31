from typing import Dict, List
from config import ZODIAC_RULES

def _split_components(text: str) -> List[str]:
    if not text:
        return []
    normalized = (
        str(text)
        .replace("、", "，")
        .replace(",", "，")
        .replace(" ", "")
        .strip()
    )
    return [p for p in normalized.split("，") if p]

def check_zodiac_tokens(zodiac_name: str, tokens_text: str) -> Dict[str, str]:
    """
    Use ONLY tokens from Excel row[4] to check.
    Rule: 凶 overrides 吉 if both exist in the same cell.
    """
    if not zodiac_name or zodiac_name == "None":
        return {"status": "neutral", "matched": ""}

    rule = ZODIAC_RULES.get(zodiac_name)
    if not rule:
        return {"status": "neutral", "matched": ""}

    tokens = _split_components(tokens_text)

    # 凶 overrides 吉
    for t in tokens:
        if t in rule["inauspicious"]:
            return {"status": "凶", "matched": t}

    for t in tokens:
        if t in rule["auspicious"]:
            return {"status": "吉", "matched": t}

    return {"status": "neutral", "matched": ""}
