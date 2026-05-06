from __future__ import annotations

from datetime import date
from pathlib import Path
from typing import Iterable

from bs4 import BeautifulSoup
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import mm
from reportlab.platypus import (
    Flowable,
    HRFlowable,
    KeepTogether,
    ListFlowable,
    ListItem,
    PageBreak,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)


ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "output" / "pdf" / "aa-website-copy-review-pack-2026-05-06.pdf"
PAGES = [
    ("Home", "index.html"),
    ("Growth", "growth.html"),
    ("Data", "data.html"),
    ("AI Solutions", "ai-solutions.html"),
    ("Proof", "proof.html"),
    ("Team", "team.html"),
    ("Contact", "contact.html"),
    ("Privacy", "privacy.html"),
    ("Terms", "terms.html"),
    ("404", "404.html"),
]


AA_ORANGE = colors.HexColor("#DF6F28")
AA_PURPLE = colors.HexColor("#4B3F72")
AA_INK = colors.HexColor("#17130F")
AA_CHARCOAL = colors.HexColor("#24201B")
AA_PAPER = colors.HexColor("#F5F1EA")
AA_SURFACE = colors.HexColor("#FFFCF6")
AA_MUTED = colors.HexColor("#766B5D")
AA_LINE = colors.HexColor("#DCD2C3")


def clean(text: str) -> str:
    return " ".join(text.replace("\xa0", " ").split())


def esc(text: str) -> str:
    return (
        clean(text)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def label_value(label: str, value: str, style_sheet) -> list[Paragraph]:
    return [
        Paragraph(esc(label.upper()), style_sheet["TinyLabel"]),
        Paragraph(esc(value or "Not set"), style_sheet["Body"]),
    ]


def styles():
    base = getSampleStyleSheet()
    base.add(
        ParagraphStyle(
            "CoverTitle",
            parent=base["Title"],
            fontName="Helvetica-Bold",
            fontSize=32,
            leading=36,
            textColor=AA_INK,
            alignment=TA_LEFT,
            spaceAfter=14,
        )
    )
    base.add(
        ParagraphStyle(
            "CoverSub",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=13,
            leading=19,
            textColor=AA_MUTED,
            spaceAfter=22,
        )
    )
    base.add(
        ParagraphStyle(
            "PageTitle",
            parent=base["Heading1"],
            fontName="Helvetica-Bold",
            fontSize=24,
            leading=28,
            textColor=AA_INK,
            spaceBefore=8,
            spaceAfter=8,
        )
    )
    base.add(
        ParagraphStyle(
            "Section",
            parent=base["Heading2"],
            fontName="Helvetica-Bold",
            fontSize=15,
            leading=19,
            textColor=AA_INK,
            spaceBefore=12,
            spaceAfter=6,
        )
    )
    base.add(
        ParagraphStyle(
            "Subsection",
            parent=base["Heading3"],
            fontName="Helvetica-Bold",
            fontSize=11.5,
            leading=15,
            textColor=AA_PURPLE,
            spaceBefore=5,
            spaceAfter=3,
        )
    )
    base.add(
        ParagraphStyle(
            "Body",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=9.4,
            leading=13.2,
            textColor=AA_INK,
            spaceAfter=5,
        )
    )
    base.add(
        ParagraphStyle(
            "Muted",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=8.4,
            leading=12,
            textColor=AA_MUTED,
            spaceAfter=4,
        )
    )
    base.add(
        ParagraphStyle(
            "TinyLabel",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=6.8,
            leading=8.5,
            textColor=AA_ORANGE,
            spaceAfter=2,
        )
    )
    base.add(
        ParagraphStyle(
            "Quote",
            parent=base["Normal"],
            fontName="Helvetica-Bold",
            fontSize=13,
            leading=17,
            textColor=AA_INK,
            leftIndent=10,
            borderColor=AA_ORANGE,
            borderWidth=0,
            spaceBefore=6,
            spaceAfter=8,
        )
    )
    base.add(
        ParagraphStyle(
            "Footer",
            parent=base["Normal"],
            fontName="Helvetica",
            fontSize=7,
            leading=9,
            textColor=AA_MUTED,
            alignment=TA_CENTER,
        )
    )
    return base


def page_footer(canvas, doc):
    canvas.saveState()
    canvas.setStrokeColor(AA_LINE)
    canvas.line(18 * mm, 16 * mm, 192 * mm, 16 * mm)
    canvas.setFillColor(AA_MUTED)
    canvas.setFont("Helvetica", 7)
    canvas.drawCentredString(
        105 * mm,
        10 * mm,
        f"Automate Accelerator website copy review pack | 2026-05-06 | Page {doc.page}",
    )
    canvas.restoreState()


def section_text(section, selector: str) -> list[str]:
    return [clean(x.get_text(" ")) for x in section.select(selector) if clean(x.get_text(" "))]


def direct_text(tag) -> str:
    parts = []
    for child in tag.children:
        if getattr(child, "name", None) is None:
            value = clean(str(child))
            if value:
                parts.append(value)
    return clean(" ".join(parts))


def add_bullets(story, items: Iterable[str], s):
    bullets = [
        ListItem(Paragraph(esc(item), s["Body"]), leftIndent=9, bulletColor=AA_ORANGE)
        for item in items
        if clean(item)
    ]
    if bullets:
        story.append(
            ListFlowable(
                bullets,
                bulletType="bullet",
                start="circle",
                leftIndent=14,
                bulletFontName="Helvetica",
                bulletFontSize=6,
                bulletColor=AA_ORANGE,
            )
        )
        story.append(Spacer(1, 4))


def add_text_block(story, label: str, text: str, s):
    if clean(text):
        story.append(Paragraph(esc(label), s["Subsection"]))
        story.append(Paragraph(esc(text), s["Body"]))


def extract_page(page_name: str, filename: str, s) -> list:
    html = (ROOT / filename).read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main") or soup
    story = []

    title = soup.title.get_text(" ") if soup.title else page_name
    desc = soup.find("meta", attrs={"name": "description"})
    desc_text = desc.get("content", "") if desc else ""

    story.append(Paragraph(esc(page_name), s["PageTitle"]))
    meta = Table(
        [
            [label_value("Title tag", title, s), label_value("Meta description", desc_text, s)],
        ],
        colWidths=[82 * mm, 82 * mm],
        hAlign="LEFT",
    )
    meta.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), AA_SURFACE),
                ("BOX", (0, 0), (-1, -1), 0.5, AA_LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, AA_LINE),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 8),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 7),
            ]
        )
    )
    story.append(meta)
    story.append(Spacer(1, 10))

    hero = main.find("header", class_="hero")
    if hero:
        story.append(Paragraph("Hero", s["Section"]))
        add_text_block(story, "Eyebrow / page label", " | ".join(section_text(hero, ".eyebrow, .page-chip")), s)
        add_text_block(story, "Headline", " ".join(section_text(hero, "h1")), s)
        add_text_block(story, "Subheadline", " ".join(section_text(hero, ".hero-sub")), s)
        ctas = [clean(a.get_text(" ")) for a in hero.select(".cta-row a")]
        if ctas:
            add_text_block(story, "CTA buttons", " | ".join(ctas), s)
        stats = [clean(x.get_text(" ")) for x in hero.select(".hero-stats div, .data-hero-stats div")]
        if stats:
            add_bullets(story, stats, s)

    skip_body_classes = {
        "path-num",
        "section-tag",
        "awards-title",
        "case-tag",
        "niche-tag",
        "layer-label",
        "founder-role",
        "org-location",
    }

    for section in main.find_all("section", recursive=False):
        if "hero" in section.get("class", []):
            continue
        tag = " | ".join(section_text(section, ".section-tag, .awards-title, .case-tag"))
        h2 = " ".join(section_text(section, "h2"))
        heading = h2 or tag or "Section"
        section_story = []
        if tag and tag != heading:
            section_story.append(Paragraph(esc(tag), s["TinyLabel"]))
        for selector in [".lede", ".case-lead", ".awards-note", ".answer-box p", ".pull p"]:
            for text in section_text(section, selector):
                section_story.append(Paragraph(esc(text), s["Body"]))

        cards = section.select("article, .card, .plan-card, .why-card, .workflow-step, .contrast-col, .layer, .dont-item, .org-card, .founder, .niche")
        for card in cards:
            card_heading = " ".join(section_text(card, "h3, h4, .niche-tag, .layer-label, .founder-role, .org-location"))
            body_items = []
            for p in card.find_all("p"):
                if set(p.get("class", [])) & skip_body_classes:
                    continue
                txt = clean(p.get_text(" "))
                if txt and txt not in card_heading and not txt.isdigit():
                    body_items.append(txt)
            lis = [clean(li.get_text(" ")) for li in card.find_all("li")]
            content = [x for x in body_items + lis if x]
            if card_heading or content:
                block = []
                if card_heading:
                    block.append(Paragraph(esc(card_heading), s["Subsection"]))
                for text in content[:6]:
                    block.append(Paragraph(esc(text), s["Body"]))
                section_story.append(KeepTogether(block))

        direct_links = [clean(a.get_text(" ")) for a in section.select(".cta-row a, .center-action a")]
        if direct_links:
            add_text_block(section_story, "CTA", " | ".join(direct_links), s)

        if section_story:
            story.append(Paragraph(esc(heading), s["Section"]))
            story.extend(section_story)

    return story


def build():
    OUT.parent.mkdir(parents=True, exist_ok=True)
    s = styles()
    doc = SimpleDocTemplate(
        str(OUT),
        pagesize=A4,
        rightMargin=18 * mm,
        leftMargin=18 * mm,
        topMargin=18 * mm,
        bottomMargin=22 * mm,
        title="Automate Accelerator Website Copy Review Pack",
        author="Automate Accelerator",
    )
    story = []
    story.append(Spacer(1, 36))
    story.append(Paragraph("Automate Accelerator", s["TinyLabel"]))
    story.append(Paragraph("Website Copy Review Pack", s["CoverTitle"]))
    story.append(
        Paragraph(
            "Copy-only review version for team feedback. This pack separates the words from the website design so reviewers can focus on flow, clarity, credibility and launch approvals.",
            s["CoverSub"],
        )
    )
    story.append(HRFlowable(width="100%", thickness=1, color=AA_ORANGE, spaceBefore=2, spaceAfter=16))
    summary = [
        ["Version folder", "2026-05-06-copy-website-v1"],
        ["Generated", date.today().isoformat()],
        ["Primary CTA", "Start the conversation"],
        ["Public review URL", "https://2026-05-06-copy-website-v1.vercel.app/"],
        ["GitHub", "https://github.com/rathinarayan/aa-website-copy-2026-05-06"],
    ]
    table = Table(summary, colWidths=[42 * mm, 116 * mm], hAlign="LEFT")
    table.setStyle(
        TableStyle(
            [
                ("BACKGROUND", (0, 0), (-1, -1), AA_SURFACE),
                ("BOX", (0, 0), (-1, -1), 0.5, AA_LINE),
                ("INNERGRID", (0, 0), (-1, -1), 0.5, AA_LINE),
                ("TEXTCOLOR", (0, 0), (0, -1), AA_ORANGE),
                ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
                ("FONTNAME", (1, 0), (1, -1), "Helvetica"),
                ("FONTSIZE", (0, 0), (-1, -1), 8.5),
                ("LEADING", (0, 0), (-1, -1), 11),
                ("VALIGN", (0, 0), (-1, -1), "TOP"),
                ("LEFTPADDING", (0, 0), (-1, -1), 8),
                ("RIGHTPADDING", (0, 0), (-1, -1), 8),
                ("TOPPADDING", (0, 0), (-1, -1), 6),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 6),
            ]
        )
    )
    story.append(table)
    story.append(Spacer(1, 18))
    story.append(Paragraph("Review Questions", s["Section"]))
    add_bullets(
        story,
        [
            "Does the homepage pass the grunt test in five seconds?",
            "Does each page explain the value in normal business language?",
            "Are the proof claims approved and safe to publish?",
            "Is the CTA clear enough for a business owner to act on?",
            "Which examples or numbers still need team input?",
        ],
        s,
    )
    story.append(PageBreak())

    story.append(Paragraph("Site Flow", s["PageTitle"]))
    story.append(
        Paragraph(
            "Home -> Growth -> Data -> AI Solutions -> Proof -> Team -> Contact",
            s["Quote"],
        )
    )
    story.append(
        Paragraph(
            "The current direction is outbound-first, buyer-clear, proof-honest, founder-credible and easy to act on.",
            s["Body"],
        )
    )
    story.append(Paragraph("Launch Checks", s["Section"]))
    add_bullets(
        story,
        [
            "Confirm exact award wording and whether logos can be used.",
            "Confirm public approval for aggregate proof numbers.",
            "Confirm whether to add any approved commercial outcome claims.",
            "Confirm booking link, ABN, LinkedIn URL and final legal details.",
            "Confirm any named client examples before adding case studies.",
        ],
        s,
    )
    story.append(PageBreak())

    for idx, (name, filename) in enumerate(PAGES):
        story.extend(extract_page(name, filename, s))
        if idx != len(PAGES) - 1:
            story.append(PageBreak())

    doc.build(story, onFirstPage=page_footer, onLaterPages=page_footer)
    print(OUT)


if __name__ == "__main__":
    build()
