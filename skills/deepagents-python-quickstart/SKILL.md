---
name: deepagents-python-quickstart
description: "Follow the live docs ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â do not invent an alternate API from memory:"
---
# Deep Agents Python quickstart

Follow the live docs ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â do not invent an alternate API from memory:

**https://docs.langchain.com/oss/python/deepagents/quickstart**

Fetch that page (Docs MCP or HTTP) and implement the research-agent shape it shows (`create_deep_agent`, research system prompt, invoke with a research question like ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œWhat is LangGraph?ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â).

## Local setup constraints

Apply these on top of the quickstart (they keep setup minimal and model-agnostic):

1. **Ask** which provider/model to use. Showcase that Deep Agents are model-agnostic. Suggested prompt:

   > Which model should this agent use? Pass a `provider:model` string ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â e.g. `openai:gpt-5.5`, `anthropic:claude-sonnet-5`, `google_genai:gemini-3.5-flash`. Default if you're unsure: **`anthropic:claude-sonnet-5`**.  
   > We'll use that provider's built-in web search (no separate search API key).

2. Create a **new** directory (e.g. `deep-agent/`) and do all work there ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â do not pollute the open project.

3. **Do not use Tavily** (or any second search vendor). Replace the quickstart's `internet_search` / Tavily tool with the chosen provider's built-in web search. Look up the current tool shape on that provider's LangChain chat docs (examples as of writing ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â re-check if needed):

   | Provider | Built-in search tool |
   |----------|----------------------|
   | Anthropic | `{"type": "web_search_20260209", "name": "web_search", "max_uses": 5}` |
   | OpenAI | `{"type": "web_search"}` |
   | Google | `{"google_search": {}}` |

   Prefer Anthropic / OpenAI / Google so provider search is available. Only secret: that provider's API key in `.env` (gitignored). Skip LangSmith tracing unless they ask.

4. Install `deepagents` (+ `python-dotenv`) and the provider package for their model ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not `tavily-python`.

5. Run the research example, show output, then stop. Point to `deep-agents-core` / customization / Managed Deep Agents for next steps.
