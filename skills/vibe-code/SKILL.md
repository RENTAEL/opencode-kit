---
name: vibe-code
description: "Conversational rapid prototyping. Describe what you want in natural language, get a working prototype fast, then iterate through conversational feedback rounds. Low ceremony, high velocity ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the goal is to get something working and refine it through dialogue."
---
# Vibe Code

Conversational rapid prototyping. Describe what you want in natural language, get a working prototype fast, then iterate through conversational feedback rounds. Low ceremony, high velocity ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the goal is to get something working and refine it through dialogue.

## When to Use

- Rapid prototyping ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "I want an app that does X, build it"
- Exploring ideas where the requirements aren't fully known upfront
- Building MVPs and proof-of-concepts quickly
- When you want to iterate through conversation rather than written specs
- Hackathon-style development where speed matters more than architecture

**Do not use when:**
- Building production-grade software with strict quality requirements ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use `plan-execute` or `tdd` instead
- Working on an existing codebase with established conventions ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use `brownfield` instead
- The task requires security hardening, comprehensive testing, or formal verification ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â use `harden` or `pipeline` instead
- Requirements are well-understood and stable ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â a structured approach will be more efficient

## Workflow

### Phase 1: Understand the Vision

1. Ask clarifying questions to understand what the user wants to build
2. Identify the key features and user flows
3. Determine the tech stack (or suggest one based on the description)
4. Set expectations: "I'll build a working prototype first, then we can iterate"

**Key questions to ask:**
- What does the app do? (core functionality)
- Who is the user? (target audience)
- What's the most important thing it needs to do? (MVP scope)
- Any preferences for tech stack, design, or platform?

### Phase 2: Build the Prototype

1. Scaffold the project with minimal configuration
2. Build the core feature first ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the one thing the app must do
3. Use familiar, productive frameworks (Next.js, Express, FastAPI, etc.)
4. Keep it simple ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â no premature abstractions, no over-engineering
5. Add basic styling ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â enough to be presentable, not pixel-perfect
6. Make it runnable ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â the user should be able to see/use it

**Building principles:**
- **Speed over perfection**: Get something working, then refine
- **Single-file prototypes**: When appropriate, keep things in fewer files for faster iteration
- **Working > complete**: A working prototype with 80% of features is better than a half-built perfect architecture
- **No tests in phase 2**: Tests come after the prototype is validated (if at all)

### Phase 3: Present & Get Feedback

1. Show the user what was built
2. Ask specific questions:
   - "Does this do what you wanted?"
   - "What should change?"
   - "What's missing?"
   - "What don't you like?"
3. Listen for both explicit requests and implicit direction

### Phase 4: Iterate

1. Apply the feedback ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â one round of changes at a time
2. Keep each iteration focused on the user's latest feedback
3. After each iteration, present the updated version
4. Ask: "What next? Anything to change, add, or remove?"

**Iteration principles:**
- One feedback round at a time ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't anticipate future requests
- Small, fast iterations ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â each cycle should take minutes, not hours
- Preserve what works ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â don't rewrite working features unless the user asks
- Say no when appropriate ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â "That would add significant complexity, here's a simpler alternative..."

### Phase 5: Harden (Optional, When Ready)

When the prototype is validated and the user wants to productionize:

1. Add error handling and edge case coverage
2. Add basic tests for critical paths
3. Improve code organization (extract components, add types)
4. Run `@security-reviewer` for a basic security check
5. Add documentation (README, API docs)

## Communication Style

- **Casual and conversational**: Use natural language, not formal specs
- **Show, don't just tell**: Demonstrate working functionality
- **Offer choices**: "We could do it this way or that way ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â which do you prefer?"
- **Be honest about tradeoffs**: "This approach is faster but less maintainable long-term"
- **Celebrate progress**: "Here's what we built ÃƒÂ¢Ã¢â€šÂ¬Ã¢â‚¬Â pretty cool, right?"

## Constraints

- **No over-engineering**: Do not add abstractions, patterns, or features that weren't requested. The goal is a working prototype, not a perfect architecture.
- **No premature optimization**: Do not optimize for scale, performance, or maintainability unless the user asks. Those come later.
- **Keep it runnable**: After every change, the app should still work. Never leave the prototype in a broken state.
- **One iteration at a time**: Apply one round of feedback before asking for the next. Do not batch multiple unrequested improvements.
- **Know when to stop**: Vibe code is for prototyping. When the prototype is validated, transition to a structured approach (plan-execute, tdd, harden) for production work.

## Reminder

Conversational rapid prototyping.
