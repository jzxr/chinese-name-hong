EXCEL_PATH = "Chinese Characters.xlsx"

FIRST_CHAR = {
    "char": "洪",
    "pinyin": "hóng",
    "element": "木",
    "strokes": 10
}

DESTINY_MEANINGS = {
    16: {
        "zh": "（吉）能夠克己助人而敦厚雅量，安富會榮而福壽雙全。女性則能益夫興家而子孫榮昌，並且賢淑而理家有方。",
        "en": "(Auspicious) Self-disciplined and generous, with refined magnanimity. Enjoys stability, prosperity, and longevity. "
              "For women: supports spouse, prospers the home, and manages family affairs wisely; descendants flourish."
    },
    25: {
        "zh": "（吉）能得天時與地利，但難以得人和，學識豐富而精神活潑，有領導的能力，若能善用人才則大可成功。至於女性則很有才氣，並且溫和賢淑而有感情。",
        "en": "(Auspicious) Blessed with favorable timing and conditions, though harmony with people needs effort. "
              "Knowledgeable and lively with leadership ability; great success comes by using talent well. "
              "For women: gifted, gentle, and affectionate."
    },
    31: {
        "zh": "（吉）能夠腳踏實地而智勇雙全，性情溫和而寬宏大量，貴人明現。",
        "en": "(Auspicious) Grounded and steadfast, possessing both wisdom and courage. Gentle and broad-minded, "
              "with benefactors appearing at key times."
    },
    41: {
        "zh": "（吉）有才能也有理智，前程似錦，有官運與財運。",
        "en": "(Auspicious) Talented and sensible, with a bright future. Strong career/authority luck and wealth fortune are indicated."
    },
    45: {
        "zh": "（吉）做事一帆風順，智勇雙全必能有所成就。女性則不要虛榮則吉，可助夫益子而使家業興隆。",
        "en": "(Auspicious) Endeavors proceed smoothly; with wisdom and courage, achievement is assured. "
              "For women: avoid vanity for better fortune; supports spouse and children, prospering the family estate."
    },
    52: {
        "zh": "（吉）有先⾒之明⽽能成功的建業，並且能⼀⼼⼀意的努⼒⽽使得名利雙收。女性則富貴清雅，並且溫和賢良⽽助夫興家。",
        "en": "(Auspicious) Endowed with foresight and the ability to build a successful career. Through wholehearted dedication and effort, both fame and wealth can be attained."
        "For women, this signifies elegance and prosperity, with a gentle and virtuous nature that supports the spouse and helps the family flourish."
    },
    65: {
        "zh": "（吉）富貴榮昌，事事如意，身體健壯，名利雙收。女性溫柔，能助夫興家。",
        "en": "(Auspicious) Prosperity and honor flourish, with everything going smoothly. Strong health leads to success and a well-established reputation. "
        "For women, this signifies a gentle nature and the ability to support the spouse and help the family prosper."
    },
}

PATTERN_MEANINGS = {
    "木木木": {
        "en": "The foundation is stable. Wishes can largely be fulfilled; prosperity and longevity follow.",
        "zh": "基礎安定，所求之事頗能如願，家業興隆而身心健全，保養得宜則能長壽。"
    },
    "木木土": {
        "en": "A steady temperament and solid fortune; health, happiness, and longevity. Be forgiving with others.",
        "zh": "性情穩健，境遇堅固，身心健康而幸福長壽；與人相處宜寬恕。"
    }
}

REQUESTED_COMBOS = {
    "木木木": [(11, 10), (1, 20), (11, 20), (21, 10), (21, 21)],
    "木木土": [(21, 14), (1, 5), (11, 24), (11, 4), (21, 34), (31, 24)],
}

PATTERN_TOTAL_FILTERS = {
    "木木木": {31, 41, 52},
    "木木土": {16, 25, 45}
}

ELEMENT_COLORS = {
    "木": "#2E7D32",
    "火": "#C62828",
    "土": "#8D6E63",
    "金": "#9E9E9E",
    "水": "#1565C0",
}

FIVE_GRID_TIPS = {
    "天格": {
        "en": "Heaven Grid: family background, ancestors, early influence",
        "zh": "天格：祖先、家族背景、早年影響"
    },
    "人格": {
        "en": "Personality Grid: core character, talent, life direction",
        "zh": "人格：主運、性格、才能與人生方向"
    },
    "地格": {
        "en": "Earth Grid: early life, relationships, foundation",
        "zh": "地格：前運、人際關係與基礎"
    },
    "總格": {
        "en": "Total Grid: overall destiny (calculated WITHOUT +1)",
        "zh": "總格：一生命運（不加1）"
    }
}

ZODIAC_RULES = {
    "Horse": {
        "auspicious": ["艹","金","禾","木","玉","米","虫","豆","月","亻","扌","土"],
        "inauspicious": ["氵","火","田","日","車","刀","力","石","馬","酉"],
    },
    "Monkey": {
        "auspicious": ["禾","木","玉","豆","金","月","山","米","田","亻","氵"],
        "inauspicious": ["石","火","入","冖","口","糸","刀","力","皮","犭"],
    },
    "Chicken": {
        "auspicious": ["木","禾","玉","田","虫","米","豆","月","冖","入","金","日","山","艹"],
        "inauspicious": ["馬","糸","車","弓","血","扌","日","酉","刀","カ","石","犭"],
    },
    "Pig": {
        "auspicious": ["魚","豆","米","玉","氵","金","禾","木","月","艹","山","亻","土"],
        "inauspicious": ["乂","皮","弓","几","カ","刀","血","糸","石"],
    },
}

ZODIAC_OPTIONS = ["None", "Horse", "Monkey", "Chicken", "Pig"]
