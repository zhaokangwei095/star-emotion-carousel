# Publishing Workflow

## Output Package

After rendering, create a platform-ready package:

```powershell
python scripts/package_publish.py `
  --input content.json `
  --images rendered `
  --out 发布包
```

The package contains:

- ordered PNG images with the cover named first;
- `发布文案.md`;
- `发布检查.md`;
- `manifest.json` for later automation.

## Before Upload

- Inspect the full-size cover and at least one content page.
- Inspect the whole set as thumbnails; the cover title must remain readable.
- Check every page for:
  - wrong characters or missing glyphs;
  - line-start punctuation;
  - text touching a decorative line or border;
  - a paragraph split in a way that changes the meaning;
  - inconsistent margins, colors, or type weights.
- Confirm the caption includes a light entertainment/self-observation boundary.
- Do not state unverified current limits for title length, caption length, hashtags, or image count. Check the live platform UI.

## Manual Publishing

1. Open the platform's creator/publish page.
2. Upload images in filename order.
3. Set the first image as the cover.
4. Paste the title, caption, and hashtags from `发布文案.md`.
5. Check the mobile preview.
6. Stop and ask the user for final confirmation before clicking the final publish button.

## Assisted Publishing

If the user explicitly asks Codex to operate the publishing UI:

- Reuse an already-authenticated browser session only with the user's permission.
- Never request, print, or store cookies, tokens, passwords, or full account data.
- Do not automate login, CAPTCHA, rate-limit bypass, or account recovery.
- Do not select “publish” until the user has seen the final images and copy.
- If the platform changes its UI or blocks automation, stop and hand the package back for manual upload.

## Revisions

If only the copy changes, regenerate the JSON and rerender the whole set. Do not patch individual images with a different font, color, or margin system, because the carousel will visibly drift.
