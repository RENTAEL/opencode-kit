---
name: why20261-xiaohongshu-keyword-search
description: "Search Xiaohongshu (小红书) by keyword: query the keyword-search API/script for matching notes and authors, then summarize the results for research or content-reference purposes."
---

# 小红书关键词搜索 (Xiaohongshu Keyword Search)

Search Xiaohongshu content by keyword and summarize matching notes.

## Usage

```bash
# Keyword search
python <skill-dir>/scripts/keyword_search.py "关键词" --limit 20
```

## Output

For each matching note, report:

- Title and author
- Note URL / ID
- Likes & saves (if available)
- Short snippet

## When to use

- Researching what Xiaohongshu users post about a keyword.
- Finding reference content for notes/campaigns.
- Competitor / trend checks.

## Rules

- Only use public search results; no login-required scraping.
- Attribute authors; do not republish full text.
- If the script is unavailable, state that instead of inventing results.
