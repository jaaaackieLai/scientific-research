# Experimental results and analysis (Experiments)

Results answer "is it better", analysis answers "why is it better, and where is it not"; write both in the same section.

## The questions this section answers

1. Under fair conditions, is it better than the latest and strongest baseline methods?
2. Which design causes the improvement? (ablation)
3. How does it do in harder, rarer, or noisier settings? Including failure cases.

## Common structure

Experimental setup (datasets, metrics and the reason for choosing them, baseline methods, implementation details) → main comparison → ablation → analysis (reasons, failures, cases or visualizations).

- Derive experiments from claims: one validation experiment per contribution, one ablation per module.
- Use figures and tables as the skeleton: first check whether each figure or table can be understood on its own and conveys only one point, then look at the text.
- Subsection titles state the finding: Larger Memory Helps Only on Long Sequences, not Effect of Memory Size.
- Put the most important result first.

## Results paragraphs

1. Point to the table and give the most important number in the same sentence (In Table 1, our method reduces the error rate to 3.2%, 1.1 points lower than the strongest baseline); do not write Table 1 reports the comparison
2. Overall conclusion
3. Where other methods perform poorly, one concrete detailed comparison
4. Acknowledge the strengths of the strongest baseline (While X performs well on ..., it ...)
5. Explain why it wins by mechanism (stems from / is attributed to)

- One to three numbers per paragraph: the most important result, the contrast that best shows the trend, the exception. Do not copy the table wholesale.
- End each paragraph with a one-sentence interpretation that adds a layer of meaning beyond what came before:
  - Weak: The gain remains at longer sequence lengths, suggesting the method also performs better on long inputs.
  - Strong: Thus, the benefit of the memory module grows with context length rather than saturating.

## Ablation and analysis

- For each ablation row, state clearly: what was removed, what replaced it (replace the learned fusion with simple concatenation), how the results changed, and what it means. An ablation that does not state the replacement cannot be judged.
- Analysis: observation → concrete example (For instance, in Figure 5 ...) → attribution. Attributions without experimental verification use hedged language, or add experiments.
- Report failure cases and unfavorable results (see writing-patterns.md 4.4 for how to write them).

## Statistical rigor

- [ ] Main results use at least 3 random seeds and report mean ± standard deviation; if run only once, explain why
- [ ] When the gap to the strongest baseline is smaller than the standard deviation, there is a significance test or confidence interval; otherwise weaken the claim
- [ ] Do not use significantly without a test
- [ ] Baseline methods get the same tuning budget as the proposed method; state the search range, number of trials, and which split was used for selection
- [ ] Release final hyperparameters (optimizer, learning rate schedule, batch size, steps) and compute resources (GPU model, count, GPU hours)
- [ ] Seeds and data splits are decided in advance; the test set is not used for tuning or model selection
- [ ] Figures have error bars or shading, and the caption states what they represent and how many runs
- [ ] Claims of no degradation (distortion-free, lossless, same level as) rest on an equivalence test (TOST), a confidence interval with a pre-set margin, or an effect size; a non-significant t-test alone means "no difference detected", and a lower t-value is not stronger support for H0
- [ ] Very low false-positive rates (e.g., FPR = 1e-6) state how the threshold was derived (analytic, or from N negatives); an empirical check on N negatives supports rates down to about 1/N only. With search-based decoding, state how the threshold accounts for multiple candidates
- [ ] The number of test samples is stated next to each main table (rates from 50 images move in steps of 0.02)
- [ ] When training is expensive and only one seed is run, the reported variance comes from the deployment-time randomness instead (keys, messages, prompts, images), and the text says so

## Other checks

- [ ] Baseline methods include the latest and strongest, not only weak ones
- [ ] Baseline and proposed-method numbers come from the same source (do not use paper-reported numbers on one side and your own runs on the other); explain when they differ
- [ ] Metrics are the standard metrics for this task
- [ ] Custom measures have a name, are defined on first appearance, are placed in a table column, and are referred to by name afterward (do not write by this measure)
- [ ] Reimplemented baselines reproduce the originally reported numbers, or the discrepancy and its likely cause are stated
- [ ] Differences in training data, compute, and parameter count from the baselines are stated, including costs outside the compared module
- [ ] Evaluation on a subset: the subset was chosen in advance and checked to be representative; missing baselines or settings are explained
- [ ] Failed runs (divergence, NaN) and design choices that did not help are reported, at least in the appendix
- [ ] When a knob trades two metrics, compare whole curves or compare at a matched value of one metric, not single points
- [ ] A hyperparameter chosen in the paper that is not the best in its own sweep table is justified in the same paragraph, with evidence
- [ ] "Same level of visual quality / same budget" statements match the table; otherwise state the actual range

## Figures and tables

- Captions: define every method name, variant, abbreviation, and subscript in them, plus what bold, underline, and colors mean. Readers should understand from the figure and caption alone.
- Architecture figure captions explain the pipeline, not just Overview of the model; the first sentence of a results figure caption states the point to be read from it. For trade-off plots, say which direction is better (lower-right is better); state where each number comes from (reported vs. reproduced) and key settings.
- Tables: caption goes above; headers mark the metric direction (Acc ↑, Error ↓) and units; decimal places are consistent within a column; one point per table; highlight with bold or underline, not heavy coloring.
- A teaser figure that places the method and baselines on the paper's two axes is effective when the claim is a trade-off; its caption states which direction is better and avoids words the data cannot prove (optimal). See writing-patterns.md 1.8.
- Bold the best value in every column, including baseline wins, and define bold/underline in the caption. Bolding only the proposed method's row, or only the average column, hides losses.
- Report overhead as a ratio and an absolute value (1.4 ms to 6.5 ms per image, 4.6x); do not call a several-fold increase marginal.

## Rewrite example

- Original: As shown in Table 1, our method significantly outperforms other methods.
- Rewrite (the user's numbers are 3.2% and 4.3%): In Table 1, our method achieves an error rate of 3.2%, compared with 4.3% for the strongest baseline.
- Explanation: give the numbers first; remove significantly because there is no test. No numbers are changed, and no comparisons or conclusions are added.
