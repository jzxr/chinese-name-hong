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
    }
}

PATTERN_MEANINGS = {
    "木木木": {
        "en": "The foundation is stable. Wishes can largely be fulfilled; prosperity and longevity follow.",
        "zh": "基礎安定，所求之事頗能如願，家業興隆而身心健全，保養得宜則能長壽。"
    },
    "木木土": {
        "en": "A steady temperament and solid fortune; health, happiness, and longevity. Be forgiving with others.",
        "zh": "性情穩健，境遇堅固，身心健康而幸福長壽；與人相處宜寬恕。"
    },
    "木土火": {
        "en": "Strong interpersonal harmony; a sound foundation supports successful growth and advancement.",
        "zh": "有人緣，基礎運健全，能成功發展。"
    }
}

REQUESTED_COMBOS = {
    "木木木": [(11, 10), (1, 20), (11, 20), (21, 10)],
    "木木土": [(21, 14), (1, 5), (11, 24)],
    "木火土": [(3, 12), (13, 2)],
}

PATTERN_TOTAL_FILTERS = {
    "木木木": {31, 41},
    "木木土": {16, 45},
    "木火土": {25}
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
