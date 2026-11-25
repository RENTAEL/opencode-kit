---
name: open-higgsfield-ai
description: Use when the user wants to generate AI images, videos, lip-sync or cinematic shots with Open Higgsfield AI (a self-hosted Higgsfield-style studio powered by Muapi, 200+ models such as Flux, Nano Banana, Kling, Sora, Veo, Seedance), or mentions Higgsfield, Open Higgsfield, Image/Video/Lip Sync/Cinema Studio, or Muapi studio.
---
# Open Higgsfield AI

Local install: `<projects-dir>/Open-Higgsfield-AI` (Next.js app, dependencies installed with `npm run setup`).

## Start the studio

1. Check whether it is already up: `curl -s -o /dev/null -w "%{http_code}" http://localhost:3000`.
2. If not, start it in the background from the install folder: `npm run dev` (run_in_background). Wait for the "Ready" line, not a sleep loop.
3. Open `http://localhost:3000` in the built-in browser for the user.

## Use

- Studios: Image (text-to-image / image-to-image), Video (text-to-video / image-to-video), Lip Sync (portrait or video + audio), Cinema (camera, lens, focal length, aperture controls).
- Generation needs a Muapi API key (https://muapi.ai). The app asks for it on first use and keeps it in the browser's localStorage. The user types the key in themselves; never enter it for them and never write it to a file.
- Every generation is a paid Muapi request. Confirm the model and prompt with the user before clicking Generate.
- Outputs are downloaded from the app's History panel.

## Update

`git pull` then `npm run setup` in the install folder.
