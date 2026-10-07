# Setup checklist

Every note answers all items. Give the location in the paper (or code), or write "not stated in the paper". An unanswered item is a finding, not a gap to fill with a guess.

## 1. Data loading and processing
| # | Question | Notes |
|---|---|---|
| 1.1 | Which datasets? | Name, what one sample is, size, where it comes from. Explain the dataset to a reader who has never seen it |
| 1.2 | Are there labels? | What the label is (class, reference translation, mask...), and whether training uses it |
| 1.3 | What is the data shape? | Per sample and per batch, e.g. `[batch, length]` token ids; variable or fixed length |
| 1.4 | Train / val / test: predefined or randomly built? | The split method; for random splits, the seed and the unit of splitting (sample, subject, time) |
| 1.5 | Preprocessing and normalization | Tokenization, normalization statistics and which split they were fit on, filtering, augmentation |

## 2. Architecture and training
| # | Question | Notes |
|---|---|---|
| 2.1 | Which task, and which learning setting? | Supervised, unsupervised, self-supervised, semi-supervised, RL; what the model takes in and outputs |
| 2.2 | Early stopping? How? | Criterion, which split it watches, patience; or a fixed number of steps |
| 2.3 | Is the training procedure fully described? | Could someone reimplement it from the paper alone? List what is missing |

## 3. Evaluation and metrics
| # | Question | Notes |
|---|---|---|
| 3.1 | How is it evaluated? Is the test set leaked? | Is the test set used for hyperparameter, checkpoint, or early-stopping decisions? Overlap between training and test data? |
| 3.2 | Overfitting? | Train vs val curves or gaps, regularization evidence |
| 3.3 | Which metrics, and how is each computed? | Definition in one or two sentences; implementation details that change the number (e.g. tokenized vs detokenized BLEU) |
| 3.4 | Cross-validation, multiple seeds, or a single seed? | **A single seed is not a valid result: it has no statistical power.** Any claim resting only on single-seed results is at most "weak" in experiment-check |

## 4. Baselines
| # | Question | Notes |
|---|---|---|
| 4.1 | Who are the baselines? | Name, source paper, and one sentence on how each works, so the reader knows what is being beaten |
| 4.2 | Where do their numbers come from? | Rerun by the authors, or copied from the original papers |
| 4.3 | Same setting? | Same data, preprocessing, metric implementation, and compute budget as the proposed method |
