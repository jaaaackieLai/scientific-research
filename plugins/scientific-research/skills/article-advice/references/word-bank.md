# Word bank

Basis: word usage statistics and reading of the main text of 10 example papers (list in "Sources" of writing-patterns.md).

Criterion: most of these words are not banned; rather, they carry no information when they appear alone. If replacing them with numbers or mechanisms makes the sentence concrete, suggest the change; if not, leave it. Good papers use these words too, but immediately followed by numbers, comparison targets, or mechanisms.

## A. Vague verbs

| Word | Suggestion |
|---|---|
| utilize | Change to use; when describing your own method, change to an operational verb |
| leverage | If kept, follow with to + a concrete action (leverage X to extract Y); otherwise change to an operational verb |
| adopt / employ | Fine when reusing someone else's off-the-shelf component (We adopt a frozen, pretrained text encoder); change to an operational verb when the object is something you designed |
| conduct / perform experiments | Change to say what is being tested: To verify that X is text-driven, we ... |

- Weak: SpineFL utilizes the activation information to wisely select neurons.
- Strong: SpineFL samples neurons with probability proportional to their historical activation, so that frequently activated neurons are more likely to be kept.

## B. Self-evaluating words

| Word | Suggestion |
|---|---|
| novel | Delete and state the difference: unlike X, our method ... (novel tasks / domains means "unseen" and is fine) |
| demonstrate the effectiveness | Change to which metric and by how much: reduces inference time by 65% at no loss in accuracy |
| superior / remarkable / powerful / promising | Delete when describing your own results and replace with numbers |
| extensive / comprehensive experiments | List datasets, models, settings: across five vision benchmarks and a sentence-embedding task |
| state-of-the-art | State the benchmark and comparison targets |
| wisely / cleverly / elegantly | Delete and state the rule itself |
| the first | Add To the best of our knowledge, and narrow the scope |

## C. Intensity adverbs

| Word | Suggestion |
|---|---|
| significantly | With a test: write statistically significant and the test used. Without: change to substantially or give the number directly |
| greatly / dramatically / seriously / very | Replace with numbers or ratios: two orders of magnitude fewer parameters |
| clearly / obviously | Delete |

- Weak: Our approach significantly outperforms the strongest baseline by clear margins.
- Strong: Under the most heterogeneous split (α = 0.3), our method exceeds the strongest baseline, [baseline], by [a] to [b] points on all four datasets. (Fill the brackets with numbers from the user's tables; do not estimate them yourself)

## D. Strength of result verbs

| Strength | Verbs | Used for |
|---|---|---|
| Strongest | prove | Mathematical proofs only |
| Strong | show, demonstrate, confirm, establish | Results measured directly by experiments |
| Medium | find, observe | Observed phenomena, without explaining causes |
| Weak | suggest, indicate, is consistent with | Inferred but not directly verified explanations |
| Weakest | may, likely, tend to, might | Possible causes, general tendencies |

A good pattern is asserting the number first and hedging the cause in the same sentence: Gains are modest under the red-anchor shift, likely because the model relies on color to separate the anchor from the block. Common errors are the reverse (demonstrate for the cause, may for the number), or adding may to every conclusion (see principles.md Section 2).

## E. Connectives

- If the same connective appears more than three times in a section, check whether each use means what it says (what follows Specifically is actually more detailed, Typically is actually about the general case).
- However often pairs with a concession in the previous sentence: Given X, doing Y is reasonable. However, ...
- In contrast is followed by a difference in mechanism, not "works better".

## E2. Sentences without information

| Pattern | Suggestion |
|---|---|
| In this section, we first present ... We then ... | State the flow and main points directly; if a roadmap is needed, each preview carries a piece of substantive information |
| In summary / Overall, these results show that X is effective. | State the property the results represent or the claim they support |
| We hope this work draws attention to ... | State the significance or a concrete next step |
| Meanwhile / Beyond X, ... | Replace with a connective that expresses the actual relation (because, in contrast, as a result), or split the paragraph |

## F. Vague quantifiers

| Word | Suggestion |
|---|---|
| many / various / several | Write the number: across 5 datasets, 28% of heads |
| large / small | Add a comparison target: two orders of magnitude fewer than MLLMs |
| fast / efficient | Give time or complexity: +0.67% end-to-end overhead, O(MN) |
| improves performance | State the metric and the change: from 43.7% to 96.0% |

## G. Common usage by native Chinese-speaking authors

| Common phrasing | Suggestion |
|---|---|
| Due to X is ... / Due to without X | due to takes only a noun phrase; change to Because X is ... / Without X, ... |
| With the development of ..., more and more ... | Delete and start directly from the problem |
| play an important role | State the concrete role |
| is seriously limited by | is limited by / cannot ... because ... |
| In recent years | Delete, or give a concrete time |
| make the model learn | encourage / force / allow the model to ... |

## H. Precise phrasings worth borrowing

| Purpose | Pattern |
|---|---|
| Trade-off | trade X for Y / without sacrificing Y |
| Comparison with baselines | matches or outperforms X / falls short of X by N points / comparable to X |
| Subsuming an old method | recovers X as a special case (e.g., when λ = 0) |
| Scope of applicability | is agnostic to X / a drop-in replacement for X |
| Naming a phenomenon | We refer to this phenomenon as X. |
| Plain-language restatement | Equivalently, ... / In essence, ... / At a high level, Theorem 1 says that ... |
| Delimiting scope | is beyond the scope of this paper / we leave X to future work |
| Limits of a claim | This does not imply that ... / should be read conditionally |
| What the goal is not | Our aim is not to X, but rather to Y. |

## Updating the word bank

`scripts/word_stats.py <paper folder>` counts, for each PDF's main text (excluding references and appendices), the occurrences of the words above and their frequency per ten thousand words. Rerun it when there are new example papers, and check whether the word bank needs adjusting.
