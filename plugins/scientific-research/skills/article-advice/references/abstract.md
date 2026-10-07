# Abstract

## The question this section answers

Reading only the abstract, the reader can say: what problem is solved, why existing methods are not enough, what was done, and how well it works.

## Common structures (pick one by number of contributions; no need to match sentence by sentence)

- **A. Challenge → contribution** (one main contribution): task → technical challenge → one to two sentences of technical contribution (name the mechanism, do not describe it step by step) → benefit → results
- **B. Challenge → key idea → contribution** (the contribution comes from a non-obvious idea): task → challenge → one verifiable key idea (not a restatement of the challenge) → technical contribution → benefit → results
- **C. Multiple contributions**: task → (optional) contrast with existing methods → for each contribution, one sentence of mechanism and one sentence of effect (the effect echoes the challenge's wording) → results
- **D. Broad to narrow** (common in cross-disciplinary journals): background any field understands → background related fields understand → the unknown problem (often starting with However) → Here we show the main result → what changed compared with prior understanding → the larger context

Two key points of D (progressively narrowing the reader level, and saying "what we used to think, and what we now know") are also worth borrowing when using A to C.

## Checklist

- [ ] Task, challenge, contribution, and results can each be found
- [ ] The first sentence starts from the problem, not from We propose; one sentence says one thing
- [ ] The challenge is a challenge of the problem itself, not "the difficulty our method has to overcome"
- [ ] It is clear why this contribution solves this challenge (e.g., the challenge is about efficiency but the contribution is about accuracy: they do not match)
- [ ] The main result is clearly marked (Here we show, We find that)
- [ ] Says what changed compared with prior understanding, not just "it works better"
- [ ] Results have concrete numbers and comparison targets, at most one to two headline numbers, all of which can be found in the experiments section
- [ ] No implementation details (backbone, how the loss is attached)
- [ ] The last sentence summarizes the contribution of the whole paper, not stopping at the last experimental result
- [ ] Terms are understandable without relying on definitions in the body text
- [ ] Word count meets the limit (commonly 150 to 250 words); when over, cut implementation details and secondary numbers first, not the problem statement or mechanism sentences

## Rewrite example

- Original: We propose a novel method that utilizes attention to achieve better performance.
- Rewrite: [first state the problem and challenge] To address this, we weight each token by its relevance to the query, which reduces the influence of irrelevant context.
- Explanation: says what attention actually does. To keep "better performance", the user must provide numbers.
