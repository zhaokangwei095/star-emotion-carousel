from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

from PIL import Image

from render_carousel import STYLES, normalize_content


def emit(level: str, message: str) -> None:
    print(f"[{level}] {message}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate carousel content and rendered images.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--images", type=Path, help="Directory containing rendered PNGs.")
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
    if any(len(line) > 13 for line in title_lines):
        warnings.append("At least one title line exceeds 13 Chinese characters and may crowd the cover.")

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
