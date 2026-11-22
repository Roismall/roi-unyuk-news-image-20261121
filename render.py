#!/usr/bin/env python3
"""Render THE WORLD front page for Saturday 21 November 2026.

A dense broadsheet: masthead + lead story + dated headlines grouped by
region. Every story below was reported on 21 November 2026 (Reuters, AP,
CNN, AFP and others). Output: entry.png, 1024x1024, well under 1 MiB.
Run: python3 render.py  (writes entry.png next to this file)
"""
import os
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.abspath(__file__))
SERIF_B = "/usr/share/fonts/truetype/dejavu/DejaVuSerif-Bold.ttf"
SANS = "/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf"
SANS_B = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
SERIF = "/usr/share/fonts/truetype/dejavu/DejaVuSerif.ttf"

W = H = 1024
INK = (17, 17, 17)
RED = (178, 24, 24)
PAPER = (253, 253, 248)
GREY = (110, 110, 105)
RULE = (200, 200, 192)


def F(path, size):
    return ImageFont.truetype(path, size)


def wrap(d, text, font, width):
    lines, cur = [], ""
    for word in text.split():
        trial = (cur + " " + word).strip()
        if d.textlength(trial, font=font) <= width:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def text_h(d, lines, font, leading):
    return len(lines) * leading


# (column, section header, [(headline, deck), ...])
SECTIONS = [
    (0, "MIDDLE EAST", [
        ("Coalition strikes Hodeidah port after Riyadh attack",
         "Saudi-led jets hit Houthi arms hub; 71 strikes in 24 hours."),
        ("Iran missiles hit tankers near Strait of Hormuz",
         "Tehran shows off new launcher as US-Iran talks stall."),
        ("US denies Iran claim it hit an F-16 over Gulf",
         "CENTCOM rejects Tehran account of a damaged jet."),
        ("Basra power station fire kills at least four",
         "Blaze at Hartha plant injures 30; PM orders inquiry."),
        ("Israeli fire kills four in Gaza, aid vehicle hit",
         "Three dead in strike on food-aid vehicle; six wounded."),
    ]),
    (0, "AFRICA", [
        ("700,000 displaced in southern Ethiopia",
         "Conflict and drought drive mass flight, agencies warn."),
        ("Turkey takes control of opposition TV Sozcu",
         "Ankara seizes broadcaster in widening media crackdown."),
        ("Malaysia to shelter 10,000 Rohingya with Turkey",
         "Kuala Lumpur finalises pact to house displaced refugees."),
    ]),
    (1, "EUROPE", [
        ("Russian strike kills boy, 7, and paramedic in Kryvyi Rih",
         "\u2018Triple-tap\u2019 attack wounds 60 in Zelenskyy\u2019s home city."),
        ("Russian cargo ship ablaze in Baltic after drone hit",
         "Sanctioned Sparta II burns in Gulf of Finland; crew saved."),
        ("Russian missiles fell in Poland in Ukraine attack",
         "Two missiles and a drone came down in overnight assault."),
        ("EU approves \u20ac1bn in military aid for Ukraine",
         "Top diplomat: Russia rejects peace as war grinds on."),
        ("French police sentenced over racist beating",
         "Court punishes officers who attacked producer Michel Zecler."),
    ]),
    (1, "OCEANIA", [
        ("Queensland health system faces reckoning",
         "Inquiry hears of \u2018preventable deaths\u2019 in hospitals."),
    ]),
    (1, "SPACE", [
        ("BepiColombo reaches Mercury after eight years",
         "ESA\u2013JAXA craft enters orbit; science starts April 2027."),
    ]),
    (2, "AMERICAS", [
        ("Mexico captures FBI most-wanted cartel boss",
         "\u2018El Chapo Isidro\u2019 seized in Sinaloa; 11 killed in backlash."),
        ("AI sell-off sinks Wall Street 3.7%",
         "S&P 500 falls; Nikkei drops 5.06% as AI doubts spread."),
        ("FBI probes suspected hack of crime database",
         "Trump calls breach of national crime records \u2018not good\u2019."),
        ("Trump orders contractors to clear Congress queries",
         "Executive order: firms must check with White House first."),
        ("Salvadoran troops fight gangs in Haiti",
         "2,500 troops deployed; two nations to build 3 prisons."),
    ]),
    (2, "ASIA", [
        ("Xi hails \u2018significant shift\u2019 with Australia",
         "Chinese leader welcomes thaw in China\u2013Australia ties."),
        ("Trump raised ousted Nvidia chief with Xi",
         "President presses Jensen Huang case; chip curbs stay."),
    ]),
    (2, "TECH", [
        ("GTA 6 scores 99 as critics hail sequel",
         "Metacritic: 99 from 152 reviews, all of them positive."),
        ("Bitcoin bounces 9% to retake $60,000",
         "Crypto rebounds from a two-year low ahead of Monday."),
        ("Amazon nears $7.5bn deal for AI start-up Decart",
         "Tech giant closes in on its biggest AI acquisition yet."),
    ]),
]


def measure_columns(d, col_w, hs, ds):
    """Return per-column heights for given headline/deck sizes."""
    hf, df = F(SERIF_B, hs), F(SANS, ds)
    totals = [0, 0, 0]
    for col, header, items in SECTIONS:
        totals[col] += 30  # section header block
        for head, deck in items:
            hl = wrap(d, head, hf, col_w)
            dl = wrap(d, deck, df, col_w)
            totals[col] += len(hl) * (hs + 4) + len(dl) * (ds + 3) + 10
    return totals


def draw_page(hs, ds):
    img = Image.new("RGB", (W, H), PAPER)
    d = ImageDraw.Draw(img)
    mx = 28
    col_w = (W - 2 * mx - 2 * 16) // 3
    col_x = [mx, mx + col_w + 16, mx + 2 * (col_w + 16)]

    # ---- masthead ----
    d.line([(mx, 18), (W - mx, 18)], fill=INK, width=3)
    mast = F(SERIF_B, 76)
    d.text((W // 2, 24), "THE WORLD", font=mast, fill=INK, anchor="ma")
    date_f = F(SANS_B, 25)
    d.text((W // 2, 108), "SATURDAY 21 NOVEMBER 2026", font=date_f,
           fill=RED, anchor="ma")
    sub_f = F(SANS, 15)
    d.text((W // 2, 140),
           "THE DAY'S NEWS IN ONE PAGE  \u2022  EVERY STORY DATED 21 NOVEMBER 2026",
           font=sub_f, fill=GREY, anchor="ma")
    d.line([(mx, 164), (W - mx, 164)], fill=INK, width=2)
    d.line([(mx, 168), (W - mx, 168)], fill=INK, width=1)

    # ---- lead story ----
    ly = 182
    lw = col_w * 2 + 16
    kick = F(SANS_B, 15)
    d.text((mx, ly), "CLIMATE  \u2022  ANTALYA, TURKEY", font=kick, fill=RED)
    lead_f = F(SERIF_B, 37)
    lead = wrap(d, "COP31 in overtime as climate talks miss deadline",
                lead_f, lw)
    y = ly + 22
    for line in lead:
        d.text((mx, y), line, font=lead_f, fill=INK)
        y += 43
    deck_f = F(SANS, 16)
    deck = wrap(d, "Nearly 200 nations haggle past Friday's close after the "
                "draft drops the fossil-fuel phase-out and the $120bn fund. "
                "The EU warns: \u201cgood deal or no deal.\u201d",
                deck_f, lw)
    for line in deck:
        d.text((mx, y), line, font=deck_f, fill=INK)
        y += 21
    lead_bottom = y + 6

    # right-hand lead box: Riyadh + Peru (height from its own content)
    bx = mx + lw + 16
    bw = W - mx - bx
    box_h = F(SANS_B, 15)
    box_t = F(SERIF_B, 17)
    box_d = F(SANS, 13)
    box_lines = []  # (text, font, fill, leading)
    box_lines.append(("RIYADH UNDER FIRE", box_h, RED, 20))
    for line in wrap(d, "Saudi defences down 3 Houthi missiles over Riyadh",
                     box_t, bw - 20):
        box_lines.append((line, box_t, INK, 21))
    for line in wrap(d, "Second attack on the capital in three days.",
                     box_d, bw - 20):
        box_lines.append((line, box_d, INK, 17))
    box_lines.append(("", box_d, INK, 8))
    box_lines.append(("PERU SHAKEN", box_h, RED, 20))
    for line in wrap(d, "M6.8 quake hits Junin Andes, felt in Lima",
                     box_t, bw - 20):
        box_lines.append((line, box_t, INK, 21))
    for line in wrap(d, "No casualties; tremor struck at 00:09 GMT.",
                     box_d, bw - 20):
        box_lines.append((line, box_d, INK, 17))
    box_h_px = sum(ln[3] for ln in box_lines) + 20
    d.rectangle([bx, ly, bx + bw, ly + box_h_px], outline=RED, width=2)
    by = ly + 10
    for text, font, fill, leading in box_lines:
        if text:
            d.text((bx + 10, by), text, font=font, fill=fill)
        by += leading
    lead_bottom = max(y + 6, ly + box_h_px)

    grid_top = lead_bottom + 14
    d.line([(mx, grid_top - 6), (W - mx, grid_top - 6)], fill=INK, width=2)

    # ---- region grid ----
    hf, df = F(SERIF_B, hs), F(SANS, ds)
    sec_f = F(SANS_B, 16)
    ys = [grid_top, grid_top, grid_top]
    for col, header, items in SECTIONS:
        x = col_x[col]
        y = ys[col]
        d.text((x, y), header, font=sec_f, fill=RED)
        d.line([(x, y + 22), (x + col_w, y + 22)], fill=RED, width=2)
        y += 30
        for head, deck in items:
            for line in wrap(d, head, hf, col_w):
                d.text((x, y), line, font=hf, fill=INK)
                y += hs + 4
            for line in wrap(d, deck, df, col_w):
                d.text((x, y), line, font=df, fill=(60, 60, 58))
                y += ds + 3
            y += 7
            d.line([(x, y - 4), (x + col_w, y - 4)], fill=RULE, width=1)
        ys[col] = y

    grid_bottom = max(ys)

    # ---- markets & sport strip ----
    sy = grid_bottom + 8
    d.line([(mx, sy), (W - mx, sy)], fill=INK, width=2)
    strip_f = F(SANS_B, 14)
    strip_d = F(SANS, 14)
    d.text((mx, sy + 8), "MARKETS 21 NOV", font=strip_f, fill=RED)
    d.text((mx + 150, sy + 8),
           "S&P 500 \u22123.7%  \u2022  Nikkei \u22125.06%  \u2022  Hang Seng \u22123.79%  "
           "\u2022  Brent $89.95  \u2022  Bitcoin $60,000",
           font=strip_d, fill=INK)
    d.text((mx, sy + 30), "SPORT 21 NOV", font=strip_f, fill=RED)
    d.text((mx + 150, sy + 30),
           "Leeds 4\u20131 Chelsea  \u2022  Newcastle 2\u20132 Arsenal  \u2022  "
           "Man City 1\u20131 Fulham  \u2022  England rout All Blacks",
           font=strip_d, fill=INK)
    d.line([(mx, sy + 56), (W - mx, sy + 56)], fill=INK, width=1)
    foot_f = F(SANS, 12)
    d.text((W // 2, sy + 62),
           "All stories from Saturday 21 November 2026  \u2022  Sources: Reuters, AP, "
           "CNN, AFP, USGS, ESA",
           font=foot_f, fill=GREY, anchor="ma")
    return img, grid_bottom


def main():
    chosen = None
    for hs, ds in [(16, 12), (15, 12), (15, 11), (14, 11), (13, 11)]:
        img, grid_bottom = draw_page(hs, ds)
        print("try", (hs, ds), "grid_bottom:", grid_bottom)
        if grid_bottom + 78 <= 1024:
            chosen = (hs, ds)
            break
    if chosen is None:
        chosen = (13, 11)
        img, grid_bottom = draw_page(*chosen)
    print("headline/deck sizes:", chosen, "grid_bottom:", grid_bottom)
    out = os.path.join(HERE, "entry.png")
    img.save(out, optimize=True)
    print("wrote", out, os.path.getsize(out), "bytes")


if __name__ == "__main__":
    main()
