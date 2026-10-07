
## Domain docs
- Before exploring or writing, read `GLOSSARY.md` (project terms and notation) and the ADRs in `{{DOCS_DIR}}/adr/` that touch the area you are working in. If they do not exist yet, proceed silently: they are created only when the first term or decision is settled.
- Use the glossary's terms and symbols in code, docs and paper text; do not drift to the synonyms it lists under _Avoid_. A concept missing from the glossary is either new language the project does not use (reconsider) or a real gap (add it).
- If your work contradicts an ADR, say so explicitly instead of silently overriding it: _Contradicts ADR-0003 (test split), but worth reopening because…_
- When a term or a decision is settled, write it down; the formats are in [{{DOCS_DIR}}/AGENTS.md]({{DOCS_DIR}}/AGENTS.md) under `## ADRs and glossary`.
