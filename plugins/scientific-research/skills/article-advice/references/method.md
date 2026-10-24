# Method

## The questions this section answers

1. Can the method be reproduced from this section alone?
2. What is the reason for each design?
3. Why does it work?

## Common structure

**Threat model or application scenario** (security, watermarking, privacy, forensics papers): before the overview, name the parties (provider, legitimate user, adversary), what each can access, what the adversary may do, and the success criterion for each scenario as a formula (detection: S(s', s) >= tau at a fixed FPR; tracing: argmax_i S(s', s_i)). Avoid absolute wording for statistical decisions (incontrovertible proof).

**Overview subsection**: task setting (input, output) → core contribution → point to the architecture figure (when the pipeline is new) → one sentence per following subsection on what it covers.

**Cross-references**: cite another section in a full sentence (Section 3.3 defines the views). Parenthetical section numbers belong to the introduction.

**One subsection per module**, in data-flow order, each containing three elements:

| Element | Content | Common opening |
|---|---|---|
| Motivation | Because there is problem X, design Y | A remaining challenge is ... |
| Design | First define the key structure, then write input → steps → output in order | Given [input], we first ... then ... |
| Advantage | Why it is better than alternatives | Compared with ..., this ... |

**Implementation details** (number of layers, dimensions, hyperparameters) go at the end or in a separate subsection, not interleaved with module design.

**Equations**: follow with a where clause defining new symbols, then one sentence explaining what it does (e.g., minimizing this term pushes features of the same class closer together).

**Dimensions**: state a tensor's symbolic size as set membership where it is introduced ($f_\theta(\tilde X)\in\mathbb{R}^{N\times T\times D}$), without the batch dimension. In prose, describe an operation by what it does (pools the $C$ channel tokens at each position into one vector), not as a shape mapping (maps B×L×C×D to B×L×D). A function signature such as $g:\mathbb{R}^{C\times D}\to\mathbb{R}^{D}$ is fine. Do not copy shape annotations from code or a glossary. Numeric sizes stay in implementation details.

## Checklist

- [ ] Motivation starts from the problem, not a restatement of the design ("use X because we need X" does not count); motivation and design are written separately
- [ ] Advantages are linked to measurable results, or marked as still needing experimental support; effect claims without experimental support are changed into design intent
- [ ] Symbols are not mixed with symbols from prior papers
- [ ] Every numbered equation is referenced in the body text
- [ ] Tensor sizes are set membership, operations are prose (Dimensions). Search for `shape` and `形狀`, and check each hit
- [ ] Cross-references are full sentences, not parenthetical numbers (Cross-references). Search for `(Section` and `（第`, and check each hit
- [ ] Components with nothing new are covered briefly; "why not use other methods" goes in related work or ablation
- [ ] Information is sufficient for reproduction; missing parts are listed
- [ ] Security-style papers: every attack in the experiments maps to a capability in the threat model, and every listed capability is tested or explicitly out of scope

## Rewrite example

- Original (the user has defined positive and negative samples elsewhere): We adopt a contrastive loss to make the features better.
- Rewrite: We apply a contrastive loss that pulls together features of augmented views from the same image and pushes apart those from different images.
- Explanation: adopt is replaced with an operational verb, better with concrete behavior.
