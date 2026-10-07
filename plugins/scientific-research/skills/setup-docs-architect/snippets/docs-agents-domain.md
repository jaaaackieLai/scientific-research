
## ADRs and glossary
- `adr/` and `papers/` hold Markdown for agents and readers of the repository; they are not Astro pages and are not converted. The project glossary is `GLOSSARY.md` at the repository root.
- Create both lazily: `GLOSSARY.md` when the first term is settled, `adr/` when the first decision needs recording. Never commit empty placeholders.

### ADRs (`adr/`)
- One file per decision: `adr/0001-<slug>.md`, numbered by taking the highest existing number plus one.
- Write one only when all three hold: changing it later is costly (past results would have to be rerun, or a lot of code rewritten); a future reader would be surprised without the context; there was a real alternative and it was rejected for a specific reason.
- Typical research decisions: evaluation protocol and metric definitions, data splits and preprocessing, a baseline run with settings that differ from its paper or official code, seed and reporting policy (mean ± std over how many runs), compute or license constraints that rule options out, and approaches tried and dropped for a non-obvious reason.
- Not ADRs: easy-to-reverse choices (you will just reverse them), the obvious default, and hyperparameter values (they belong in configs and result files).
- Template; a single paragraph is enough:
  ```md
  # <Short title of the decision>

  <1-3 sentences: the context, what was decided, and why.>
  ```
- Optional, only when they add something: a `Status:` line (`proposed | accepted | deprecated | superseded by ADR-NNNN`), `## Considered options` when the rejected ones are worth remembering, `## Consequences` when the downstream effects are not obvious (e.g. which results tables become stale).
- Do not edit a superseded ADR's decision; write a new ADR and mark the old one `superseded by ADR-NNNN`.

### Glossary (`GLOSSARY.md` at the repository root)
- Only terms specific to this project (the method and its variants, model roles, data and metric names); not general ML vocabulary.
- Be opinionated: pick one term per concept and list the rejected synonyms under _Avoid_. Definitions say what the thing is, in one or two sentences.
- `## Notation` maps each symbol to its meaning and to its name in code, so papers, docs and code use the same symbols.
- Template:
  ```md
  # <Project name>

  <One or two sentences on what the project studies.>

  ## Language

  **Teacher model**:
  The frozen pretrained model whose outputs supervise the student.
  _Avoid_: oracle, base model

  ## Notation

  | Symbol | Meaning | In code |
  |---|---|---|
  | $x_t$ | input at step $t$ | `x[:, t]` |
  ```
