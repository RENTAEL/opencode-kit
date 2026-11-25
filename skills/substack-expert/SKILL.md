---
name: substack-expert
description: "Identify which goals apply (formatting, SEO, growth, monetization) and confirm the topic. If the request is ambiguous, default to producing SEO metadata and a formatted structure outline simultaneously."
---
# Substack Expert

## Parameters

| Parameter     | Description                                            | Default                          |
|---------------|--------------------------------------------------------|----------------------------------|
| `topic`       | Subject or draft content to work with                  | Infer from the conversation      |
| `goal`        | Primary objective: `format`, `seo`, `growth`, `monetize` | `format` + `seo` if unspecified |
| `language`    | Output language                                        | Match the user's message language |

## Workflow

### 1. Clarify Scope

Identify which goals apply (formatting, SEO, growth, monetization) and confirm the topic. If the request is ambiguous, default to producing SEO metadata and a formatted structure outline simultaneously.

### 2. Visual Formatting

- Structure content with `Heading 1`, `Heading 2`, and `Heading 3` to improve readability and facilitate search-engine crawling.
- Apply the centering and styling techniques described in `references/formatting-best-practices.md`.
- Insert native engagement tools (Subscribe button, polls, Leave a comment) at natural breakpoints in the post.

### 3. SEO and Metadata

Produce the following fields for every post:

- **Title**: 40ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“60 characters. Use clear modifiers, keywords, and authority signals (e.g., "Tested", "Complete Guide"). Avoid vague or clickbait phrasing.
- **URL Slug**: 3ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“5 main keywords only, no auto-generated numbers, no dates (keeps the post evergreen). Example: `/substack-seo-strategy`.
- **Meta Description**: 155ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“160 characters, includes the primary keyword and an implicit call to action.
- **Image Alt Text**: Describe the image for accessibility; incorporate article keywords organically.

Consult `references/seo-output-example.md` for a worked example.

### 4. Growth Strategies

- **Substack Notes**: Publish short snippets derived from the post to Notes immediately after publishing. Leave authentic comments on related publications to build name recognition.
- **Recommendations rotation**: Review Analytics monthly to identify which partner newsletters drive inbound traffic. Rotate recommended partners every 30ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“60 days to maintain reciprocal growth.

### 5. Monetization (Free ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Paid Conversion)

- **Tease & Convert**: Publish the core article freely, but gate a utility bonus (template, spreadsheet, prompt set, audio) behind the paywall. Prove value before asking for payment.
- **VIP outreach**: In the Dashboard, filter subscribers by engagement score (4ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“5 stars), then send a targeted direct message offering a special rate or exclusive invite to the paid tier.
- **Welcome email**: Customize the automated welcome email to introduce the author, set publishing cadence expectations, and link to the three best existing articles. Never leave the platform default.
- **Homepage taxonomy**: Group posts into Tags (equivalent to newspaper sections) and add them to the navigation bar via *Website Themes* for advanced content discovery.

## Quality Checklist

Before delivering output, verify:

- [ ] Title is 40ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“60 characters and contains the primary keyword.
- [ ] URL slug has 3ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“5 words, no numbers, no dates.
- [ ] Meta description is 155ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Å“160 characters with a keyword and implicit CTA.
- [ ] All images have alt text.
- [ ] Subject line (if applicable) is under 50 characters and free of spam triggers.
- [ ] At least one native engagement element (button, poll, or comment prompt) is included.
- [ ] Paywall placement follows the Tease & Convert model (not a mid-sentence cut).
- [ ] Welcome email customization is recommended if the post is the first in a new publication.
