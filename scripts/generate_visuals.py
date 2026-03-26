"""
Generate all visual assets for Africa x Caribbean Live watch party.
Outputs: hero poster, team cards, OG image, and social media kit.
Design philosophy: Diasporic Voltage — kinetic opposition, chromatic tension.
"""

import math
import os
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

# Paths
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PUBLIC = os.path.join(BASE, "public")
SOCIAL = os.path.join(PUBLIC, "social")
FONTS = r"C:\Users\bukas\AppData\Roaming\Claude\local-agent-mode-sessions\skills-plugin\4c55955b-0256-4ad7-a217-fdf21e39cbe3\76653da3-e734-4180-bebb-e75bc6a4754e\skills\canvas-design\canvas-fonts"

os.makedirs(SOCIAL, exist_ok=True)

# Colors
SLATE_950 = (2, 6, 23)
ORANGE = (234, 88, 12)
ORANGE_DARK = (180, 60, 8)
CYAN = (14, 165, 233)
BLUE_DEEP = (30, 64, 175)
WHITE = (255, 255, 255)
WHITE_DIM = (148, 163, 184)
GOLD = (247, 214, 24)

def load_font(name, size):
    path = os.path.join(FONTS, name)
    try:
        return ImageFont.truetype(path, size)
    except:
        return ImageFont.load_default()

def radial_glow(draw, cx, cy, radius, color, steps=60):
    """Draw a soft radial glow."""
    for i in range(steps, 0, -1):
        alpha = int((i / steps) * 40)
        r = int(radius * (i / steps))
        c = (*color, alpha)
        draw.ellipse([cx - r, cy - r, cx + r, cy + r], fill=c)

def draw_diagonal_split(img, color_left, color_right, angle_offset=0):
    """Create a diagonal gradient split with atmospheric blending."""
    w, h = img.size
    overlay = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    for y in range(h):
        for x in range(0, w, 2):
            # Diagonal position: how far left or right of center diagonal
            diag_pos = (x / w) - (y / h) + angle_offset
            if diag_pos < -0.15:
                # Left zone (Africa - orange)
                intensity = min(1.0, abs(diag_pos + 0.15) * 2)
                alpha = int(intensity * 25)
                draw.rectangle([x, y, x + 1, y], fill=(*color_left, alpha))
            elif diag_pos > 0.15:
                # Right zone (Caribbean - cyan)
                intensity = min(1.0, abs(diag_pos - 0.15) * 2)
                alpha = int(intensity * 25)
                draw.rectangle([x, y, x + 1, y], fill=(*color_right, alpha))

    img.paste(Image.alpha_composite(Image.new("RGBA", img.size, (0,0,0,0)), overlay), (0, 0), overlay)

def add_noise(img, amount=8):
    """Add subtle film grain."""
    random.seed(42)
    pixels = img.load()
    w, h = img.size
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            noise = random.randint(-amount, amount)
            r, g, b = pixels[x, y][:3]
            pixels[x, y] = (
                max(0, min(255, r + noise)),
                max(0, min(255, g + noise)),
                max(0, min(255, b + noise)),
            )

def draw_grid_lines(draw, w, h, spacing=80, color=(255, 255, 255, 6)):
    """Draw subtle grid lines for structure."""
    for x in range(0, w, spacing):
        draw.line([(x, 0), (x, h)], fill=color, width=1)
    for y in range(0, h, spacing):
        draw.line([(0, y), (w, y)], fill=color, width=1)

def draw_soccer_ball(draw, cx, cy, radius, color=(255, 255, 255, 60)):
    """Draw a stylized soccer ball outline."""
    # Outer circle
    draw.ellipse([cx-radius, cy-radius, cx+radius, cy+radius], outline=color, width=2)
    # Pentagon pattern (simplified)
    for angle_deg in range(0, 360, 72):
        angle = math.radians(angle_deg)
        x1 = cx + int(radius * 0.6 * math.cos(angle))
        y1 = cy + int(radius * 0.6 * math.sin(angle))
        x2 = cx + int(radius * math.cos(angle))
        y2 = cy + int(radius * math.sin(angle))
        draw.line([(x1, y1), (x2, y2)], fill=color, width=1)
    # Inner pentagon
    points = []
    for angle_deg in range(0, 360, 72):
        angle = math.radians(angle_deg - 90)
        points.append((cx + int(radius * 0.35 * math.cos(angle)),
                       cy + int(radius * 0.35 * math.sin(angle))))
    draw.polygon(points, outline=color)

def text_center_x(draw, text, font, canvas_width):
    bbox = draw.textbbox((0, 0), text, font=font)
    tw = bbox[2] - bbox[0]
    return (canvas_width - tw) // 2

# ============================================================
# 1. HERO POSTER (800x1000)
# ============================================================
def create_hero_poster():
    W, H = 800, 1000
    img = Image.new("RGBA", (W, H), (*SLATE_950, 255))
    draw = ImageDraw.Draw(img)

    # Background atmospheric glows
    glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    glow_draw = ImageDraw.Draw(glow_layer)

    # Orange glow - left side
    radial_glow(glow_draw, 100, 300, 500, ORANGE, 80)
    # Blue glow - right side
    radial_glow(glow_draw, 700, 700, 500, CYAN, 80)
    # Central collision glow
    radial_glow(glow_draw, 400, 500, 300, (255, 255, 255), 40)

    img = Image.alpha_composite(img, glow_layer)
    draw = ImageDraw.Draw(img)

    # Subtle grid
    grid_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    grid_draw = ImageDraw.Draw(grid_layer)
    draw_grid_lines(grid_draw, W, H, 60, (255, 255, 255, 4))
    img = Image.alpha_composite(img, grid_layer)
    draw = ImageDraw.Draw(img)

    # Diagonal light streak
    streak = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    streak_draw = ImageDraw.Draw(streak)
    for i in range(40):
        alpha = int((1 - i / 40) * 15)
        offset = i * 3
        streak_draw.line([(0, 350 + offset), (W, 650 + offset)],
                        fill=(255, 255, 255, alpha), width=2)
    img = Image.alpha_composite(img, streak)
    draw = ImageDraw.Draw(img)

    # Soccer ball watermark
    ball_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    ball_draw = ImageDraw.Draw(ball_layer)
    draw_soccer_ball(ball_draw, 400, 480, 120, (255, 255, 255, 20))
    img = Image.alpha_composite(img, ball_layer)
    draw = ImageDraw.Draw(img)

    # Top badge
    font_mono_sm = load_font("GeistMono-Regular.ttf", 11)
    badge_text = "2026 FIFA WORLD CUP QUALIFIERS"
    bx = text_center_x(draw, badge_text, font_mono_sm, W)
    # Badge background
    bbox = draw.textbbox((bx, 60), badge_text, font=font_mono_sm)
    pad = 12
    draw.rounded_rectangle([bbox[0]-pad, bbox[1]-6, bbox[2]+pad, bbox[3]+6],
                          radius=20, fill=(255, 255, 255, 15), outline=(255, 255, 255, 30))
    draw.text((bx, 60), badge_text, font=font_mono_sm, fill=(247, 214, 24, 220))

    # Live indicator dot
    dot_x = bx - 18
    dot_y = 66
    draw.ellipse([dot_x, dot_y, dot_x+8, dot_y+8], fill=(239, 68, 68, 255))

    # Main title - AFRICA
    font_title = load_font("BigShoulders-Bold.ttf", 130)
    font_vs = load_font("InstrumentSans-BoldItalic.ttf", 60)
    font_subtitle = load_font("BigShoulders-Bold.ttf", 130)

    # AFRICA
    ax = text_center_x(draw, "AFRICA", font_title, W)
    # Orange gradient effect via layered text
    draw.text((ax+3, 203), "AFRICA", font=font_title, fill=(0, 0, 0, 80))
    draw.text((ax, 200), "AFRICA", font=font_title, fill=ORANGE)
    # Bright highlight on top
    highlight = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hdraw = ImageDraw.Draw(highlight)
    hdraw.text((ax, 198), "AFRICA", font=font_title, fill=(255, 140, 50, 60))
    img = Image.alpha_composite(img, highlight)
    draw = ImageDraw.Draw(img)

    # VS
    vx = text_center_x(draw, "VERSUS", font_vs, W)
    draw.text((vx, 340), "VERSUS", font=font_vs, fill=(255, 255, 255, 100))

    # Decorative line through VS
    draw.line([(100, 375), (vx - 15, 375)], fill=(255, 255, 255, 40), width=1)
    bbox_vs = draw.textbbox((vx, 340), "VERSUS", font=font_vs)
    draw.line([(bbox_vs[2] + 15, 375), (700, 375)], fill=(255, 255, 255, 40), width=1)

    # CARIBBEAN
    cx_text = text_center_x(draw, "CARIBBEAN", font_subtitle, W)
    draw.text((cx_text+3, 403), "CARIBBEAN", font=font_subtitle, fill=(0, 0, 0, 80))
    draw.text((cx_text, 400), "CARIBBEAN", font=font_subtitle, fill=CYAN)
    # Highlight
    highlight2 = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    hdraw2 = ImageDraw.Draw(highlight2)
    hdraw2.text((cx_text, 398), "CARIBBEAN", font=font_subtitle, fill=(80, 200, 255, 60))
    img = Image.alpha_composite(img, highlight2)
    draw = ImageDraw.Draw(img)

    # LIVE WATCH PARTY subtitle
    font_sub = load_font("InstrumentSans-Bold.ttf", 28)
    sub_text = "LIVE WATCH PARTY"
    sx = text_center_x(draw, sub_text, font_sub, W)
    draw.text((sx, 560), sub_text, font=font_sub, fill=(255, 255, 255, 180))

    # Decorative accent lines
    draw.line([(250, 600), (550, 600)], fill=(255, 255, 255, 25), width=1)

    # Date
    font_date = load_font("GeistMono-Bold.ttf", 22)
    date_text = "MARCH 26, 2026"
    dx = text_center_x(draw, date_text, font_date, W)
    draw.text((dx, 620), date_text, font=font_date, fill=GOLD)

    # Time
    font_time = load_font("GeistMono-Regular.ttf", 16)
    time_text = "8:00 PM UTC  •  GLOBAL DISCORD STADIUM"
    tx = text_center_x(draw, time_text, font_time, W)
    draw.text((tx, 660), time_text, font=font_time, fill=WHITE_DIM)

    # Country flags row (as text)
    font_flags = load_font("InstrumentSans-Regular.ttf", 14)
    flags_text = "NIGERIA  •  JAMAICA  •  DR CONGO  •  TRINIDAD  •  GHANA  •  HAITI"
    fx = text_center_x(draw, flags_text, font_flags, W)
    draw.text((fx, 720), flags_text, font=font_flags, fill=(255, 255, 255, 60))

    # Bottom bar
    draw.line([(0, 920), (W, 920)], fill=(255, 255, 255, 15), width=1)

    font_bottom = load_font("GeistMono-Regular.ttf", 10)
    draw.text((30, 940), "VIRTUAL WATCH PARTY 2026", font=font_bottom, fill=(255, 255, 255, 40))
    draw.text((30, 960), "A LEOPARDS USA EXPERIENCE", font=font_bottom, fill=(234, 88, 12, 80))

    right_text = "discord.gg/africa-caribbean"
    rbbox = draw.textbbox((0, 0), right_text, font=font_bottom)
    rw = rbbox[2] - rbbox[0]
    draw.text((W - 30 - rw, 940), right_text, font=font_bottom, fill=(255, 255, 255, 40))
    draw.text((W - 30 - rw, 960), "FREE ENTRY  •  DONATIONS WELCOME", font=font_bottom, fill=(255, 255, 255, 30))

    # Convert and save
    final = img.convert("RGB")
    add_noise(final, 5)
    final.save(os.path.join(PUBLIC, "image.png"), quality=95)
    print("  ✓ Hero poster saved")

# ============================================================
# 2. TEAM CARDS (600x400 each)
# ============================================================
def create_team_card(name, color_primary, color_secondary, filename, symbol_fn):
    W, H = 600, 400
    img = Image.new("RGBA", (W, H), (*SLATE_950, 255))

    # Glow
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    radial_glow(gdraw, 150, 200, 400, color_primary, 60)
    radial_glow(gdraw, 450, 300, 300, color_secondary, 40)
    img = Image.alpha_composite(img, glow)

    draw = ImageDraw.Draw(img)

    # Grid
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw2 = ImageDraw.Draw(grid)
    draw_grid_lines(gdraw2, W, H, 40, (255, 255, 255, 3))
    img = Image.alpha_composite(img, grid)
    draw = ImageDraw.Draw(img)

    # Symbol
    symbol_fn(draw, W, H)

    # Team name
    font_name = load_font("BigShoulders-Bold.ttf", 72)
    nx = text_center_x(draw, name, font_name, W)
    draw.text((nx+2, 152), name, font=font_name, fill=(0, 0, 0, 60))
    draw.text((nx, 150), name, font=font_name, fill=color_primary)

    # Subtitle
    font_sub = load_font("GeistMono-Regular.ttf", 13)
    sub = "SELECT YOUR TRIBE  •  JOIN THE DISCORD"
    sx = text_center_x(draw, sub, font_sub, W)
    draw.text((sx, 240), sub, font=font_sub, fill=(255, 255, 255, 80))

    # Border
    draw.rounded_rectangle([2, 2, W-3, H-3], radius=16, outline=(*color_primary, 40), width=1)

    final = img.convert("RGB")
    add_noise(final, 4)
    final.save(os.path.join(PUBLIC, filename), quality=95)
    print(f"  ✓ {filename} saved")

def africa_symbol(draw, w, h):
    # Flame-like shapes
    layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    ldraw = ImageDraw.Draw(layer)
    # Abstract flame arcs
    for i in range(5):
        y_off = i * 15
        alpha = 15 - i * 2
        ldraw.arc([200 - i*20, 60 + y_off, 400 + i*20, 200 + y_off],
                  200, 340, fill=(*ORANGE, alpha), width=3)
    # Return composite not needed, draw on main

def caribbean_symbol(draw, w, h):
    # Wave-like shapes
    for i in range(6):
        y = 80 + i * 12
        alpha = 20 - i * 3
        points = []
        for x in range(0, w, 4):
            wave_y = y + int(15 * math.sin((x + i * 30) / 40))
            points.append((x, wave_y))
        if len(points) > 1:
            draw.line(points, fill=(*CYAN, max(5, alpha)), width=2)

# ============================================================
# 3. OG IMAGE (1200x630)
# ============================================================
def create_og_image():
    W, H = 1200, 630
    img = Image.new("RGBA", (W, H), (*SLATE_950, 255))

    # Glows
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    radial_glow(gdraw, 200, 315, 500, ORANGE, 60)
    radial_glow(gdraw, 1000, 315, 500, CYAN, 60)
    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)

    # Title
    font_title = load_font("BigShoulders-Bold.ttf", 100)
    font_vs = load_font("InstrumentSans-BoldItalic.ttf", 40)

    # AFRICA
    ax = text_center_x(draw, "AFRICA", font_title, W)
    draw.text((ax, 140), "AFRICA", font=font_title, fill=ORANGE)

    # VS
    vx = text_center_x(draw, "VS", font_vs, W)
    draw.text((vx, 250), "VS", font=font_vs, fill=(255, 255, 255, 120))

    # CARIBBEAN
    cx_t = text_center_x(draw, "CARIBBEAN", font_title, W)
    draw.text((cx_t, 290), "CARIBBEAN", font=font_title, fill=CYAN)

    # Subtitle
    font_sub = load_font("InstrumentSans-Bold.ttf", 22)
    sub = "LIVE WATCH PARTY  •  MARCH 26, 2026  •  DISCORD"
    sx = text_center_x(draw, sub, font_sub, W)
    draw.text((sx, 430), sub, font=font_sub, fill=(255, 255, 255, 160))

    # Bottom bar
    font_bot = load_font("GeistMono-Regular.ttf", 12)
    bot = "THE GLOBAL WATCH ROOM  •  A LEOPARDS USA EXPERIENCE"
    bx = text_center_x(draw, bot, font_bot, W)
    draw.text((bx, 570), bot, font=font_bot, fill=(255, 255, 255, 50))

    final = img.convert("RGB")
    add_noise(final, 4)
    final.save(os.path.join(PUBLIC, "og-image.png"), quality=95)
    print("  ✓ OG image saved")

# ============================================================
# 4. SOCIAL MEDIA KIT
# ============================================================
def create_social_square(title_lines, subtitle, accent_color, filename, badge_text=None):
    """Generic square social graphic (1080x1080)."""
    W, H = 1080, 1080
    img = Image.new("RGBA", (W, H), (*SLATE_950, 255))

    # Glows
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    radial_glow(gdraw, 200, 400, 600, ORANGE, 70)
    radial_glow(gdraw, 880, 680, 600, CYAN, 70)
    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)

    # Grid
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw2 = ImageDraw.Draw(grid)
    draw_grid_lines(gdraw2, W, H, 60, (255, 255, 255, 3))
    img = Image.alpha_composite(img, grid)
    draw = ImageDraw.Draw(img)

    # Top badge
    if badge_text:
        font_badge = load_font("GeistMono-Regular.ttf", 13)
        bx = text_center_x(draw, badge_text, font_badge, W)
        bbox = draw.textbbox((bx, 80), badge_text, font=font_badge)
        draw.rounded_rectangle([bbox[0]-14, bbox[1]-8, bbox[2]+14, bbox[3]+8],
                              radius=20, fill=(255, 255, 255, 12), outline=(255, 255, 255, 25))
        draw.text((bx, 80), badge_text, font=font_badge, fill=GOLD)

    # Soccer ball watermark
    ball = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(ball)
    draw_soccer_ball(bdraw, 540, 500, 180, (255, 255, 255, 10))
    img = Image.alpha_composite(img, ball)
    draw = ImageDraw.Draw(img)

    # Title lines
    font_big = load_font("BigShoulders-Bold.ttf", 110)
    y_start = 300
    for i, line in enumerate(title_lines):
        lx = text_center_x(draw, line, font_big, W)
        color = ORANGE if i == 0 else CYAN if i == 2 else (255, 255, 255, 200)
        if isinstance(color, tuple) and len(color) == 3:
            draw.text((lx+3, y_start + i * 120 + 3), line, font=font_big, fill=(0,0,0,60))
        draw.text((lx, y_start + i * 120), line, font=font_big, fill=color)

    # Subtitle
    font_sub = load_font("InstrumentSans-Bold.ttf", 24)
    sx = text_center_x(draw, subtitle, font_sub, W)
    draw.text((sx, 750), subtitle, font=font_sub, fill=(255, 255, 255, 150))

    # Bottom
    font_bot = load_font("GeistMono-Regular.ttf", 12)
    bot = "VIRTUAL WATCH PARTY 2026  •  A LEOPARDS USA EXPERIENCE"
    botx = text_center_x(draw, bot, font_bot, W)
    draw.text((botx, 980), bot, font=font_bot, fill=(255, 255, 255, 40))

    # Border
    draw.rounded_rectangle([20, 20, W-21, H-21], radius=24, outline=(255, 255, 255, 15), width=1)

    final = img.convert("RGB")
    add_noise(final, 4)
    final.save(os.path.join(SOCIAL, filename), quality=95)
    print(f"  ✓ {filename} saved")

def create_social_story():
    """Vertical story (1080x1920)."""
    W, H = 1080, 1920
    img = Image.new("RGBA", (W, H), (*SLATE_950, 255))

    # Glows
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw = ImageDraw.Draw(glow)
    radial_glow(gdraw, 200, 500, 700, ORANGE, 80)
    radial_glow(gdraw, 880, 1400, 700, CYAN, 80)
    radial_glow(gdraw, 540, 960, 400, (255, 255, 255), 30)
    img = Image.alpha_composite(img, glow)
    draw = ImageDraw.Draw(img)

    # Grid
    grid = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gdraw2 = ImageDraw.Draw(grid)
    draw_grid_lines(gdraw2, W, H, 60, (255, 255, 255, 3))
    img = Image.alpha_composite(img, grid)
    draw = ImageDraw.Draw(img)

    # Top badge
    font_badge = load_font("GeistMono-Regular.ttf", 14)
    badge = "2026 FIFA WORLD CUP QUALIFIERS"
    bx = text_center_x(draw, badge, font_badge, W)
    bbox = draw.textbbox((bx, 180), badge, font=font_badge)
    draw.rounded_rectangle([bbox[0]-16, bbox[1]-10, bbox[2]+16, bbox[3]+10],
                          radius=20, fill=(255, 255, 255, 12), outline=(255, 255, 255, 25))
    draw.text((bx, 180), badge, font=font_badge, fill=GOLD)

    # Soccer ball
    ball = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    bdraw = ImageDraw.Draw(ball)
    draw_soccer_ball(bdraw, 540, 800, 200, (255, 255, 255, 12))
    img = Image.alpha_composite(img, ball)
    draw = ImageDraw.Draw(img)

    # Title
    font_mega = load_font("BigShoulders-Bold.ttf", 140)
    font_vs = load_font("InstrumentSans-BoldItalic.ttf", 50)

    lines = [("AFRICA", ORANGE, 500), ("VERSUS", (255,255,255,100), 660), ("CARIBBEAN", CYAN, 780)]
    for text, color, y in lines:
        font = font_vs if text == "VERSUS" else font_mega
        tx = text_center_x(draw, text, font, W)
        if len(color) == 3:
            draw.text((tx+3, y+3), text, font=font, fill=(0,0,0,60))
        draw.text((tx, y), text, font=font, fill=color)

    # Subtitle
    font_sub = load_font("InstrumentSans-Bold.ttf", 30)
    sub = "LIVE WATCH PARTY"
    sx = text_center_x(draw, sub, font_sub, W)
    draw.text((sx, 960), sub, font=font_sub, fill=(255, 255, 255, 180))

    # Date
    font_date = load_font("GeistMono-Bold.ttf", 26)
    date = "MARCH 26, 2026  •  8:00 PM UTC"
    dx = text_center_x(draw, date, font_date, W)
    draw.text((dx, 1040), date, font=font_date, fill=GOLD)

    # CTA box
    cta_y = 1250
    draw.rounded_rectangle([200, cta_y, 880, cta_y + 80], radius=40,
                          fill=(*ORANGE, 230))
    font_cta = load_font("InstrumentSans-Bold.ttf", 26)
    cta = "JOIN THE DISCORD"
    ctx = text_center_x(draw, cta, font_cta, W)
    draw.text((ctx, cta_y + 22), cta, font=font_cta, fill=WHITE)

    # Flags text
    font_flags = load_font("InstrumentSans-Regular.ttf", 16)
    flags = "NIGERIA • JAMAICA • DR CONGO • TRINIDAD • GHANA • HAITI"
    fx = text_center_x(draw, flags, font_flags, W)
    draw.text((fx, 1400), flags, font=font_flags, fill=(255, 255, 255, 50))

    # Bottom
    font_bot = load_font("GeistMono-Regular.ttf", 11)
    bot = "A LEOPARDS USA EXPERIENCE"
    botx = text_center_x(draw, bot, font_bot, W)
    draw.text((botx, 1780), bot, font=font_bot, fill=(255, 255, 255, 35))

    final = img.convert("RGB")
    add_noise(final, 4)
    final.save(os.path.join(SOCIAL, "social-story.png"), quality=95)
    print("  ✓ social-story.png saved")


# ============================================================
# RUN ALL
# ============================================================
if __name__ == "__main__":
    print("\n🎨 Generating Africa x Caribbean Live visual assets...\n")

    print("[1/7] Hero poster (800x1000)")
    create_hero_poster()

    print("[2/7] Team Africa card")
    create_team_card("TEAM AFRICA", ORANGE, ORANGE_DARK, "team-africa-card.png", africa_symbol)

    print("[3/7] Team Caribbean card")
    create_team_card("TEAM CARIBBEAN", CYAN, BLUE_DEEP, "team-caribbean-card.png", caribbean_symbol)

    print("[4/7] OG image (1200x630)")
    create_og_image()

    print("[5/7] Social announce (1080x1080)")
    create_social_square(
        ["AFRICA", "VERSUS", "CARIBBEAN"],
        "LIVE WATCH PARTY  •  MARCH 26, 2026",
        ORANGE, "social-announce.png",
        badge_text="2026 FIFA WORLD CUP QUALIFIERS"
    )

    print("[6/7] Social countdown (1080x1080)")
    create_social_square(
        ["MATCH DAY", "IS", "TOMORROW"],
        "JOIN THE GLOBAL DISCORD STADIUM",
        GOLD, "social-countdown.png",
        badge_text="AFRICA x CARIBBEAN LIVE"
    )

    print("[7/7] Social story (1080x1920)")
    create_social_story()

    # social-join
    print("[BONUS] Social join CTA (1080x1080)")
    create_social_square(
        ["JOIN THE", "WATCH", "PARTY"],
        "FREE DISCORD ACCESS  •  DONATIONS WELCOME",
        CYAN, "social-join.png",
        badge_text="VIRTUAL STADIUM  •  MARCH 26"
    )

    print("\n✅ All 8 visual assets generated!")
    print(f"   Hero:   {os.path.join(PUBLIC, 'image.png')}")
    print(f"   Cards:  {PUBLIC}/team-*.png")
    print(f"   OG:     {os.path.join(PUBLIC, 'og-image.png')}")
    print(f"   Social: {SOCIAL}/")
