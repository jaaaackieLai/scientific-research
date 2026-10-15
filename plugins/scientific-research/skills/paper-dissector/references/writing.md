# Writing the note

The reader should finish the note understanding the idea well enough to explain it to someone else, and knowing what to trust. Summarizing is not enough.

## 1. Define everything, once
- Every symbol and term is defined at first use, in words, including what it depends on. Not "$h_t$ depends on $h_{t-1}$", but "the RNN keeps a representation of the sequence read so far, the hidden state $s_t$; computing $s_t$ needs $s_{t-1}$, so positions must be processed one after another".
- One symbol, one meaning across the whole note. If the paper reuses a symbol (e.g. $h$ for both the RNN hidden state and the number of heads), rename one and say so in the notation table.
- One concept, one name. Pick one term (e.g. "head", "baseline") and use it every time; do not rotate synonyms or translations.
- The notation table sits at the top, before any equation.
- Abbreviations (BLEU, BPE, FLOPs) are spelled out and explained in one sentence the first time.

## 2. Insight: make the reader want to know more
- Write it like telling a colleague the interesting part: what everyone assumed, what the paper did instead, and why that is surprising or useful.
- Plain words, three to five sentences. No equations, no method names as a substitute for the idea.
- End with the takeaway that transfers beyond this paper (a lesson the reader can reuse).

## 3. Background: important, hard, unsolved
Answer three separate questions; do not let one stand in for another.
- **Why it matters**: the authors' reason. Tag it [paper] unless they back it with data (usage, cost, a failure in practice); an asserted importance stays asserted.
- **Why it is hard**: what the naive approach is and why it fails. Say whether the paper runs the naive approach or only claims it fails.
- **Why it was not solved before**: what existing methods do and where each breaks. A problem nobody tried is not thereby hard; if the paper's case for difficulty is only "no prior work", say so.

## 4. Method: how and why, borrowed vs new
For each component, in the order a reader needs them:
1. The problem it solves (link back to the problem section).
2. What it does, with the equation if there is one.
3. **Borrowed or new**: if borrowed, from which paper and what was there before; if new, what exactly is new. A component can be borrowed with a new twist; say which part is the twist.
4. Why it was designed this way: the authors' reason, and alternatives they rejected.

Do not list components as bullets of facts. Each component is a short paragraph that answers these four.

## 5. Why it works: lead the reader's thinking
- Start from the question a careful reader would ask (e.g. "if every position looks at every other position, why did nobody do this before?"), then walk through the answer step by step.
- After the reasoning, say how strong the support is: which step an experiment shows, which only the authors argue, which is your inference.
- End with the honest answer to "what really made it better", even if it differs from the authors' story.

## 6. Format
- Prose for explanations. Tables only for look-up content: notation, setup checklist, baselines, claims, code comparison.
- Short paragraphs. No emoji, no star ratings.
- Keep the source's certainty. If the paper says "we suspect", write that the authors suspect; do not turn a guess into a fact or an estimate into a measurement.
- No hollow modifiers: no stacked hedges ("may potentially help to some extent") and no quality words ("powerful", "significant") without a number behind them.

## 7. Citing the paper
This is the one rule for pointing back to the paper; the other files refer here.
- **Default**: each factual statement about the paper names its location in parentheses: "(Sec. 3.2)", "(Eq. 4)", "(Table 2)", "(Fig. 1)". Table columns named Evidence or Paper hold the same citations.
- **Citable units**: the paper's own numbered sections, equations, tables, figures, algorithms, and appendices. Page and line numbers differ between the HTML and PDF versions, so cite the numbered unit instead.
- **When the host or caller turns location citations off**: leave out location words everywhere, table columns included, and write the content itself: the equation, or the number with what it measures and under which setting ("28.4 BLEU on WMT 2014 English-German"). A reader can then check the statement without opening the paper. The [paper] / [evidence] / [inference] tags stay.
