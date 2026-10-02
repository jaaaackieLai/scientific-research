# Experiment check

Goal: decide, claim by claim, whether the experiments support what the paper says. Do `setup-checklist.md` first; its answers feed this check.

## 1. Claim-to-evidence table

List the paper's claims (abstract, contribution list, conclusion), then:

| Claim | Evidence (Table / Fig / Sec) | Verdict | Reason |
|---|---|---|---|
| ... | ... | supported / weak / none | ... |

- **supported**: a fair comparison or ablation directly tests the claim, over multiple seeds or folds.
- **weak**: evidence exists but has one of the problems in Section 2, or rests on a single seed (setup-checklist 3.4).
- **none**: no experiment tests it (often "efficient", "general", "interpretable").

## 2. Problems to check
Leakage, test-set reuse, and seeds are covered in setup-checklist Section 3; also check:

| Problem | What to look for |
|---|---|
| Unfair baseline | Baselines copied from older papers with different budgets, data, or tuning; only the proposed method was tuned |
| Ablation does not match the claim | The component credited for the gain is never removed alone; several changes are ablated together |
| Confounded comparison | More parameters, compute, data, or training steps than the baselines, not controlled |
| Selected benchmarks | Datasets or metrics where the method is weak are missing, compared with the baselines' papers |
| Metric mismatch | The metric reported does not measure what the claim is about |
| Cost not reported | No training time, FLOPs, or memory when the claim involves efficiency |

## 3. Output
Fill the "Claims vs evidence" section of the note with the table. List every "weak" or "none" claim in the chat reply.
