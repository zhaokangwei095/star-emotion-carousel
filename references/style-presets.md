# Built-in Style Presets

The presets are layout systems, not image-generation prompts. Every preset
keeps one `focus` statement as the page protagonist, a smaller `kicker`, and a
lower-weight body layer. A text-free background can be added to any preset; the
renderer applies a stronger wash to the upper-left reading zone and preserves
the lower-right for one restrained visual subject.

All presets are implemented in `scripts/render_carousel.py` and can be listed with:

```powershell
python scripts/render_carousel.py --list-styles
```

Render a six-style cover gallery with:

```powershell
python scripts/render_carousel.py --input examples/sample_content.json --out style-gallery.png --gallery
```

## Selection Guide

| Style key | Best for | Visual identity | Avoid when |
|---|---|---|---|
| `blush-manuscript` | Long emotional essays, relationship复盘, a reference like 白桃星座 | Warm ivory paper, crimson Song type, map-like pink linework, 1080×1800 | The topic needs diagrams, rankings, or a highly rational tone |
| `nocturne` | Astrology-specific insight, attachment patterns, "night thought" content | Navy paper, ivory body, brass orbital lines, 1080×1440 | The copy is very long or the user wants a bright feminine look |
| `sage-letter` | Healing, self-growth, boundaries, gentle advice | Cream and sage, moss-green type, botanical linework, 1080×1440 | The topic is sharp, confrontational, or ranking-driven |
| `cobalt-grid` | Rankings, lists, opinion posts, "X signs do Y" | Off-white grid, black and cobalt sans, vermilion accents, 1080×1440 | The copy is lyrical, intimate, or full of long paragraphs |
| `ink-noir` | Clear-eyed boundaries, mature relationship analysis, strong statements | Charcoal, bone, muted brass, dramatic serif, 1080×1440 | The topic needs softness, warmth, or a very light visual mood |
| `photo-veil` | A supplied ambient photo or a generated text-free background | Photo with an ivory translucent text veil, 1080×1440 | No usable background image is available |

`photo-veil` is a full-photo treatment. For the other five styles,
`editorial-background` keeps the preset's typography and paper identity while
placing a quiet still-life subject beneath the text. Pass one background per
page with `--background-dir`.

## Mixing Rules

- Choose one style for the entire post. Do not switch palettes or fonts between pages.
- Keep the title font, body font, margins, and page-number behavior fixed across the set.
- Keep the focus size, focus rule, kicker position, and body hierarchy fixed across the set.
- Vary decoration placement only when it prevents collision with text.
- If a post contains both a ranking and an emotional essay, choose the dominant reading mode. Use `cobalt-grid` for ranking-led posts and `ink-noir` for analysis-led posts.

## Style-Specific Notes

### `blush-manuscript`

- Default when the user's reference is a 1080×1800 text essay with a large crimson title.
- Page 1 carries the title, one cover hook, and the opening body. Later pages each carry one focus statement, one kicker, and at most two supporting paragraphs.
- Use 3 title lines when possible, with the last line noticeably shorter.
- Keep the pale map/contour linework behind the text at roughly 5–10% visibility.
- In `editorial-background` mode, use warm ivory still lifes with one crimson,
  blush, or paper object in the lower-right. Keep the upper-left 55% empty.

### `nocturne`

- Use for astrology as a language of observation, not fortune-telling.
- Keep the cover title in ivory and reserve brass for small labels and lines.
- Body copy should be shorter than `blush-manuscript`; page capacity is lower.

### `sage-letter`

- Keep botanical decoration at the edges.
- Use first-person-plural or second-person language sparingly; the visual already feels intimate.
- Good for "you are allowed to..." endings without turning them into empty affirmations.
- With a background, prefer pressed flowers, seed pods, folded paper, or one
  leaf rather than a full bouquet.

### `cobalt-grid`

- Use Noto Sans Black for the title and a visible grid.
- Good for numbered lists, categories, and comparisons.
- Avoid long poetic paragraphs; the focus statement should be a direct claim,
  and each supporting paragraph should advance only one step.

### `ink-noir`

- Use for the emotional "sober conclusion", not for crisis content.
- Keep the gold line thin and the vignette subtle.
- Avoid horror, occult, or overly cinematic styling.
- With a background, use one dark, tactile object with low detail; never let the
  subject become a second headline competing with the focus statement.

### `photo-veil`

- Generate or select a background with no text, logos, faces, or recognizable private information.
- Use an ambient scene that matches the article's emotional temperature.
- Add Chinese text with the renderer, not with the image model.
- Because the photo is full-bleed, verify contrast and legibility after the
  veil is applied; do not rely on the source image's brightness.

## Extending a Style

If the user asks for a new visual direction:

1. Add a `Style` entry in `scripts/render_carousel.py`.
2. Reuse the existing pagination and validation pipeline.
3. Keep the title/body hierarchy and safe margins non-negotiable.
4. Add one new decoration family; do not combine several existing families into a busy collage.
5. Render a validation sample before presenting it as a built-in style.
6. Prove that a typical page has one dominant focus statement at phone-feed
   size and that supporting text remains visibly subordinate.
