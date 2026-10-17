# Explanation techniques of good papers

word-bank.md governs which word to use; this file governs how to explain something clearly. When reviewing, use it to judge what a paragraph is missing; when rewriting, apply it only to content already in the original, and do not supply arguments or experiments for the user. Example sentences are illustrative, not original text.

Format: **Number Technique** (applicable sections): how to do it. Check: the question to ask when reviewing.

## 1. Posing the question

- **1.1 Write the research question as a question** (introduction, start of method): This leads to a more general question: do design principles distilled from text models transfer to other modalities? Check: after reading the introduction, can you state in one sentence the question this paper answers?
- **1.2 Show the question is not obvious** (introduction): first acknowledge that both answers are plausible. A priori, the answer is not obvious: time series share sequential structure with text, but unlike text they are not naturally discrete. Check: if the answer seems obvious, is there an explanation of why it still needs study?
- **1.3 First acknowledge that the existing approach is reasonable under its assumptions, then point out the gap** (introduction, related work): Given X, doing Y is reasonable. However, when Z, Y fails. Check: is the criticism of prior work restricted to the conditions under which the problem arises?
- **1.4 State what the goal is not** (abstract, introduction, analysis papers): Rather than proposing yet another model and claiming it wins on benchmarks, our objective is to understand ... In contributions, also say which components are not new: We do not propose a new X or Y; the contribution is the combination of ... Check: are known components presented as if they were new?
- **1.5 Define the criteria before comparing** (introduction, related work): first list the conditions a method should satisfy, then use a table to show which ones each existing method satisfies. The axes can also be design choices (prediction space × loss space; fixed vs. input-dependent weights), with this paper filling an empty cell.
- **1.6 Give each limitation or challenge a short label** (introduction, method, experiments): name it in 2 to 3 words (reference ambiguity, computational cost) and reuse the same label in the contributions, method subsections, and experiments, so the correspondence is visible. Check: can each label be traced to one module and one experiment?
- **1.7 Measure the problem before proposing the method** (introduction, a section before the method): when the method rests on an empirical premise (a trade-off, a failure mode, a scaling trend), first show it with a diagnostic experiment, then propose the method. Check: is the premise of the method itself supported by evidence, or only asserted?
- **1.8 Visualize the gap on page one** (introduction, Figure 1): plot measured results, not a schematic, in the space where the gap lives (a radar chart across distortion types; a two-axis trade-off scatter with a "Better" arrow), with this paper's method and one representative per prior family. The caption states which direction is better and the reading in checkable terms (lies in the upper-right of this plot), not optimal. Check: is the gap claimed in the introduction visible in a measured figure before the method is described?
- **1.9 Two-horn dilemma** (abstract, introduction): when prior work splits along a trade-off, name one representative at each end and the cost each pays: Some methods achieve X by constraining Y, which costs Z, while others preserve Y but fail at X. Check: are both horns cited, and does the main table measure both axes for every method?
- **1.10 Pair requirements with solutions by number** (introduction, start of method): list the conditions a solution must meet as numbered run-in items (Essential requirements. 1) ... 2) ...), then answer each in the same order (Proposed solution. For 1), ... For 2), ...). Reuse the numbers or labels in method subsections and ablations. Check: does every requirement have exactly one component and one experiment, and does every component answer a requirement?
- **1.11 Decompose the pipeline or objective to locate the gap** (introduction, method): split the standard pipeline or loss into named parts, state which part prior work optimizes, and show that the overlooked part is where the failure lies. The embedding process comprises discrete encoding and continuous sampling; prior work concentrates on encoding, but sign errors arise in sampling. / Decomposing the MSE loss into deflation, inflation and regularization terms shows that only the deflation term reduces decoding error. Check: is the decomposition exact (or its approximation stated), and is each part's role verified by training or evaluating with that part alone?
- **1.12 Invert the assumption: turn the nuisance into the signal** (abstract, introduction): when prior work tries to be invariant to a disturbance, first state why invariance may be unattainable (it is not clear whether such an invariant exists), then propose to exploit the disturbance instead. Rather than resisting geometric transformations, the injected template changes with them, so the transformation itself becomes a cue for correction. Check: is the reversal backed by a mechanism and a control (e.g., a passive baseline that predicts the nuisance without the injected signal)? Is the contrast sentence worded the same in the abstract and introduction?

## 2. Explaining concepts and methods

- **2.1 Name the phenomenon and give an operational definition** (method, analysis): We refer to the increase of numerical rank across layers as the flow-of-ranks. Define it precisely on first appearance, then use it consistently throughout. For custom metrics, write out how they are computed and restate them in plain language (2.3).
- **2.2 Give intuition first, then formalize** (method, theory): Intuitively, ... The following theorem formalizes this intuition. Check: before an equation or theorem, is there a sentence saying what is about to be shown?
- **2.3 Restate in plain language after formalizing** (method, theory): In essence / Equivalently / At a high level, this says that ... Check: after each theorem or main equation, is there a plain-language sentence explaining its meaning? Also say what it does not guarantee: which assumption is essential, how loose the bound is, and which cases have only empirical support (X is guaranteed when ...; for the general case we only have simulations).
- **2.4 Illustrate the problem with a simplified example whose answer is known** (introduction, method, interpretability and analysis papers): construct a model or data whose correct answer is known in advance, and show that existing methods get it wrong while this paper's method gets it right.
- **2.5 Answer in advance the questions readers will ask** (method, analysis): One may wonder: why ...? / One may be tempted to do X instead. However, ... Check: is there an obvious alternative approach that is not mentioned?
- **2.6 Show that a design choice is deliberate** (method): The X is deliberate: it recovers the baseline when ..., and only departs from it when ... In particular, explain under which conditions it reduces to the original method.
- **2.7 Put analogies after the mechanism** (any section): first state the property precisely, then add the analogy. Check: does the claim survive after the analogy is removed? (principles.md Section 6) When borrowing a term or analogy from another field, state which sense is meant and where the correspondence breaks, and claim only the weak version (We assume only that the near future is predictable from the past, not determinism).
- **2.8 Start from the ideal version, then approximate it** (introduction, method): Suppose we had access to X. Then the problem reduces to Y. The difficulty is obtaining X; we approximate it by ... Check: is it clear which part of the method is exact and which part is an approximation?

## 3. Designing experiments

- **3.1 Write the hypothesis first, then how it is tested** (experiments, analysis): Our central hypothesis is that ... To test this hypothesis, we ... For contrast, we ... Check: at the start of each experiment subsection, can the reader say what it tests?
- **3.2 Add controls to rule out other explanations** (experiments): To verify that the gain comes from X rather than Y, we ... (random controls, corrupted inputs, removing key components). Check: does the main result have other possible explanations? Is there an experiment that rules them out? Build the cheapest obvious fix as an extra baseline (gradient clipping, the same model without the new component) and report it even when it is strong. When no control is possible, write what each alternative explanation would predict and show which pattern the data has.
- **3.3 Explain why the comparison is fair** (experimental setup, table captions): state which conditions are identical (training steps, vocabulary size, validation set used for hyperparameter selection) and why these methods were chosen for comparison. We compare A and B because they share the same backbone, comparable sizes, and similar pretraining data. If the setup favors the baseline (hyperparameters tuned for it), say so; use the strongest version of the baseline; count costs outside the compared module (decoder, teacher pretraining, training data).
- **3.4 Report statistical details** (experiments): see "Statistical rigor" in experiments.md.
- **3.5 Write ablations as questions** (experiments): use a question as the subsection title, e.g., Which parameters to adapt?
- **3.6 Validate theory in three layers** (experiments of theory papers): (i) a setting that matches the assumptions, (ii) one where they no longer hold, (iii) real data. Report how loose the bound is in practice, and say when a check is only an algebraic identity rather than an empirical test. Check: does the reader know how far the experiments are from the theorem's assumptions?
- **3.7 Measure the side effect of every search, ensemble or test-time component** (experiments): if a component tries several candidates and keeps the best (exhaustive search, test-time augmentation, multiple decodings), it can inflate false positives or cost. Run the same procedure on negatives and report the resulting score distribution and threshold, plus runtime as a ratio and an absolute value. Check: could the component's benefit come from more chances to succeed, and is its false-positive rate reported with it enabled?
- **3.8 Support plug-and-play or compatibility claims with at least two hosts** (abstract, experiments): name each combination Host-Ours, report the host with and without the component in the same table, and state the added parameters or time. Check: does every "compatible with / plug-and-play / general" claim point to two or more host methods? With one host, write "can be combined with X".

## 4. Reporting results

- **4.1 Mark each conclusion separately** (experiments, analysis): at the start or end of a subsection, write the conclusion as a standalone sentence, optionally in bold or in a box (Finding 1: ... / Takeaway: ...).
- **4.2 Subsection titles state the finding** (experiments): see "Common structure" in experiments.md.
- **4.3 Numbers need a reference point** (abstract, experiments, conclusion): from A to B / N points higher than X / +0.67% overhead; distinguish percentage points from relative percentages. The reference point can also be a chance floor (random retention gives AUPRC 0.04), a noise floor (Monte Carlo variability alone gives KL 0.055), or a unit with fixed meaning (1 bit = a two-way tie).
- **4.4 State unfavorable results directly, and speculate on causes with hedged language** (experiments, analysis, conclusion): write out cases where it did not win, won by little, or got worse, followed by likely / might to explain possible causes, and if needed say what would be required to fix it. Gains are modest under the color shift, likely because the model relies on color to separate objects; this may require explicit invariance regularization. Check: are the table cells where this paper's method does not win mentioned in the body text?
- **4.5 State the limits of the results** (experiments, analysis, conclusion): This establishes X, but it does not imply Y. / The table should be read conditionally.
- **4.6 Describe as trade-offs, not simply good or bad** (analysis, conclusion): Whether this is an advantage or a drawback depends on the task: it helps when ..., but hurts when ...
- **4.7 When no column is won, define the win honestly** (experiments, abstract): if the method is best on the average but not on any single condition, say so and report the property it actually leads on (highest worst-case accuracy, smallest variance across conditions, best point on a trade-off curve). The method is not best on any single distortion, but its lowest per-distortion accuracy is 96.25%, versus 84.29% for the best baseline. Check: count the columns the method wins; if the count is zero or small, does the text avoid "superior" and name the property it leads on?
- **4.8 Report the attack's own cost next to the failure** (experiments, robustness and security papers): state the failure in numbers first, then put the attacked input's quality in the same sentence (TPR drops to 0.000 at strength 0.7, where PSNR is 15.44 dB). Do not replace the number with "performance gradually declines", and do not use "other methods share this weakness" unless the table shows it. Check: is every failure cell in the attack table quoted in the text?

## 5. Closing

- **5.1 Write limitations concretely** (conclusion or Limitations): list as points the required assumptions, untested cases, choices not explored in depth, and possible consequences. See conclusion.md for how to classify them.
- **5.2 Future directions extend from limitations or observations** (analysis, conclusion): pose concrete open questions from this paper's observations. This motivates future work: how does architecture determine ...?
- **5.3 Warn that results may be misused** (Broader Impact; interpretability, medical, and similar fields): state that outputs cannot be taken as definitive proof and must be interpreted with domain knowledge.
- **5.4 Give practical recommendations with their scope** (analysis, conclusion): We recommend A for ranking and B when accurate estimates are needed. / These results give the direction of the effect, not a complete allocation rule. Check: does each recommendation say when it applies?

## Sources

| Paper | What is referenced |
|---|---|
| ICML 2026, When Softmax Fails at the Top (WEINCE) | 1.1, 2.6, 2.7, 3.4, 4.5; most precise wording |
| ICLR 2026, Understanding Transformers for Time Series | 1.1, 1.2, 2.1, 2.2, 2.3, 2.5 |
| ICLR 2026, Implicit Biases of Design Choices for TSFMs | 1.4, 2.1, 4.1, 4.6 |
| ECCV 2026 oral, Steerable Visual Representations | 1.3, 1.5, 3.2, 4.1, 4.2, 4.3, 4.4 |
| ICML 2026 spotlight, Universal Redundancies in TSFMs | 2.1, 3.1, 4.5, 5.2 |
| ICML 2026 spotlight, Time Series Saliency Maps | 2.4, 5.1, 5.3 |
| arXiv 2026, AVQ-Attention | 2.5, 2.6, 3.3 |
| arXiv 2026, On Training in Imagination | 1.6, 3.6, 5.4 |
| arXiv 2026, Crys-JEPA | 1.6, 1.7; counterexample for claim strength drifting across sections |
| arXiv 2026, Residual-as-Teacher; TILT | 1.3, 2.8, 3.3, 3.6, 5.1 |
| arXiv 2026, Pretraining RNNs without Recurrence (SMT); Fast KV Compaction | 2.5, 2.8, 4.4 |
| arXiv 2026, Attention Residuals; Pixel MeanFlow | 1.5, 1.6, 2.3, 3.3 |
| arXiv 2026, S-JEPA; SGLRW; Flowing with Confidence | 1.4, 3.2, 4.3; counterexamples for "consistently" / "dominates" |
| arXiv 2026, Epiplexity; TDV; Goldstone modes | 1.7, 2.3, 2.7, 5.4 |
| arXiv 2026, ELF; stable-worldmodel | trade-off plots and reproduction checks in experiments.md |
| arXiv 2026, AdaJEPA | 3.5, 4.3, 4.4 |
| ECCV 2026 oral, World Knowledge in the Weights | 4.1; more exaggerated wording, reference its structure only |
| ICML 2026 spotlight, Required Spine Optional Limbs (SpineFL) | Counterexample for wording (utilize, effectiveness, wisely in word-bank.md mostly come from this paper); its RQ1 to RQ3 research-question structure is worth referencing |
| ICCV 2025, SynTag; NeurIPS 2025, T2SMark; ICML 2025, Lightweight-Mark; TDSC 2026, DRAW | 1.8 to 1.12, 3.7, 3.8, 4.7, 4.8; threat model in method.md. Counterexamples for averages hiding per-column losses, hyperparameter choices contradicting their sweep table, "marginal" for a 4.6x slowdown, accepting H0 from a t-test, FPR claims beyond the sample size, and citations that do not support the sentence |
