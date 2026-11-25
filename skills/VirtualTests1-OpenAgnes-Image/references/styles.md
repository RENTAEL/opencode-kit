# Style Reference

## Style-specific Prompt Templates

| Style | Prompt template |
|-------|----------------|
| **Real Photo** | `A real photograph of [subject], taken with a camera. [setting]. Natural lighting, [composition], [color_tone] tones, [mood] atmosphere. [real-world details]. Slightly imperfect, natural colors, authentic, real world textures.` |
| **Realistic Illustration** | `[subject], detailed digital illustration, [color_tone] palette, [composition], [lighting], [mood]. Clean lines, professional shading, rich textures.` |
| **Anime** | `[subject], anime art style, cel shading, crisp linework, vibrant [color_tone] colors, [composition], [lighting], [mood]. Studio Ghibli inspired.` |
| **Oil Painting** | `[subject], oil painting on canvas, thick brushstrokes, rich impasto texture, [color_tone] palette, [composition], [lighting], [mood]. Classical technique.` |
| **Watercolor** | `[subject], watercolor painting, soft edges, paper texture, color bleeding, [color_tone] palette, [composition], [mood]. Hand-painted feel.` |
| **3D Render** | `[subject], 3D render, octane render, global illumination, [color_tone] palette, [composition], [lighting], [mood]. Highly detailed, volumetric lighting.` |
| **Minimalist** | `[subject], minimalist style, clean lines, negative space, [color_tone] palette, [composition], [lighting], [mood]. Simple, elegant.` |
| **Surrealist** | `[subject], surrealist style, dreamlike, impossible geometry, [color_tone] palette, [composition], [lighting], [mood]. Dali-esque, symbolic.` |
| **Pixel Art** | `[subject], pixel art, retro game style, 8-bit, limited color palette, [color_tone] colors, [composition], [mood]. Blocky, charming.` |
| **Cyberpunk** | `[subject], cyberpunk style, neon lights, rain-slicked streets, high contrast, [color_tone] palette, [composition], [lighting], [mood]. Futuristic, Blade Runner aesthetic.` |
| **Fantasy Art** | `[subject], fantasy art, epic, magical atmosphere, [color_tone] palette, [composition], [lighting], [mood]. Mythical, otherworldly, detailed.` |
| **Sketch** | `[subject], sketch, black and white, charcoal or pencil, [composition], [lighting], [mood]. Rough lines, artistic, minimalist, monochrome.` |

---

## Real Photo Critical Rules

**DO NOT use** (AI-generation tells):
`photorealistic`, `masterpiece`, `best quality`, `8K`, `sharp focus`,
`subsurface scattering`, `ray tracing`, `volumetric lighting`,
`cinematic`, `studio lighting`, `depth of field`, `intricate details`,
`highly detailed`, `octane render`

**DO use**:
`real photograph`, `taken with a camera`, `natural lighting`,
`slightly imperfect`, `authentic`, `unposed`, `everyday scene`,
`natural colors`, `real world textures`, `slightly grainy`

---

## Prompt Placeholders

| Placeholder | Maps From | Example |
|-------------|-----------|---------|
| `[subject]` | User-provided subject | `a fluffy orange cat sleeping on a windowsill` |
| `[setting]` | Derived from subject + extra | `in a cozy sunlit living room` |
| `[composition]` | Composition choice | `close-up view` |
| `[color_tone]` | Color tone choice | `warm golden` |
| `[lighting]` | Lighting choice | `soft natural light` |
| `[mood]` | Mood choice | `serene and peaceful` |
| `[real-world details]` | Extra user details | `with dust motes floating in the sunbeam` |
