# Prompt Frameworks & How to Pick One

Frameworks are recipes: they force you to include the elements a great prompt
needs. Use them to build the **Master Spec** in SKILL.md. You don't need all of
them - pick the best fit, or merge. Default to **GRASP+Q** for interactive work
and **CRAFT(+C)** for reusable task templates.

---

## GRASP + Q  (best default for interactive requests)
- **G - Goal:** the outcome you want.
- **R - Role:** who the AI should act as (expertise + priorities).
- **A - Additional context:** background, audience, constraints-source, assets.
- **S - Structure:** exact format/look-and-feel of the output.
- **P - Parameters:** rules & limits (length, accuracy, cited sources, do-nots).
- **+ Q - Clarifying question:** end with "Before responding, ask me any
  clarifying questions until you're confident you can give a correct answer."
Write each part in natural language (as if briefing a colleague), not keywords.

## CRAFT (+C)  (best for reusable, general-purpose task templates)
- **C - Context** | **R - Role** | **A - Action (what you want)** | **F/T - Format (how the output should look)** | **+ C - Constraints / negative prompting.**
Great for code review, analysis, marketing copy. Keep 2-3 CRAFT templates on hand and adapt per task. Optionally add "think step by step" for reasoning tasks.

## CO-STAR  (great for content/marketing/comms)
- **C - Context | O - Objective | S - Style | T - Tone | A - Audience | R - Response (format).**

## Google "prompting essentials" - TCREI  (mnemonic: Tiny Crabs Ride Enormous Iguanas)
- **T - Task** (include a **Persona** and **Format**) | **C - Context** (more is better) | **R - References** (examples) | **E - Evaluate** (is this what I wanted?) | **I - Iterate** (ABI: always be iterating).
**Four iteration moves** (mnemonic: Ramen Saves Tragic Idiots):
1. **Revisit** the framework (add role/context/references).
2. **Separate** a long prompt into shorter sentences / feed step by step.
3. **Try different phrasing** or an analogous task.
4. **Introduce constraints** to narrow focus.

## RTF / CREATE  (quick vs. rich)
- **RTF - Request, Task, Format:** fast, lightweight, everyday tasks.
- **CREATE - Character, Request, Examples, Adjustments, Type of output, Extras:** richer, when detail matters.

---

## The five-step operating loop (wrap any framework in this)
**Task -> Context -> References -> Evaluate -> Iterate.** Start simple, then
layer role + context + references until the Evaluate check passes. Rarely one-shot.

---

## How to choose

| Situation | Use |
|---|---|
| Underspecified interactive request | GRASP+Q |
| Reusable template you'll run often (code review, analysis, copy) | CRAFT(+C) |
| Marketing / content / comms with a clear audience & tone | CO-STAR |
| Teaching users a repeatable habit / general everyday tasks | Google TCREI |
| Quick one-off | RTF |
| Rich, high-detail deliverable | CREATE |
| Reasoning-heavy (debug, plan, math, root-cause) | any + Chain of Thought |
| Big/ambiguous build | any + decomposition/chaining, ToT for key choices |

Whatever you pick, the non-negotiable elements are: **Role, Goal+success
criteria, Context, Format, Constraints, and either Clarification or stated
Assumptions.**
