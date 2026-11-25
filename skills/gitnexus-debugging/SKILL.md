---
name: gitnexus-debugging
description: "1. gitnexus_query({query: \"<error or symptom>\"}) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Find related execution flows 2. gitnexus_context({name: \"<suspect>\"}) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ See callers/callees/processes 3. READ gitnexus://repo/{name}/process/{name} ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Trace execution flow 4..."
---
# Debugging with GitNexus

## When to Use

- "Why is this function failing?"
- "Trace where this error comes from"
- "Who calls this method?"
- "This endpoint returns 500"
- Investigating bugs, errors, or unexpected behavior

## Workflow

```
1. gitnexus_query({query: "<error or symptom>"})            ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Find related execution flows
2. gitnexus_context({name: "<suspect>"})                    ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ See callers/callees/processes
3. READ gitnexus://repo/{name}/process/{name}                ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Trace execution flow
4. gitnexus_cypher({query: "MATCH path..."})                 ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Custom traces if needed
```

> If "Index is stale" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ run `npx gitnexus analyze` in terminal.

## Checklist

```
- [ ] Understand the symptom (error message, unexpected behavior)
- [ ] gitnexus_query for error text or related code
- [ ] Identify the suspect function from returned processes
- [ ] gitnexus_context to see callers and callees
- [ ] Trace execution flow via process resource if applicable
- [ ] gitnexus_cypher for custom call chain traces if needed
- [ ] Read source files to confirm root cause
```

## Debugging Patterns

| Symptom              | GitNexus Approach                                          |
| -------------------- | ---------------------------------------------------------- |
| Error message        | `gitnexus_query` for error text ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ `context` on throw sites |
| Wrong return value   | `context` on the function ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ trace callees for data flow    |
| Intermittent failure | `context` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ look for external calls, async deps            |
| Performance issue    | `context` ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ find symbols with many callers (hot paths)     |
| Recent regression    | `detect_changes` to see what your changes affect           |

## Tools

**gitnexus_query** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â find code related to error:

```
gitnexus_query({query: "payment validation error"})
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Processes: CheckoutFlow, ErrorHandling
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Symbols: validatePayment, handlePaymentError, PaymentException
```

**gitnexus_context** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â full context for a suspect:

```
gitnexus_context({name: "validatePayment"})
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Incoming calls: processCheckout, webhookHandler
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Outgoing calls: verifyCard, fetchRates (external API!)
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Processes: CheckoutFlow (step 3/7)
```

**gitnexus_cypher** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â custom call chain traces:

```cypher
MATCH path = (a)-[:CodeRelation {type: 'CALLS'}*1..2]->(b:Function {name: "validatePayment"})
RETURN [n IN nodes(path) | n.name] AS chain
```

## Example: "Payment endpoint returns 500 intermittently"

```
1. gitnexus_query({query: "payment error handling"})
   ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Processes: CheckoutFlow, ErrorHandling
   ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Symbols: validatePayment, handlePaymentError

2. gitnexus_context({name: "validatePayment"})
   ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Outgoing calls: verifyCard, fetchRates (external API!)

3. READ gitnexus://repo/my-app/process/CheckoutFlow
   ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Step 3: validatePayment ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ calls fetchRates (external)

4. Root cause: fetchRates calls external API without proper timeout
```
