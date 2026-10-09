"""Export PDF (reportlab) : fiches (cards_pdf) et tableaux (table_pdf)."""
import io
from xml.sax.saxutils import escape
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import KeepTogether, Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

G = colors.HexColor("#0e7c66")
SS = getSampleStyleSheet()
H1 = ParagraphStyle("h1", parent=SS["Title"], textColor=G, fontSize=20, alignment=0, spaceAfter=4)
H3 = ParagraphStyle("h3", parent=SS["Heading3"], fontSize=11, spaceBefore=8, spaceAfter=1)
SUB = ParagraphStyle("sub", parent=SS["Normal"], fontSize=8, textColor=colors.HexColor("#5d6f69"))
TXT = ParagraphStyle("txt", parent=SS["Normal"], fontSize=9.5, leading=12.5)
CEL = ParagraphStyle("cel", parent=SS["Normal"], fontSize=7.5, leading=9)

def c(s):
    """Texte sûr pour reportlab (polices standard) : échappe le XML et retire les caractères hors cp1252."""
    return escape(str("" if s is None else s).encode("cp1252", "ignore").decode("cp1252"))

def _build(title, story, meta, size):
    buf = io.BytesIO()
    def foot(cv, doc):
        cv.setFont("Helvetica", 8); cv.setFillColor(colors.grey)
        cv.drawString(1.5 * cm, 1 * cm, c(f"{meta[0]} - {meta[1]}")); cv.drawRightString(size[0] - 1.5 * cm, 1 * cm, f"Page {doc.page}")
    SimpleDocTemplate(buf, pagesize=size, leftMargin=1.5 * cm, rightMargin=1.5 * cm, topMargin=1.5 * cm, bottomMargin=1.8 * cm, title=c(title)).build(story, onFirstPage=foot, onLaterPages=foot)
    return buf.getvalue()

def cards_pdf(title, items, meta):
    """items : liste de (titre, sous-titre, texte)."""
    story = [Paragraph(c(title), H1), Paragraph(c(f"{meta[0]} - {meta[1]} - {len(items)} éléments"), SUB), Spacer(1, 8)]
    for t, s, x in items:
        story.append(KeepTogether([Paragraph(f"<b>{c(t)}</b>", H3), Paragraph(c(s), SUB), Paragraph(c(x), TXT)]))
    if not items:
        story.append(Paragraph("Aucune donnée disponible.", TXT))
    return _build(title, story, meta, A4)

def table_pdf(title, df, meta):
    df = df.fillna("").astype(str)
    story = [Paragraph(c(title), H1), Paragraph(c(f"{meta[0]} - {meta[1]} - {len(df)} lignes"), SUB), Spacer(1, 8)]
    if df.empty:
        story.append(Paragraph("Aucune donnée disponible.", TXT))
    else:
        size = landscape(A4)
        w = (size[0] - 3 * cm) / len(df.columns)
        rows = [[Paragraph(f"<b>{c(h)}</b>", ParagraphStyle("th", parent=CEL, textColor=colors.white)) for h in df.columns]] + [[Paragraph(c(v), CEL) for v in r] for r in df.values.tolist()]
        t = Table(rows, colWidths=[w] * len(df.columns), repeatRows=1)
        t.setStyle(TableStyle([("BACKGROUND", (0, 0), (-1, 0), G), ("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#c9d6d1")), ("VALIGN", (0, 0), (-1, -1), "TOP"), ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#f1f7f4")])]))
        story.append(t)
        return _build(title, story, meta, size)
    return _build(title, story, meta, A4)
