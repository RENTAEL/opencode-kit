# Negative Prompt Library

Categorized negative prompts for image and video generation. The agent selects and appends the relevant categories automatically based on the subject and medium; the user never needs to ask.

## Universal (always include for every generation)

```
blurry, low quality, pixelated, watermark, signature, text overlay,
jpeg artifacts, cropped, out of frame
```

## Human / Anatomy

Auto-add when the subject involves people, faces, hands, or bodies.

```
deformed fingers, extra digits, malformed hands, fused fingers,
missing fingers, extra limbs, disfigured, bad anatomy,
asymmetrical eyes, mutated, deformed face, cross-eyed,
poorly drawn hands, poorly drawn face, clone face
```

## Landscape / Scene

Auto-add for landscapes, cityscapes, nature, and environment shots.

```
oversaturated, flat lighting, empty composition, tilted horizon,
lens distortion, chromatic aberration, overexposed sky,
underexposed foreground, dull colors
```

## Product / Commercial

Auto-add for product photos, e-commerce, and branding imagery.

```
harsh shadows, cluttered background, inconsistent lighting,
low resolution, color banding, reflections of photographer,
dust, scratches, fingerprints
```

## Video-Specific

Auto-add for ALL video generation, regardless of subject.

```
flickering, frame inconsistency, jittery, sudden cuts,
morphing artifacts, temporal aliasing, warping, unstable edges,
ghosting, frame stuttering
```

## Style Conflicts

Add the conflicting block when a specific style is chosen. This prevents the model from blending incompatible aesthetics.

### When style = Photorealistic

```
cartoon, anime, illustration, painting, sketch, drawing,
cel-shaded, flat color
```

### When style = Anime / Illustration

```
photorealistic, photograph, 3D render, hyperrealistic,
DSLR, RAW photo
```

### When style = Minimalist

```
cluttered, busy background, ornate, baroque, maximalist,
overly detailed, noisy
```

### When style = 3D Render

```
flat, 2D, hand-drawn, sketch, photograph, film grain
```

### When style = Watercolor / Painting

```
photorealistic, 3D render, sharp edges, digital, pixelated,
vector, flat design
```

### When style = Cinematic

```
flat lighting, amateur, snapshot, overexposed, webcam quality
```

### When style = Pixel Art

```
smooth gradients, anti-aliased edges, photorealistic, 3D render,
photograph, high-resolution detail
```

## Usage Rules

- Maximum 30 negative keywords per prompt. Trim to the most relevant.
- Typical set: Universal + one subject category + Video-Specific (if video) + one Style Conflicts block.
- Do NOT add all categories. Only add what is relevant to the current subject.
- If the user explicitly says "no negative prompts", respect that.
- Negative prompts are comma-separated, lowercase, with no punctuation beyond commas.
