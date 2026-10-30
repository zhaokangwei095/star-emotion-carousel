from __future__ import annotations

import argparse
import json
import math
import random
import re
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable

from PIL import Image, ImageDraw, ImageFilter, ImageFont


SERIF_PATH = r"C:\Windows\Fonts\NotoSerifSC-VF.ttf"
SANS_PATH = r"C:\Windows\Fonts\NotoSansSC-VF.ttf"

NO_LINE_START = set("，。！？；：、）》】」』’”％‰…")
NO_LINE_END = set("（《【「『‘“")
FOCUS_LABEL_GAP = 52
FOCUS_BODY_GAP = 46


@dataclass(frozen=True)
class Style:
    key: str
    label: str
    width: int
    height: int
    bg: str
    title_color: str
    body_color: str
    muted: str
    accent: str
    secondary: str
    title_font_path: str
    title_weight: bytes
    title_size: int
    title_line_gap: int
    body_font_path: str
    body_weight: bytes
    body_size: int
    body_line_gap: int
    margin_x: int
    body_width: int
    title_y: int
    cover_body_gap: int
    page_body_top: int
    cover_body_bottom: int
    body_bottom: int
    paragraph_gap: int
    footer_mode: str
    decoration: str
    panel_rgba: tuple[int, int, int, int] | None = None

    @property
    def aspect_ratio(self) -> float:
        return self.width / self.height


STYLES: dict[str, Style] = {
    "blush-manuscript": Style(
        key="blush-manuscript",
        label="白桃式淡粉手稿",
        width=1080,
        height=1800,
        bg="#FCF9F8",
        title_color="#D72B58",
        body_color="#272225",
        muted="#D58A9B",
        accent="#F3C7D2",
        secondary="#F8E3E8",
        title_font_path=SERIF_PATH,
        title_weight=b"Black",
        title_size=112,
        title_line_gap=30,
        body_font_path=SERIF_PATH,
        body_weight=b"Regular",
        body_size=38,
        body_line_gap=27,
        margin_x=82,
        body_width=916,
        title_y=360,
        cover_body_gap=76,
        page_body_top=92,
        cover_body_bottom=1548,
        body_bottom=1712,
        paragraph_gap=54,
        footer_mode="none",
        decoration="blush",
    ),
    "nocturne": Style(
        key="nocturne",
        label="夜航星图",
        width=1080,
        height=1440,
        bg="#0F1B2B",
        title_color="#F4EBDD",
        body_color="#E3D8C7",
        muted="#8293A3",
        accent="#C9A553",
        secondary="#D15B43",
        title_font_path=SERIF_PATH,
        title_weight=b"Black",
        title_size=96,
        title_line_gap=22,
        body_font_path=SANS_PATH,
        body_weight=b"Medium",
        body_size=30,
        body_line_gap=18,
        margin_x=78,
        body_width=880,
        title_y=260,
        cover_body_gap=58,
        page_body_top=106,
        cover_body_bottom=1218,
        body_bottom=1322,
        paragraph_gap=34,
        footer_mode="index",
        decoration="nocturne",
    ),
    "sage-letter": Style(
        key="sage-letter",
        label="鼠尾草来信",
        width=1080,
        height=1440,
        bg="#F3EDE2",
        title_color="#344536",
        body_color="#2C2C28",
        muted="#7A8A72",
        accent="#AA6040",
        secondary="#C7D2BE",
        title_font_path=SERIF_PATH,
        title_weight=b"Bold",
        title_size=102,
        title_line_gap=24,
        body_font_path=SERIF_PATH,
        body_weight=b"Regular",
        body_size=31,
        body_line_gap=20,
        margin_x=88,
        body_width=852,
        title_y=306,
        cover_body_gap=64,
        page_body_top=104,
        cover_body_bottom=1206,
        body_bottom=1324,
        paragraph_gap=40,
        footer_mode="brand",
        decoration="sage",
    ),
    "cobalt-grid": Style(
        key="cobalt-grid",
        label="钴蓝编辑网格",
        width=1080,
        height=1440,
        bg="#F4F0E6",
        title_color="#14213D",
        body_color="#20242C",
        muted="#727783",
        accent="#E24A33",
        secondary="#2F54C6",
        title_font_path=SANS_PATH,
        title_weight=b"Black",
        title_size=90,
        title_line_gap=22,
        body_font_path=SANS_PATH,
        body_weight=b"Regular",
        body_size=30,
        body_line_gap=18,
        margin_x=80,
        body_width=860,
        title_y=300,
        cover_body_gap=54,
        page_body_top=102,
        cover_body_bottom=1194,
        body_bottom=1320,
        paragraph_gap=34,
        footer_mode="index",
        decoration="cobalt",
    ),
    "ink-noir": Style(
        key="ink-noir",
        label="墨黑清醒",
        width=1080,
        height=1440,
        bg="#151515",
        title_color="#F2E8D7",
        body_color="#E5DFD3",
        muted="#7C7165",
        accent="#B9935B",
        secondary="#8D2F2B",
        title_font_path=SERIF_PATH,
        title_weight=b"Bold",
        title_size=108,
        title_line_gap=24,
        body_font_path=SERIF_PATH,
        body_weight=b"Regular",
        body_size=31,
        body_line_gap=20,
        margin_x=88,
        body_width=858,
        title_y=278,
        cover_body_gap=60,
        page_body_top=100,
        cover_body_bottom=1208,
        body_bottom=1322,
        paragraph_gap=38,
        footer_mode="brand",
        decoration="ink",
    ),
    "photo-veil": Style(
        key="photo-veil",
        label="柔光照片纱幕",
        width=1080,
        height=1440,
        bg="#EEE8DF",
        title_color="#20252A",
        body_color="#33363A",
        muted="#7C7770",
        accent="#B86A4A",
        secondary="#D9C6B6",
        title_font_path=SERIF_PATH,
        title_weight=b"Black",
        title_size=96,
        title_line_gap=24,
        body_font_path=SANS_PATH,
        body_weight=b"Medium",
        body_size=29,
        body_line_gap=18,
        margin_x=72,
        body_width=760,
        title_y=250,
        cover_body_gap=56,
        page_body_top=88,
        cover_body_bottom=1218,
        body_bottom=1330,
        paragraph_gap=34,
        footer_mode="brand",
        decoration="photo",
        panel_rgba=(250, 246, 240, 224),
    ),
}


def load_font(path: str, size: int, weight: bytes) -> ImageFont.FreeTypeFont:
    font = ImageFont.truetype(path, size)
    try:
        font.set_variation_by_name(weight)
    except (OSError, ValueError):
        pass
    return font


def hex_rgba(color: str, alpha: int) -> tuple[int, int, int, int]:
    color = color.lstrip("#")
    return int(color[0:2], 16), int(color[2:4], 16), int(color[4:6], 16), alpha


def add_grain(image: Image.Image, strength: int = 3) -> Image.Image:
    noise = Image.effect_noise(image.size, 18).convert("L")
    layer = Image.new("RGBA", image.size, (110, 90, 80, 0))
    layer.putalpha(noise.point(lambda value: strength if value > 128 else 0))
    return Image.alpha_composite(image.convert("RGBA"), layer)


def add_soft_wash(
    image: Image.Image,
    box: tuple[int, int, int, int],
    color: tuple[int, int, int, int],
    blur: int,
) -> Image.Image:
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    ImageDraw.Draw(layer).ellipse(box, fill=color)
    layer = layer.filter(ImageFilter.GaussianBlur(blur))
    return Image.alpha_composite(image.convert("RGBA"), layer)


def cover_crop(image: Image.Image, size: tuple[int, int]) -> Image.Image:
    target_w, target_h = size
    scale = max(target_w / image.width, target_h / image.height)
    resized = image.resize(
        (math.ceil(image.width * scale), math.ceil(image.height * scale)),
        Image.Resampling.LANCZOS,
    )
    left = (resized.width - target_w) // 2
    top = (resized.height - target_h) // 2
    return resized.crop((left, top, left + target_w, top + target_h))


def organic_blob(
    draw: ImageDraw.ImageDraw,
    cx: float,
    cy: float,
    radius: float,
    color: tuple[int, int, int, int],
    seed: int,
    points: int = 18,
    width: int = 2,
) -> None:
    rng = random.Random(seed)
    phase = rng.uniform(0, math.tau)
    coords: list[tuple[float, float]] = []
    for i in range(points):
        angle = phase + math.tau * i / points
        wobble = 1 + 0.16 * math.sin(angle * 3 + seed) + 0.07 * math.sin(angle * 7 - seed)
        coords.append((cx + math.cos(angle) * radius * wobble, cy + math.sin(angle) * radius * wobble))
    coords.append(coords[0])
    draw.line(coords, fill=color, width=width, joint="curve")


def draw_blush_decoration(image: Image.Image, style: Style) -> Image.Image:
    image = add_soft_wash(image, (670, -280, 1320, 420), (249, 226, 232, 95), 96)
    image = add_soft_wash(image, (-260, 1180, 470, 1900), (250, 232, 237, 80), 120)
    image = add_grain(image, 3)

    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    line = hex_rgba(style.accent, 92)
    faint = hex_rgba(style.accent, 58)

    draw.rectangle((22, 22, style.width - 22, style.height - 22), outline=line, width=2)
    draw.line((22, 300, style.width - 22, 300), fill=faint, width=2)
    draw.line((22, 1690, style.width - 22, 1690), fill=faint, width=2)

    rng = random.Random(31)
    anchors = [
        (95, 110, 90),
        (930, 130, 145),
        (1040, 510, 105),
        (70, 850, 78),
        (960, 1510, 125),
        (190, 1740, 120),
    ]
    for index, (x, y, radius) in enumerate(anchors):
        for ring in range(3):
            organic_blob(
                draw,
                x + rng.uniform(-22, 22),
                y + rng.uniform(-22, 22),
                radius * (0.62 + ring * 0.18),
                faint,
                seed=index * 13 + ring,
                width=2,
            )
        for _ in range(7):
            px = x + rng.uniform(-radius, radius)
            py = y + rng.uniform(-radius, radius)
            draw.ellipse((px - 2, py - 2, px + 2, py + 2), fill=faint)
    image.alpha_composite(layer)
    return image


def draw_nocturne_decoration(image: Image.Image, style: Style) -> Image.Image:
    image = add_grain(image, 4)
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    rng = random.Random(77)

    for _ in range(95):
        x = rng.randint(42, style.width - 42)
        y = rng.randint(36, style.height - 36)
        radius = rng.choice([1, 1, 1, 2])
        alpha = rng.randint(48, 120)
        draw.ellipse(
            (x - radius, y - radius, x + radius, y + radius),
            fill=hex_rgba(style.accent, alpha),
        )

    for box in [
        (-320, -280, 860, 640),
        (640, 840, 1450, 1640),
        (720, -240, 1380, 420),
    ]:
        draw.arc(box, start=18, end=340, fill=hex_rgba(style.accent, 55), width=2)

    draw.line((70, 78, 1010, 78), fill=hex_rgba(style.accent, 55), width=1)
    draw.line((70, 1360, 1010, 1360), fill=hex_rgba(style.accent, 40), width=1)
    image.alpha_composite(layer)
    return image


def draw_sage_decoration(image: Image.Image, style: Style) -> Image.Image:
    image = add_grain(image, 3)
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)
    line = hex_rgba(style.muted, 82)
    faint = hex_rgba(style.muted, 45)

    draw.line((54, 54, style.width - 54, 54), fill=faint, width=1)
    draw.line((54, style.height - 54, style.width - 54, style.height - 54), fill=faint, width=1)

    stems = [
        ((900, 1320), (930, 1130), (912, 900)),
        ((990, 1380), (1010, 1150), (1040, 910)),
        ((105, 960), (86, 760), (112, 560)),
    ]
    for stem in stems:
        draw.line(stem, fill=line, width=2, joint="curve")

    rng = random.Random(9)
    for x, y in [(920, 1110), (934, 1030), (950, 950), (1018, 1130), (1025, 1020), (95, 760), (105, 680)]:
        for side in (-1, 1):
            leaf_w = rng.randint(30, 54)
            leaf_h = rng.randint(16, 28)
            box = (x - leaf_w // 2, y - leaf_h // 2, x + leaf_w // 2, y + leaf_h // 2)
            draw.arc(box, start=205 if side < 0 else -25, end=345 if side < 0 else 115, fill=line, width=2)

    image.alpha_composite(layer)
    return image


def draw_cobalt_decoration(image: Image.Image, style: Style, page_index: int) -> Image.Image:
    image = add_grain(image, 3)
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    grid = hex_rgba(style.secondary, 33)
    for x in range(80, style.width, 80):
        draw.line((x, 0, x, style.height), fill=grid, width=1)
    for y in range(80, style.height, 80):
        draw.line((0, y, style.width, y), fill=grid, width=1)

    number_font = load_font(style.title_font_path, 250, b"Black")
    draw.text(
        (style.width - 40, 110),
        f"{page_index + 1:02d}",
        font=number_font,
        fill=hex_rgba(style.secondary, 22),
        anchor="ra",
    )
    draw.rectangle((44, 44, 54, 116), fill=hex_rgba(style.accent, 230))
    image.alpha_composite(layer)
    return image


def draw_ink_decoration(image: Image.Image, style: Style) -> Image.Image:
    image = add_grain(image, 5)
    layer = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(layer)

    for width, alpha in [(520, 28), (410, 34), (300, 40)]:
        draw.ellipse(
            (
                style.width // 2 - width,
                style.height // 2 - width,
                style.width // 2 + width,
                style.height // 2 + width,
            ),
            outline=hex_rgba(style.accent, alpha),
            width=2,
        )

    draw.line((88, 72, style.width - 88, 72), fill=hex_rgba(style.accent, 110), width=2)
    draw.line((88, style.height - 72, style.width - 88, style.height - 72), fill=hex_rgba(style.accent, 70), width=1)
    image.alpha_composite(layer)
    return image


def draw_photo_decoration(
    image: Image.Image,
    style: Style,
    background: Image.Image | None,
) -> Image.Image:
    if background:
        image = cover_crop(background.convert("RGB"), (style.width, style.height)).convert("RGBA")
        image = image.filter(ImageFilter.GaussianBlur(2))
        veil = Image.new("RGBA", image.size, (25, 21, 18, 68))
        image = Image.alpha_composite(image, veil)
    else:
        image = add_soft_wash(
            image,
            (-200, -200, 1180, 1500),
            (232, 196, 178, 96),
            170,
        )

    panel = Image.new("RGBA", (style.width, style.height), (0, 0, 0, 0))
    ImageDraw.Draw(panel).rounded_rectangle(
        (48, 48, style.width - 48, style.height - 48),
        radius=2,
        fill=style.panel_rgba,
    )
    image = Image.alpha_composite(image, panel)
    image = add_grain(image, 3)
    draw = ImageDraw.Draw(image)
    draw.rectangle(
        (70, 70, style.width - 70, style.height - 70),
        outline=hex_rgba(style.secondary, 105),
        width=1,
    )
    return image


def draw_editorial_background(
    image: Image.Image,
    style: Style,
    background: Image.Image,
    page_index: int,
) -> Image.Image:
    """Use a generated still life as a lower-page visual, not as a text backdrop.

    The top wash is deliberately stronger than the bottom. This preserves the
    upper-left reading zone while letting the subject remain visible in the
    lower-right, which is the composition contract required by the skill.
    """
    width, height = style.width, style.height
    image = cover_crop(background.convert("RGB"), (width, height))
    image = image.filter(ImageFilter.GaussianBlur(1.2)).convert("RGBA")

    wash_color = hex_rgba(style.bg, 255)
    wash = Image.new("RGBA", (width, height), wash_color)

    gradient = Image.new("L", (1, height))
    top_alpha = 220
    bottom_alpha = 64
    for y in range(height):
        t = y / max(1, height - 1)
        eased = t**0.78
        alpha = round(top_alpha + (bottom_alpha - top_alpha) * eased)
        gradient.putpixel((0, y), alpha)
    wash.putalpha(gradient.resize((width, height)))
    image = Image.alpha_composite(image, wash)

    # The generator is allowed creative freedom, but it is not allowed to
    # compete with the reading zone. This feathered panel enforces the
    # upper-left text-safe area after the image has been cropped.
    reading_mask = Image.new("L", (width, height), 0)
    ImageDraw.Draw(reading_mask).rounded_rectangle(
        (-60, -60, int(width * 0.72), int(height * 0.70)),
        radius=90,
        fill=255,
    )
    reading_mask = reading_mask.filter(ImageFilter.GaussianBlur(58))
    reading_panel = Image.new("RGBA", (width, height), hex_rgba(style.bg, 255))
    reading_panel.putalpha(reading_mask.point(lambda value: round(value * 0.44)))
    image = Image.alpha_composite(image, reading_panel)
    image = add_grain(image, 3)

    draw = ImageDraw.Draw(image)
    border = hex_rgba(style.accent, 94)
    faint = hex_rgba(style.accent, 54)
    draw.rectangle((22, 22, width - 22, height - 22), outline=border, width=2)
    draw.line((22, 300, width - 22, 300), fill=faint, width=2)

    # A page-specific accent keeps the still-life set from feeling like a
    # repeated template while the typography and margins stay fixed.
    marker_x = width - 132 + (page_index % 3) * 18
    marker_y = height - 178
    draw.line((marker_x, marker_y, marker_x + 68, marker_y), fill=hex_rgba(style.accent, 170), width=3)
    draw.ellipse(
        (marker_x - 7, marker_y - 7, marker_x + 7, marker_y + 7),
        fill=hex_rgba(style.accent, 215),
    )
    return image


def make_base(
    style: Style,
    page_index: int,
    background: Image.Image | None = None,
) -> Image.Image:
    image = Image.new("RGBA", (style.width, style.height), hex_rgba(style.bg, 255))
    if background is not None:
        if style.decoration == "photo":
            return draw_photo_decoration(image, style, background)
        return draw_editorial_background(image, style, background, page_index)
    if style.decoration == "blush":
        return draw_blush_decoration(image, style)
    if style.decoration == "nocturne":
        return draw_nocturne_decoration(image, style)
    if style.decoration == "sage":
        return draw_sage_decoration(image, style)
    if style.decoration == "cobalt":
        return draw_cobalt_decoration(image, style, page_index)
    if style.decoration == "ink":
        return draw_ink_decoration(image, style)
    if style.decoration == "photo":
        return draw_photo_decoration(image, style, background)
    return add_grain(image, 3)


def wrap_cjk(
    text: str,
    font: ImageFont.FreeTypeFont,
    max_width: int,
    draw: ImageDraw.ImageDraw,
) -> list[str]:
    text = re.sub(r"\s+", " ", text.strip())
    if not text:
        return []

    lines: list[str] = []
    current = ""
    for char in text:
        trial = current + char
        fits = draw.textlength(trial, font=font) <= max_width
        if fits or not current:
            current = trial
            continue

        if char in NO_LINE_START:
            current = trial
            continue
        if current[-1] in NO_LINE_END:
            moved = current[-1]
            lines.append(current[:-1])
            current = moved + char
            continue

        lines.append(current.rstrip())
        current = char

    if current:
        lines.append(current.rstrip())
    return lines


def make_title_font(style: Style, title_lines: list[str], draw: ImageDraw.ImageDraw) -> ImageFont.FreeTypeFont:
    size = style.title_size
    while size > 74:
        font = load_font(style.title_font_path, size, style.title_weight)
        if max((draw.textlength(line, font=font) for line in title_lines), default=0) <= style.body_width:
            return font
        size -= 2
    return load_font(style.title_font_path, size, style.title_weight)


def title_height(font: ImageFont.FreeTypeFont, line_count: int, line_gap: int) -> int:
    return line_count * font.size + max(0, line_count - 1) * line_gap


def draw_title(
    draw: ImageDraw.ImageDraw,
    style: Style,
    title_lines: list[str],
    top: int,
) -> tuple[int, ImageFont.FreeTypeFont]:
    font = make_title_font(style, title_lines, draw)
    current_y = top
    for line in title_lines:
        draw.text(
            (style.margin_x, current_y),
            line,
            font=font,
            fill=style.title_color,
            anchor="la",
        )
        current_y += font.size + style.title_line_gap
    return current_y - style.title_line_gap, font


def draw_body_block(
    draw: ImageDraw.ImageDraw,
    style: Style,
    lines: list[str],
    x: int,
    y: int,
    font: ImageFont.FreeTypeFont,
) -> int:
    current_y = y
    for line in lines:
        draw.text((x, current_y), line, font=font, fill=style.body_color, anchor="la")
        current_y += font.size + style.body_line_gap
    return current_y - style.body_line_gap


def wrap_text_block(
    text: str,
    font: ImageFont.FreeTypeFont,
    max_width: int,
    draw: ImageDraw.ImageDraw,
) -> list[str]:
    """Wrap explicit lines separately so a focus statement can control its pauses."""
    lines: list[str] = []
    for part in str(text).splitlines():
        part = part.strip()
        if part:
            lines.extend(wrap_cjk(part, font, max_width, draw))
    return lines


def prepare_focus(
    style: Style,
    text: str,
    draw: ImageDraw.ImageDraw,
) -> tuple[ImageFont.FreeTypeFont, list[str]]:
    max_width = max(320, style.body_width - 30)
    max_height = max(260, int(style.height * 0.23))
    size = min(style.title_size, max(54, round(style.body_size * 1.9)))
    font = load_font(style.title_font_path, size, style.title_weight)
    lines = wrap_text_block(text, font, max_width, draw)
    line_gap = max(12, round(size * 0.18))

    while size > 46:
        height = len(lines) * font.size + max(0, len(lines) - 1) * line_gap
        if len(lines) <= 4 and height <= max_height:
            break
        size -= 4
        font = load_font(style.title_font_path, size, style.title_weight)
        lines = wrap_text_block(text, font, max_width, draw)
        line_gap = max(12, round(size * 0.18))

    return font, lines


def focus_block_height(
    style: Style,
    text: str,
    draw: ImageDraw.ImageDraw,
) -> int:
    if not text:
        return 0
    font, lines = prepare_focus(style, text, draw)
    line_gap = max(12, round(font.size * 0.18))
    text_height = len(lines) * font.size + max(0, len(lines) - 1) * line_gap
    return FOCUS_LABEL_GAP + text_height + FOCUS_BODY_GAP


def draw_focus(
    draw: ImageDraw.ImageDraw,
    style: Style,
    page_spec: dict[str, Any],
    page_index: int,
    top: int,
) -> int:
    text = str(page_spec.get("focus", "")).strip()
    if not text:
        return top

    font, lines = prepare_focus(style, text, draw)
    line_gap = max(12, round(font.size * 0.18))
    label = str(page_spec.get("kicker", "")).strip() or f"{page_index + 1:02d} / 本页重点"
    label_font = load_font(SANS_PATH, 20, b"Bold")
    draw.text(
        (style.margin_x, top),
        label,
        font=label_font,
        fill=style.accent,
        anchor="la",
    )

    text_top = top + FOCUS_LABEL_GAP
    text_height = len(lines) * font.size + max(0, len(lines) - 1) * line_gap
    draw.rectangle(
        (style.margin_x, text_top + 4, style.margin_x + 5, text_top + text_height + 8),
        fill=hex_rgba(style.accent, 210),
    )

    current_y = text_top
    for line in lines:
        draw.text(
            (style.margin_x + 28, current_y),
            line,
            font=font,
            fill=style.title_color,
            anchor="la",
        )
        current_y += font.size + line_gap

    return current_y - line_gap + FOCUS_BODY_GAP


def prepare_cover_hook(
    style: Style,
    text: str,
    draw: ImageDraw.ImageDraw,
) -> tuple[ImageFont.FreeTypeFont, list[str], int]:
    if not text:
        return load_font(style.body_font_path, style.body_size, style.body_weight), [], 0

    size = min(48, max(34, round(style.body_size * 1.08)))
    font = load_font(style.title_font_path, size, b"Bold")
    lines = wrap_text_block(text, font, style.body_width, draw)
    while len(lines) > 3 and size > 34:
        size -= 2
        font = load_font(style.title_font_path, size, b"Bold")
        lines = wrap_text_block(text, font, style.body_width, draw)
    line_gap = max(10, round(size * 0.24))
    text_height = len(lines) * font.size + max(0, len(lines) - 1) * line_gap
    return font, lines, text_height + style.cover_body_gap


def draw_cover_hook(
    draw: ImageDraw.ImageDraw,
    style: Style,
    text: str,
    top: int,
) -> int:
    if not text:
        return top
    font, lines, block_height = prepare_cover_hook(style, text, draw)
    line_gap = max(10, round(font.size * 0.24))
    current_y = top
    for line in lines:
        draw.text(
            (style.margin_x, current_y),
            line,
            font=font,
            fill=style.body_color,
            anchor="la",
        )
        current_y += font.size + line_gap
    return top + block_height


def draw_eyebrow(
    draw: ImageDraw.ImageDraw,
    style: Style,
    text: str,
    page_index: int,
) -> None:
    if not text:
        return
    font = load_font(SANS_PATH, 20, b"Medium")

    if style.decoration == "blush":
        draw.text((style.margin_x, 82), text, font=font, fill=style.muted, anchor="la")
        draw.line(
            (style.margin_x, 118, style.margin_x + 150, 118),
            fill=hex_rgba(style.accent, 100),
            width=1,
        )
        return

    if style.decoration == "cobalt":
        label = f"{page_index + 1:02d}  {text}"
        draw.text((94, 76), label, font=font, fill=style.secondary, anchor="la")
        draw.line((94, 112, 330, 112), fill=style.accent, width=3)
        return

    if style.decoration == "nocturne":
        label = f"{text}  /  {page_index + 1:02d}"
        draw.text((style.margin_x, 106), label, font=font, fill=style.accent, anchor="la")
        return

    if style.decoration == "ink":
        draw.text((style.margin_x, 104), text.upper(), font=font, fill=style.accent, anchor="la")
        return

    draw.text((style.margin_x, 82), text, font=font, fill=style.muted, anchor="la")


def draw_footer(
    draw: ImageDraw.ImageDraw,
    style: Style,
    brand: str,
    page_index: int,
    total_pages: int,
) -> None:
    font = load_font(SANS_PATH, 17, b"Regular")
    footer_color = hex_rgba(style.muted, 175)

    if style.footer_mode in {"page", "index"}:
        draw.text(
            (style.width - style.margin_x, style.height - 48),
            f"{page_index + 1:02d} / {total_pages:02d}",
            font=font,
            fill=footer_color,
            anchor="ra",
        )
    if style.footer_mode == "brand" and brand:
        draw.text(
            (style.margin_x, style.height - 48),
            brand,
            font=font,
            fill=footer_color,
            anchor="la",
        )


def normalize_content(content: dict[str, Any], style_key: str | None) -> tuple[Style, dict[str, Any]]:
    selected_style = style_key or content.get("style") or "blush-manuscript"
    if selected_style not in STYLES:
        available = ", ".join(STYLES)
        raise ValueError(f"Unknown style '{selected_style}'. Available: {available}")
    style = STYLES[selected_style]

    title_lines = content.get("title_lines") or []
    if isinstance(title_lines, str):
        title_lines = [title_lines]
    title_lines = [str(line).strip() for line in title_lines if str(line).strip()]
    if not title_lines:
        title = str(content.get("title", "")).strip()
        if not title:
            raise ValueError("Provide title_lines or title.")
        title_lines = [title]

    manual_pages_raw = content.get("pages")
    manual_pages: list[dict[str, Any]] | None = None
    if manual_pages_raw:
        if not isinstance(manual_pages_raw, list):
            raise ValueError("pages must be a list when provided.")
        manual_pages = []
        for page_number, page in enumerate(manual_pages_raw, 1):
            if isinstance(page, dict):
                page_spec = dict(page)
                page = page.get("paragraphs", [])
            else:
                page_spec = {}
            if isinstance(page, str):
                page = [page]
            if not isinstance(page, list):
                raise ValueError(f"pages[{page_number}] must contain a paragraph list.")
            clean_page = [str(paragraph).strip() for paragraph in page if str(paragraph).strip()]
            if not clean_page:
                raise ValueError(f"pages[{page_number}] is empty.")
            page_spec["paragraphs"] = clean_page
            page_spec["focus"] = str(page_spec.get("focus", "")).strip()
            page_spec["kicker"] = str(page_spec.get("kicker", "")).strip()
            page_spec["visual_prompt"] = str(page_spec.get("visual_prompt", "")).strip()
            manual_pages.append(page_spec)
        paragraphs = [paragraph for page in manual_pages for paragraph in page["paragraphs"]]
    else:
        paragraphs = content.get("paragraphs")
        if paragraphs is None:
            body = str(content.get("body", "")).strip()
            paragraphs = [part.strip() for part in re.split(r"\n\s*\n", body) if part.strip()]
        if not isinstance(paragraphs, list):
            raise ValueError("paragraphs must be a list of strings.")
        paragraphs = [str(paragraph).strip() for paragraph in paragraphs if str(paragraph).strip()]
    if not paragraphs:
        raise ValueError("At least one body paragraph is required.")

    normalized = dict(content)
    normalized["title_lines"] = title_lines
    normalized["paragraphs"] = paragraphs
    normalized["manual_pages"] = manual_pages
    normalized["cover_hook"] = str(content.get("cover_hook", "")).strip()
    normalized["visual_mode"] = str(content.get("visual_mode", "typographic")).strip()
    normalized["background_safe_zone"] = str(content.get("background_safe_zone", "")).strip()
    normalized.setdefault("eyebrow", "")
    normalized.setdefault("brand", "")
    normalized.setdefault("image_alt", [])
    normalized.setdefault("caption", "")
    normalized.setdefault("hashtags", [])
    normalized.setdefault("post_title", normalized.get("title", "".join(title_lines)))
    normalized.setdefault("strict_pages", False)
    return style, normalized


def paginate(
    style: Style,
    title_lines: list[str],
    paragraphs: list[str],
    manual_pages: list[dict[str, Any]] | None = None,
    cover_hook: str = "",
    strict_manual_pages: bool = False,
) -> tuple[list[list[list[str]]], list[list[str]]]:
    probe = Image.new("RGBA", (style.width, style.height), (0, 0, 0, 0))
    draw = ImageDraw.Draw(probe)
    body_font = load_font(style.body_font_path, style.body_size, style.body_weight)
    title_font = make_title_font(style, title_lines, draw)

    blocks: list[list[str]] = []
    for paragraph in paragraphs:
        lines = wrap_cjk(paragraph, body_font, style.body_width, draw)
        if lines:
            blocks.append(lines)

    cover_body_top = max(style.title_y + title_height(title_font, len(title_lines), style.title_line_gap) + style.cover_body_gap, 0)
    cover_body_top += prepare_cover_hook(style, cover_hook, draw)[2]
    if cover_body_top > style.body_bottom - 120:
        raise ValueError("Title leaves too little cover body space. Shorten title lines or choose another style.")

    line_advance = body_font.size + style.body_line_gap

    if manual_pages:
        rendered_pages: list[list[list[str]]] = []
        overflow_message: str | None = None
        for page_index, page_spec in enumerate(manual_pages):
            page_paragraphs = page_spec["paragraphs"]
            start_y = cover_body_top if page_index == 0 else style.page_body_top
            if page_index > 0:
                start_y += focus_block_height(style, page_spec.get("focus", ""), draw)
            bottom = style.cover_body_bottom if page_index == 0 else style.body_bottom
            page_blocks: list[list[str]] = []
            current_y = start_y
            for block_index, paragraph in enumerate(page_paragraphs):
                block = wrap_cjk(paragraph, body_font, style.body_width, draw)
                if not block:
                    continue
                if block_index:
                    current_y += style.paragraph_gap
                current_y += len(block) * line_advance - style.body_line_gap
                if current_y > bottom:
                    overflow_message = (
                        f"Manual page {page_index + 1} overflows by {current_y - bottom}px. "
                        "Move a paragraph to the next page or shorten it."
                    )
                    if strict_manual_pages:
                        raise ValueError(overflow_message)
                    break
                page_blocks.append(block)
            if overflow_message:
                break
            if not page_blocks:
                raise ValueError(f"Manual page {page_index + 1} has no renderable text.")
            rendered_pages.append(page_blocks)
        if not overflow_message:
            if len(rendered_pages) > 12:
                raise ValueError("Manual page count exceeds 12.")
            return rendered_pages, title_lines
        print(f"WARN: {overflow_message} Falling back to automatic pagination.", file=sys.stderr)

    def block_height(lines: list[str]) -> int:
        return len(lines) * line_advance - style.body_line_gap

    def max_lines(y: int, bottom: int) -> int:
        available = bottom - y + style.body_line_gap
        return max(0, available // line_advance)

    def pack_page(
        queue: list[list[str]],
        start_y: int,
        bottom: int,
        allow_split: bool,
    ) -> tuple[list[list[str]], list[list[str]]]:
        page: list[list[str]] = []
        current_y = start_y
        while queue:
            block = queue[0]
            added_height = block_height(block) if not page else style.paragraph_gap + block_height(block)
            if current_y + added_height <= bottom:
                page.append(block)
                queue.pop(0)
                current_y += added_height
                continue

            if not page and allow_split:
                count = max_lines(current_y, bottom)
                if count > 0:
                    page.append(block[:count])
                    remainder = block[count:]
                    queue.pop(0)
                    if remainder:
                        queue.insert(0, remainder)
                break
            break
        return page, queue

    cover_page, remaining = pack_page(blocks[:], cover_body_top, style.cover_body_bottom, allow_split=True)
    pages: list[list[list[str]]] = [cover_page]
    while remaining:
        page, remaining = pack_page(
            remaining,
            style.page_body_top,
            style.body_bottom,
            allow_split=True,
        )
        if not page:
            raise ValueError("Unable to paginate text; check body font size and page bounds.")
        pages.append(page)
        if len(pages) > 12:
            raise ValueError("Content produced more than 12 pages. Split it into multiple posts.")

    if not pages[0]:
        raise ValueError("The cover has no room for body copy. Shorten the title or reduce title size.")
    return pages, title_lines


def render(
    content: dict[str, Any],
    style_key: str | None,
    output_dir: Path,
    background_path: Path | None = None,
    background_dir: Path | None = None,
    max_pages: int | None = None,
) -> list[Path]:
    style, content = normalize_content(content, style_key)
    pages, title_lines = paginate(
        style,
        content["title_lines"],
        content["paragraphs"],
        content.get("manual_pages"),
        content.get("cover_hook", ""),
        bool(content.get("strict_pages", False)),
    )
    if max_pages is not None:
        pages = pages[:max_pages]

    output_dir.mkdir(parents=True, exist_ok=True)
    if background_dir:
        expected: list[str] = []
        for page_index in range(len(pages)):
            found = next(
                (
                    background_dir / f"{page_index + 1:02d}{suffix}"
                    for suffix in (".png", ".jpg", ".jpeg", ".webp")
                    if (background_dir / f"{page_index + 1:02d}{suffix}").exists()
                ),
                None,
            )
            if found is None:
                expected.append(f"{page_index + 1:02d}.png/.jpg")
        if expected:
            missing = ", ".join(expected)
            raise ValueError(
                "background-dir must contain one text-free image per rendered page. "
                f"Missing: {missing}"
            )

    background = Image.open(background_path).convert("RGB") if background_path else None
    body_font = load_font(style.body_font_path, style.body_size, style.body_weight)
    manual_pages = content.get("manual_pages") or []
    paths: list[Path] = []

    for page_index, page_blocks in enumerate(pages):
        page_spec = manual_pages[page_index] if page_index < len(manual_pages) else {}
        page_background = background
        if background_dir:
            for suffix in (".png", ".jpg", ".jpeg", ".webp"):
                candidate = background_dir / f"{page_index + 1:02d}{suffix}"
                if candidate.exists():
                    page_background = Image.open(candidate).convert("RGB")
                    break
        image = make_base(style, page_index, page_background)
        draw = ImageDraw.Draw(image)

        if page_index == 0:
            draw_eyebrow(draw, style, content.get("eyebrow", ""), page_index)
        body_y = style.page_body_top

        if page_index == 0:
            title_bottom, _ = draw_title(draw, style, title_lines, style.title_y)
            body_y = draw_cover_hook(
                draw,
                style,
                content.get("cover_hook", ""),
                title_bottom + style.cover_body_gap,
            )

            if style.decoration == "cobalt":
                draw.rectangle(
                    (style.margin_x, title_bottom + 22, style.margin_x + 96, title_bottom + 28),
                    fill=style.accent,
                )
            elif style.decoration == "sage":
                draw.line(
                    (style.margin_x, title_bottom + 28, style.margin_x + 150, title_bottom + 28),
                    fill=hex_rgba(style.accent, 120),
                    width=2,
                )
            elif style.decoration == "ink":
                draw.line(
                    (style.margin_x, title_bottom + 26, style.margin_x + 120, title_bottom + 26),
                    fill=hex_rgba(style.accent, 150),
                    width=2,
                )
        elif page_spec.get("focus"):
            body_y = draw_focus(draw, style, page_spec, page_index, style.page_body_top)

        current_y = body_y
        for block_index, lines in enumerate(page_blocks):
            if block_index:
                current_y += style.paragraph_gap
            page_bottom = style.cover_body_bottom if page_index == 0 else style.body_bottom
            if current_y + len(lines) * (body_font.size + style.body_line_gap) - style.body_line_gap > page_bottom:
                raise ValueError(f"Page {page_index + 1} overflowed after pagination.")
            current_y = draw_body_block(
                draw,
                style,
                lines,
                style.margin_x,
                current_y,
                body_font,
            )

        draw_footer(draw, style, content.get("brand", ""), page_index, len(pages))
        path = output_dir / f"{page_index + 1:02d}.png"
        image.convert("RGB").save(path, quality=95)
        paths.append(path)
    return paths


def render_style_preview(content: dict[str, Any], output_path: Path, background: Path | None = None) -> Path:
    sample_pages: list[tuple[str, Image.Image]] = []
    for key, style in STYLES.items():
        style_content = dict(content)
        style_content["style"] = key
        _, normalized = normalize_content(style_content, key)
        pages, title_lines = paginate(
            style,
            normalized["title_lines"],
            normalized["paragraphs"],
            normalized.get("manual_pages"),
            normalized.get("cover_hook", ""),
            bool(normalized.get("strict_pages", False)),
        )
        image = make_base(style, 0, Image.open(background).convert("RGB") if background else None)
        draw = ImageDraw.Draw(image)
        draw_eyebrow(draw, style, normalized.get("eyebrow", ""), 0)
        title_bottom, _ = draw_title(draw, style, title_lines, style.title_y)
        body_font = load_font(style.body_font_path, style.body_size, style.body_weight)
        current_y = draw_cover_hook(
            draw,
            style,
            normalized.get("cover_hook", ""),
            title_bottom + style.cover_body_gap,
        )
        for block_index, block in enumerate(pages[0]):
            if block_index:
                current_y += style.paragraph_gap
            current_y = draw_body_block(
                draw,
                style,
                block,
                style.margin_x,
                current_y,
                body_font,
            )
        draw_footer(draw, style, normalized.get("brand", ""), 0, len(pages))
        sample_pages.append((style.label, image.convert("RGB")))

    cell_w = 410
    cell_h = 620
    columns = 3
    rows = 2
    canvas = Image.new("RGB", (cell_w * columns, cell_h * rows), "#E6E0DC")
    canvas_draw = ImageDraw.Draw(canvas)
    label_font = load_font(SANS_PATH, 24, b"Medium")
    number_font = load_font(SANS_PATH, 17, b"Regular")

    for index, (label, image) in enumerate(sample_pages):
        col = index % columns
        row = index // columns
        cell_x = col * cell_w
        cell_y = row * cell_h
        max_w = cell_w - 64
        max_h = cell_h - 110
        scale = min(max_w / image.width, max_h / image.height)
        thumb = image.resize(
            (math.floor(image.width * scale), math.floor(image.height * scale)),
            Image.Resampling.LANCZOS,
        )
        x = cell_x + (cell_w - thumb.width) // 2
        y = cell_y + 38 + (max_h - thumb.height) // 2
        canvas.paste(thumb, (x, y))
        canvas_draw.rectangle((x, y, x + thumb.width - 1, y + thumb.height - 1), outline="#CFC6C1")
        canvas_draw.text(
            (cell_x + cell_w // 2, cell_y + cell_h - 44),
            label,
            font=label_font,
            fill="#292526",
            anchor="ms",
        )
        canvas_draw.text(
            (cell_x + cell_w // 2, cell_y + cell_h - 17),
            f"{image.width} × {image.height}",
            font=number_font,
            fill="#7A716D",
            anchor="ms",
        )

    output_path.parent.mkdir(parents=True, exist_ok=True)
    canvas.save(output_path, quality=95)
    return output_path


def load_json(path: Path) -> dict[str, Any]:
    with path.open("r", encoding="utf-8") as handle:
        data = json.load(handle)
    if not isinstance(data, dict):
        raise ValueError("Input JSON must be an object.")
    return data


def main() -> None:
    parser = argparse.ArgumentParser(description="Render a Chinese astrology/emotion carousel.")
    parser.add_argument("--input", type=Path, help="Content JSON path.")
    parser.add_argument("--out", type=Path, help="Output directory or gallery image path.")
    parser.add_argument("--style", choices=sorted(STYLES), help="Override the style in the JSON.")
    parser.add_argument("--background", type=Path, help="Optional text-free background image for photo-veil.")
    parser.add_argument(
        "--background-dir",
        type=Path,
        help="Optional directory of text-free page backgrounds named 01.png, 02.png, ...",
    )
    parser.add_argument("--list-styles", action="store_true", help="List built-in styles.")
    parser.add_argument("--gallery", action="store_true", help="Render a six-style cover gallery.")
    parser.add_argument("--max-pages", type=int, help="Limit pages for a quick preview.")
    args = parser.parse_args()

    if args.list_styles:
        for key, style in STYLES.items():
            print(f"{key}\t{style.label}\t{style.width}x{style.height}")
        return

    if not args.input or not args.out:
        raise SystemExit("--input and --out are required unless --list-styles is used.")

    content = load_json(args.input)
    if args.gallery:
        output = args.out
        if output.suffix.lower() != ".png":
            output = output / "style-gallery.png"
        render_style_preview(content, output, args.background)
        print(output)
        return

    paths = render(
        content,
        args.style,
        args.out,
        background_path=args.background,
        background_dir=args.background_dir,
        max_pages=args.max_pages,
    )
    for path in paths:
        print(path)


if __name__ == "__main__":
    main()
