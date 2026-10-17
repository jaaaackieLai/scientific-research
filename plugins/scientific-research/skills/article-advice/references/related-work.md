# Related Work

## The question this section answers

Reading only this section, a reviewer can confirm: the novelty claim holds, the most relevant prior work is all mentioned, and how this paper differs from it.

## Common structure

Group by technical topic into 2 to 4 groups, not by year. Common groupings: mainstream methods for the task, methods closest to this paper's core idea, auxiliary techniques this paper uses.

One paragraph per group: topic sentence → summarize representative methods → limitations → this paper's difference.

## Checklist

- [ ] Each group's limitations link to a challenge in the introduction; the listed shortcomings are addressed by this paper
- [ ] The latest, strongest, and most directly competing methods all appear (reviewers check this first)
- [ ] Differences are described by mechanism, assumption, or failure case ("requires retuning for each scene"), not "works better"
- [ ] No paragraphs like "A [1], B [2], C [3] studied X" that only list citations
- [ ] Descriptions are fair (writing-patterns.md 1.3)
- [ ] Closely related methods that are not compared are named, with the reason stated as a difference in goal or setting (detection vs. traceability; optimization-based vs. training-free), not omitted silently
- [ ] When the field has an established taxonomy (e.g., post-hoc / fine-tuning / inversion-based), state which family this paper belongs to and which shared limitation it inherits

## Rewrite example

- Original (the user has explained the approach and assumptions of [1-3]): Many methods [1-5] have been proposed for domain adaptation, but they have limitations.
- Rewrite: Feature-alignment methods [1-3] reduce the distribution gap by matching source and target statistics, but they assume the label distribution is shared across domains. In contrast, our method [to be provided by the user].
