# Shared principles

Apply to all sections; read before reviewing.

## 0. A paper tests hypotheses

- The reader should be able to say: what hypothesis this paper tests, and which one each experiment tests.
- Order by importance, not by the history of the research ("first tried A and failed, then tried B").

## 1. Claims and evidence

- Every claim must point to evidence: a number, table, citation, or derivation. If none can be found, add evidence, or weaken or delete the claim.
- "Adding A raises the score" is not the same as "A causes the increase"; an ablation that removes only A is required.
- Results hold only in the settings tested: effective on 3 datasets cannot be written as effective on all kinds of data.

## 2. Wording strength matches evidence strength

| Content | Tone | Verbs |
|---|---|---|
| Measured results | Assertive | achieves, reduces, outperforms, shows |
| Interpretation beyond the data | Hedged | suggests, indicates, is consistent with |

- Do not mix the two tones in the same clause.
- Do not write measured results as may / seems; do not write speculation as fact (the experiment only measures accuracy, yet writes proves the model learns semantics).
- Do not over-hedge: main conclusions with clear evidence use assertive sentences; hedging is reserved for explanations where the gap is smaller than the standard deviation, the result holds only in some settings, or there is no control experiment. When rewriting, do not weaken assertive sentences that have sufficient evidence.

## 3. Exaggerated wording

Mark on sight and replace with numbers or mechanisms:
- Novelty: novel (without saying what is new), innovative, pioneering, revolutionary, paradigm shift
- Performance: superior, remarkable, unprecedented, significantly (without a test), state-of-the-art (without saying which benchmark)
- Empty phrases: pave the way for, highlight the potential of, extensive experiments, comprehensive analysis
- We are the first to: must be verified. We solve X: usually only an improvement; write improve and the magnitude.

Mark notably, underscore, and reveal only when repeated many times or when they carry no substance. See word-bank.md for alternatives.

## 4. Consistent terminology

- One thing has one name throughout the paper (modules, methods, datasets, metrics, adjectives all count). Example: the abstract calls it lift and the method calls it map; readers will think they are two different things.
- One symbol or one noun denotes only one thing; not even within the same paragraph may a word have two meanings (source referring to both the data source and the source model). If a distinction is needed, give it another name.
- Define abbreviations and symbols on first appearance.

## 5. Paragraphs

- The first sentence states the point; reading only the first sentence of each paragraph reveals the argument of the whole section. If it cannot preview what follows, split the paragraph.
- The next sentence picks up what the end of the previous sentence mentioned; several consecutive sentences with unrelated subjects read like a bulleted list.
- Connectives mean what they say: However introduces a contrast, Consequently a result, Specifically a detail.
- The same paragraph opening (To test whether, To evaluate, In this section) appears no more than twice in the whole paper.
- A summary sentence draws a conclusion only once: it does not restate the previous sentence in the same paragraph, and the end of a subsection does not restate conclusions each paragraph already drew (common: every paragraph has Overall ..., and the subsection adds In summary ...).

## 6. Sentences

- Verbs state the operation: when utilize, leverage, adopt, or consider is the main verb, replace it with something like encode, project, weight, mask, sample.
- Replace adjectives with measurable properties: high efficiency → reduces inference time by 40%.
- The claim must survive after the metaphor is removed.
- Do not start every sentence with we: use we for design decisions, the method name for capabilities, the module name for mechanisms.
- Follow this with a noun: This misalignment leads to ...
- Comparisons state the target: higher accuracy than X.
- When three or more nouns are stacked, break them up with prepositions.

## 7. Common English errors

- Singular countable nouns need an article: propose a method.
- Tense: present for the method, past for the experimental procedure, consistent within the same section when citing prior work.
- Use that for restrictive clauses, which for non-restrictive (with a comma).
- A comma cannot join two independent clauses.
- One main idea per sentence.
- Use active voice for important sentences.

## 8. Issue severity levels

| Level | Meaning | Examples |
|---|---|---|
| Must fix | Will be rejected if not fixed, or violates academic ethics | Claim without evidence, contribution not found in experiments, inconsistent numbers, suspected copying |
| Should fix | Reviewers will likely raise it in the first round | Multiple exaggerated phrases, missing topic sentences, inconsistent terminology, incomplete ablation |
| Could fix | Writing quality | Sentences too long, article errors, repeated wording |

Personal stylistic preferences do not constitute must fix.
