#!/usr/bin/env python3
"""V166 — news-image-20261126 entry renderer (PIL, build-time only).

Layout V166 'broadsheet spine': masthead, DATE CHECK ribbon, L-shaped
hero cluster (big left + two stacked right), 2x5 card grid, world map +
ALSO columns at the bottom. 50 stories: 3 heroes + 10 cards + 37 ALSO.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFont

W, H = 1024, 1024
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "entry.png")

# ---------------------------------------------------------------- content
DATE_CHECK = [
    "COP31 failed 22 Nov",
    "Shenzhou-24 launched 25 Nov",
    "Cairo tanker blast, 31 dead, 25 Nov",
    "Cartagena hostages freed 25 Nov",
    "Australia-Solomon pact 25 Nov",
    "UK energy prices +26% announced 25 Nov",
    "Huawei convicted 24 Nov",
]

HEROES = [
    {
        "kicker": "NEW YORK  |  CULTURE  [C]",
        "headline": "Macy's 100th parade postponed \u2014 a first for weather",
        "deck": ("Thanksgiving parade put off by an East Coast storm; "
                 "gusts to 60 mph. New date: Sat 28 Nov, 08:30 ET."),
        "why": ("WHY IT MATTERS: The parade's centenary, halted by "
                "weather for the first time ever."),
    },
    {
        "kicker": "STRAIT OF HORMUZ  [CL]",
        "headline": "IRGC claims 2 tankers hit by mines",
        "deck": ("Tehran says a supertanker carrying 2m barrels is among "
                 "them. Claim unverified; Brent $93.80."),
        "why": "WHY IT MATTERS: The Iran war threatens the oil chokepoint.",
    },
    {
        "kicker": "TRADE  |  MARKETS  [C]",
        "headline": "Trump tariffs: markets rebound",
        "deck": ("Stocks rally as levies on 14 partners look milder than "
                 "feared; STOXX +1.6%, MSCI +0.4%. Nvidia \u22123.91% to "
                 "$149.30; gold $3,572, \u22120.2%."),
        "why": "WHY IT MATTERS: The trade shock looks modest \u2014 for now.",
    },
]

CARDS = [
    ("GAZA", "Israel strike kills Hamas education deputy",
     "Hamas deputy Abu Nada and wife killed in Deir al-Balah; 9 dead.",
     "9 KILLED", "[C]"),
    ("UKRAINE", "Russian missiles hit Kyiv mall; 7 hurt",
     "Missiles and 113 drones overnight; mall in Desnianskyi hit.",
     "7 WOUNDED", "[C]"),
    ("INDONESIA", "Flooded gold mine: 13 dead, 13 missing",
     "Miners trapped ~100 m down after rain in Bogor.",
     "13 DEAD \u00b7 13 MISSING", "[C]"),
    ("ISRAEL", "Judge urges bribery charge dropped",
     "Court urges prosecutors to drop Case 4000, the only bribery count.",
     "CASE 4000", "[C]"),
    ("NORTH KOREA", "Kim urges tactical nukes at plant tour",
     "KCNA: Kim urges wider use of tactical nuclear weapons.",
     "TACTICAL NUKES", "[R]"),
    ("SPACE", "FCC clears 1m orbital data-centre satellites",
     "SpaceX 'Starmind' approved 25 Nov; first space data-centre nod.",
     "1M SATELLITES", "[C]"),
    ("UNITED KINGDOM", "Net migration falls to 77,000",
     "Lowest since 1997 outside the pandemic, year to June 2026.",
     "77,000", "[C]"),
    ("RUSSIA", "Record post-Soviet military budget passed",
     "Biggest post-Soviet military budget approved.",
     "RECORD", "[C]"),
    ("THAILAND", "Oil depot blast hurts 7",
     "Depot blast; evacuation alert, fire out in ~30 min.",
     "7 HURT", "[C]"),
    ("GERMANY", "2 Iraqis held over synagogue plot",
     "Held in Cologne and Heidelberg over late-March synagogue plot.",
     "2 HELD", "[C]"),
]

ALSO = [
    "Eisenkot seals first Israel coalition deal [C]",
    "Merz warns Russia's aims go beyond Ukraine [C]",
    "UK on alert over drone threat to airbases [R]",
    "Norse Atlantic halts all flights, warns of bankruptcy [C]",
    "Poundland in administration; 11,000 jobs at risk [C]",
    "Malaysia sues Google for $146m over content [C]",
    "Kenya court halts US-backed Ebola facility [C]",
    "Zelensky refuses Belarus offer of Moscow flight [C]",
    "Kushner calls Putin a 'grandmaster of politics' [C]",
    "Estonia decides to shut its border [C]",
    "Copernicus: longest stretch above 2\u00b0C warming [C]",
    "Nvidia halts AI server shipments to 4 nations [R]",
    "US Bitcoin ETFs: record $4.94bn Nov outflows [C]",
    "Blast near tanker 50 nm west of Dubai; crew safe [R]",
    "Kharkiv strike kills couple, 37 and 38, at home [C]",
    "18 wounded in Kryvyi Rih strikes [C]",
    "5 warplanes damaged at Savasleyka airbase [R]",
    "Subkhankulovo pump station ablaze after drone hit [R]",
    "UN rights chief warns of atrocity crimes in Gaza [C]",
    "OPEC+ to meet 29 Nov on 2027 output [C]",
    "Ras Tanura hit claimed; 4 drones downed [CL] 25 Nov",
    "Saudi downs 2 missiles headed for Riyadh [CL]",
    "Philadelphia parade cancelled in storm [C]",
    "Projectile hits Jazan refinery; 1 worker killed [R]",
    "Guinea-Bissau delays elections to Nov 2028 [C]",
    "2 Italians killed in Iranian drone hit in Kuwait [C]",
    "ECB picks Pablo Hernandez de Cos as next chief [C]",
    "Slavyansk refinery ablaze after drone attack [R]",
    "DR Congo Ebola passes 12,000 cases, ~6,000 dead [R]",
    "Haiti: 4.9m need health aid, WHO warns [R]",
    "Trump uses Thanksgiving post to attack foes [C]",
    "Trump demands probe of pre-midterm GDP data [R]",
    "Brazil mid-Nov inflation eases to 0.22% [C]",
    "EU leaders wrestle over budget, Ukraine funds [R]",
    "Japan, China trade blame over ship incursions [R]",
    "Kurdish protests erupt as Baghdad takes oil control [R]",
    "Bank of Korea raises rate to 3.25% [C]",
]

# pins: (lon, lat, legend label)
PINS = [
    (-74.0, 40.7, "New York \u2014 Macy's parade"),
    (-75.2, 40.0, "Philadelphia \u2014 parade cancelled"),
    (30.5, 50.4, "Kyiv \u2014 mall strike"),
    (34.5, 31.5, "Gaza \u2014 Hamas deputy killed"),
    (56.2, 26.2, "Khasab \u2014 tanker mines claim"),
    (100.5, 13.75, "Bangkok \u2014 depot blast"),
    (106.8, -6.6, "Bogor \u2014 mine flood"),
    (-0.1, 51.5, "London \u2014 migration 77,000"),
    (13.4, 52.5, "Berlin \u2014 synagogue plot arrests"),
    (127.0, 37.5, "Seoul \u2014 Bank of Korea"),
    (-15.6, 11.9, "Bissau \u2014 elections delayed"),
]
PIN_R = 6

# ---------------------------------------------------------------- helpers
FONT_DIR = "/usr/share/fonts/truetype/dejavu"
_font_cache = {}


def font(size, bold=False, italic=False):
    key = (size, bold, italic)
    if key not in _font_cache:
        name = "DejaVuSans-Bold.ttf" if bold else "DejaVuSans.ttf"
        _font_cache[key] = ImageFont.truetype(
            os.path.join(FONT_DIR, name), size)
    return _font_cache[key]


def wrap(text, fnt, max_w):
    """Greedy word wrap; returns list of lines that fit max_w."""
    words, lines, cur = text.split(), [], ""
    for word in words:
        trial = word if not cur else cur + " " + word
        if fnt.getlength(trial) <= max_w:
            cur = trial
        else:
            if cur:
                lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


ART_RECTS = []    # (x0, y0, x1, y1, label) — drawn art, must not touch text
TEXT_RECTS = []   # (x0, y0, x1, y1, label) — drawn text lines


def _overlap(a, b):
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])


def draw_lines(draw, lines, x, y, fnt, fill, box, lh, label):
    """Draw lines inside box; assert each line stays in box (margin>=2)."""
    bx0, by0, bx1, by1 = box
    cy = y
    for ln in lines:
        bb = draw.textbbox((x, cy), ln, font=fnt)
        assert bb[0] >= bx0 + 2 and bb[1] >= by0 + 2, \
            f"{label}: text escapes box left/top {bb} vs {box}"
        assert bb[2] <= bx1 - 2 and bb[3] <= by1 - 2, \
            f"{label}: text escapes box right/bottom {bb} vs {box}"
        draw.text((x, cy), ln, font=fnt, fill=fill)
        TEXT_RECTS.append((bb[0], bb[1], bb[2], bb[3], label))
        cy += lh
    return cy


def draw_one(draw, text, x, y, fnt, fill, box, label, anchor="la"):
    bb = draw.textbbox((x, y), text, font=fnt, anchor=anchor)
    bx0, by0, bx1, by1 = box
    assert bb[0] >= bx0 + 2 and bb[1] >= by0 + 2, \
        f"{label}: text escapes box {bb} vs {box}"
    assert bb[2] <= bx1 - 2 and bb[3] <= by1 - 2, \
        f"{label}: text escapes box {bb} vs {box}"
    draw.text((x, y), text, font=fnt, fill=fill, anchor=anchor)
    TEXT_RECTS.append((bb[0], bb[1], bb[2], bb[3], label))
    return bb


def register_art(box, label):
    ART_RECTS.append((box[0], box[1], box[2], box[3], label))


def check_art_text_separation():
    for a in ART_RECTS:
        for t in TEXT_RECTS:
            assert not _overlap(a, t), \
                f"art/text overlap: {a[4]} {a[:4]} vs {t[4]} {t[:4]}"


# ---------------------------------------------------------------- palette
PAPER = (244, 239, 230)
INK = (26, 26, 26)
NAVY = (20, 33, 61)
NAVY2 = (30, 48, 88)
RED = (185, 28, 28)
RED_BG = (253, 232, 232)
CARD_BG = (255, 255, 255)
GREY = (90, 90, 90)
OCEAN = (188, 214, 230)
LAND = (227, 211, 168)
LAND_EDGE = (160, 140, 95)
GOLD = (212, 175, 55)
TAG_FILL = {"[C]": (34, 120, 60), "[R]": (180, 120, 10), "[CL]": (160, 30, 30)}

# ---------------------------------------------------------------- map
# Equirectangular world map. Coarse but recognisable continent outlines.
NA = [(-168, 66), (-140, 70), (-125, 72), (-110, 68), (-95, 69), (-85, 66),
      (-80, 62), (-75, 58), (-70, 58), (-65, 60), (-60, 55), (-55, 52),
      (-60, 47), (-65, 44), (-70, 42), (-75, 38), (-76, 35), (-80, 32),
      (-81, 26), (-84, 30), (-90, 29), (-97, 26), (-97, 22), (-94, 18),
      (-90, 16), (-87, 13), (-83, 9), (-79, 9), (-77, 7), (-80, 8),
      (-83, 10), (-86, 12), (-88, 15), (-91, 16), (-94, 17), (-97, 19),
      (-100, 20), (-105, 22), (-110, 24), (-114, 28), (-117, 32),
      (-122, 37), (-124, 42), (-125, 48), (-130, 54), (-135, 58),
      (-145, 60), (-155, 58), (-162, 58), (-168, 66)]
GREENLAND = [(-58, 64), (-52, 60), (-45, 60), (-40, 64), (-32, 68),
             (-22, 70), (-30, 74), (-45, 76), (-58, 76), (-60, 70)]
SA = [(-79, 9), (-77, 4), (-80, -3), (-81, -6), (-77, -12), (-72, -18),
      (-70, -23), (-70, -30), (-72, -37), (-73, -44), (-74, -50),
      (-70, -54), (-66, -55), (-68, -50), (-65, -45), (-62, -41),
      (-58, -38), (-52, -33), (-48, -28), (-41, -23), (-39, -17),
      (-35, -9), (-35, -6), (-40, -3), (-44, -2), (-50, 0), (-53, 4),
      (-58, 6), (-62, 9), (-68, 11), (-72, 12), (-76, 10)]
AFRICA = [(-17, 15), (-16, 20), (-15, 27), (-10, 31), (-5, 35), (0, 36),
          (10, 37), (11, 34), (20, 32), (25, 32), (30, 31), (32, 31),
          (34, 28), (35, 24), (37, 20), (39, 18), (43, 12), (48, 11),
          (51, 10), (46, 5), (42, 0), (40, -5), (40, -10), (38, -15),
          (36, -20), (33, -26), (28, -33), (20, -35), (17, -32),
          (15, -27), (13, -20), (12, -15), (13, -10), (12, -6), (9, -1),
          (9, 4), (4, 6), (-2, 5), (-8, 5), (-13, 8), (-17, 12)]
EURASIA = [(-10, 36), (-9, 38), (-9, 43), (-2, 44), (-1, 46), (-4, 48),
           (-2, 50), (0, 51), (3, 53), (8, 57), (10, 59), (5, 60), (5, 62),
           (10, 64), (13, 66), (18, 69), (25, 71), (30, 70), (35, 68),
           (40, 68), (45, 68), (50, 69), (55, 68), (60, 69), (65, 69),
           (70, 72), (75, 73), (80, 73), (85, 74), (90, 75), (95, 76),
           (100, 77), (105, 78), (110, 74), (115, 73), (120, 73),
           (125, 72), (130, 71), (135, 72), (140, 72), (145, 72),
           (150, 70), (155, 69), (160, 69), (165, 66), (170, 66),
           (178, 65), (178, 64), (170, 62), (162, 60), (158, 55),
           (155, 52), (150, 59), (142, 59), (141, 55), (140, 50),
           (138, 46), (135, 43), (132, 43), (130, 42), (129, 39),
           (127, 35), (126, 33), (122, 32), (120, 28), (118, 25),
           (112, 22), (108, 18), (106, 10), (105, 9), (103, 7), (100, 8),
           (98, 10), (97, 15), (94, 17), (92, 21), (90, 22), (88, 22),
           (86, 20), (83, 18), (80, 15), (77, 8), (75, 10), (72, 20),
           (70, 23), (66, 25), (62, 25), (58, 26), (56, 26), (52, 26),
           (50, 29), (48, 30), (42, 32), (38, 34), (36, 36), (33, 36),
           (30, 36), (27, 37), (26, 38), (23, 36), (22, 37), (20, 39),
           (19, 42), (18, 44), (15, 44), (12, 44), (10, 44), (8, 44),
           (6, 43), (3, 43), (0, 40), (-2, 37), (-6, 36), (-9, 37)]
AUSTRALIA = [(113, -22), (114, -30), (115, -35), (118, -35), (124, -33),
             (129, -32), (132, -32), (135, -35), (138, -35), (140, -38),
             (145, -38), (150, -37), (153, -32), (153, -27), (150, -23),
             (146, -19), (142, -15), (142, -11), (137, -12), (135, -15),
             (132, -12), (130, -13), (126, -14), (122, -17), (118, -20),
             (113, -22)]
# Small island / coastal blobs that pins sit on: (clon, clat, rx, ry) deg
BLOBS = [
    (35.0, 31.5, 2.6, 1.6),    # Levant — Gaza pin
    (56.3, 26.3, 1.4, 1.0),    # Musandam — Khasab pin
    (-1.5, 53.0, 2.6, 2.6),    # Great Britain — London pin
    (139.0, 37.0, 2.5, 3.0),   # Japan
    (101.0, -1.0, 2.5, 3.5),   # Sumatra
    (122.0, -2.0, 2.0, 2.0),   # Sulawesi
    (141.0, -4.0, 3.0, 2.0),   # New Guinea
]
JAVA = [(105, -6), (108, -6.5), (111, -7), (114, -7.5), (114, -8.5),
        (110, -8), (106, -7.5), (105, -6.8)]
BORNEO = [(109, 1), (112, 4), (116, 6), (118, 2), (117, -2), (114, -4),
          (110, -3), (109, 1)]
MADAGASCAR = [(44, -16), (47, -15), (50, -16), (49, -20), (47, -25),
              (45, -25), (43, -20), (44, -16)]

MAP_BOX = (16, 674, 452, 854)   # map drawing area inside map panel
MAP_LAT_TOP, MAP_LAT_BOT = 84.0, -58.0


def lonlat_to_xy(lon, lat):
    x0, y0, x1, y1 = MAP_BOX
    x = x0 + (lon + 180.0) / 360.0 * (x1 - x0)
    y = y0 + (MAP_LAT_TOP - lat) / (MAP_LAT_TOP - MAP_LAT_BOT) * (y1 - y0)
    return x, y


def draw_land(draw):
    for poly in (NA, GREENLAND, SA, AFRICA, EURASIA, AUSTRALIA, JAVA,
                 BORNEO, MADAGASCAR):
        pts = [lonlat_to_xy(lon, lat) for lon, lat in poly]
        draw.polygon(pts, fill=LAND, outline=LAND_EDGE)
    for clon, clat, rx, ry in BLOBS:
        cx, cy = lonlat_to_xy(clon, clat)
        sx = rx / 360.0 * (MAP_BOX[2] - MAP_BOX[0])
        sy = ry / (MAP_LAT_TOP - MAP_LAT_BOT) * (MAP_BOX[3] - MAP_BOX[1])
        draw.ellipse([cx - sx, cy - sy, cx + sx, cy + sy],
                     fill=LAND, outline=LAND_EDGE)


def land_mask_image():
    """Black/white mask of land, for the pixel land check on pin centres."""
    m = Image.new("L", (W, H), 0)
    d = ImageDraw.Draw(m)
    for poly in (NA, GREENLAND, SA, AFRICA, EURASIA, AUSTRALIA, JAVA,
                 BORNEO, MADAGASCAR):
        pts = [lonlat_to_xy(lon, lat) for lon, lat in poly]
        d.polygon(pts, fill=255)
    for clon, clat, rx, ry in BLOBS:
        cx, cy = lonlat_to_xy(clon, clat)
        sx = rx / 360.0 * (MAP_BOX[2] - MAP_BOX[0])
        sy = ry / (MAP_LAT_TOP - MAP_LAT_BOT) * (MAP_BOX[3] - MAP_BOX[1])
        d.ellipse([cx - sx, cy - sy, cx + sx, cy + sy], fill=255)
    return m

# ---------------------------------------------------------------- drawing
def draw_masthead(draw):
    draw.rectangle([0, 0, W, 68], fill=NAVY)
    draw.rectangle([0, 68, W, 71], fill=GOLD)
    box = (0, 0, W, 68)
    draw_one(draw, "THE WORLD IN ONE DAY", 16, 12, font(34, bold=True),
             (255, 255, 255), box, "masthead-title")
    draw_one(draw, "THURSDAY 26 NOVEMBER 2026", 1008, 10,
             font(20, bold=True), (255, 255, 255), box,
             "masthead-date", anchor="ra")
    draw_one(draw, "50 STORIES  \u00b7  10 REGIONS  \u00b7  ONE DAY",
             1008, 38, font(11, bold=True), GOLD, box,
             "masthead-sub", anchor="ra")


def draw_date_check(draw):
    draw.rectangle([8, 74, 1016, 122], fill=RED_BG, outline=RED, width=2)
    box = (8, 74, 1016, 122)
    draw_one(draw, "DATE CHECK \u2014 THESE ARE NOT 26 NOVEMBER",
             16, 76, font(11, bold=True), RED, box, "dc-label")
    l1 = "  \u00b7  ".join(f"{i + 1} {DATE_CHECK[i]}" for i in range(4))
    l2 = "  \u00b7  ".join(f"{i + 1} {DATE_CHECK[i]}" for i in range(4, 7))
    draw_one(draw, l1, 16, 90, font(12), INK, box, "dc-line1")
    draw_one(draw, l2, 16, 104, font(12), INK, box, "dc-line2")


def draw_balloon_art(draw, box):
    x0, y0, x1, y1 = box
    register_art(box, "hero1-art")
    draw.rectangle(box, fill=(168, 205, 232))
    # sun + clouds
    draw.ellipse([x1 - 70, y0 + 8, x1 - 30, y0 + 48], fill=(255, 214, 90))
    for cx, cy in ((x0 + 40, y0 + 18), (x0 + 300, y0 + 12)):
        draw.ellipse([cx, cy, cx + 70, cy + 18], fill=(240, 244, 248))
    # skyline
    base = y1
    for bx, bw, bh in ((x0 + 8, 46, 42), (x0 + 60, 34, 58),
                       (x0 + 100, 52, 34), (x0 + 380, 44, 48),
                       (x0 + 430, 38, 40)):
        draw.rectangle([bx, base - bh, bx + bw, base], fill=(70, 82, 105))
    # giant balloon
    cx, cy = (x0 + x1) // 2, y0 + 52
    draw.ellipse([cx - 78, cy - 34, cx + 78, cy + 34], fill=(220, 60, 60))
    draw.ellipse([cx - 78, cy - 34, cx + 78, cy + 34], outline=(140, 20, 20),
                 width=3)
    draw.line([cx - 40, cy - 28, cx - 40, cy + 28], fill=(140, 20, 20),
              width=2)
    draw.line([cx + 40, cy - 28, cx + 40, cy + 28], fill=(140, 20, 20),
              width=2)
    draw.rectangle([cx - 16, cy + 34, cx + 16, cy + 46], fill=(90, 60, 30))
    # rain streaks
    for rx in range(x0 + 20, x1 - 10, 34):
        draw.line([rx, y0 + 66, rx - 8, y0 + 92], fill=(120, 150, 180),
                  width=2)


def draw_tanker_art(draw, box):
    x0, y0, x1, y1 = box
    register_art(box, "hero2-art")
    draw.rectangle(box, fill=(168, 205, 232))
    sea_y = y0 + 88
    draw.rectangle([x0, sea_y, x1, y1], fill=(38, 84, 124))
    # tanker hull + containers
    draw.rectangle([x0 + 10, sea_y - 26, x1 - 10, sea_y + 6], fill=(40, 40, 40))
    for i, col in enumerate(((200, 60, 40), (60, 140, 80), (220, 150, 40))):
        draw.rectangle([x0 + 16 + i * 34, sea_y - 48, x0 + 46 + i * 34,
                        sea_y - 26], fill=col)
    draw.rectangle([x1 - 34, sea_y - 58, x1 - 14, sea_y - 26],
                   fill=(230, 230, 230))
    # flame + smoke
    fx = (x0 + x1) // 2
    draw.polygon([(fx - 16, sea_y - 44), (fx, sea_y - 78),
                  (fx + 16, sea_y - 44)], fill=(255, 140, 0))
    draw.polygon([(fx - 8, sea_y - 44), (fx, sea_y - 62),
                  (fx + 8, sea_y - 44)], fill=(255, 220, 0))
    draw.ellipse([fx - 26, sea_y - 96, fx - 6, sea_y - 76], fill=(90, 90, 90))
    draw.ellipse([fx + 4, sea_y - 104, fx + 24, sea_y - 84], fill=(110, 110, 110))
    # sea mine
    mx, my = x1 - 22, y1 - 14
    draw.ellipse([mx - 8, my - 8, mx + 8, my + 8], fill=(20, 20, 20))
    for dx, dy in ((-10, 0), (10, 0), (0, -10), (0, 10), (-7, -7), (7, 7)):
        draw.line([mx, my, mx + dx, my + dy], fill=(20, 20, 20), width=2)


def draw_chart_art(draw, box):
    x0, y0, x1, y1 = box
    register_art(box, "hero3-art")
    draw.rectangle(box, fill=(232, 240, 228))
    # bars
    base = y1 - 18
    heights = (22, 34, 28, 46, 40, 58, 52, 70)
    bw = (x1 - x0 - 24) // len(heights)
    for i, hh in enumerate(heights):
        bx = x0 + 12 + i * bw
        draw.rectangle([bx, base - hh, bx + bw - 5, base], fill=(120, 160, 120))
    # rising line + arrow
    pts = [(x0 + 12 + i * bw, base - hh - 8) for i, hh in enumerate(heights)]
    draw.line(pts, fill=(34, 120, 60), width=4, joint="curve")
    ex, ey = pts[-1]
    draw.polygon([(ex, ey - 12), (ex + 12, ey + 2), (ex - 2, ey + 2)],
                 fill=(34, 120, 60))
    draw.line([x0 + 8, base, x1 - 8, base], fill=(60, 60, 60), width=2)
    draw.line([x0 + 8, y0 + 10, x0 + 8, base], fill=(60, 60, 60), width=2)

def draw_hero1(draw):
    box = (8, 128, 500, 426)
    draw.rectangle(box, fill=CARD_BG, outline=NAVY, width=2)
    draw.rectangle([8, 128, 500, 134], fill=RED)
    art = (16, 140, 492, 248)
    draw_balloon_art(draw, art)
    inner = (8, 128, 500, 426)
    draw_one(draw, HEROES[0]["kicker"], 16, 254, font(11, bold=True), RED,
             inner, "h1-kicker")
    hl = wrap(HEROES[0]["headline"], font(26, bold=True), 476)
    assert len(hl) <= 2, f"h1 headline wraps to {len(hl)} lines"
    draw_lines(draw, hl, 16, 272, font(26, bold=True), INK, inner, 30,
               "h1-headline")
    dk = wrap(HEROES[0]["deck"], font(12, bold=False), 476)
    assert len(dk) <= 2, f"h1 deck wraps to {len(dk)} lines"
    draw_lines(draw, dk, 16, 336, font(12), INK, inner, 16, "h1-deck")
    wy = wrap(HEROES[0]["why"], font(11), 476)
    assert len(wy) <= 2, f"h1 why wraps to {len(wy)} lines"
    draw_lines(draw, wy, 16, 374, font(11), GREY, inner, 14, "h1-why")


def draw_hero_side(draw, hero, box, art_fn, tag):
    x0, y0, x1, y1 = box
    draw.rectangle(box, fill=CARD_BG, outline=NAVY, width=2)
    draw.rectangle([x0, y0, x1, y0 + 6], fill=RED)
    art = (x0 + 8, y0 + 12, x0 + 142, y1 - 8)
    art_fn(draw, art)
    tx = x0 + 150
    inner = (x0, y0, x1, y1)
    draw_one(draw, hero["kicker"], tx, y0 + 10, font(11, bold=True), RED,
             inner, f"{tag}-kicker")
    hl = wrap(hero["headline"], font(19, bold=True), x1 - 8 - tx)
    assert len(hl) <= 2, f"{tag} headline wraps to {len(hl)} lines"
    cy = draw_lines(draw, hl, tx, y0 + 28, font(19, bold=True), INK, inner,
                    23, f"{tag}-headline")
    dk = wrap(hero["deck"], font(11, bold=False), x1 - 8 - tx)
    assert len(dk) <= 3, f"{tag} deck wraps to {len(dk)} lines"
    cy = draw_lines(draw, dk, tx, cy + 4, font(11), INK, inner, 14,
                    f"{tag}-deck")
    wy = wrap(hero["why"], font(10), x1 - 8 - tx)
    assert len(wy) <= 2, f"{tag} why wraps to {len(wy)} lines"
    draw_lines(draw, wy, tx, cy + 4, font(10), GREY, inner, 13,
               f"{tag}-why")


def draw_cards(draw):
    cols = [8, 211, 414, 617, 820]
    rows = [432, 538]
    accent = [(185, 28, 28), (20, 60, 140), (34, 120, 60), (120, 60, 140),
              (180, 120, 10), (20, 100, 120), (140, 40, 90), (90, 90, 90),
              (200, 90, 20), (40, 90, 160)]
    for i, (region, title, deck, stat, tag) in enumerate(CARDS):
        x0 = cols[i % 5]
        y0 = rows[i // 5]
        x1, y1 = x0 + 196, y0 + 98
        draw.rectangle([x0, y0, x1, y1], fill=CARD_BG, outline=(200, 200, 200))
        draw.rectangle([x0, y0, x0 + 5, y1], fill=accent[i])
        inner = (x0, y0, x1, y1)
        draw_one(draw, region, x0 + 12, y0 + 6, font(9, bold=True),
                 accent[i], inner, f"card{i}-region")
        # tag chip top-right
        tf = font(9, bold=True)
        tw = tf.getlength(tag) + 10
        chip = (x1 - 8 - tw, y0 + 6, x1 - 8, y0 + 22)
        draw.rounded_rectangle(chip, radius=4, fill=TAG_FILL[tag])
        tb = draw.textbbox((chip[0] + 5, y0 + 8), tag, font=tf)
        draw.text((chip[0] + 5, y0 + 8), tag, font=tf, fill=(255, 255, 255))
        TEXT_RECTS.append((tb[0], tb[1], tb[2], tb[3], f"card{i}-tag"))
        ti = wrap(title, font(13, bold=True), 176)
        assert len(ti) <= 2, f"card{i} title wraps to {len(ti)} lines"
        cy = draw_lines(draw, ti, x0 + 12, y0 + 22, font(13, bold=True), INK,
                        inner, 15, f"card{i}-title")
        dk = wrap(deck, font(10), 176)
        assert len(dk) <= 2, f"card{i} deck wraps to {len(dk)} lines"
        cy = draw_lines(draw, dk, x0 + 12, cy + 2, font(10), INK, inner, 12,
                        f"card{i}-deck")
        sf = font(9, bold=True)
        sw = sf.getlength(stat) + 12
        schip = (x0 + 12, y1 - 18, x0 + 12 + sw, y1 - 4)
        draw.rounded_rectangle(schip, radius=4, fill=(240, 234, 220),
                               outline=accent[i])
        sb = draw.textbbox((schip[0] + 6, y1 - 16), stat, font=sf)
        assert sb[2] <= x1 - 10, f"card{i} stat chip overflows"
        draw.text((schip[0] + 6, y1 - 16), stat, font=sf, fill=INK)
        TEXT_RECTS.append((sb[0], sb[1], sb[2], sb[3], f"card{i}-stat"))

def pin_centres():
    """Drawn pin centres in pixels; pin 2 (Philadelphia) is offset so it
    does not touch pin 1 (New York), with a leader line to its true spot."""
    out = []
    for i, (lon, lat, _lbl) in enumerate(PINS):
        x, y = lonlat_to_xy(lon, lat)
        if i == 1:
            x, y = x - 12, y + 8
        out.append((x, y))
    return out


def draw_map_panel(draw, mask):
    box = (8, 642, 460, 1016)
    draw.rectangle(box, fill=(255, 255, 255), outline=NAVY, width=2)
    inner = (8, 642, 460, 1016)
    draw_one(draw, "WHERE IT HAPPENED", 16, 648, font(13, bold=True), NAVY,
             inner, "map-title")
    draw_one(draw, "11 PLACES", 448, 650, font(10, bold=True), GREY, inner,
             "map-count", anchor="ra")
    draw.rectangle(MAP_BOX, fill=OCEAN, outline=LAND_EDGE)
    register_art(MAP_BOX, "map-area")
    draw_land(draw)
    # graticule
    for lon in range(-150, 181, 30):
        x, _ = lonlat_to_xy(lon, 0)
        draw.line([x, MAP_BOX[1], x, MAP_BOX[3]], fill=(235, 240, 245))
    centres = pin_centres()
    # leader line for offset Philadelphia pin (drawn first, under pins)
    tx, ty = lonlat_to_xy(PINS[1][0], PINS[1][1])
    ox, oy = centres[1]
    draw.line([ox, oy, tx, ty], fill=INK, width=2)
    for i, (cx, cy) in enumerate(centres):
        draw.ellipse([cx - PIN_R, cy - PIN_R, cx + PIN_R, cy + PIN_R],
                     fill=RED, outline=(255, 255, 255), width=2)
        nf = font(8, bold=True)
        label = str(i + 1)
        tw = nf.getlength(label)
        draw.text((cx - tw / 2, cy - 5), label, font=nf,
                  fill=(255, 255, 255))
    # legend: two columns, every pin number present
    leg = [(16, 862), (238, 862)]
    for i, (_lon, _lat, lbl) in enumerate(PINS):
        row = i % 6
        y = 862 + row * 24
        x = leg[0][0] if i < 6 else leg[1][0]
        draw.ellipse([x, y + 2, x + 12, y + 14], fill=RED,
                     outline=(255, 255, 255))
        nf = font(8, bold=True)
        num = str(i + 1)
        draw.text((x + 6 - nf.getlength(num) / 2, y + 4), num, font=nf,
                  fill=(255, 255, 255))
        txt = f"{lbl}"
        bb = draw.textbbox((x + 18, y + 2), txt, font=font(10))
        assert bb[2] <= 452 - 2, f"legend {i + 1} overflows panel"
        draw.text((x + 18, y + 2), txt, font=font(10), fill=INK)
        TEXT_RECTS.append((bb[0], bb[1], bb[2], bb[3], f"legend{i + 1}"))
    return centres


def draw_also_panel(draw):
    box = (468, 642, 1016, 1016)
    draw.rectangle(box, fill=(255, 255, 255), outline=NAVY, width=2)
    inner = (468, 642, 1016, 1016)
    draw_one(draw, "ALSO ON 26 NOVEMBER \u2014 37 MORE STORIES", 476, 648,
             font(13, bold=True), NAVY, inner, "also-title")
    cols = [(476, 736), (744, 1008)]
    fnt = font(9)
    for i, item in enumerate(ALSO):
        col = 0 if i < 19 else 1
        row = i if i < 19 else i - 19
        x0, x1 = cols[col]
        y = 678 + row * 17
        lines = wrap(item, fnt, x1 - x0 - 12)
        assert len(lines) == 1, f"ALSO {i + 1} wraps to {len(lines)}: {item!r}"
        draw.ellipse([x0, y + 3, x0 + 5, y + 8], fill=RED)
        draw_one(draw, item, x0 + 10, y, fnt, INK,
                 (x0, y - 2, x1, y + 15), f"also{i + 1}")


# ---------------------------------------------------------------- asserts
PREPS = {"in", "on", "at", "to", "of", "for", "by", "with", "from", "after",
         "before", "over", "under", "into", "per", "via", "amid", "near"}


def shingles(text, n=4):
    words = text.lower().replace("\u2014", " ").split()
    words = [w.strip(".,;:!?\"'()[]") for w in words]
    return {" ".join(words[i:i + n]) for i in range(len(words) - n + 1)}


def run_asserts(centres, mask):
    assert len(ALSO) == 37, f"ALSO has {len(ALSO)} items, need 37"
    assert DATE_CHECK == [
        "COP31 failed 22 Nov",
        "Shenzhou-24 launched 25 Nov",
        "Cairo tanker blast, 31 dead, 25 Nov",
        "Cartagena hostages freed 25 Nov",
        "Australia-Solomon pact 25 Nov",
        "UK energy prices +26% announced 25 Nov",
        "Huawei convicted 24 Nov",
    ], "DATE CHECK list does not match the verbatim 7"
    assert len(PINS) == 11 and 10 <= len(PINS) <= 12
    # pins: on land (pixel check on mask), inside panel, spaced apart
    for i, (cx, cy) in enumerate(centres):
        assert mask.getpixel((int(cx), int(cy))) == 255, \
            f"pin {i + 1} centre is not on land: {(cx, cy)}"
        assert (MAP_BOX[0] + PIN_R + 2 <= cx <= MAP_BOX[2] - PIN_R - 2
                and MAP_BOX[1] + PIN_R + 2 <= cy <= MAP_BOX[3] - PIN_R - 2), \
            f"pin {i + 1} circle not fully inside map panel"
    for i in range(len(centres)):
        for j in range(i + 1, len(centres)):
            dx = centres[i][0] - centres[j][0]
            dy = centres[i][1] - centres[j][1]
            assert (dx * dx + dy * dy) ** 0.5 >= 2 * PIN_R + 2, \
                f"pins {i + 1} and {j + 1} too close"
    assert {i + 1 for i in range(len(PINS))} == set(range(1, 12))
    # every ALSO item carries a tag, is not ending on a preposition
    for i, item in enumerate(ALSO):
        assert any(t in item for t in ("[C]", "[R]", "[CL]")), \
            f"ALSO {i + 1} has no tag: {item!r}"
        before_tag = item.rsplit("[", 1)[0].split()
        assert before_tag and before_tag[-1].lower() not in PREPS, \
            f"ALSO {i + 1} ends on a preposition: {item!r}"
        if "25 Nov" in item:
            assert "[CL]" in item, f"ALSO {i + 1} is 25 Nov but not [CL]"
    # no duplicated story between heroes/cards and ALSO (4-word shingles)
    hero_card_texts = [h["headline"] + " " + h["deck"] for h in HEROES]
    hero_card_texts += [t + " " + d for _r, t, d, _s, _t in CARDS]
    base_sh = set()
    for t in hero_card_texts:
        base_sh |= shingles(t)
    for i, item in enumerate(ALSO):
        clash = shingles(item) & base_sh
        assert not clash, f"ALSO {i + 1} duplicates hero/card: {clash}"
    also_sh = set()
    for i, item in enumerate(ALSO):
        s = shingles(item)
        assert not (s & also_sh), f"ALSO {i + 1} duplicates another ALSO item"
        also_sh |= s
    # forbidden strings / caps across all rendered text
    all_text = " ".join([h["kicker"] + " " + h["headline"] + " " + h["deck"]
                         for h in HEROES])
    all_text += " " + " ".join(t + " " + d for _r, t, d, _s, _t in CARDS)
    all_text += " " + " ".join(ALSO) + " " + " ".join(DATE_CHECK)
    for bad in ("186", "161", "720", "Bangchak", "significant figure",
                "third senior Hamas official", "AWACS",
                "Brazil wins WTO", "Australia passes new gas law",
                "tariffs announced"):
        assert bad not in all_text, f"forbidden string present: {bad!r}"
    assert all_text.count("Ras Tanura") <= 1, "Ras Tanura appears >1x"
    assert all_text.count("Riyadh") <= 1, "Riyadh appears >1x"
    check_art_text_separation()


def main():
    img = Image.new("RGB", (W, H), PAPER)
    draw = ImageDraw.Draw(img)
    mask = land_mask_image()
    draw_masthead(draw)
    draw_date_check(draw)
    draw_hero1(draw)
    draw_hero_side(draw, HEROES[1], (508, 128, 1016, 272), draw_tanker_art,
                   "h2")
    draw_hero_side(draw, HEROES[2], (508, 280, 1016, 426), draw_chart_art,
                   "h3")
    draw_cards(draw)
    centres = draw_map_panel(draw, mask)
    draw_also_panel(draw)
    run_asserts(centres, mask)
    img.save(OUT, optimize=True)
    print(f"wrote {OUT} {os.path.getsize(OUT)} bytes")


if __name__ == "__main__":
    main()
