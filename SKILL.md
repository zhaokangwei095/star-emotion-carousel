---
name: star-emotion-carousel
description: Convert finished Chinese astrology or relationship copy into publish-ready Xiaohongshu carousels with built-in visual styles, deterministic Chinese typography, automatic pagination, and a publishing package.
license: MIT
metadata:
  slug: star-emotion-carousel
  version: 1.1.0
  displayName: 星座情感图文工坊
  summary: 把已完成的星座或情感正文拆成有主次层级的小红书图文：每页一个重点句、可选无文字背景、代码叠加中文，并生成发布包。
  tags: [astrology, xiaohongshu, carousel, chinese, image-generation, publishing]
  homepage: https://github.com/zhaokangwei095/star-emotion-carousel
---

# Star Emotion Carousel

Turn finished copy into a coherent set of vertical text images. The visual
system, page fitting, hierarchy, and Chinese typography are deterministic; do
not ask an image model to render the Chinese text.

The defining rule is **one page, one idea**. Every content page needs one large
`focus` statement, a short `kicker`, and at most two subordinate paragraphs.
A prompt alone is not a design system: the renderer enforces the hierarchy and
the background image must obey a fixed text-free composition contract.

## What This Skill Produces

- A content plan in JSON.
- Ordered 1080×1800 or 1080×1440 PNG pages.
- Optional per-page, text-free editorial backgrounds.
- A validated publishing package with images, title, caption, hashtags, alt text, and a pre-upload checklist.

## Workflow

Resolve script paths relative to this skill directory. If the working directory is elsewhere, use the absolute path to `scripts/render_carousel.py`.

### 1. Read the copy before changing it

Treat the user's article as the source of truth. Preserve its argument,
relationship boundaries, and wording unless the user asks for a rewrite. You
may:

- choose one existing sentence per page as its focus statement;
- divide paragraphs for page rhythm and move detail to the next page;
- turn the opening claim into a 2–3 line cover title;
- write one cover hook that opens the question;
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
- A full-bleed ambient photo → `photo-veil`; a lighter editorial still-life can
  be layered under any of the other five presets.

Use one style for the entire set. If the user asks for multiple directions, render a gallery first; do not render complete long posts in every style.

### 3. Storyboard the hierarchy before generating any image

Read [references/content-planning.md](references/content-planning.md) for the schema and pagination guidance.

Create a working JSON in the conversation folder. At minimum include:

- `style`
- `post_title`
- `title_lines`
- `cover_hook`
- `visual_mode`
- `pages`
- `caption`
- `hashtags`
- `image_alt`

Use manual `title_lines` when line rhythm matters. Use `pages` for a focus-led
carousel. For every page after the cover, provide:

- `focus`: one statement, preferably 12-32 visible Chinese characters;
- `kicker`: the page's role, not a second headline;
- `visual_prompt`: one text-free image brief when `visual_mode` is
  `editorial-background`;
- `paragraphs`: zero to two short pieces of supporting copy.

Do not create pages by slicing the essay at equal character counts. First
decide the argument each page must make, then choose the sentence that becomes
its visual protagonist.

If `visual_mode` is `editorial-background`, also define
`background_safe_zone`. The default contract is: keep the upper-left 55% quiet
and text-free; place one restrained still-life subject in the lower-right
35-45%.

Keep `strict_pages` false unless the exact page count is a hard requirement.

### 4. Generate the text-free visual layer

When the user wants the richer reference-like treatment, generate one
background per page from its `visual_prompt`. The prompt must specify:

- one subject and its exact placement;
- light direction, texture, palette, and amount of negative space;
- a fixed text-free reading zone;
- no text, letters, numbers, logos, watermarks, interfaces, faces, or
  recognizable private information.

Do not ask the image model to write Chinese, include a title, or design the
layout. AI provides one atmospheric visual subject; the renderer provides the
whole information hierarchy. Save the results as `01.png`, `02.jpg`, and so on
in one directory.

Use this compact brief shape instead of an open-ended style prompt:

```text
[one simple object], placed in the lower-right 35-45%,
on [paper/fabric/stone] in [preset palette],
[direction] soft light and [texture],
keep the upper-left 55% quiet and almost empty,
no text, no letters, no numbers, no logo, no watermark, no face.
```

### 5. Render

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

For one shared image, pass:

```powershell
--background background.png
```

For the required one-image-per-page mode, pass:

```powershell
--background-dir backgrounds
```

The renderer raises an error when a page is missing its background. For every
preset except `photo-veil`, it applies a stronger wash to the upper-left and
keeps the lower-right visual visible. `photo-veil` uses the full-bleed photo
treatment.

Keep all Chinese text in the renderer. Do not bake it into an AI-generated image.

### 6. Inspect the actual output

Open every page at full size and inspect the full set as thumbnails. Check:

- no missing glyphs or wrong characters;
- no line-start punctuation;
- no text crossing decorations or borders;
- no awkward one-character final lines;
- the cover title is readable at phone-feed size;
- every later page has exactly one dominant focus statement;
- the kicker and supporting paragraphs are visibly subordinate to the focus;
- the background subject does not sit under the text or create a second focal
  point;
- the lower-page visual and upper-page text form one balanced composition.

Revise the JSON and rerender the whole set if the typography changes. Do not patch one page with a different font or margin.

Validate:

```powershell
python scripts/validate_carousel.py `
  --input content.json `
  --images rendered `
  --backgrounds backgrounds `
  --strict
```

Strict mode rejects missing focus statements, overlong focus lines, excessive
supporting paragraphs, missing visual briefs, and a background count that does
not match the page count.

### 7. Package for publishing

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

- `scripts/render_carousel.py` — hierarchy, per-page backgrounds, pagination, and PNG rendering.
- `scripts/validate_carousel.py` — focus, hierarchy, visual-brief, background, and image checks.
- `scripts/package_publish.py` — ordered images and publishing copy.
- `references/style-presets.md` — style selection and visual rules.
- `references/content-planning.md` — one-page-one-idea schema, visual contracts, and pagination.
- `references/platform-publishing.md` — package, upload, and assisted-publishing rules.
- `examples/sample_content.json` — runnable example.
