---
name: lh-visual-craft
description: "To make something more important: first try MORE SPACE around it, then weight, then size, then color ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â and only then decoration (borders, backgrounds). Beginners reach for color and boxes first; that's why beginner UIs look busy. The squint test: blur your eye..."
---
## Critical Patterns

### 1. Hierarchy is built with size, weight, and space ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â in that order of cost

To make something more important: first try MORE SPACE around it, then weight,
then size, then color ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â and only then decoration (borders, backgrounds).
Beginners reach for color and boxes first; that's why beginner UIs look busy.
The squint test: blur your eyes (or scale to 25%) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the primary action and
content grouping should still be obvious.

### 2. Spacing on a scale, grouping by proximity

- All spacing from one geometric scale (4/8-based: 4, 8, 12, 16, 24, 32, 48,
  64). A value off the scale needs a reason you can say ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â an optical
  correction, a platform metric, a 1px border. Without one, an arbitrary
  `13px` is drift, and drift is what the scale exists to stop.
- Proximity IS grouping: related things closer, unrelated things farther.
  Most "needs a border/divider" problems are actually spacing-ratio problems ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â
  the space INSIDE a group must be visibly smaller than the space BETWEEN groups.
- When something feels cramped, the fix is almost always more whitespace, not
  smaller content. Whitespace is a feature, not leftover room.

### 3. Typography: few sizes, fewer weights, readable measure

- A type scale of 4-6 sizes covers a whole product (e.g. 12/14/16/20/24/32);
  two weights (regular + semibold/bold) do 95% of the work.
- Body text: 16px baseline, line-height ~1.5, line length 45-75 characters.
  Long-form text wider than ~75ch is a reading bug.
- Hierarchy in text comes from size+weight+color TOGETHER stepping down
  (heading strong/dark ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ body regular ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ metadata smaller/muted), not from six
  heading levels.

### 4. Color: semantic roles, neutral base, one accent doing the work

- Colors are ROLES, not values ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the token indirection whose naming rules live
  in [lh-dev-handoff](../lh-dev-handoff/SKILL.md) #2. Here the judgment is which
  roles a palette needs: background, surface, border, text-primary,
  text-muted, one accent, and the success/warning/danger trio; only the
  palette file knows hex codes.
- Neutral grays carry the interface; ONE accent color marks interactivity and
  primary actions. If the accent appears everywhere, it marks nothing.
- Contrast is non-negotiable: 4.5:1 for body text, 3:1 for large text and UI
  components. Check it, don't eyeball it ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â muted-gray-on-gray is the most
  common accessibility failure in modern UIs.
- Never encode meaning in color alone (add icon/label) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â colorblind users exist.

### 5. Layout: alignment is invisible until it's broken

- Everything aligns to something: pick edges (left-align text almost always)
  and stick to them. Mixed alignments read as sloppiness even when nobody can
  name the problem.
- Consistent container widths and gutters per breakpoint; content constrained
  (max-width) on large screens ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â full-bleed text walls are not "using the space".
- Elevation (shadows) sparingly and consistently: 2-3 levels max, each meaning
  something (raised, overlay). Ten different shadows = no elevation system.
- Layout changes at a breakpoint when the content stops working, not because a
  device class exists: a table that becomes cards, a sidebar that becomes a
  sheet. Scale until it breaks; reflow only then.
- Touch targets and motion are constraints the persona promises and this skill
  carries: 44px minimum hit area on anything tappable (visual size can be
  smaller, the target can't), and motion only where it explains a state change
  ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â with `prefers-reduced-motion` honoured, because for some users animation
  is not decoration, it's nausea.

### 6. Diagnosing "it feels off" ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the checklist order

When a screen feels wrong, check in this order (highest hit-rate first):
inconsistent spacing ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ competing emphasis (two primary things) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ misalignment ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢
too many font sizes/weights ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ low contrast text ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ accent color overused. Name
the finding in these terms, not as taste.

## Resources

- Sibling skills: [lh-ux-flows](../lh-ux-flows/SKILL.md) (what the screen DOES),
  [lh-dev-handoff](../lh-dev-handoff/SKILL.md) (turning these choices into tokens),
  [lh-mockups](../lh-mockups/SKILL.md) (rendering them)
