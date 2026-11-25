# Positive Prompt Components

Vocabulary for the positive (desired) portion of image and video generation prompts. Select components by category and combine them with the assembly formula in SKILL.md.

## Styles

Pick exactly one style per prompt.

| Style          | Keywords                                                                              | Best for                                        |
| -------------- | ------------------------------------------------------------------------------------- | ----------------------------------------------- |
| Photorealistic | photorealistic, hyperrealistic, RAW photo, DSLR quality, 8k uhd                       | Portraits, products, landscapes, architecture   |
| Cinematic      | cinematic, film grain, anamorphic lens, color graded, 2.39:1 aspect                   | Storytelling, drama, scenes, video              |
| Anime          | anime style, cel-shaded, vibrant flat colors, clean lineart                           | Characters, illustrations, backgrounds          |
| Watercolor     | watercolor painting, soft edges, pastel palette, wet-on-wet, hand-painted             | Art prints, greeting cards, book covers         |
| Oil Painting   | oil painting, impasto, visible brush strokes, canvas texture, classical               | Fine art, portraits, landscapes                 |
| 3D Render      | 3D render, octane render, volumetric lighting, subsurface scattering, CGI             | Products, architecture, sci-fi, abstract        |
| Minimalist     | minimalist, clean lines, negative space, flat design, simple geometry                 | Icons, logos, UI mockups, posters               |
| Cyberpunk      | cyberpunk, neon-lit, holographic, rain-slicked streets, dark atmosphere               | Sci-fi, gaming, urban night scenes              |
| Editorial      | editorial photography, magazine quality, fashion-forward, styled shoot                | Fashion, lifestyle, brand imagery               |
| Concept Art    | concept art, matte painting, environment design, production art                       | Games, film pre-visualization, worldbuilding    |
| Pixel Art      | pixel art, retro, 16-bit, sprite style, limited palette                               | Games, icons, nostalgic designs                 |
| Isometric      | isometric view, 3D illustration, diorama, miniature, tilt-shift                       | Infographics, game assets, architecture         |
| Surreal        | surreal, dreamlike, impossible geometry, ethereal, uncanny juxtaposition              | Art, album covers, creative campaigns           |
| Vintage        | vintage, film photography, faded colors, grain, retro aesthetic                       | Nostalgia, branding, editorial                  |
| Line Art       | line art, ink drawing, clean outlines, cross-hatching, monochrome linework            | Icons, coloring pages, editorial illustration   |
| Low Poly       | low poly, faceted geometry, flat shading, polygonal, geometric                        | Game assets, abstract scenes, tech visuals      |
| Claymation     | claymation, stop-motion look, plasticine texture, handcrafted, miniature set          | Playful scenes, children's content, comedy      |
| Ukiyo-e        | ukiyo-e, woodblock print, flat perspective, bold outlines, traditional Japanese print | Posters, decorative art, wave and nature motifs |

## Quality Boosters

Layered by goal; start with Universal and add at most one higher tier.

| Tier        | Keywords                                                                | When to use                  |
| ----------- | ----------------------------------------------------------------------- | ---------------------------- |
| Universal   | highly detailed, sharp focus, professional                              | Every prompt (default)       |
| Photo-grade | 8k uhd, high dynamic range, crisp details, natural skin tones           | When the user wants realism  |
| Product     | studio lighting, clean background, commercial photography, product shot | Product images, e-commerce   |
| Art-grade   | intricate details, masterpiece, award-winning, gallery quality          | Artistic pieces, portfolios  |
| Video-grade | smooth motion, high frame rate, cinematic quality, broadcast-ready      | Video generation             |
| Print-grade | 300 dpi, print quality, high resolution, color-accurate                 | When the output is for print |

## Lighting

| Type             | Keywords                                                         | Mood                               |
| ---------------- | ---------------------------------------------------------------- | ---------------------------------- |
| Golden hour      | golden hour, warm sunlight, long shadows, amber glow             | Warm, romantic, nostalgic          |
| Blue hour        | blue hour, twilight, cool ambient, dusk                          | Calm, mysterious, urban            |
| Studio soft      | soft studio lighting, three-point, diffused, even                | Clean, professional, neutral       |
| Dramatic         | chiaroscuro, rim lighting, high contrast, single light source    | Intense, moody, theatrical         |
| Neon             | neon glow, colored lighting, pink and blue, cyberpunk            | Futuristic, urban, nightlife       |
| Natural overcast | overcast sky, soft diffused daylight, no harsh shadows           | Calm, organic, documentary         |
| Backlit          | backlit, silhouette, lens flare, glowing edges                   | Ethereal, dramatic, hopeful        |
| Candlelight      | candlelight, warm flicker, intimate, low key                     | Cozy, romantic, historical         |
| Volumetric       | volumetric lighting, god rays, light shafts, atmospheric haze    | Epic, spiritual, cinematic         |
| Flat / Even      | flat lighting, no shadows, even exposure, clinical               | Technical, product, scientific     |
| Moonlight        | moonlight, cool night light, silvery glow, low-key night         | Night scenes, mystery, romance     |
| Hard midday sun  | harsh midday sun, direct sunlight, hard shadows, bright daylight | Street, documentary, summer energy |
| Split lighting   | split lighting, half-lit face, strong side light, 90-degree key  | Portraits, drama, tension          |

## Composition and Camera Angle

| Type                | Keywords                                                    | Effect                                 |
| ------------------- | ----------------------------------------------------------- | -------------------------------------- |
| Close-up            | close-up, macro, tight crop, shallow depth of field, bokeh  | Intimacy, detail, emotion              |
| Wide / Establishing | wide-angle, panoramic, establishing shot, expansive         | Context, scale, environment            |
| Aerial              | aerial view, drone shot, bird's eye view, top-down          | Overview, pattern, geography           |
| Low angle           | low angle, looking up, heroic, imposing                     | Power, grandeur, dominance             |
| Eye level           | eye-level, straight-on, natural perspective                 | Neutral, relatable, portrait           |
| Dutch angle         | dutch angle, tilted frame, diagonal composition, unsettling | Tension, disorientation, action        |
| Over-the-shoulder   | over-the-shoulder, foreground blur, POV-adjacent            | Narrative, connection                  |
| Symmetric           | centered, symmetrical, reflection, mirror composition       | Order, calm, formality                 |
| Rule of thirds      | rule of thirds, off-center subject, balanced negative space | Natural, dynamic, professional         |
| Frame within frame  | framed by doorway, window, archway, natural frame           | Depth, focus, voyeuristic              |
| First-person POV    | first-person view, POV, subjective camera, hands in frame   | Immersion, action, gaming              |
| Fisheye             | fisheye lens, ultra-wide distortion, curved horizon         | Action sports, skate, playful creative |

## Color Mood

| Mood            | Keywords                                              | Feel                               |
| --------------- | ----------------------------------------------------- | ---------------------------------- |
| Warm            | warm tones, amber, orange, golden, cozy               | Comfort, energy, passion           |
| Cool            | cool tones, blue, teal, silver, icy                   | Calm, technology, distance         |
| Monochrome      | monochrome, black and white, grayscale, high contrast | Timeless, dramatic, editorial      |
| Pastel          | pastel colors, soft palette, muted, gentle            | Soft, delicate, dreamy             |
| Vibrant         | vibrant, saturated, bold colors, popping              | Energy, youth, excitement          |
| Earthy          | earth tones, olive, terracotta, brown, natural        | Organic, grounded, rustic          |
| Dark / Moody    | dark palette, deep shadows, desaturated, noir         | Mystery, luxury, drama             |
| Neon / Electric | neon colors, electric blue, hot pink, fluorescent     | Futuristic, nightlife, cyber       |
| Sepia           | sepia tone, aged photograph, brownish tint, antique   | Nostalgia, history, memory         |
| Duotone         | duotone, two-color palette, high-contrast two-tone    | Posters, music, editorial graphics |

## Texture and Material

| Material | Keywords                                                      | Use                              |
| -------- | ------------------------------------------------------------- | -------------------------------- |
| Metal    | brushed metal, chrome, steel, reflective, industrial          | Products, sci-fi, architecture   |
| Glass    | glass, transparent, refraction, crystal, prismatic            | Luxury, abstract, science        |
| Fabric   | silk, linen, woven texture, soft cloth, draping               | Fashion, interior, still life    |
| Wood     | natural wood grain, oak, walnut, carved, rustic               | Interior, craft, warmth          |
| Stone    | marble, granite, rough stone, carved, ancient                 | Architecture, sculpture, fantasy |
| Organic  | leaves, petals, skin, fur, feathers, natural                  | Nature, portraits, wildlife      |
| Ceramic  | glossy ceramic, porcelain, glazed surface, smooth pottery     | Tableware, craft, product shots  |
| Liquid   | liquid splash, viscous flow, water droplets, rippling surface | Beverages, cosmetics, abstract   |
