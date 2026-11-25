---
name: react-key-prop
description: "Covers key prop reconciliation, component architecture, performance patterns, and hooks conventions."
---
# React Best Practices

Covers key prop reconciliation, component architecture, performance patterns, and hooks conventions.

## When to Use

- Reviewing React components that render lists with `.map()`
- Troubleshooting stale state, incorrect reordering, or unnecessary remounts
- Evaluating component architecture and composition patterns
- Checking hooks rule compliance in code review
- Onboarding developers to React reconciliation behavior

---

## Core Principle

**Keys must be stable, unique, and predictable.** They tell React how to match elements between renders during reconciliation.

```typescript
// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Good: stable, unique, predictable
items.map((item) => <ListItem key={item.id} item={item} />);

// ÃƒÂ¢Ã‚ÂÃ…â€™ Bad: unstable, changes every render
items.map((item, index) => <ListItem key={index} item={item} />);

// ÃƒÂ¢Ã‚ÂÃ…â€™ Bad: non-unique
items.map((item) => <ListItem key={item.type} item={item} />);

// ÃƒÂ¢Ã‚ÂÃ…â€™ Bad: random ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â causes full remount every render
items.map((item) => <ListItem key={Math.random()} item={item} />);
```

---

## The Index-as-Key Anti-Pattern

Using array index as key is the most common React key bug.

### When it breaks

| Scenario | Effect |
|----------|--------|
| Items reordered | React reuses wrong component instances ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â state, refs, and DOM attached to wrong items |
| Items inserted/deleted at start | All subsequent indices shift ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â every component remounts or gets wrong state |
| List is filtered | Same index shift problem |
| Items have local state (inputs, checkboxes) | State persists on wrong elements ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â user sees stale/incorrect data |

### When it's acceptable (rare)

- Static list that never changes order or length
- Items have no local state, refs, or side effects
- List is read-only display (no inputs, no animations)

```typescript
// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Acceptable: static, read-only, never changes
const DAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri'];
days.map((day, i) => <span key={i}>{day}</span>);
```

---

## Stable Key Sources

| Source | Stable? | Notes |
|--------|---------|-------|
| Database ID (`item.id`) | ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Yes | Best choice ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â unique, stable, persistent |
| UUID generated at creation | ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Yes | Good for optimistic UI before server response |
| Content hash | ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Yes | Works when no ID exists ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â hash of item content |
| Array index | ÃƒÂ¢Ã‚ÂÃ…â€™ No | Breaks on reorder/insert/delete |
| `Math.random()` | ÃƒÂ¢Ã‚ÂÃ…â€™ No | Changes every render ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â full remount |
| `Date.now()` | ÃƒÂ¢Ã‚ÂÃ…â€™ No | Changes every render ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â full remount |
| `crypto.randomUUID()` | ÃƒÂ¢Ã‚ÂÃ…â€™ No | Changes every render ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â full remount |

---

## Key Placement

Keys belong on the **element returned from `.map()`**, not on nested children:

```typescript
// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Correct: key on the outermost returned element
items.map((item) => (
  <div key={item.id}>
    <ListItem item={item} />
  </div>
));

// ÃƒÂ¢Ã‚ÂÃ…â€™ Wrong: key on a child, not the map return
items.map((item) => (
  <div>
    <ListItem key={item.id} item={item} />
  </div>
));

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Correct: key on Fragment shorthand (<> doesn't accept key)
items.map((item) => (
  <React.Fragment key={item.id}>
    <dt>{item.term}</dt>
    <dd>{item.def}</dd>
  </React.Fragment>
));
```

### Key on custom components

Keys are **not** passed as props ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â they're internal to React's reconciliation:

```typescript
function ListItem({ item }: { item: Item }) {
  // ÃƒÂ¢Ã‚ÂÃ…â€™ Can't access props.key ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â it's reserved
  return <div>{item.name}</div>;
}

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Key is set on the JSX element, not inside the component
items.map((item) => <ListItem key={item.id} item={item} />);
```

---

## Reconciliation Behavior

| Key change | React behavior |
|------------|----------------|
| Same key, same position | Re-render (update existing instance) |
| Same key, different position | Move (reorder DOM nodes, preserve state) |
| Different key | Unmount old, mount new (reset all state) |
| Key removed | Unmount (destroy state, refs, effects) |

---

## Common Pitfalls

### 1. Using `key` to force remount

Sometimes you want a fresh component instance (e.g., resetting a form):

```typescript
// Remounts UserForm when userId changes ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â resets all internal state
<UserForm key={userId} userId={userId} />
```

### 2. Non-unique keys from partial data

```typescript
// ÃƒÂ¢Ã‚ÂÃ…â€™ Bad: type is not unique across items
items.map((item) => <Item key={item.type} />);

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Good: combine with another field
items.map((item) => <Item key={`${item.type}-${item.id}`} />);
```

### 3. Key on Fragment shorthand

```typescript
// ÃƒÂ¢Ã‚ÂÃ…â€™ Syntax error: <> doesn't accept key
items.map((item) => (
  < key={item.id}>  {/* ÃƒÂ¢Ã‚ÂÃ…â€™ */}
    <dt>{item.term}</dt>
    <dd>{item.def}</dd>
  </>
));

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ Use React.Fragment
items.map((item) => (
  <React.Fragment key={item.id}>
    <dt>{item.term}</dt>
    <dd>{item.def}</dd>
  </React.Fragment>
));
```

### 4. Key on array of primitives

```typescript
// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ React uses the value itself as key for primitives
const numbers = [1, 2, 3];
numbers.map((n) => <li>{n}</li>);
// React internally uses the value as key when none is provided
// But explicit key is still better for clarity
```

---

## Quick Reference

```typescript
// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ DO: stable unique ID
items.map((item) => <Item key={item.id} item={item} />);

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ DO: content hash when no ID
items.map((item) => <Item key={hashContent(item)} item={item} />);

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ DO: composite key when needed
items.map((item) => <Item key={`${item.type}-${item.seq}`} item={item} />);

// ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ DO: key on Fragment for multiple elements
items.map((item) => (
  <React.Fragment key={item.id}>
    <ChildA item={item} />
    <ChildB item={item} />
  </React.Fragment>
));

// ÃƒÂ¢Ã‚ÂÃ…â€™ DON'T: array index (unless static read-only list)
items.map((item, i) => <Item key={i} item={item} />);

// ÃƒÂ¢Ã‚ÂÃ…â€™ DON'T: random/date keys
items.map((item) => <Item key={Math.random()} item={item} />);

// ÃƒÂ¢Ã‚ÂÃ…â€™ DON'T: key on child instead of map return
items.map((item) => (
  <div>
    <Item key={item.id} item={item} />
  </div>
));
```

---

## Component Composition Patterns

### Props vs Children

| Pattern | Use When | Example |
|---------|----------|---------|
| **Props** | Data-driven, known shape | `<Card title={t} body={b} />` |
| **Children** | Flexible layout, unknown content | `<Card><p>Any JSX</p></Card>` |
| **Render props** | Shared logic, varying render | `<DataProvider render={data => <View {...data} />} />` |

### Controlled vs Uncontrolled

```typescript
// Controlled ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â state managed by parent
function Input({ value, onChange }: { value: string; onChange: (v: string) => void }) {
  return <input value={value} onChange={e => onChange(e.target.value)} />;
}

// Uncontrolled ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â state managed internally via ref
function FileInput() {
  const ref = useRef<HTMLInputElement>(null);
  return <input ref={ref} type="file" />;
}
```

**Rule:** Prefer controlled for form inputs. Use uncontrolled for file inputs, media playback, and third-party DOM interop.

### Lifting State Up

Duplicate or derived state across siblings ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ lift to the nearest common ancestor:

```typescript
function Parent() {
  const [selectedId, setSelectedId] = useState<string | null>(null);
  return (
    <>
      <List onSelect={setSelectedId} />
      <Detail id={selectedId} />
    </>
  );
}
```

---

## Hooks Rules & Patterns

### Rules of Hooks

1. **Only call hooks at the top level** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â not inside conditions, loops, or callbacks
2. **Only call hooks from React functions** ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â components or custom hooks, not regular JS functions

### Common Custom Hooks

```typescript
// Debounced value
function useDebounce<T>(value: T, delay: number): T {
  const [debounced, setDebounced] = useState(value);
  useEffect(() => {
    const id = setTimeout(() => setDebounced(value), delay);
    return () => clearTimeout(id);
  }, [value, delay]);
  return debounced;
}

// Toggle
function useToggle(initial = false) {
  return useReducer(state => !state, initial);
}
```

### Effect Cleanup

Every `useEffect` that subscribes, sets intervals, or starts async work MUST return a cleanup:

```typescript
useEffect(() => {
  const sub = source.subscribe(data => setData(data));
  return () => sub.unsubscribe(); // ÃƒÂ¢Ã…â€œÃ¢â‚¬Â¦ cleanup
}, [source]);
```

Missing cleanup ÃƒÂ¢Ã¢â‚¬Â Ã¢â‚¬â„¢ memory leaks, stale closures, duplicate subscriptions on StrictMode re-mounts.

---

## Performance Patterns

| Pattern | Problem | Solution |
|---------|---------|----------|
| `React.memo` | Unnecessary re-renders of pure presentational components | Wrap leaf components with stable props |
| `useMemo` | Expensive computations re-running | Memoize derived data |
| `useCallback` | Callback identity changing every render | Stable function reference for memo children |
| Lazy loading | Large component bundles | `React.lazy(() => import('./BigComponent'))` |

```typescript
// Before: re-renders on every parent render
function ExpensiveList({ items }: { items: Item[] }) { /* ... */ }

// After: skips re-render if items reference hasn't changed
const ExpensiveList = React.memo(function ExpensiveList({ items }: { items: Item[] }) {
  return /* ... */;
});
```
