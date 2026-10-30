# Content Planning

## The Hierarchy Contract

This skill is not a prompt wrapper around an image model. It produces a fixed,
measurable typographic hierarchy first, then optionally places a text-free
visual underneath it.

Every content page must contain:

1. **One `focus` statement** - the single idea the viewer should remember.
2. **A short `kicker`** - the role of the page, not a second headline.
3. **Zero to two short supporting paragraphs** - evidence, explanation, or
   consequence. They must not compete with the focus statement.

The cover is different: it carries `title_lines`, one `cover_hook`, and the
opening paragraphs. Do not add a second focus statement to the cover.

If a page needs two equally large statements, it should be two pages.

## Input Contract

```json
{
  "style": "blush-manuscript",
  "post_title": "用于发布页的短标题",
  "title_lines": ["封面第一行", "封面第二行", "第三行更短"],
  "cover_hook": "一句让人继续翻页的封面钩子。",
  "eyebrow": "星座观察 / 关系边界",
  "brand": "账号名",
  "visual_mode": "editorial-background",
  "background_safe_zone": "Keep the upper-left 55% quiet and text-free; place one subject in the lower-right 35-45%.",
  "pages": [
    {
      "kicker": "01 / 你真正舍不得的是什么",
      "focus": "你不是放不下他，\n是不甘心付出没有回声。",
      "visual_prompt": "One wilted red flower on warm ivory paper, positioned lower right, soft shadow, generous empty upper-left space, no text, no logo.",
      "paragraphs": [
        "第一段短辅证。",
        "第二段短辅证。"
      ]
    }
  ],
  "caption": "发布页正文。\n\n结尾保留娱乐与自我观察边界。",
  "hashtags": ["#星座", "#情感"],
  "image_alt": ["首图描述", "第二页描述"]
}
```

`paragraphs` can still be used for a purely typographic essay. A focus-led
carousel should use `pages`; automatic pagination cannot infer which sentence
deserves to become the visual protagonist.

## Page Storyboard

Plan the carousel as a sequence of arguments, not a stream of paragraphs.

Recommended shapes:

- **Cover**: tension or contradiction in the title; one sentence that opens the
  emotional question.
- **Page 2**: name the hidden cost, false belief, or real source of pain.
- **Page 3**: explain the mechanism that keeps the reader stuck.
- **Page 4**: turn toward a boundary, choice, or new interpretation.
- **Optional final page**: close with one restrained line of agency. Do not add
  an empty affirmation just to fill a page.

Use 3-6 pages for most posts. Twelve is a technical maximum, not a target.

## Focus Statement Rules

The focus statement is the page's visual protagonist.

- Aim for 12-32 visible Chinese characters; hard ceiling is 36.
- Prefer 1-3 explicit lines. Use `\n` only where the pause is intentional.
- Put the contrast, verb, or turn early.
- Write a claim, not a category label.
- Keep it distinct from the `kicker`; the kicker names the lens, the focus makes
  the claim.
- Do not repeat the cover title on a later page.

Useful shapes:

```text
不是 A，是 B
你以为是 A，其实是 B
越 A，越 B
A 最危险的，不是 B，而是 C
```

These are prompts for thinking, not templates to force onto every page.

## Supporting Copy Rules

- At most two paragraphs per page.
- Prefer 35-90 visible characters per paragraph.
- A paragraph must support the focus through explanation, example, mechanism,
  or consequence. If it introduces a new main idea, move it to another page.
- Do not stack several equal-weight insights and call the page "rich".
- White space is a hierarchy tool. Do not fill it with generic reassurance.

## Visual Background Contract

Set `visual_mode` to:

- `typographic` when typography and built-in decoration are enough.
- `editorial-background` when each page receives a generated or selected
  text-free still life.

For `editorial-background`:

1. Write one `visual_prompt` per page, including the cover.
2. State the exact subject, placement, light, texture, palette, and amount of
   negative space.
3. Reserve a fixed `background_safe_zone` for Chinese text. The default is the
   upper-left 55%, with the subject in the lower-right 35-45%.
4. Require no text, letters, numbers, logos, watermarks, interfaces, faces, or
   recognizable private information.
5. Generate one distinct image per page. Do not reuse one image across a set.
6. Save images as `01.png`, `02.jpg`, and so on in one directory; pass that
   directory with `--background-dir`.

The image model creates atmosphere and a subject. Pillow creates every Chinese
character. Never let the model render the title or body copy.

## Title Construction

- Prefer 2-3 cover lines, usually 4-8 Chinese characters each.
- The final line should be shorter to create a visual pause.
- Keep the strongest verb or contrast at the start of a line.
- No hashtags, account names, or platform slogans inside the title.
- The `cover_hook` should be one sentence under 42 visible characters.

## Pagination

The renderer measures actual font width and subtracts the cover hook and focus
block before fitting body copy.

- Use `strict_pages: true` only when an exact page count is mandatory.
- With `strict_pages: false`, overflow falls back to automatic pagination.
- Automatic pagination does not create focus statements. Use it only for a
  deliberately typographic essay.

## Preserve Before Rewriting

- Treat the user's finished article as the source of truth.
- Preserve its argument, relationship boundaries, and wording unless asked to
  rewrite.
- You may split paragraphs, isolate one existing sentence as the focus, build a
  cover title, and write publishing metadata.
- Do not silently soften a clear boundary or add astrological claims.
- If the draft is too long for one post, propose a series before cutting
  substantive content.

## Astrology Boundaries

- Use astrology as culture, entertainment, and self-observation.
- Qualify claims with `更容易`, `常常`, `在某种关系里`, or similar wording.
- Avoid `注定`, `一定会`, `所有某星座都`, and claims that a sign determines
  relationship outcomes.
- Do not present the copy as diagnosis, medical advice, or prediction.

## Caption, Hashtags, and Alt Text

The caption should restate the hook in 1-2 short paragraphs, add one useful
sentence not already on the images, and end with a light self-observation
boundary. Use 4-8 specific hashtags.

Write one alt line per page describing the visual style, the focus idea, and
the emotional contrast. Do not paste the whole page text.
