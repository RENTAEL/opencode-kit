---
name: Tarnishsilver-OpenVision
description: "Triggered by `/openvision` or whenever the user asks to analyze a screenshot, generate an image, OCR text, compare designs, or do anything visual."
---
Triggered by `/openvision` or whenever the user asks to analyze a screenshot, generate an image, OCR text, compare designs, or do anything visual.

## Agent-driven flow (MUST follow in order)

### Phase 0: Auto-setup (first run only)

Before anything else, ensure the skill is ready:

1. Check if `SKILL_DIR/node_modules` exists. If not:
   - Tell the user: "Installing dependencies..."
   - Run `npm install --silent` in `SKILL_DIR`
2. Check if `SKILL_DIR/.env` has a valid `NVIDIA_API_KEY` (exists and doesn't contain `nvapi-...` placeholder):
   - If missing or placeholder: **Prompt the user** to get a key and paste it:
     - "Go to https://build.nvidia.com/black-forest-labs/flux-1-dev, sign in, generate an API key, and paste it here:"
     - Use the `question` tool with `custom: true` so they can paste the key
     - Write it to `SKILL_DIR/.env` as `NVIDIA_API_KEY=<their-key>`
   - If valid: silently proceed

### Phase 1: Parse the user's message

The user may have already typed content after `/openvision`. Parse the message to determine mode and extract parameters.

**Detect mode from the message:**

| Clue | Mode | What to extract |
|------|------|----------------|
| No text after command, or vague ("generate", "make") | **Ask mode** | Prompt the user with generate vs describe options |
| Text that describes a scene (no file paths, no keywords like "describe/caption/what's in") | **generate** | The text after the command IS the prompt |
| Keywords like "read text", "OCR", "extract text" followed by a file path | **ocr** | The file path is `image_path`, prompt = "Read all the text in this image. Return only the text content." |
| Keywords like "describe", "caption", "analyze", "what's in", "what is this" followed by a file path or image mention | **describe** | Extract the file path from the message |
| A file path (.png, .jpg, .jpeg) is present | **describe** | The file path is `image_path` |

**Examples of smart parsing:**

| User input | Detected mode | Extracted |
|-----------|---------------|-----------|
| `/openvision a boy throwing rugby` | generate | prompt = "a boy throwing rugby" |
| `/openvision` | ask mode | ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â |
| `/openvision describe ~/photo.png` | describe | image_path = "~/photo.png" |
| `/openvision what's in this /home/user/img.jpg` | describe | image_path = "/home/user/img.jpg" |
| `/openvision generate` | generate | prompt = (ask for it) |
| `/openvision make a cat` | generate | prompt = "make a cat" |

**Optional params in the message:** If the user includes `cfg=`, `steps=`, or `seed=` in their message (e.g. `/openvision a spaceship cfg=8 steps=40 seed=123`), parse those out of the prompt and skip asking for them. Strip them from the prompt text before passing to the script.

### Phase 2a: Generate mode

If the user already provided the prompt, **skip directly to optional parameters**. Skip the mode question entirely.

Collect missing parameters **one at a time** using `question` with `custom: true`. Show description and default.

**Prompt** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â skip if already provided by the user.
**cfg_scale** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â always ask (unless user specified it). Description: "Classifier-free guidance scale. Higher (7-10) = stricter prompt adherence. Lower (3-5) = more creative freedom. Range 1-20."
**steps** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â always ask (unless user specified it). Description: "Denoising steps. More (30-50) = higher quality but slower. Range 1-50."
**seed** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â always ask (unless user specified it). Description: "Random seed for reproducibility. Same seed + same prompt = same image. Leave blank for random."

After collecting, confirm the full payload, then run:

```bash
node SKILL_DIR/generate-image.mjs "<prompt>" <cfg_scale> <steps> <seed> <output.png>
```

Read and display the image.

### Phase 2b: Describe mode

If the user already provided the image path, skip the `image_path` question.

Collect missing parameters **one at a time**:

- **image_path** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â skip if already provided. Ask: "Path to the image file."
- **prompt** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â always ask with default. Description: "What to ask about the image. E.g. 'Describe this image in detail', 'What color is the background?'"

Then run:

```bash
node SKILL_DIR/describe-image.mjs "<image_path>" "<prompt>"
```

Print the description to the user.

### Phase 2c: Ask mode (no clue)

If the user just typed `/openvision` with no usable context, ask:

> What would you like to do?
> 1. Generate an image
> 2. Describe / analyze an image
> 3. Read text from an image (OCR)

Then proceed to the relevant Phase 2 flow.

## Scripts

| Script | Purpose |
|--------|---------|
| `generate-image.mjs` | Generate image from prompt via Flux.1-dev |
| `describe-image.mjs` | Describe / OCR / analyze image via PaliGemma |

## API details

- **Generate**: POST `https://ai.api.nvidia.com/v1/genai/black-forest-labs/flux.1-dev`
- **Vision (describe/OCR/analyze)**: POST `https://ai.api.nvidia.com/v1/vlm/google/paligemma`
- **Auth**: Bearer token via `NVIDIA_API_KEY` env var (loaded from `.env`)

## Sharing

Share the entire `OpenVision/` directory (excluding `node_modules/` and `.env`). The recipient loads it as a skill and types `/openvision` ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â auto-setup handles the rest.
