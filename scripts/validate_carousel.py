from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from PIL import Image

from render_carousel import STYLES, normalize_content


def emit(level: str, message: str) -> None:
    print(f"[{level}] {message}")


def visible_length(text: str) -> int:
    return len(re.sub(r"\s+", "", text))


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate carousel content and rendered images.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--images", type=Path, help="Directory containing rendered PNGs.")
    parser.add_argument("--backgrounds", type=Path, help="Directory containing one text-free background per page.")
    parser.add_argument("--strict", action="store_true", help="Exit non-zero on warnings.")
    args = parser.parse_args()

    with args.input.open("r", encoding="utf-8") as handle:
        content = json.load(handle)

    style, content = normalize_content(content, content.get("style"))
    errors: list[str] = []
    warnings: list[str] = []

    title_lines = content["title_lines"]
    if len(title_lines) > 4:
        warnings.append("Title uses more than 4 lines; check first-frame readability.")
    if any(visible_length(line) > 10 for line in title_lines):
        warnings.append("At least one title line exceeds 10 visible characters and may crowd the cover.")

    cover_hook = str(content.get("cover_hook", "")).strip()
    if not cover_hook:
        warnings.append("cover_hook is missing; the cover has no bridge between the title and body copy.")
    elif visible_length(cover_hook) > 42:
        warnings.append("cover_hook exceeds 42 visible characters; keep the first-frame hook to one breath.")

    manual_pages = content.get("manual_pages") or []
    if not manual_pages:
        warnings.append(
            "No manual pages are defined. A focus-led carousel needs pages[].focus to make each page's main idea explicit."
        )
    else:
        if len(manual_pages) < 2:
            warnings.append("Only one manual page is defined; the carousel has no page-level progression.")
        for page_number, page in enumerate(manual_pages, 1):
            focus = str(page.get("focus", "")).strip()
            paragraphs = page.get("paragraphs", [])
            if page_number > 1 and not focus:
                warnings.append(
                    f"Page {page_number} has no focus statement; one page should carry exactly one dominant idea."
                )
            if focus:
                focus_length = visible_length(focus)
                if focus_length > 36:
                    warnings.append(
                        f"Page {page_number} focus has {focus_length} visible characters; "
                        "aim for 12-32 and keep it to at most 36."
                    )
                if focus_length < 8:
                    warnings.append(
                        f"Page {page_number} focus is only {focus_length} visible characters; "
                        "it may read as a label rather than the page's main claim."
                    )
            if page_number > 1 and not str(page.get("kicker", "")).strip():
                warnings.append(
                    f"Page {page_number} has no kicker; add a short role label above the focus statement."
                )
            if len(paragraphs) > 2:
                warnings.append(
                    f"Page {page_number} has {len(paragraphs)} supporting paragraphs; "
                    "use at most two so the focus remains dominant."
                )
            if any(visible_length(paragraph) > 120 for paragraph in paragraphs):
                warnings.append(
                    f"Page {page_number} has a supporting paragraph over 120 visible characters; "
                    "move detail to the next page."
                )

    visual_mode = str(content.get("visual_mode", "typographic")).strip()
    if visual_mode not in {"typographic", "editorial-background"}:
        warnings.append(
            "visual_mode must be 'typographic' or 'editorial-background'."
        )
    if visual_mode == "editorial-background":
        if not content.get("background_safe_zone"):
            warnings.append(
                "background_safe_zone is missing; define the fixed text-free area the image model must preserve."
            )
        if not manual_pages:
            warnings.append(
                "editorial-background mode needs one visual_prompt per manual page."
            )
        for page_number, page in enumerate(manual_pages, 1):
            visual_prompt = str(page.get("visual_prompt", "")).strip()
            if not visual_prompt:
                warnings.append(
                    f"Page {page_number} has no visual_prompt; generated-background mode needs one image brief per page."
                )
                continue
            if visible_length(visual_prompt) < 28:
                warnings.append(
                    f"Page {page_number} visual_prompt is too thin; specify subject, placement, light, texture, and negative space."
                )
            lowered = visual_prompt.lower()
            no_text_terms = ("no text", "without text", "text-free", "无文字", "不要文字", "不出现文字")
            if not any(term in lowered for term in no_text_terms):
                warnings.append(
                    f"Page {page_number} visual_prompt should explicitly require a text-free image."
                )

    joined_body = "\n".join(content["paragraphs"])
    if len(joined_body) < 180:
        warnings.append("Body copy is under 180 Chinese characters; the result may feel like a quote card.")
    if len(joined_body) > 1800:
        warnings.append("Body copy exceeds 1800 Chinese characters; consider splitting it into multiple posts.")

    risky_patterns = {
        r"所有.{0,5}座": "absolute claim about all signs",
        r"注定": "fatalistic wording",
        r"一定会": "absolute prediction",
        r"绝对": "absolute claim",
        r"永远": "absolute claim",
    }
    for pattern, reason in risky_patterns.items():
        if re.search(pattern, joined_body):
            warnings.append(f"Found {reason}: /{pattern}/. Use qualified phrasing.")

    post_title = str(content.get("post_title", "")).strip()
    caption = str(content.get("caption", "")).strip()
    hashtags = content.get("hashtags", [])

    if not post_title:
        warnings.append("post_title is empty.")
    elif len(post_title) > 24:
        warnings.append("post_title is longer than 24 Chinese characters; verify the current platform title limit.")

    if not caption:
        warnings.append("caption is empty.")
    elif len(caption) > 1000:
        warnings.append("caption exceeds 1000 characters; verify the current platform limit.")
    if "仅供" not in caption and "自我观察" not in caption:
        warnings.append("Caption does not include a light entertainment/self-observation boundary.")

    if len(hashtags) > 10:
        warnings.append("More than 10 hashtags; keep the caption clean and verify current platform limits.")

    if style.decoration == "photo":
        if not content.get("background_image_hint") and not content.get("background_image"):
            warnings.append("photo-veil works best with a generated text-free background; none is declared.")

    if args.images:
        images = sorted(args.images.glob("*.png"))
        if not images:
            errors.append(f"No PNG images found in {args.images}")
        if len(images) > 12:
            warnings.append(f"{len(images)} images rendered; verify the current platform carousel limit.")

        allowed_sizes = {(1080, 1440), (1080, 1800)}
        for image_path in images:
            try:
                with Image.open(image_path) as image:
                    if image.size not in allowed_sizes:
                        warnings.append(f"{image_path.name} is {image.width}x{image.height}, not 1080x1440 or 1080x1800.")
                    if image.mode not in {"RGB", "RGBA"}:
                        warnings.append(f"{image_path.name} uses mode {image.mode}; convert to RGB before upload.")
            except OSError as exc:
                errors.append(f"Cannot open {image_path.name}: {exc}")

        numbers = [int(path.stem) for path in images if path.stem.isdigit()]
        if numbers and numbers != list(range(1, len(images) + 1)):
            warnings.append("Image filenames are not continuous from 01.png.")

        if args.backgrounds:
            backgrounds = sorted(
                path
                for path in args.backgrounds.iterdir()
                if path.is_file() and path.suffix.lower() in {".png", ".jpg", ".jpeg", ".webp"}
            ) if args.backgrounds.exists() else []
            if len(backgrounds) != len(images):
                warnings.append(
                    f"Found {len(backgrounds)} background images for {len(images)} rendered pages; "
                    "the visual layer should be unique on every page."
                )

    for warning in warnings:
        emit("WARN", warning)
    for error in errors:
        emit("ERROR", error)

    if not errors:
        emit("OK", f"Style={style.key}; title_lines={len(title_lines)}; paragraphs={len(content['paragraphs'])}")
    if errors or (args.strict and warnings):
        raise SystemExit(1)


if __name__ == "__main__":
    main()
