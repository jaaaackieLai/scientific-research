# Related Work

## The question this section answers

Reading only this section, a reviewer can confirm: the novelty claim holds, the most relevant prior work is all mentioned, and how this paper differs from it.

## Common structure

Group by technical topic into 2 to 4 groups, not by year. Common groupings: mainstream methods for the task, methods closest to this paper's core idea, auxiliary techniques this paper uses.

One paragraph per group: topic sentence → summarize representative methods (not a string of citations) → limitations (linked to the challenges in the introduction) → explain this paper's difference by mechanism, assumption, or failure case.

## Checklist

- [ ] Each group's limitations link to a challenge in the introduction; the listed shortcomings are addressed by this paper
- [ ] The latest, strongest, and most directly competing methods all appear (reviewers check this first)
- [ ] Differences are described by mechanism ("requires retuning for each scene"), not "works better"
- [ ] No paragraphs like "A [1], B [2], C [3] studied X" that only list citations
- [ ] Descriptions are fair and consistent with the criticism in the introduction
- [ ] Described in your own words, not copied from the original papers (copying is must fix)

## Rewrite points

- Content about prior work may only come from material the user provides; do not fill in what a paper did on your own. When needed, ask the user to provide the abstract or original text.
- Example (the user has explained the approach and assumptions of [1-3]):
  - Original: Many methods [1-5] have been proposed for domain adaptation, but they have limitations.
  - Rewrite: Feature-alignment methods [1-3] reduce the distribution gap by matching source and target statistics, but they assume the label distribution is shared across domains. In contrast, our method [to be provided by the user].
