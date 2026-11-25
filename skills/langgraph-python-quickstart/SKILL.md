---
name: langgraph-python-quickstart
description: "Follow the live docs ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â do not invent an alternate API from memory:"
---
# LangGraph Python quickstart

Follow the live docs ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â do not invent an alternate API from memory:

**https://docs.langchain.com/oss/python/langgraph/quickstart**

Fetch that page (Docs MCP or HTTP) and implement what it shows (calculator / math agent with the Graph API). Prefer the Graph API path over the Functional API unless the user asks otherwise. Skip IPython graph visualization.

## Local setup constraints

Apply these on top of the quickstart (they keep setup minimal and model-agnostic):

1. **Ask** which provider/model to use. Showcase that LangGraph works with any LangChain chat model. Suggested prompt:

   > Which model should this agent use? Pass a `provider:model` string ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â e.g. `openai:gpt-5.5`, `anthropic:claude-sonnet-5`, `google_genai:gemini-2.5-flash-lite`. Default if you're unsure: **`anthropic:claude-sonnet-5`**.

   The docs often hardcode Anthropic ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â replace with `init_chat_model("<MODEL>")` (or equivalent) using their choice. If using Claude Sonnet 5+, omit `temperature` / `top_p` / `top_k` (unsupported).

2. Create a **new** directory (e.g. `langgraph-agent/`) and do all work there ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â do not pollute the open project.

3. Only secret: the provider API key in `.env` (gitignored). No LangSmith / Tavily unless they ask. Prefer they edit `.env` themselves ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't paste keys into chat.

4. Install packages from the quickstart plus the provider package for their model.

5. Run the example (e.g. ÃƒÂ¢Ã¢â€šÂ¬Ã…â€œAdd 3 and 4.ÃƒÂ¢Ã¢â€šÂ¬Ã‚Â), show output, then stop. Point to `langgraph-fundamentals` for next steps. For a higher-level agent API, use LangChain `create_agent` instead.
