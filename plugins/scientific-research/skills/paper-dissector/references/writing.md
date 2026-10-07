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

## 3. Method: how and why, borrowed vs new
For each component, in the order a reader needs them:
1. The problem it solves (link back to the problem section).
2. What it does, with the equation if there is one.
3. **Borrowed or new**: if borrowed, from which paper and what was there before; if new, what exactly is new. A component can be borrowed with a new twist; say which part is the twist.
4. Why it was designed this way: the authors' reason, and alternatives they rejected.

Do not list components as bullets of facts. Each component is a short paragraph that answers these four.

## 4. Why it works: lead the reader's thinking
- Start from the question a careful reader would ask (e.g. "if every position looks at every other position, why did nobody do this before?"), then walk through the answer step by step.
- After the reasoning, say how strong the support is: which step an experiment shows, which only the authors argue, which is your inference.
- End with the honest answer to "what really made it better", even if it differs from the authors' story.

## 5. Format
- Prose for explanations. Tables only for look-up content: notation, setup checklist, baselines, claims, code comparison.
- Every factual statement cites its location (Sec., Eq., Table, Fig.).
- Short paragraphs. No emoji, no star ratings.
- Keep the source's certainty. If the paper says "we suspect", write that the authors suspect; do not turn a guess into a fact or an estimate into a measurement.
- No hollow modifiers: no stacked hedges ("may potentially help to some extent") and no quality words ("powerful", "significant") without a number behind them.
