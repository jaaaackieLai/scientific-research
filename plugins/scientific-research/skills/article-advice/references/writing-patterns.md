# Explanation techniques of good papers

word-bank.md governs which word to use; this file governs how to explain something clearly. When reviewing, use it to judge what a paragraph is missing; when rewriting, apply it only to content already in the original, and do not supply arguments or experiments for the user. Example sentences are illustrative, not original text.

Format: **Number Technique** (applicable sections): how to do it. Check: the question to ask when reviewing.

## 1. Posing the question

- **1.1 Write the research question as a question** (introduction, start of method): This leads to a more general question: do design principles distilled from text models transfer to other modalities? Check: after reading the introduction, can you state in one sentence the question this paper answers?
- **1.2 Show the question is not obvious** (introduction): first acknowledge that both answers are plausible. A priori, the answer is not obvious: time series share sequential structure with text, but unlike text they are not naturally discrete. Check: if the answer seems obvious, is there an explanation of why it still needs study?
- **1.3 First acknowledge that the existing approach is reasonable under its assumptions, then point out the gap** (introduction, related work): Given X, doing Y is reasonable. However, when Z, Y fails. Check: is the criticism of prior work restricted to the conditions under which the problem arises?
- **1.4 State what the goal is not** (abstract, introduction, analysis papers): Rather than proposing yet another model and claiming it wins on benchmarks, our objective is to understand ...
- **1.5 Define the criteria before comparing** (introduction, related work): first list the conditions a method should satisfy, then use a table to show which ones each existing method satisfies.

## 2. Explaining concepts and methods

- **2.1 Name the phenomenon and give an operational definition** (method, analysis): We refer to the increase of numerical rank across layers as the flow-of-ranks. Define it precisely on first appearance, then use it consistently throughout. For custom metrics, write out how they are computed and restate them in plain language (2.3).
- **2.2 Give intuition first, then formalize** (method, theory): Intuitively, ... The following theorem formalizes this intuition. Check: before an equation or theorem, is there a sentence saying what is about to be shown?
- **2.3 Restate in plain language after formalizing** (method, theory): In essence / Equivalently / At a high level, this says that ... Check: after each theorem or main equation, is there a plain-language sentence explaining its meaning?
- **2.4 Illustrate the problem with a simplified example whose answer is known** (introduction, method, interpretability and analysis papers): construct a model or data whose correct answer is known in advance, and show that existing methods get it wrong while this paper's method gets it right.
- **2.5 Answer in advance the questions readers will ask** (method, analysis): One may wonder: why ...? / One may be tempted to do X instead. However, ... Check: is there an obvious alternative approach that is not mentioned?
- **2.6 Show that a design choice is deliberate** (method): The X is deliberate: it recovers the baseline when ..., and only departs from it when ... In particular, explain under which conditions it reduces to the original method.
- **2.7 Put analogies after the mechanism** (any section): first state the property precisely, then add the analogy. Check: does the claim survive after the analogy is removed? (principles.md Section 6)

## 3. Designing experiments

- **3.1 Write the hypothesis first, then how it is tested** (experiments, analysis): Our central hypothesis is that ... To test this hypothesis, we ... For contrast, we ... Check: at the start of each experiment subsection, can the reader say what it tests?
- **3.2 Add controls to rule out other explanations** (experiments): To verify that the gain comes from X rather than Y, we ... (random controls, corrupted inputs, removing key components). Check: does the main result have other possible explanations? Is there an experiment that rules them out?
- **3.3 Explain why the comparison is fair** (experimental setup, table captions): state which conditions are identical (training steps, vocabulary size, validation set used for hyperparameter selection) and why these methods were chosen for comparison. We compare A and B because they share the same backbone, comparable sizes, and similar pretraining data.
- **3.4 Report statistical details** (experiments): see "Statistical rigor" in experiments.md.
- **3.5 Write ablations as questions** (experiments): use a question as the subsection title, e.g., Which parameters to adapt?

## 4. Reporting results

- **4.1 Mark each conclusion separately** (experiments, analysis): at the start or end of a subsection, write the conclusion as a standalone sentence, optionally in bold or in a box (Finding 1: ... / Takeaway: ...).
- **4.2 Subsection titles state the finding** (experiments): see "Common structure" in experiments.md.
- **4.3 Numbers need a reference point** (abstract, experiments, conclusion): from A to B / N points higher than X / +0.67% overhead; distinguish percentage points from relative percentages.
- **4.4 State unfavorable results directly, and speculate on causes with hedged language** (experiments, analysis, conclusion): write out cases where it did not win, won by little, or got worse, followed by likely / might to explain possible causes, and if needed say what would be required to fix it. Gains are modest under the color shift, likely because the model relies on color to separate objects; this may require explicit invariance regularization. Check: are the table cells where this paper's method does not win mentioned in the body text?
- **4.5 State the limits of the results** (experiments, analysis, conclusion): This establishes X, but it does not imply Y. / The table should be read conditionally.
- **4.6 Describe as trade-offs, not simply good or bad** (analysis, conclusion): Whether this is an advantage or a drawback depends on the task: it helps when ..., but hurts when ...

## 5. Closing

- **5.1 Write limitations concretely** (conclusion or Limitations): list as points the required assumptions, untested cases, choices not explored in depth, and possible consequences. See conclusion.md for how to classify them.
- **5.2 Future directions extend from limitations or observations** (analysis, conclusion): pose concrete open questions from this paper's observations. This motivates future work: how does architecture determine ...?
- **5.3 Warn that results may be misused** (Broader Impact; interpretability, medical, and similar fields): state that outputs cannot be taken as definitive proof and must be interpreted with domain knowledge.

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
| arXiv 2026, AdaJEPA | 3.5, 4.3, 4.4 |
| ECCV 2026 oral, World Knowledge in the Weights | 4.1; more exaggerated wording, reference its structure only |
| ICML 2026 spotlight, Required Spine Optional Limbs (SpineFL) | Counterexample for wording (utilize, effectiveness, wisely in word-bank.md mostly come from this paper); its RQ1 to RQ3 research-question structure is worth referencing |
