# OpenVision

Bring multimodal vision to OpenCode. Analyze screenshots, generate images, perform OCR, compare designs, and build visual workflows directly from the terminal.

## Features

- **Image generation** — create images from text descriptions via Flux.1-dev
- **Image analysis** — describe, caption, and analyze any image
- **OCR** — extract text from screenshots, scans, and photos
- **Smart parsing** — `/openvision a dragon cfg=8 seed=42` skips right to generation
- **Auto-setup** — installs dependencies and prompts for API key on first run

## Prerequisites

- Node.js 22+
- NVIDIA API key from [build.nvidia.com](https://build.nvidia.com/black-forest-labs/flux_1-dev)

## Installation

Clone or download the repo and place it in your opencode skills directory:

```bash
git clone https://github.com/<your-user>/OpenVision.git ~/.config/opencode/skills/OpenVision
```

Or manually copy the `OpenVision/` folder into `~/.config/opencode/skills/`.

## Usage

| Command | Action |
|---------|--------|
| `/openvision a cat in space` | Generate — prompt extracted, only asks for optional params |
| `/openvision` | Interactive — asks what you want to do |
| `/openvision describe ~/screenshot.png` | Analyze / describe an image |
| `/openvision read text ~/scan.jpg` | OCR — extracts text |
| `/openvision a dragon cfg=8 steps=40 seed=123` | Full params inline, zero questions |

### Generation parameters

| Param | Default | Description |
|-------|---------|-------------|
| `prompt` | — | Image description (required) |
| `cfg_scale` | 5 | Prompt adherence 1-20. Higher = stricter |
| `steps` | 25 | Quality vs speed 1-50. Higher = better |
| `seed` | random | Same seed + same prompt = same image |

## First run

The skill auto-installs `npm` dependencies and prompts you for your API key. No manual setup needed.

## Scripts

| Script | Purpose |
|--------|---------|
| `generate-image.mjs` | Generate image from prompt |
| `describe-image.mjs` | Describe / OCR / analyze an image |

## Topics

`opencode` `opencode-skill` `multimodal` `vision` `flux` `paligemma` `nvidia` `image-generation` `ocr` `ai`
