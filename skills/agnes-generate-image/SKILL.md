---
name: agnes-generate-image
description: "Generate or edit images with `agnes-image-2.1-flash`."
---
# Agnes Generate Image

Generate or edit images with `agnes-image-2.1-flash`.

## When to use

- The user asks for an image, icon, banner, mockup, product photo, or edited image.
- The user provides a reference image and wants a variation or edit.

## Inputs

- `--prompt`: Text description of the desired image.
- `--size`: Output size, e.g. `1024x768`, `1024x1024`, `768x1024`. Default `1024x768`.
- `--image`: Optional reference image (local path or URL) for image-to-image.
- `--response-format`: `base64` (default) or `url`. Base64 mode saves images locally.
- `--n`: Number of images. Default 1.
- `--output-dir`: Directory for saved images. Default is `~/AgnesAI/images`.
- `--no-open`: Do not open the output folder after saving.
- `--model`: Optional model override. Default is `agnes-image-2.1-flash`.

## Prompt Enhancement (before running the script)

Consult the `prompt-components` skill to assemble a high-quality prompt:

1. Determine interaction mode:
   - User gave subject + style + mood ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ **Mode 1** (assemble directly, no questions)
   - User gave subject but missing style/mood ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ **Mode 2** (suggest 2ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ3 combinations)
   - User is vague ("draw something") ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ **Mode 3** (ask up to 4 questions)
2. Read `prompt-components/references/positive.md` for styles, quality boosters, lighting, and composition vocabulary.
3. Read `prompt-components/references/negative.md` and auto-append relevant negatives (universal + subject-category + style-conflict).
4. Translate non-English user input to English for the final prompt.
5. Keep positive prompt ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â°Ãƒâ€šÃ‚Â¤ 80 words, negative ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â°Ãƒâ€šÃ‚Â¤ 30 words.

## Steps

1. Enhance the prompt using the rules above (do not skip this).
2. Run the helper script in this skill directory:
   ```bash
   bash scripts/generate_image.sh --prompt "a cat in space" --size 1024x1024
   ```
3. Return to the user: **both** the saved file path(s) **and** the API image URL(s). If the script output contains a URL, always show it. If only a file path is available, state that clearly.

## Example

```bash
bash scripts/generate_image.sh \
  --prompt "A minimalist logo of a rocket, vector style, blue gradient" \
  --size 1024x1024 \
  --response-format url
```

## Output location

By default (`--response-format base64`) the generated image is saved to `--output-dir` and the folder is opened automatically.

- Default: `~/AgnesAI/images` on macOS/Linux, or `%USERPROFILE%\AgnesAI\images` when running under Git Bash on Windows.
- Custom: `bash scripts/generate_image.sh --output-dir ./my_images ...`
- Skip opening the folder: add `--no-open`.
- URL-only mode: `--response-format url` returns a public URL without saving locally.

## Templates / references

- `references/templates.md` ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â prompt templates for creative design, marketing, social media, product shots, style transfer, thumbnails/banners, etc.

## API reference

- Model: `agnes-image-2.1-flash`
- Docs: https://agnes-ai.com/zh-Hans/docs/agnes-image-21-flash

## Setup

Set `AGNES_API_KEY` as an environment variable or in a `.env` file.
