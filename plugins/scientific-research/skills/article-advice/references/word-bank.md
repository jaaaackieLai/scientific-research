# Word bank

Basis: word usage statistics and reading of the main text of 39 example papers.

Criterion: these words are not banned; they carry no information when they appear alone. Good papers use them too, immediately followed by numbers, comparison targets, or mechanisms. Suggest a change only when replacing them with numbers or mechanisms makes the sentence concrete.

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
| extensive / comprehensive experiments | List datasets, models, settings: across five vision benchmarks and a sentence-embedding task |
| state-of-the-art | State the benchmark and comparison targets |
| wisely / cleverly / elegantly | Delete and state the rule itself |
| the first | Add To the best of our knowledge, and narrow the scope |
| optimal / optimally (balance, trade-off) | Only with a proof or a defined optimization; otherwise "the best balance among the compared methods" with one number per axis |
| powerful / innovative / groundbreaking / wonderful / incontrovertible | Delete when describing your own method or results; state the capability or number |

## C. Intensity adverbs

| Word | Suggestion |
|---|---|
| significantly | With a test: write statistically significant and the test used. Without: change to substantially or give the number directly (in 25 arXiv 2026 papers: 49 uses in 17 papers, "statistically significant" 0 times) |
| consistently / across all / dominates / on all benchmarks | Check every cell of the table; the most common false sentence in good papers (contradicted by the paper's own table in 5 of 25). Rewrite as a count (lowest on two of four datasets, second on the other two) or name the exceptions |
| greatly / dramatically / seriously / very | Replace with numbers or ratios: two orders of magnitude fewer parameters |
| clearly / obviously | Delete |
| marginal / negligible / slightly / just behind | Give the ratio or gap (4.6x; 9.2 points); keep the word only if the gap is within noise |

- Weak: Our approach significantly outperforms the strongest baseline by clear margins.
- Strong: Under the most heterogeneous split (α = 0.3), our method exceeds the strongest baseline, [baseline], by [a] to [b] points on all four datasets. (Fill the brackets with numbers from the user's tables; do not estimate them yourself)

## D. Urgency words

| Word | Suggestion |
|---|---|
| crucial / pressing / imperative / urgent(ly) | At most one per introduction, followed by a concrete consequence or event (a documented misuse case with a citation); otherwise delete |

## E. Connectives

- If the same connective appears more than three times in a section, check whether each use means what it says (principles.md Section 5; Typically introduces the general case).
- In contrast is followed by a difference in mechanism, not "works better".

## F. Sentences without information

| Pattern | Suggestion |
|---|---|
| In this section, we first present ... We then ... | State the flow and main points directly; if a roadmap is needed, each preview carries a piece of substantive information |
| In summary / Overall, these results show that X is effective. | State the property the results represent or the claim they support |
| Meanwhile / Beyond X, ... | Replace with a connective that expresses the actual relation (because, in contrast, as a result), or split the paragraph |

## G. Vague quantifiers

| Word | Suggestion |
|---|---|
| many / various / several | Write the number: across 5 datasets, 28% of heads |
| large / small | Add a comparison target: two orders of magnitude fewer than MLLMs |
| fast / efficient | Give time or complexity: +0.67% end-to-end overhead, O(MN) |
| improves performance | State the metric and the change: from 43.7% to 96.0% |
| up to N× / N% | Also give the typical value or the condition where the maximum occurs |

## H. Common usage by native Chinese-speaking authors

| Common phrasing | Suggestion |
|---|---|
| Due to X is ... / Due to without X | due to takes only a noun phrase; change to Because X is ... / Without X, ... |
| With the development of ..., more and more ... | Delete and start directly from the problem |
| play an important role | State the concrete role |
| is seriously limited by | is limited by / cannot ... because ... |
| In recent years | Delete, or give a concrete time |
| make the model learn | encourage / force / allow the model to ... |
| Besides, ... also ... (sentence-initial) | In addition, ... or merge into the previous sentence; Besides plus also repeats the meaning |
| It can be seen that / As we can see / It is clear to see that | Start with the finding: In Table 2, X reaches ... |
| Such results indicate the great/strong X of the proposed method | State which property the result shows and by how much |
| the proposed method (repeated as the subject) | Use the method's name |
| As the increase of X, ... | As X increases, ... |
| targetedly / be consisted of / an corresponding | selectively / consist of / a corresponding |
| shall (in descriptive text) | is / should / must |
| We summarize the reason as that ... | We attribute this to ... |
| well-trained / well-fine-tuned | trained / fine-tuned / pretrained |
| a common sense operation / In high level sense / testing frame | common practice / At a high level / test time |

## I. Precise phrasings worth borrowing

| Purpose | Pattern |
|---|---|
| Trade-off | trade X for Y / without sacrificing Y |
| Comparison with baselines | matches or outperforms X / falls short of X by N points / comparable to X |
| Scope of applicability | is agnostic to X / a drop-in replacement for X |
| Delimiting scope | is beyond the scope of this paper / we leave X to future work |
| Difference in mechanism | does X rather than Y / enters only through X, not through Y (rather than: 100 uses in 23 of 25 papers) |
| Correlation, not cause | We do not claim that X causes Y, only that X is correlated with Y. |

## Updating the word bank

`scripts/word_stats.py <paper folder>` counts, for each PDF's main text (excluding references and appendices), the occurrences of the words above and of the result verbs in principles.md Section 2, and their frequency per ten thousand words. Rerun it when there are new example papers, and check whether the word bank needs adjusting.
