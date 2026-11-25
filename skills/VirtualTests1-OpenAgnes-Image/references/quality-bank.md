# Quality Enhancement Vocabulary

## Quality Keywords by Category

Inject 2-3 per prompt based on style:

| Category | Keywords |
|----------|----------|
| General quality | `high quality`, `detailed`, `well-composed` |
| Texture (art styles) | `rich texture`, `fine details`, `brush strokes`, `paper grain` |
| Atmosphere | `atmospheric`, `immersive`, `moody`, `ethereal`, `vibrant`, `serene` |
| Clarity | `crisp`, `clear`, `defined` |
| Artistic | `aesthetic`, `artistic`, `stylized`, `expressive` |

## Style-Specific Enhancement Pairs

| Style | Recommended quality terms | Avoid |
|-------|--------------------------|-------|
| Real Photo | `natural colors`, `authentic`, `real textures` | `masterpiece`, `8K`, `highly detailed` |
| Realistic Illustration | `rich textures`, `professional shading`, `detailed` | `photorealistic` |
| Anime | `crisp linework`, `vibrant`, `clean` | `realistic`, `3D` |
| Oil Painting | `thick impasto`, `canvas texture`, `rich` | `smooth`, `digital` |
| Watercolor | `soft edges`, `paper grain`, `color bleeding` | `sharp`, `crisp` |
| 3D Render | `global illumination`, `highly detailed`, `volumetric` | `flat`, `2D` |
| Minimalist | `clean lines`, `simple`, `elegant` | `busy`, `detailed` |
| Surrealist | `dreamlike`, `symbolic`, `impossible` | `realistic`, `ordinary` |
| Pixel Art | `blocky`, `charming`, `limited palette` | `smooth`, `detailed` |
| Cyberpunk | `neon`, `high contrast`, `futuristic` | `natural`, `soft` |
| Fantasy Art | `epic`, `magical`, `mythical`, `otherworldly` | `ordinary`, `mundane` |
| Sketch | `rough lines`, `artistic`, `monochrome` | `colorful`, `polished` |

## Negative Prompt Guidance

Include negative terms conditionally:

| Condition | Negative terms |
|-----------|---------------|
| Style is Real Photo | `cartoonish, illustration, painting, anime` |
| Style is Anime | `realistic, photorealistic, 3D, oil painting` |
| Style is 3D Render | `flat, 2D, cartoon, sketch` |
| Style is Watercolor | `photorealistic, sharp, digital` |
| Style is Sketch | `colorful, photorealistic, 3D` |
| Color tone is Warm | `cold, blue, gray` |
| Color tone is Cool | `warm, yellow, orange` |
| Color tone is Monochrome | `colorful, vibrant, saturated` |
| Color tone is Vivid | `washed out, dull, muted` |
| Color tone is Dark | `bright, sunny, light` |
