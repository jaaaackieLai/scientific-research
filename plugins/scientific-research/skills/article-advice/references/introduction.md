# Introduction

## The question this section answers

Reading only the introduction, the reader will believe: the problem is important, existing methods have a gap, the method is designed for that gap, and there is quantitative evidence that it works.

## Common structure: six-paragraph chain of argument

It need not be exactly six paragraphs, but all six functions must be present and every arrow must hold.

| Paragraph | Writing points |
|---|---|
| 1 Background and motivation | Start from the task, not from the technique; ideally include a concrete example that can be reused later |
| 2 Limitations of existing methods | At most 3 points, each written as "method X cannot handle Y" |
| 3 Nature of the problem and goal | Can be short for method papers; for papers proposing a new problem, this paragraph is the core |
| 4 Key challenges | At most 3 points; one sentence on the obstacle, one to two sentences on why directly extending existing methods fails. Do not preview the solution |
| 5 Method overview | Modules, with section numbers in parentheses |
| 6 Contributions | 3 to 4 points, each a verifiable mechanism or result, marking which section delivers it |

When explaining why existing methods fail, walk through the causal chain: existing design → inherent property (due to) → failure (fails to) → consequence (Consequently) → lost capability (limiting).

## Checklist

- [ ] Importance is "necessary" rather than "popular": "X is popular" is not motivation
- [ ] The i-th limitation → i-th challenge → i-th module correspond; when the counts do not match, there is an explanation. Short labels reused across sections make this visible (writing-patterns.md 1.6)
- [ ] Contributions say which components are borrowed and what is new (writing-patterns.md 1.4)
- [ ] Challenges are derived from the problem, not reasons invented for the modules
- [ ] Contributions contain nothing the paper did not actually do; an experimental contribution (when the venue norm lists one) names the claim, benchmarks and headline number instead of "Extensive experiments demonstrate the superiority"
- [ ] Detailed descriptions of other people's methods go in related work
- [ ] Figure 1, when present, carries the main claim: from it and its caption alone, a reader can say what the paper shows (e.g., the prior view and this paper's view side by side)
- [ ] No contribution predicts adoption (will see broader application); move such sentences to the impact statement and hedge them
- [ ] A concrete scenario used for motivation has a matching experiment, and the introduction gives its section number

## Rewrite example

- Original: Graph neural networks have become very popular in recent years.
- Rewrite (the user has said the application is drug screening): Accurate property prediction for molecules is a prerequisite for screening drug candidates at scale, and graph neural networks are now the standard tool for this task.
- Explanation: changes "popular" into "why it is necessary".
