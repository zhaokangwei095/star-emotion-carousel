---
name: star-emotion-carousel
description: Convert finished Chinese astrology or relationship copy into publish-ready Xiaohongshu carousels with built-in visual styles, deterministic Chinese typography, automatic pagination, and a publishing package.
license: MIT
metadata:
  slug: star-emotion-carousel
  version: 1.0.0
  displayName: 星座情感图文工坊
  summary: 把已经完成的星座或情感正文拆成可发布的小红书图文，内置六种视觉风格、自动分页、中文排版与发布包生成。
  tags: [astrology, xiaohongshu, carousel, chinese, image-generation, publishing]
  homepage: https://github.com/zhaokangwei095/star-emotion-carousel
---

# Star Emotion Carousel

Turn finished copy into a coherent set of vertical text images. The visual system, page fitting, and Chinese typography are deterministic; do not ask an image model to render the Chinese text.

## What This Skill Produces

- A content plan in JSON.
- Ordered 1080×1800 or 1080×1440 PNG pages.
- A validated publishing package with images, title, caption, hashtags, alt text, and a pre-upload checklist.

## Workflow

Resolve script paths relative to this skill directory. If the working directory is elsewhere, use the absolute path to `scripts/render_carousel.py`.

### 1. Read the copy before changing it

Treat the user's article as the source of truth. Preserve its argument, relationship boundaries, and wording unless the user asks for a rewrite. You may only:

- divide paragraphs for page rhythm;
- turn the opening claim into a 2–3 line cover title;
- add a platform caption, hashtags, and alt text.

If the copy is too long for one post, say so and propose a series before cutting substantive content.

### 2. Choose one style

Read [references/style-presets.md](references/style-presets.md) when the user wants options or when choosing a style is not obvious.

Default decisions:

- A 1080×1800 text essay like the supplied 白桃星座 reference → `blush-manuscript`.
- Relationship analysis with an astrology angle → `nocturne`.
- Healing and self-growth → `sage-letter`.
- Rankings or listicles → `cobalt-grid`.
- Sharp, mature boundaries → `ink-noir`.
- A supplied ambient photo or generated text-free background → `photo-veil`.

Use one style for the entire set. If the user asks for multiple directions, render a gallery first; do not render complete long posts in every style.

### 3. Build the content JSON

Read [references/content-planning.md](references/content-planning.md) for the schema and pagination guidance.

Create a working JSON in the conversation folder. At minimum include:

- `style`
- `post_title`
- `title_lines`
- `paragraphs`
- `caption`
- `hashtags`
- `image_alt`

Use manual `title_lines` when line rhythm matters. The renderer measures actual font width and automatically paginates the body.

When page endings and whitespace matter, use the `pages` array for intentional breaks. Keep `strict_pages` false unless the exact page count is a hard requirement.

### 4. Render

List presets:

```powershell
python scripts/render_carousel.py --list-styles
```

Render the chosen style:

```powershell
python scripts/render_carousel.py `
  --input content.json `
  --out rendered
```

Render a quick style gallery:

```powershell
python scripts/render_carousel.py `
  --input content.json `
  --out style-gallery.png `
  --gallery
```

For `photo-veil`, first generate or select a text-free background, then pass:

```powershell
--background background.png
```

Keep all Chinese text in the renderer. Do not bake it into an AI-generated image.

### 5. Inspect the actual output

Open every page at full size and inspect the full set as thumbnails. Check:

- no missing glyphs or wrong characters;
- no line-start punctuation;
- no text crossing decorations or borders;
- no awkward one-character final lines;
- the cover title is readable at phone-feed size;
- later pages continue the essay rather than repeating the cover hierarchy.

Revise the JSON and rerender the whole set if the typography changes. Do not patch one page with a different font or margin.

Validate:

```powershell
python scripts/validate_carousel.py `
  --input content.json `
  --images rendered
```

### 6. Package for publishing

```powershell
python scripts/package_publish.py `
  --input content.json `
  --images rendered `
  --out 发布包
```

Read [references/platform-publishing.md](references/platform-publishing.md) before operating a live publishing page.

If the user only asks for creation, stop after presenting the images and publishing copy. If the user explicitly asks Codex to upload or publish, reuse an authenticated browser session with permission, fill the draft, and stop for final confirmation before the final publish action.

## Content Boundaries

- Frame astrology as culture, entertainment, and self-observation, not diagnosis or fate.
- Prefer `更容易`, `常常`, `在某种关系里` over absolute claims.
- Do not invent studies, statistics, experts, platform limits, or account policies.
- Do not use real private conversations, names, faces, or account data in images.

## Supporting Files

- `scripts/render_carousel.py` — style presets, pagination, and PNG rendering.
- `scripts/validate_carousel.py` — content and image checks.
- `scripts/package_publish.py` — ordered images and publishing copy.
- `references/style-presets.md` — style selection and visual rules.
- `references/content-planning.md` — JSON schema, title rhythm, and pagination.
- `references/platform-publishing.md` — package, upload, and assisted-publishing rules.
- `examples/sample_content.json` — runnable example.
