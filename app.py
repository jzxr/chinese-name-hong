import streamlit as st
import pandas as pd

from config import EXCEL_PATH, ELEMENT_COLORS, FIVE_GRID_TIPS, ZODIAC_OPTIONS
from logic import generate_rows_cached, load_db_raw

# ============================================================
# UI HELPERS
# ============================================================
def five_grid_tooltip(key: str, lang: str) -> str:
    tip = FIVE_GRID_TIPS[key]
    if lang == "English":
        return tip["en"]
    if lang == "Chinese":
        return tip["zh"]
    return f"{tip['en']} ｜ {tip['zh']}"

def element_badge(element: str) -> str:
    color = ELEMENT_COLORS.get(element, "#333333")
    return f"<span style='color:{color}; font-weight:700;'>{element}</span>"

def zodiac_badge(status: str, matched: str = "") -> str:
    """
    status: 吉 | 凶 | neutral
    matched: which component matched (e.g. 艹 / 火)
    """
    if status == "凶":
        return f"<span style='background:#ffebee;color:#c62828;padding:2px 8px;border-radius:999px;font-weight:700;'>凶</span> <span style='color:#c62828;'>({matched})</span>"
    if status == "吉":
        return f"<span style='background:#e8f5e9;color:#2e7d32;padding:2px 8px;border-radius:999px;font-weight:700;'>吉</span> <span style='color:#2e7d32;'>({matched})</span>"
    return "<span style='background:#eeeeee;color:#555;padding:2px 8px;border-radius:999px;font-weight:700;'>—</span>"

def horse_row_status(row: dict) -> str:
    """
    Returns: "吉" | "凶" | "neutral"
    Rule:
      - If any character is 凶 -> overall 凶
      - Else if any character is 吉 -> overall 吉
      - Else neutral
    """
    checks = row.get("ZodiacHorseCheck", []) or []
    statuses = [c.get("status") for c in checks]

    if "凶" in statuses:
        return "凶"
    if "吉" in statuses:
        return "吉"
    return "neutral"
def render_pagination_bar(total: int, page_size: int, key_prefix: str = "pg"):
    total_pages = max(1, (total + page_size - 1) // page_size)

    # init + clamp
    if "page" not in st.session_state:
        st.session_state.page = 1
    st.session_state.page = max(1, min(int(st.session_state.page), total_pages))

    start = (st.session_state.page - 1) * page_size
    end = min(start + page_size, total)

    c1, c2, c3 = st.columns([1, 3, 1])

    with c1:
        if st.button("⬅ Previous", key=f"{key_prefix}_prev", disabled=(st.session_state.page <= 1)):
            st.session_state.page -= 1
            st.rerun()

    with c2:
        if total == 0:
            st.markdown("No results.")
        else:
            st.markdown(
                f"Showing **{start+1}–{end}** of **{total}** · "
                f"Page **{st.session_state.page}/{total_pages}**"
            )

    with c3:
        if st.button("Next ➡", key=f"{key_prefix}_next", disabled=(st.session_state.page >= total_pages)):
            st.session_state.page += 1
            st.rerun()

    return start, end

@st.cache_data(show_spinner=False)
def load_db_cached(path: str):
    return load_db_raw(path)

def ensure_state():
    if "favorites" not in st.session_state:
        st.session_state.favorites = []

def add_favorite(row_dict):
    for f in st.session_state.favorites:
        if f.get("Name") == row_dict.get("Name"):
            return False
    st.session_state.favorites.append(row_dict)
    return True

def remove_favorite(name: str):
    st.session_state.favorites = [f for f in st.session_state.favorites if f.get("Name") != name]

def clear_favorites():
    st.session_state.favorites = []

# ============================================================
# APP
# ============================================================
ensure_state()

if "_btn_counter" not in st.session_state:
    st.session_state["_btn_counter"] = 0
    
st.set_page_config(page_title="（洪）Professional Name Generator", layout="wide")
st.title("🔮（洪）Professional Chinese Name Generator")
st.caption("✅ 第二/第三字只依筆畫配對（不需符合Excel五行）｜✅ 組合五行依 +1 規則｜✅ 總格數理不加 +1")

guide_lang = st.sidebar.radio("Guide Language | 說明語言", ["English", "Chinese", "Both"], index=0)

with st.expander("📘 How to Read This Name Analysis | 使用說明（必讀）", expanded=True):
    if guide_lang in ("English", "Both"):
        st.markdown("## 🌟 English Guide")
        st.markdown("""
**This tool generates Chinese names based on traditional name numerology (姓名學) and Five-Element theory (五行).**

### 1️⃣ Five Grids (五格)
- **Heaven Grid (天格)** – family background and ancestral influence  
- **Personality Grid (人格)** – core personality, talent, and life direction  
- **Earth Grid (地格)** – early life, relationships, and foundation  
- **Total Grid (總格)** – overall destiny (**NO +1**)

### 2️⃣ Five-Element Pattern (五行組合)
- Surname strokes + 1  
- Surname + first given name  
- First + second given name  

### 3️⃣ Destiny Meaning (數理)
Determined by total strokes **without +1**.

### 4️⃣ Character Meanings
Pinyin, strokes, element, and meanings from the database.
""")

    if guide_lang in ("Chinese", "Both"):
        st.markdown("## 🌟 中文說明")
        st.markdown("""
**本系統依據傳統姓名學與五行數理設計。**

### 1️⃣ 五格說明
- **天格**：祖先、家族背景  
- **人格**：主運、性格與才能  
- **地格**：前運、人際關係  
- **總格**：一生命運（**總格不加1**）

### 2️⃣ 五行組合
- 姓氏筆畫 + 1  
- 姓氏 + 名字第一字  
- 名字第一字 + 第二字  

### 3️⃣ 數理含義
數理僅以三字總筆畫判斷，不加1。

### 4️⃣ 單字含義
展開卡片可查看拼音、筆畫、五行與中英文含義。
""")

db, by_strokes, by_char = load_db_cached(EXCEL_PATH)

# Sidebar controls
st.sidebar.header("Controls")
lang = st.sidebar.radio("Meaning Language", ["English", "Chinese", "Both"], 0)
show_destiny = st.sidebar.toggle("Show destiny meaning (總格數理)", value=True)
page_size = st.sidebar.selectbox("Cards per page", [100, 200, 800], index=0)
max_generate = st.sidebar.slider("Max results to generate (perf)", 100, 5000, 500, step=200)
search = st.sidebar.text_input("Search (Name / Pinyin)", "")

# One zodiac selector (covers horse / monkey / chicken / pig / etc.)
zodiac_name = st.sidebar.selectbox("Select Zodiac Rule", ZODIAC_OPTIONS, index=0)

zodiac_filter_mode = "OFF"
if zodiac_name != "None":
    zodiac_filter_mode_ui = st.sidebar.radio(
        "2nd + 3rd character filter",
        ["OFF", "EXCLUDE 凶 (recommended)", "REQUIRE 吉 (strict)"],
        index=1
    )
    zodiac_filter_mode = {
        "OFF": "OFF",
        "EXCLUDE 凶 (recommended)": "EXCLUDE_XIONG",
        "REQUIRE 吉 (strict)": "REQUIRE_JI",
    }[zodiac_filter_mode_ui]

selected_patterns = st.sidebar.multiselect(
    "Select patterns",
    options=list({"木木木", "木木土"}),  # UI only: options list
    default=list({"木木木", "木木土"})
)

rows = generate_rows_cached(
    by_strokes, by_char,
    tuple(selected_patterns),
    zodiac_name,
    zodiac_filter_mode,
    max_generate
)

df = pd.DataFrame([{
    "Name": r["Name"],
    "Pinyin": r["Pinyin"],
    "PatternComputed": r["PatternComputed"],
    "DestinyTotal": r["DestinyTotal"],
    "DestinyElement": r["DestinyElement"],
    "PatternCalc": r["PatternCalc"],
    "PatternMeaning_EN": r.get("PatternMeaning_EN", ""),
    "PatternMeaning_ZH": r.get("PatternMeaning_ZH", ""),
    "DestinyMeaning_EN": r.get("DestinyMeaning_EN", ""),
    "DestinyMeaning_ZH": r.get("DestinyMeaning_ZH", ""),
} for r in rows])

df = df.drop_duplicates(subset=["Name", "Pinyin", "PatternComputed", "DestinyTotal"]).reset_index(drop=True)
df["_c1"] = df["Name"].str[0]
df["_c2"] = df["Name"].str[1]
df["_c3"] = df["Name"].str[2]
df = df.sort_values(by=["_c1", "_c2", "_c3"])
df = df.drop(columns=["_c1", "_c2", "_c3"]).reset_index(drop=True)
if df.empty:
    st.warning("No results found. Check Excel strokes availability, requested tuples, pattern filters, or destiny total filters.")
    st.stop()

if search.strip():
    q = search.strip().lower()
    df = df[
        df["Name"].astype(str).str.lower().str.contains(q) |
        df["Pinyin"].astype(str).str.lower().str.contains(q)
    ]

# Summary
c1, c2, c3 = st.columns([1.2, 1, 1])
c1.metric("Results", f"{len(df)}")
c2.metric("Patterns", f"{df['PatternComputed'].nunique()}")
c3.metric("Destiny Totals", f"{df['DestinyTotal'].nunique()}")

st.divider()

with st.expander("📋 Table view / Export"):
    base_cols = ["PatternComputed", "Name", "Pinyin", "DestinyTotal", "DestinyElement", "PatternCalc"]
    extra_cols = []
    if lang in ("English", "Both"):
        extra_cols += ["PatternMeaning_EN"]
    if lang in ("Chinese", "Both"):
        extra_cols += ["PatternMeaning_ZH"]
    if show_destiny:
        if lang == "English":
            extra_cols += ["DestinyMeaning_EN"]
        elif lang == "Chinese":
            extra_cols += ["DestinyMeaning_ZH"]
        else:
            extra_cols += ["DestinyMeaning_EN", "DestinyMeaning_ZH"]

    show_cols = base_cols + extra_cols
    st.dataframe(df[show_cols], height=360)
    csv = df[show_cols].to_csv(index=False).encode("utf-8-sig")
    st.download_button("Download CSV", data=csv, file_name="name_results.csv", mime="text/csv")

# ============================================================
# NAME CARDS
# ============================================================
st.subheader("✨ Name Cards")
st.caption("Expand each card to see 五格, 五行組合計算, 總格數理, and each character meaning. Save names to Favorites for comparison and PDF export.")

# Apply the same search filter to rows (so cards match table)
filtered_rows = rows
if search.strip():
    q = search.strip().lower()
    filtered_rows = [
        r for r in rows
        if q in str(r.get("Name","")).lower() or q in str(r.get("Pinyin","")).lower()
    ]

# Sort rows by chars (same as df sort)
def name_sort_key(r):
    n = str(r.get("Name",""))
    return (n[0] if len(n)>0 else "", n[1] if len(n)>1 else "", n[2] if len(n)>2 else "")

filtered_rows = sorted(filtered_rows, key=name_sort_key)

# =========================
# PAGINATION
# =========================
total = len(filtered_rows)

# top bar
start, end = render_pagination_bar(total, page_size, key_prefix="top")
for i, r in enumerate(filtered_rows[start:end], start=start):

    fg = r["FiveGrids"]

    if lang == "English":
        title = f"{r['Name']} · {r['Pinyin']} · Total {r['DestinyTotal']} · Pattern {r['PatternComputed']}"
    elif lang == "Chinese":
        title = f"{r['Name']} · {r['Pinyin']} · 總格 {r['DestinyTotal']} · 組合 {r['PatternComputed']}"
    else:
        title = f"{r['Name']} · {r['Pinyin']} · Total/總格 {r['DestinyTotal']} · Pattern/組合 {r['PatternComputed']}"

    with st.expander(title):
        colA, colB = st.columns([1, 5])
        with colA:
            st.session_state["_btn_counter"] += 1
            btn_key = f"save_{r['Name']}_{st.session_state['_btn_counter']}"
            if st.button("⭐ Save", key=f"save_{r['Name']}_{i}_{r.get('PatternComputed','')}_{r.get('DestinyTotal','')}"):
                ok = add_favorite(r)
                st.success("Saved to favorites!") if ok else st.info("Already in favorites.")
        with colB:
            st.write("")

        # Five grids
        if lang == "English":
            st.markdown("### 🧭 Five Grids (Heaven · Personality · Earth · Total)")
        elif lang == "Chinese":
            st.markdown("### 🧭 五格（天格・人格・地格・總格）")
            st.caption("天格：姓+1 ｜ 人格：姓+名1 ｜ 地格：名1+名2 ｜ 總格：三字總和（總格不加1）")
        else:
            st.markdown("### 🧭 Five Grids 五格（Heaven・Personality・Earth・Total）")
            st.caption("Heaven 天格：surname + 1 ｜ Personality 人格：surname + 名1 ｜ Earth 地格：名1+名2 ｜ Total 總格：sum (NO +1 / 不加1)")

        fg = r["FiveGrids"]
        cols = st.columns(4)
        for i, key in enumerate(["天格", "人格", "地格", "總格"]):
            strokes, elem = fg[key]

            if lang == "English":
                label_map = {"天格": "Heaven Grid", "人格": "Personality Grid", "地格": "Earth Grid", "總格": "Total Grid"}
                label = label_map[key]
            elif lang == "Chinese":
                label = key
            else:
                label_map = {
                    "天格": "Heaven Grid 天格",
                    "人格": "Personality Grid 人格",
                    "地格": "Earth Grid 地格",
                    "總格": "Total Grid 總格",
                }
                label = label_map[key]

            cols[i].metric(label=label, value=str(strokes), delta=elem, help=five_grid_tooltip(key, lang))

        st.divider()

        left, right = st.columns([1.05, 1.35])
        with left:
            st.markdown("#### 🔢 Calculations")
            st.write(f"**Pattern calc (+1 rule):** {r['PatternCalc']}")
            st.write(f"**Destiny total (no +1):** {r['DestinyTotal']} → 五行: **{r['DestinyElement']}**")

        with right:
            st.markdown("#### 📖 Meanings")
            if lang == "English":
                st.markdown("**Pattern Meaning (EN)**")
                st.write(r.get("PatternMeaning_EN", "") or "—")
            elif lang == "Chinese":
                st.markdown("**組合含義（中文）**")
                st.write(r.get("PatternMeaning_ZH", "") or "—")
            else:
                st.markdown("**Pattern Meaning (EN)**")
                st.write(r.get("PatternMeaning_EN", "") or "—")
                st.markdown("**組合含義（中文）**")
                st.write(r.get("PatternMeaning_ZH", "") or "—")

            if show_destiny:
                st.markdown(f"**Destiny Meaning 總格數理（{r['DestinyTotal']}）**")
                if lang == "English":
                    st.success(r.get("DestinyMeaning_EN", "Not defined."))
                elif lang == "Chinese":
                    st.success(r.get("DestinyMeaning_ZH", "（未定義）"))
                else:
                    st.success(r.get("DestinyMeaning_EN", "Not defined."))
                    st.info(r.get("DestinyMeaning_ZH", "（未定義）"))

        st.divider()
        st.markdown("### 🔤 Character Details（每個字：拼音・筆畫・五行・含義）")

        if zodiac_name != "None":
            z = r.get("ZodiacCheck", {}) or {}
            checks = z.get("checks") or []
            if len(checks) >= 3:
                c2 = checks[1]  # 2nd char
                c3 = checks[2]  # 3rd char

        zodiac_checks = (r.get("ZodiacCheck", {}) or {}).get("checks", [])

        for idx, ch in enumerate(r["CharDetails"]):
            z = zodiac_checks[idx] if idx < len(zodiac_checks) else {"status": "neutral", "matched": ""}

            st.markdown(
                f"**{ch.get('char','')}** · *{ch.get('pinyin','')}* · {ch.get('strokes','')} strokes · "
                f"Element: {element_badge(ch.get('element',''))} · 马年:",
                unsafe_allow_html=True
            )

            st.markdown(
                zodiac_badge(z.get("status", "neutral"), z.get("matched", "")),
                unsafe_allow_html=True
            )

            if lang == "English":
                st.write(f"English: {ch.get('meaning_en','') or '—'}")
            elif lang == "Chinese":
                st.write(f"中文: {ch.get('meaning_zh','') or '—'}")
            else:
                st.write(f"English: {ch.get('meaning_en','') or '—'}")
                st.write(f"中文: {ch.get('meaning_zh','') or '—'}")

            st.write("")
            
render_pagination_bar(total, page_size, key_prefix="bottom")
