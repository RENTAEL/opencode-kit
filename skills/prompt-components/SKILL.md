---
name: prompt-components
description: "Structured vocabulary and assembly rules for building effective image and video generation prompts. Read the reference files for component options, then assemble them with the modes and formulas below."
---
# Prompt Components

Structured vocabulary and assembly rules for building effective image and video generation prompts. Read the reference files for component options, then assemble them with the modes and formulas below.

## When to Activate

- The user asks to generate an image or video, with or without details.
- The request is vague ("draw something", "make me a cool video").
- Another skill needs prompt enhancement before calling a generation API.
- The user asks "what style should I use?" or "how do I get better quality?".
- The user asks for negative prompts or quality-improvement tips.

## Three Interaction Modes

Pick the mode from how complete the request is. Never mix modes: if the intent is clear, do not ask questions; if it is vague, do not guess silently.

### Mode 1: Direct

**Trigger:** The user provides subject + style + mood (or clearly equivalent detail).

**Action:** Map the user's words to components, assemble the full prompt, and execute immediately. Do not ask questions. Do not suggest alternatives.

> "A cyberpunk city at night, neon lights, cinematic wide shot, 8k"

Recognize: style = Cyberpunk, lighting = Neon, composition = Wide, quality = Photo-grade. Assemble and run.

### Mode 2: Suggest

**Trigger:** The user provides a subject but is missing style, mood, lighting, or composition.

**Action:** Propose 2ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“3 distinct component combinations as labeled options. Let the user pick one, mix elements, or say "surprise me".

> "Generate a product photo of headphones"

Respond with three directions:

- **A) Studio clean:** soft three-point lighting, white background, commercial photography, 8k uhd
- **B) Lifestyle:** golden hour, wooden desk, shallow depth of field, editorial photography
- **C) Bold graphic:** gradient background, dramatic rim lighting, high contrast, 3D render

Then ask: "Which direction ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â or should I combine elements from several?"

### Mode 3: Guide

**Trigger:** No usable specifics ("draw something", "generate a video"), or the request is too ambiguous to assemble.

**Action:** Ask focused questions one at a time, maximum 4. After the last answer, assemble immediately without further questions.

**Question order:**

1. Subject ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "What should be in the image/video?"
2. Style ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Photorealistic, illustration, 3D render, anime, or another style?"
3. Mood / lighting ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Bright and clean? Dark and dramatic? Warm? Cool?"
4. Use case ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "Social post? Wallpaper? Product listing? Presentation?"

**Rules for Mode 3:**

- Never ask more than 4 questions in total.
- If one reply answers several questions, skip the answered ones.
- If the user says "you decide" or "surprise me", switch to Mode 1 with your best judgment.
- Show the final assembled prompt before executing.

## Assembly Formula

### Image prompt

```
[style] + [subject and action] + [environment/background] + [lighting] + [composition/angle] + [quality boosters]
```

Worked example:

```
cyberpunk, neon-lit city street at night, rain-slicked asphalt reflecting signs,
neon glow with pink and blue lighting, wide-angle establishing shot,
8k uhd, highly detailed, sharp focus
```

Negative (always append; the user never needs to ask):

```
[universal negatives] + [subject-category negatives] + [style-conflict negatives]
```

### Video prompt

```
[camera movement] + [scene description] + [subject action] + [time of day / weather] + [style] + [quality keywords] + [pacing]
```

Worked example:

```
slow orbit shot, misty pine forest at dawn, a deer walking between trees,
soft morning light, cinematic, smooth motion, high frame rate,
gentle meditative pace, leaves rustling, mist drifting
```

Negative (always append):

```
[universal negatives] + [video-specific negatives]
```

## Auto-Enhancement Rules

Do all of the following automatically, without waiting for the user to ask:

| Condition                                                | Action                                                            |
| -------------------------------------------------------- | ----------------------------------------------------------------- |
| Any image or video generation                            | Append universal negatives from `references/negative.md`          |
| Subject involves people, faces, or hands                 | Also append Human / Anatomy negatives                             |
| Subject involves a product or commercial shot            | Also append Product / Commercial negatives                        |
| Subject is a landscape or environment                    | Also append Landscape / Scene negatives                           |
| Any video generation                                     | Also append Video-Specific negatives                              |
| A specific style is chosen                               | Also append the matching Style Conflicts block                    |
| User writes in Chinese (or another non-English language) | Translate the prompt to English; models respond better to English |
| No quality keywords given                                | Add "highly detailed, sharp focus"                                |
| No size given                                            | Image: 1024x768. Video: 1152x768                                  |
| No lighting given                                        | Do NOT invent lighting; leave the model default                   |
| User says "high quality", "HD", or "4k/8k"               | Add quality boosters from `references/positive.md`                |

## Rules

Hard constraints that override everything above:

- Positive prompt: at most 80 words. Trim filler and adjectives that add no visual information.
- Negative prompt: at most 30 words. Only include categories relevant to the current subject.
- Output language: always English prompts, even when the user speaks another language.
- One style per prompt. Never mix incompatible styles ("photorealistic anime watercolor").
- No keyword spam: never repeat a keyword ("8k, 8k resolution, 8k uhd" ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â pick one).
- Prefer specific over generic: "golden hour backlight" beats "nice lighting".
- Never invent trigger words outside the reference files unless they are standard photography, art, or film terminology.
- Video: always specify camera movement. "Static shot" is a valid choice, but it must be explicit.
- Keep environment motion to 1ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“2 details and subject motion to one main action per short clip.

## Reference Files

| File                     | Contents                                                             | When to read                    |
| ------------------------ | -------------------------------------------------------------------- | ------------------------------- |
| `references/positive.md` | Styles, quality boosters, lighting, composition, color mood, texture | Always when assembling a prompt |
| `references/negative.md` | Categorized negative prompts                                         | Always (auto-append)            |
| `references/motion.md`   | Camera movement, pacing, transitions, environment and subject motion | Video generation only           |
