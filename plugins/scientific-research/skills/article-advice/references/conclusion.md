# Conclusion

## The question this section answers

For a reader who has read the whole paper, explain: what this paper establishes, which piece of evidence is strongest, and what remains unsolved.

The conclusion is not the abstract: it does not reintroduce background or restate experimental results.

## Common structure

Problem and core idea (same wording as the abstract and introduction) → strongest evidence (concrete numbers or datasets) → impact or new insight → limitations → concrete future directions.

## Classify limitations

| Type | Criterion | How to write |
|---|---|---|
| Scope | Limited by the task setting (data, assumptions, deployment conditions), but still competitive within the setting | Write it as a natural boundary: currently only validated on short sequences |
| Technical flaw | Loses to strong baselines on important metrics, or has an unacceptable cost | Must be stated directly |

Classify by the experimental numbers, not by how the author would like to phrase it. Packaging a technical flaw as a scope limitation is the most damaging problem for credibility.

When the submission venue requires a separate Limitations section (e.g., NeurIPS, ICLR), keep only one sentence in the conclusion.

## Checklist

- [ ] Evidence sentences have concrete numbers or datasets, but detailed conditions stay in the experiments section
- [ ] Each limitation is classified and matches the experimental numbers
- [ ] Says which hypotheses were confirmed or overturned, and what that means for the field
- [ ] No sentences repeated verbatim from the abstract
- [ ] No claims unsupported by the body text (e.g., data efficiency with no data-scaling experiment)
- [ ] Future directions are concrete (not We will explore more applications)
- [ ] The last sentence states significance or a concrete next step, not a soft ending like we hope this work draws attention to
- [ ] Tense is present perfect (we have shown) or present
- [ ] Every weakness stated in the experiments or appendix (vulnerable, fails, drops; e.g., 9 points below the best baseline on one distortion family) also appears in the Limitations section or conclusion
- [ ] The Limitations section neither opens nor closes with praise (Despite its wonderful performance ...; our work represents a significant advancement)

## Rewrite example

- Original: In the future, we will apply our method to more tasks.
- Rewrite (the user's experiments only cover sequences up to 512): Our experiments are limited to sequences shorter than 512 tokens; extending the memory module to longer contexts is a natural next step.
- Explanation: connects a vague future direction to a concrete scope limitation.
