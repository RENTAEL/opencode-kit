---
name: tag-resources
description: "Scans all global OpenCode resources ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â skills, agents, rules, and archetypes ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â and validates or suggests tag metadata for resource_tags-based filtering."
---
# Tag Resources

Scans all global OpenCode resources ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â skills, agents, rules, and archetypes ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â and validates or suggests tag metadata for resource_tags-based filtering.

## When to Use

- After creating new skills, agents, or rules to ensure they're tagged for discoverability
- During config maintenance to audit tagging coverage
- Before running `stack-recommender` to ensure accurate mapping
- When a project uses `resource_tags` filtering and resources are missing from results

## Workflow

### Step 1: Scan All Resources

Check every resource for its tags frontmatter:

**Skills:** `~/.config/opencode/skills/*/SKILL.md`
**Agents:** `~/.config/opencode/agents/*.md`
**Rules:** `~/.config/opencode/rules/*.md`
**Archetypes:** `~/.config/opencode/templates/projects/*/manifest.json`

### Step 2: Classify Each Resource

| Status           | Criteria                                      |
|------------------|-----------------------------------------------|
| ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Tagged         | Has valid tags frontmatter with ÃƒÂ¢Ã¢â‚¬Â°Ã‚Â¥2 tags        |
| ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â Minimal tags  | Has tags but only 1 tag (needs at least 2)     |
| ÃƒÂ¢Ã‚ÂÃ…â€™ Untagged       | No tags field in frontmatter                   |
| ÃƒÂ°Ã…Â¸Ã¢â‚¬ÂÃ‚Â§ Needs review  | Tags exist but are non-standard or misspelled  |

### Step 3: Suggest Tags

For each untagged resource, infer appropriate tags from its content:

- **Skill name/description** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â extract language, framework, domain keywords
- **Agent role/success criteria** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â infer function tags
- **Rule content** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â infer conventions or domain tags
- **Hint-pack manifest** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â ensure manifest `tags` are accurate for stack matching

### Step 4: Report and Apply

```markdown
## Tag Audit Report

### Summary
- ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ 72/95 skills tagged
- ÃƒÂ¢Ã…Â¡Ã‚Â ÃƒÂ¯Ã‚Â¸Ã‚Â 12 skills with minimal tags (need at least 2)
- ÃƒÂ¢Ã‚ÂÃ…â€™ 8 skills untagged ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ suggest tags below
- ÃƒÂ¢Ã‚ÂÃ…â€™ 3 agents untagged
- ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ All 14 rules tagged

### Missing Tags for [skill-name]

Suggested: `[typescript, api, conventions]`
Based on: Skill covers TypeScript API design patterns and naming conventions.

### Untagged Resources

| Resource | Type | Suggested Tags |
|----------|------|---------------|
| my-skill | skill | [typescript, react, testing] |
| my-agent | agent | [testing, playwright, e2e] |
| my-rule | rule | [conventions, python, django] |
```

### Step 5: Apply Tags (with user confirmation)

Before modifying any file, present the proposed changes and confirm:
- "Add suggested tags to [n] resources? (y/n)"
- "Skip any specific resources? (list indices or 'all')"

Apply by editing the frontmatter of each untagged resource.

## Tag Reference

See `~/.config/opencode/rules/resource-tags.md` for the complete tag vocabulary and conventions.

## Integration

### From init-project setup

Before `stack-recommender` runs, `tag-resources` can run to ensure complete coverage:

```
init-project detect ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ tag-resources (if needed) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ stack-recommender ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ project-config-composer
```

### From config maintenance

```bash
# Run as standalone to audit
/resource-hub create rule  # or direct invocation of tag-resources skill
```

### Automated gating

CI or post-commit hooks can run tag-resources to flag new untagged resources:
- Warn if a new skill is added without tags
- Block merge if tag coverage drops below 80%
