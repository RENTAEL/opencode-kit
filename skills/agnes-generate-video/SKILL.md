---
name: agnes-generate-video
description: "Generate videos with `agnes-video-v2.0`. Video generation is asynchronous; the script creates a task and polls until completion."
---
# Agnes Generate Video

Generate videos with `agnes-video-v2.0`. Video generation is asynchronous; the script creates a task and polls until completion.

## When to use

- The user asks for a short video, animation, or cinematic clip.
- The user provides a starting image and wants it animated.

## Inputs

- `--prompt`: Text description of the desired video.
- `--image`: Optional starting image (local path or URL) for image-to-video.
- `--width`, `--height`: Output resolution. Default `1152x768`.
- `--duration`: Target duration in seconds. Default ~5 seconds.
- `--frame-rate`: FPS. Default 24.
- `--num-frames`: Override duration; must follow `8n + 1` rule and be ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â°Ãƒâ€šÃ‚Â¤ 441.
- `--poll-interval`: Seconds between status checks. Default 10.
- `--max-wait`: Max seconds to wait. Default 1800.
- `--download`: Optional local path or directory to save the MP4. Default is `~/AgnesAI/videos/agnes_video_<timestamp>.mp4`.
- `--no-open`: Do not open the output folder after saving.

## Prompt Enhancement (before running the script)

Consult the `prompt-components` skill to assemble a high-quality prompt:

1. Determine interaction mode:
   - User gave subject + style + mood ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ **Mode 1** (assemble directly, no questions)
   - User gave subject but missing style/mood ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ **Mode 2** (suggest 2ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œ3 combinations)
   - User is vague ("make a video") ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â ÃƒÂ¢Ã¢â€šÂ¬Ã¢â€žÂ¢ **Mode 3** (ask up to 4 questions)
2. Read `prompt-components/references/positive.md` for styles and quality vocabulary.
3. Read `prompt-components/references/negative.md` and auto-append relevant negatives (universal + video-specific + subject-category + style-conflict).
4. Read `prompt-components/references/motion.md` for camera movement, pacing, and environment motion. Always specify at least one camera movement.
5. Translate non-English user input to English for the final prompt.
6. Keep positive prompt ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â°Ãƒâ€šÃ‚Â¤ 80 words, negative ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â°Ãƒâ€šÃ‚Â¤ 30 words.

## Steps

1. Enhance the prompt using the rules above (do not skip this).
2. Run the helper script in this skill directory:
   ```bash
   bash scripts/generate_video.sh --prompt "A cat walking on a beach at sunset" --duration 5
   ```
3. Return to the user: **both** the saved file path **and** the video URL. The URL must always be shown even when the file is downloaded locally.

## Example

```bash
bash scripts/generate_video.sh \
  --prompt "A cinematic drone shot over a futuristic city at dusk, neon lights, 4k quality" \
  --duration 10 \
  --download ./future_city.mp4
```

## Output location

By default the completed MP4 is downloaded to `~/AgnesAI/videos/agnes_video_<timestamp>.mp4` and the folder is opened automatically.

- macOS/Linux: `~/AgnesAI/videos/`
- Windows (Git Bash/WSL): `~/AgnesAI/videos/` resolves to your user profile folder.

Override with `--download`:

```bash
bash scripts/generate_video.sh --prompt "..." --download ./my_video.mp4
bash scripts/generate_video.sh --prompt "..." --download ./my_video_dir/
```

Skip opening the folder: add `--no-open`.

## Templates / references

- `references/templates.md` ÃƒÆ’Ã‚Â¢ÃƒÂ¢Ã¢â‚¬Å¡Ã‚Â¬ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â prompt templates for cinematic text-to-video, image-to-video animation, product demos, social media shorts, keyframe transitions, etc.

## API reference

- Model: `agnes-video-v2.0`
- Docs: https://agnes-ai.com/zh-Hans/docs/agnes-video-v20

## Setup

Set `AGNES_API_KEY` as an environment variable or in a `.env` file.
