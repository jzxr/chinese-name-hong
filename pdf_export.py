from io import BytesIO
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

def _wrap_text(canvas_obj, text, x, y, max_width, line_height=14, font_name="Helvetica", font_size=10):
    canvas_obj.setFont(font_name, font_size)
    words = (text or "").split()
    line = ""
    lines = []

    for w in words:
        test = (line + " " + w).strip()
        if canvas_obj.stringWidth(test, font_name, font_size) <= max_width:
            line = test
        else:
            if line:
                lines.append(line)
            line = w

    if line:
        lines.append(line)

    for ln in lines:
        canvas_obj.drawString(x, y, ln)
        y -= line_height
    return y

def generate_pdf(favorites, lang_mode="Both"):
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4
    y = height - 40

    c.setFont("Helvetica-Bold", 14)
    c.drawString(40, y, "Chinese Name Analysis Report")
    y -= 18
    c.setFont("Helvetica", 10)
    c.drawString(40, y, "Favorites comparison export (五格・五行組合・總格數理)")
    y -= 24

    for idx, f in enumerate(favorites, start=1):
        if y < 140:
            c.showPage()
            y = height - 40

        c.setFont("Helvetica-Bold", 12)
        c.drawString(40, y, f"{idx}. {f['Name']}  ({f['Pinyin']})")
        y -= 16

        fg = f["FiveGrids"]
        c.setFont("Helvetica", 10)
        c.drawString(40, y, f"Pattern (組合): {f['PatternComputed']}   |   Total (總格): {f['DestinyTotal']} ({f['DestinyElement']})")
        y -= 14
        c.drawString(
            40, y,
            f"Five Grids 五格: 天格 {fg['天格'][0]}({fg['天格'][1]}) · 人格 {fg['人格'][0]}({fg['人格'][1]}) · "
            f"地格 {fg['地格'][0]}({fg['地格'][1]}) · 總格 {fg['總格'][0]}({fg['總格'][1]})"
        )
        y -= 16

        c.setFont("Helvetica-Oblique", 10)
        c.drawString(40, y, "Pattern calculation (+1 rule):")
        y -= 14
        c.setFont("Helvetica", 10)
        y = _wrap_text(c, f.get("PatternCalc", ""), 50, y, max_width=width - 90, line_height=13)

        y -= 6
        c.setFont("Helvetica-Oblique", 10)
        c.drawString(40, y, "Meanings:")
        y -= 14
        c.setFont("Helvetica", 10)

        if lang_mode in ("English", "Both"):
            y = _wrap_text(c, "Pattern (EN): " + (f.get("PatternMeaning_EN") or "—"), 50, y, width - 90)
            y = _wrap_text(c, "Destiny (EN): " + (f.get("DestinyMeaning_EN") or "—"), 50, y, width - 90)
            y -= 4
        if lang_mode in ("Chinese", "Both"):
            y = _wrap_text(c, "組合(中): " + (f.get("PatternMeaning_ZH") or "—"), 50, y, width - 90)
            y = _wrap_text(c, "數理(中): " + (f.get("DestinyMeaning_ZH") or "—"), 50, y, width - 90)
            y -= 4

        c.setFont("Helvetica-Oblique", 10)
        c.drawString(40, y, "Characters:")
        y -= 14
        c.setFont("Helvetica", 10)

        for ch in f.get("CharDetails", []):
            if y < 120:
                c.showPage()
                y = height - 40
                c.setFont("Helvetica", 10)

            line = f"{ch.get('char','')} ({ch.get('pinyin','')}), {ch.get('strokes','')} strokes, element {ch.get('element','')}"
            c.drawString(50, y, line)
            y -= 12
            if lang_mode in ("English", "Both"):
                y = _wrap_text(c, "EN: " + (ch.get("meaning_en") or "—"), 60, y, width - 100, line_height=12)
            if lang_mode in ("Chinese", "Both"):
                y = _wrap_text(c, "中: " + (ch.get("meaning_zh") or "—"), 60, y, width - 100, line_height=12)
            y -= 6

        c.line(40, y, width - 40, y)
        y -= 16

    c.save()
    buffer.seek(0)
    return buffer
