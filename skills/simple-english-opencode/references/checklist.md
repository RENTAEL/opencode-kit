# Verification checklist

Run after drafting. Ordered from mechanical to judgment.

## Mechanical (searchable)

Every hit outside code and quoted text is a problem.

| Search                                                                 | Problem               | Fix                                     |
| ---------------------------------------------------------------------- | --------------------- | --------------------------------------- |
| `utilize`, `leverage`, `facilitate`                                    | corporate filler      | use / help / enable                     |
| `simply`, `just`, `easily`, `seamlessly`, `effortlessly`               | empty intensifier     | delete                                  |
| `robust`, `powerful`, `comprehensive`, `performant`, `seamless`        | empty adjective       | delete or give a number from the source |
| `in order to`, `due to the fact that`, `prior to`, `in the event that` | padded phrase         | to / because / before / if              |
| `has been`, `have been`, `had been`                                    | perfect-tense padding | simple past or simple present           |
| `is being`, `are being`, `was being`                                   | progressive passive   | active, simple tense                    |
| `, making`, `, allowing`, `, enabling`, `, ensuring`                   | dangling -ing clause  | new sentence with a subject             |
| `should`, `would`, `may`, `might`, `could`                             | soft hedge            | must / can / fact / delete              |
| `;`                                                                    | semicolon             | two sentences                           |
| `Let's dive`, `In this article`, `In conclusion`, `Great question`     | AI scaffolding        | delete                                  |
| mid-sentence `if` / `when` in procedures                               | trailing condition    | move condition to the start             |

## Countable

1. Sentence length: procedural max 20 words; descriptive max 25.
2. Paragraph size: max 6 sentences; one topic.
3. Noun chains: max 3 words; break longer ones with of/on/in/for.
4. Instructions per sentence: one (unless simultaneous).

## Judgment

5. Classification: procedural vs descriptive cleanly split.
6. Voice: passive only when actor unknown or formal-spec object focus.
7. Vocabulary lock: one term for check/verify/confirm; one for config/settings.
8. Untouchables: code, paths, product names, quoted errors unchanged.
9. No invented facts: cuts only; never add metrics the source lacked.
10. Output shape: Rewrite/Check format matched exactly.
