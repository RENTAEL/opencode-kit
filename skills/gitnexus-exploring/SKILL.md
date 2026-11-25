---
name: gitnexus-exploring
description: "1. READ gitnexus://repos ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Discover indexed repos 2. READ gitnexus://repo/{name}/context ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Codebase overview, check staleness 3. gitnexus_query({query: \"<what you want to understand>\"}) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Find related execution flows 4. git..."
---
# Exploring Codebases with GitNexus

## When to Use

- "How does authentication work?"
- "What's the project structure?"
- "Show me the main components"
- "Where is the database logic?"
- Understanding code you haven't seen before

## Workflow

```
1. READ gitnexus://repos                          ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Discover indexed repos
2. READ gitnexus://repo/{name}/context             ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Codebase overview, check staleness
3. gitnexus_query({query: "<what you want to understand>"})  ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Find related execution flows
4. gitnexus_context({name: "<symbol>"})            ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Deep dive on specific symbol
5. READ gitnexus://repo/{name}/process/{name}      ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Trace full execution flow
```

> If step 2 says "Index is stale" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ run `npx gitnexus analyze` in terminal.

## Checklist

```
- [ ] READ gitnexus://repo/{name}/context
- [ ] gitnexus_query for the concept you want to understand
- [ ] Review returned processes (execution flows)
- [ ] gitnexus_context on key symbols for callers/callees
- [ ] READ process resource for full execution traces
- [ ] Read source files for implementation details
```

## Resources

| Resource                                | What you get                                            |
| --------------------------------------- | ------------------------------------------------------- |
| `gitnexus://repo/{name}/context`        | Stats, staleness warning (~150 tokens)                  |
| `gitnexus://repo/{name}/clusters`       | All functional areas with cohesion scores (~300 tokens) |
| `gitnexus://repo/{name}/cluster/{name}` | Area members with file paths (~500 tokens)              |
| `gitnexus://repo/{name}/process/{name}` | Step-by-step execution trace (~200 tokens)              |

## Tools

**gitnexus_query** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â find execution flows related to a concept:

```
gitnexus_query({query: "payment processing"})
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Processes: CheckoutFlow, RefundFlow, WebhookHandler
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Symbols grouped by flow with file locations
```

**gitnexus_context** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â 360-degree view of a symbol:

```
gitnexus_context({name: "validateUser"})
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Incoming calls: loginHandler, apiMiddleware
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Outgoing calls: checkToken, getUserById
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Processes: LoginFlow (step 2/5), TokenRefresh (step 1/3)
```

## Example: "How does payment processing work?"

```
1. READ gitnexus://repo/my-app/context       ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ 918 symbols, 45 processes
2. gitnexus_query({query: "payment processing"})
   ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ CheckoutFlow: processPayment ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ validateCard ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ chargeStripe
   ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ RefundFlow: initiateRefund ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ calculateRefund ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ processRefund
3. gitnexus_context({name: "processPayment"})
   ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Incoming: checkoutHandler, webhookHandler
   ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Outgoing: validateCard, chargeStripe, saveTransaction
4. Read src/payments/processor.ts for implementation details
```
