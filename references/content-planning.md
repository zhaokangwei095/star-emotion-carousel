# Content Planning

## Input Contract

The renderer accepts a UTF-8 JSON object. The minimum useful shape is:

```json
{
  "style": "blush-manuscript",
  "post_title": "用于发布页的短标题",
  "title_lines": [
    "封面第一行",
    "封面第二行",
    "第三行更短"
  ],
  "eyebrow": "星座观察 / 关系边界",
  "brand": "账号名",
  "paragraphs": [
    "第一段正文。",
    "第二段正文。"
  ],
  "caption": "发布页正文。\n\n结尾保留娱乐与自我观察边界。",
  "hashtags": [
    "#星座",
    "#情感"
  ],
  "image_alt": [
    "首图描述",
    "第二页描述"
  ]
}
```

`paragraphs` is preferred over a single `body` string because paragraph boundaries control reading rhythm. If only `body` is supplied, split it on blank lines.

### Manual page breaks

For an essay where whitespace and page endings are part of the composition, provide `pages` instead of `paragraphs`:

```json
{
  "pages": [
    {"paragraphs": ["第 1 页第一段", "第 1 页第二段"]},
    {"paragraphs": ["第 2 页第一段", "第 2 页第二段"]},
    {"paragraphs": ["第 3 页收束段"]}
  ],
  "strict_pages": false
}
```

- `strict_pages: false` keeps the intended breaks when they fit and automatically repaginates if the chosen style is too small.
- `strict_pages: true` fails instead of repaginating. Use it only when an exact three-page ending is a hard requirement.
- The renderer flattens `pages` into `paragraphs` for validation and publishing metadata.

## Preserve Before Rewriting

- Treat the user's finished article as the source of truth.
- Do not silently change the argument, soften a clear boundary, or add astrological claims.
- You may:
  - split paragraphs for page rhythm;
  - shorten a title into 2–4 lines;
  - remove repeated transition phrases;
  - add a short platform caption and hashtags.
- If the draft is too long for one post, say so and propose a series before cutting substantive content.

## Title Construction

The cover title is a reading hook, not a summary.

- Prefer 2–3 lines.
- Each line should usually contain 6–10 Chinese characters.
- The final line should be shorter to create a visual pause.
- Keep the strongest verb or contrast at the beginning of a line.
- Do not put a hashtag, account name, or platform slogan on the cover.
- Do not use unexplained astrological jargon in the title unless the audience already knows it.

Useful title shapes:

```text
不是 A，是 B
你以为是 A，其实是 B
越 A，越 B
真正让人 A 的，不是 B，是 C
```

These are starting points, not a requirement to force every title into the same formula.

## Page Rhythm

The renderer paginates by measured text, not by a fixed character count. To control rhythm:

- Use one paragraph per emotional beat.
- Keep paragraphs roughly 35–100 Chinese characters.
- Put the strongest sentence at the beginning or end of a paragraph, not in the middle of a dense block.
- For `blush-manuscript`, expect a 3-page essay to hold roughly 650–1000 Chinese characters depending on paragraph breaks.
- For the 1080×1440 styles, expect 2–4 pages for a similar length.
- A final page may have generous whitespace; do not force filler copy just to fill the canvas.

## Astrology Boundaries

- Use astrology as a cultural and self-reflection language.
- Qualify claims with `更容易`, `常常`, `在某种关系里`, or `在流行星座叙事里`.
- Avoid `注定`, `一定会`, `所有某星座都`, and claims that a sign determines relationship outcomes.
- Do not present the copy as psychological diagnosis, medical advice, or a prediction.
- Keep a light boundary in the publishing caption, not necessarily on the image itself.

## Caption and Hashtags

The caption should:

1. Restate the emotional hook in 1–2 short paragraphs.
2. Add one useful sentence that is not already verbatim on the images.
3. End with a light self-observation boundary.
4. Use 4–8 specific hashtags; avoid filling the caption with generic tags.

Platform title, caption, and hashtag limits can change. Do not invent a current limit; verify the live publishing page when exact compliance matters.

## Image Alt Text

Write one short alt line per rendered page. It should describe:

- the visual style;
- the page's main idea;
- any important emotional contrast.

Do not repeat the entire page text.
