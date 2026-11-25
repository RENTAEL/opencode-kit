---
name: gitnexus-refactoring
description: "1. gitnexus_impact({target: \"X\", direction: \"upstream\"}) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Map all dependents 2. gitnexus_query({query: \"X\"}) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Find execution flows involving X 3. gitnexus_context({name: \"X\"}) ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ See all incoming/outgoing refs 4. Plan upda..."
---
# Refactoring with GitNexus

## When to Use

- "Rename this function safely"
- "Extract this into a module"
- "Split this service"
- "Move this to a new file"
- Any task involving renaming, extracting, splitting, or restructuring code

## Workflow

```
1. gitnexus_impact({target: "X", direction: "upstream"})  ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Map all dependents
2. gitnexus_query({query: "X"})                            ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Find execution flows involving X
3. gitnexus_context({name: "X"})                           ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ See all incoming/outgoing refs
4. Plan update order: interfaces ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ implementations ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ callers ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ tests
```

> If "Index is stale" ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ run `npx gitnexus analyze` in terminal.

## Checklists

### Rename Symbol

```
- [ ] gitnexus_rename({symbol_name: "oldName", new_name: "newName", dry_run: true}) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â preview all edits
- [ ] Review graph edits (high confidence) and ast_search edits (review carefully)
- [ ] If satisfied: gitnexus_rename({..., dry_run: false}) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â apply edits
- [ ] gitnexus_detect_changes() ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â verify only expected files changed
- [ ] Run tests for affected processes
```

### Extract Module

```
- [ ] gitnexus_context({name: target}) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â see all incoming/outgoing refs
- [ ] gitnexus_impact({target, direction: "upstream"}) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â find all external callers
- [ ] Define new module interface
- [ ] Extract code, update imports
- [ ] gitnexus_detect_changes() ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â verify affected scope
- [ ] Run tests for affected processes
```

### Split Function/Service

```
- [ ] gitnexus_context({name: target}) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â understand all callees
- [ ] Group callees by responsibility
- [ ] gitnexus_impact({target, direction: "upstream"}) ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â map callers to update
- [ ] Create new functions/services
- [ ] Update callers
- [ ] gitnexus_detect_changes() ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â verify affected scope
- [ ] Run tests for affected processes
```

## Tools

**gitnexus_rename** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â automated multi-file rename:

```
gitnexus_rename({symbol_name: "validateUser", new_name: "authenticateUser", dry_run: true})
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ 12 edits across 8 files
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ 10 graph edits (high confidence), 2 ast_search edits (review)
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Changes: [{file_path, edits: [{line, old_text, new_text, confidence}]}]
```

**gitnexus_impact** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â map all dependents first:

```
gitnexus_impact({target: "validateUser", direction: "upstream"})
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ d=1: loginHandler, apiMiddleware, testUtils
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Affected Processes: LoginFlow, TokenRefresh
```

**gitnexus_detect_changes** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â verify your changes after refactoring:

```
gitnexus_detect_changes({scope: "all"})
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Changed: 8 files, 12 symbols
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Affected processes: LoginFlow, TokenRefresh
ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Risk: MEDIUM
```

**gitnexus_cypher** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â custom reference queries:

```cypher
MATCH (caller)-[:CodeRelation {type: 'CALLS'}]->(f:Function {name: "validateUser"})
RETURN caller.name, caller.filePath ORDER BY caller.filePath
```

## Risk Rules

| Risk Factor         | Mitigation                                |
| ------------------- | ----------------------------------------- |
| Many callers (>5)   | Use gitnexus_rename for automated updates |
| Cross-area refs     | Use detect_changes after to verify scope  |
| String/dynamic refs | gitnexus_query to find them               |
| External/public API | Version and deprecate properly            |

## Example: Rename `validateUser` to `authenticateUser`

```
1. gitnexus_rename({symbol_name: "validateUser", new_name: "authenticateUser", dry_run: true})
   ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ 12 edits: 10 graph (safe), 2 ast_search (review)
   ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Files: validator.ts, login.ts, middleware.ts, config.json...

2. Review ast_search edits (config.json: dynamic reference!)

3. gitnexus_rename({symbol_name: "validateUser", new_name: "authenticateUser", dry_run: false})
   ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Applied 12 edits across 8 files

4. gitnexus_detect_changes({scope: "all"})
   ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Affected: LoginFlow, TokenRefresh
   ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ Risk: MEDIUM ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â run tests for these flows
```
