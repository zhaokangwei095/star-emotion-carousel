from __future__ import annotations

import argparse
import json
import shutil
from pathlib import Path

from PIL import Image

from render_carousel import STYLES, normalize_content


def safe_slug(value: str, fallback: str = "carousel") -> str:
    cleaned = "".join(char if char.isalnum() or char in "-_" else "_" for char in value.strip())
    cleaned = cleaned.strip("_")
    return cleaned[:48] or fallback


def main() -> None:
    parser = argparse.ArgumentParser(description="Create a Xiaohongshu-ready publishing package.")
    parser.add_argument("--input", required=True, type=Path)
    parser.add_argument("--images", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    args = parser.parse_args()

    with args.input.open("r", encoding="utf-8") as handle:
        raw_content = json.load(handle)

    style, content = normalize_content(raw_content, raw_content.get("style"))
    image_paths = sorted(args.images.glob("*.png"))
    if not image_paths:
        raise SystemExit(f"No PNG images found in {args.images}")

    args.out.mkdir(parents=True, exist_ok=True)
    copied: list[str] = []
    for index, source in enumerate(image_paths, 1):
        suffix = "封面" if index == 1 else f"第{index:02d}页"
        target = args.out / f"{index:02d}_{suffix}.png"
        shutil.copy2(source, target)
        copied.append(target.name)

    alt_text = content.get("image_alt", [])
    title = str(content.get("post_title") or "".join(content["title_lines"])).strip()
    caption = str(content.get("caption", "")).strip()
    hashtags = [str(tag).strip() for tag in content.get("hashtags", []) if str(tag).strip()]
    hashtag_line = " ".join(hashtags)

    image_rows = []
    for index, name in enumerate(copied):
        alt = alt_text[index] if index < len(alt_text) else ""
        image_rows.append(f"{index + 1}. `{name}`" + (f"：{alt}" if alt else ""))

    publish_copy = f"""# 发布文案

## 标题

{title}

## 正文

{caption}

{hashtag_line}

## 图片顺序

{chr(10).join(image_rows)}

## 发布时检查

- 先确认首图标题在手机缩略图中完整可读。
- 逐张检查没有错字、孤字、标点出现在行首、段落被异常截断。
- 发布前重新核对星座表述是否使用“更容易、常常、在某种关系里”等限定语。
- 平台的字数、标签数量和图片数量限制可能调整，发布前以当前页面提示为准。
"""
    (args.out / "发布文案.md").write_text(publish_copy, encoding="utf-8")

    manifest = {
        "style": style.key,
        "style_label": style.label,
        "title": title,
        "caption": caption,
        "hashtags": hashtags,
        "images": copied,
        "image_alt": alt_text[: len(copied)],
        "source_content": str(args.input.resolve()),
    }
    (args.out / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    with Image.open(args.out / copied[0]) as cover:
        size_line = f"{cover.width} × {cover.height}"

    checklist = f"""# 发布检查

- 风格：{style.label}（`{style.key}`）
- 图片数量：{len(copied)}
- 单图尺寸：{size_line}
- 首图：`{copied[0]}`
- 文案：`发布文案.md`
- 顺序清单：`manifest.json`

## 必查

- [ ] 首图只承担一个情绪钩子，没有把全文塞进封面。
- [ ] 所有页面字号、边距、颜色和装饰保持一致。
- [ ] 没有错字、乱码、伪文字、意外裁切或文字压到装饰线。
- [ ] 星座内容保留娱乐与自我观察边界，不写成诊断或命运承诺。
- [ ] 正文、标题和标签在当前平台发布页再核对一次限制。
- [ ] 用户明确要求代发时，才进入浏览器上传流程；最终“发布”按钮前必须停下确认。
"""
    (args.out / "发布检查.md").write_text(checklist, encoding="utf-8")

    slug = safe_slug(title)
    print(args.out.resolve())
    print(f"slug={slug}")
    print(f"images={len(copied)} size={size_line} style={style.key}")


if __name__ == "__main__":
    main()
