# Three learning settings in deep learning: supervised, unsupervised, semi-supervised

Purpose of this document: make clear, for each of the three settings, "how to train, how to evaluate, when labels are needed", and where research commonly goes wrong.
The focus is on **making experimental conclusions hold up**, not "adding A raised the score, so use A".

---

## 0. A few shared terms first

| Term | Meaning |
|---|---|
| Label | The "correct answer" for each data point, e.g. whether an image is a cat or a dog. Usually requires human annotation, which is costly. |
| Training / validation / test set | The training set updates model parameters; the validation set is used to pick hyperparameters and decide when to stop; the test set is used only once at the end to report the final score. |
| Hyperparameter | A setting the model does not learn itself, e.g. learning rate, batch size, loss weights. |
| Data leakage | Information from the test set influences training or model selection in any way, inflating the score. |
| Distribution | The overall statistical properties of "what the data looks like". Training and test data coming from the same distribution is an assumption of most methods. |

**A principle that runs through the whole document:** "where labels are used" must be looked at on two levels:
1. Whether labels are used **during training** (this determines which setting it belongs to).
2. Whether labels are used **during evaluation and model selection** (almost every setting needs some kind of label or external reference at this level).

Many papers go wrong at level 2: they claim "no labels needed", but actually use many labels to pick hyperparameters.

---

## 1. Supervised Learning

### 1.1 Definition
Every training data point has (input x, label y). The model learns a function f(x) ≈ y.

### 1.2 How to train
- Define a loss function measuring the gap between predictions and labels. Classification commonly uses cross-entropy, regression commonly uses MSE.
- Minimize the average loss on the training set with gradient descent.
- Use the validation set to watch for overfitting (training loss keeps falling while validation loss starts to rise).

### 1.3 How to evaluate
- Compute metrics on a test set that **never took part in training or selection**.
- Classification: accuracy, precision / recall, F1, AUROC. With class imbalance, accuracy is misleading, e.g. if 99% are negative, guessing all negative gives 99% accuracy.
- Regression: MAE, RMSE, R².
- Report the mean and standard deviation over multiple random seeds, not the single best result.

### 1.4 Role of labels
- Training: needed.
- Validation / test: needed.

### 1.5 Special cases and pitfalls
1. **Data leakage**: Kapoor & Narayanan (2023) compiled 329 affected papers across 17 fields, found leakage to be the main cause of irreproducibility in ML research, and identified 8 types of leakage. Common ones:
   - Normalizing / selecting features on all data first, then splitting train / test.
   - Different slices of the same patient or the same video appearing in both the training and test sets.
   - Random splits of time series, letting the model "see the future".
2. **Reusing the test set**: repeatedly looking at test scores to change the model amounts to using the test set as a validation set. Recht et al. (2019) rebuilt the CIFAR-10 and ImageNet test sets following the original process, and model accuracy dropped by 3% to 15%. Their analysis attributes this mainly not to test set reuse, but to the new test sets being slightly "harder" and models failing to generalize. This shows that **"the score on a particular test set" is not the same as "true generalization ability"**.
3. **Label noise**: human annotations themselves contain errors, and the model may be learning the annotators' mistakes.
4. **Distribution shift**: data in the deployment environment differs from the training data, e.g. switching to a different hospital's scanner. A high score on an i.i.d. test set does not guarantee performance in this case.
5. **Class imbalance**: choose the right metrics, and state the sampling or weighting scheme.

---

## 2. Unsupervised Learning

### 2.1 Definition
Training data has only x, no y. The goal is to find structure in the data itself.

Common tasks:
- **Clustering**: group similar data together.
- **Dimensionality reduction / representation learning**: compress high-dimensional data into lower-dimensional, meaningful vectors, e.g. autoencoders.
- **Generative models**: learn the data distribution and produce new samples, e.g. VAE, GAN, diffusion models.
- **Self-supervised learning**: create "pseudo-labels" from the data itself for training, e.g. masking part of an image for the model to fill back in, or pulling two augmented versions of the same image close together in vector space. It needs no human labels, so it is usually grouped under the unsupervised umbrella, but its training form closely resembles supervised learning.

### 2.2 How to train
There is no y to compare against, so the loss function comes from the data itself:
- Reconstruction error (autoencoder: input x, output must recover x).
- Maximizing the likelihood of the data (VAE, flow models).
- Contrastive loss (self-supervised: different views of the same data should be close, different data should be apart).
- Clustering objectives (k-means: minimize the total distance from each point to its cluster center).

### 2.3 How to evaluate (the hardest part)
Unsupervised learning "has no ground truth", so the evaluation method depends on the purpose:

| Method | Labels needed? | Explanation |
|---|---|---|
| Internal metrics | No | E.g. the silhouette score for clustering, which only looks at intra-cluster compactness and inter-cluster separation. The problem: a high score does not mean the clusters have the meaning you want. |
| External metrics | Yes | E.g. computing NMI, ARI, or clustering accuracy with true classes. At this point labels are already being used for evaluation. |
| Downstream task evaluation | Yes (a few or all) | Standard practice for self-supervised learning; see below. |
| Generation quality metrics | Depends on the metric | E.g. log-likelihood, FID. Theis et al. (2016) point out that on high-dimensional data, log-likelihood, Parzen window estimates, and the visual quality of samples are **nearly independent of each other**; being good on one does not mean being good on another. So choose evaluation methods based on the actual use. |

**Three downstream evaluation methods for self-supervised representations** (from simple to complex):
1. **kNN**: freeze the model and classify directly by nearest neighbors on the vectors. No training needed; most directly reflects the structure of the vector space.
2. **Linear probing**: freeze the model and train only a linear classifier on top. Measures "whether the classes are linearly separable in this representation".
3. **Fine-tuning**: train the whole model together with labels. Measures "how good it is as an initialization", but mixes in the effect of supervised training itself.

These three methods can give different rankings, so a paper should state clearly which one is used, and preferably report several.

### 2.4 Role of labels
- Training: not needed.
- Evaluation: **actually needed in most cases**, just at the evaluation stage.
- Hyperparameter selection: in theory should not use labels, but in practice they are often used quietly.

### 2.5 Special cases and pitfalls
1. **Without labels, model selection is hard**: Locatello et al. (2019, ICML best paper) trained more than 12,000 models and found that without true labels, it is impossible to identify which models learned good "disentangled representations" (each dimension corresponds to one independent generative factor). They also proved theoretically that without adding assumptions (inductive biases) on the model or data, this kind of unsupervised disentanglement is impossible in itself.
   → Research implication: if you used labels to pick hyperparameters, state it honestly; this is no longer "purely unsupervised".
2. **"Learned structure" may not be what you want**: clustering may split by background color rather than by object category. The objective the model minimizes is not necessarily the objective you have in mind.
3. **Evaluation depends on specific downstream datasets**: good linear probing on ImageNet does not mean it is also good on medical images.
4. **The choice of augmentation carries prior knowledge**: choosing which augmentations to use in self-supervised learning amounts to telling the model what is "unimportant". This is an assumption injected by the designer and should be stated in the paper.

---

## 3. Semi-supervised Learning

### 3.1 Definition
There is **a small amount of labeled data** and **a large amount of unlabeled data**, both used together to train a model for the same task.
Typical setting: CIFAR-10 with only 250 or 4000 labeled images, and the remaining 40,000+ given without labels.

### 3.2 Why does unlabeled data help? (assumptions required)
Unlabeled data carries no answers itself; it can only help if **there is some relation between the data distribution and the labels**. Common assumptions (see the survey by van Engelen & Hoos, 2020):
- **Smoothness assumption**: two points close together in input space should have the same label.
- **Low-density assumption**: the decision boundary should lie where data is sparse, not pass through dense regions.
- **Manifold assumption**: high-dimensional data actually lies on a low-dimensional surface, and points close together on that surface have the same label.
- **Cluster assumption**: data in the same cluster usually belongs to the same class.

**When the assumptions do not hold, adding unlabeled data may not help, and may even hurt performance.** This must be verified or discussed in research, not assumed to always be useful.

### 3.3 How to train
Loss = supervised loss on the labeled part + λ × loss on the unlabeled part. Common methods:
- **Pseudo-labeling / self-training**: use the model to predict unlabeled data, and treat high-confidence predictions as labels for further training.
- **Consistency regularization**: apply different perturbations to the same unlabeled data point; the model's predictions should be consistent.
- **Hybrid methods**: e.g. FixMatch, which combines pseudo-labels from weak augmentation with a consistency requirement on strong augmentation.

λ and the confidence threshold are both hyperparameters and have a large effect on results.

### 3.4 How to evaluate
- Evaluate with supervised metrics on a fully labeled test set.
- **Always compare with "a supervised baseline trained only on that small amount of labeled data"**, and tune the baseline seriously too. Otherwise you cannot show whether the improvement comes from the unlabeled data or from better tuning.
- Report results at different numbers of labels (e.g. 40, 250, 4000), because the relative merits of methods change with the number of labels.

### 3.5 Role of labels
- Training: a small amount needed.
- Validation: **needed, and this is where cheating is easiest** (see below).
- Test: needed.

### 3.6 Special cases and pitfalls (key reminders from Oliver et al., 2018)
Oliver et al. (NeurIPS 2018) systematically examined how semi-supervised learning is evaluated and pointed out several problems:
1. **Validation set larger than the training labels**: many papers claim to use only 250 labels but tune on a labeled validation set of 5000. This is unrealistic. On SVHN, they found that with a validation set of only 100 to 1000 examples, validation accuracy fluctuates so much that it **cannot reliably distinguish which methods are better**.
2. **Baselines too weak**: the supervised baseline is not properly tuned, making the improvement of semi-supervised methods look larger than it is.
3. **Class distribution mismatch**: real-world unlabeled data often contains things outside the training classes. When unlabeled data is mixed with samples that belong to no target class, semi-supervised methods can drop sharply in performance, even below not using unlabeled data at all.
4. **Comparison with transfer learning**: directly fine-tuning a model pretrained on another large dataset is sometimes better than semi-supervised methods. Research should include it as a comparison target.
5. **Confirmation bias**: if pseudo-labels are wrong at the start, the model grows increasingly confident in the wrong answers.
6. **Class imbalance**: during pseudo-labeling the model leans toward majority classes, so minority classes get labeled less and less.

---

## 4. Comparison of the three

| | Supervised | Unsupervised | Semi-supervised |
|---|---|---|---|
| Training data | All labeled | All unlabeled | A few labeled + many unlabeled |
| Training objective | Predict labels | Find data structure / reconstruct / generate / self-supervised objective | Predict labels, and exploit the structure of unlabeled data |
| Labels needed for evaluation? | Yes | Usually (external metrics or downstream tasks) | Yes |
| Labels needed for hyperparameter selection? | Yes | Should not be in theory, often used in practice (must be stated) | Yes, but limited to the amount realistically available |
| Core assumptions | Training / test from the same distribution | Data structure relates to what you care about | Smoothness, cluster, manifold, low-density assumptions hold; labeled and unlabeled data from the same distribution |
| Most common research pitfalls | Data leakage, repeatedly looking at the test set | Objective disconnected from evaluation, quietly using labels to pick models | Validation set too large, baselines too weak, distribution mismatch |

---

## 5. When to use which?

- **Labels are cheap and plentiful**: supervised. Get the supervised baseline right first.
- **No labels at all, and the goal is to explore structure**: unsupervised. But first think clearly about "what counts as good", or you cannot evaluate.
- **No labels, but there will be downstream tasks later**: self-supervised pretraining, then linear probing or fine-tuning with a small number of labels.
- **A few labels and a lot of unlabeled data of the same type**: semi-supervised. But first check whether the unlabeled data comes from the same distribution and has the same classes as the labeled data.

---

## 6. Research checklist

When writing experiments or reviewing papers, confirm item by item:

1. **Is the amount of labels used at each stage stated clearly?** Including training, validation (hyperparameter selection, early stopping), and testing.
2. **Is the test set used only at the end?** Was the model changed based on test results?
3. **Does the data split leak?** Is preprocessing fit only on the training set? Is data from the same source split across both sides?
4. **Are the baselines fair?** Do the baselines and the proposed method use the same tuning budget, data augmentation, and training time?
5. **Are the mean and standard deviation over multiple seeds reported?** Is the gap larger than the standard deviation?
6. **What assumptions does the method rely on? Is there verification or discussion of what happens when they do not hold?**
7. **Is the source of the improvement broken down clearly?** Use ablation experiments (remove one component at a time to see its effect) to show the contribution of each component, and explain "why" it works, not just "that" it works.
8. **Do the evaluation metrics correspond to the goal you actually care about?** Especially for unsupervised and generative models.

A final note: a method raising a score is only an observation; explaining **under what assumptions and why** it raises the score, and ruling out other explanations (leakage, tuning differences, randomness), is what makes a scientific conclusion.

---

## References

- Oliver, A., Odena, A., Raffel, C., Cubuk, E. D., & Goodfellow, I. (2018). *Realistic Evaluation of Deep Semi-Supervised Learning Algorithms*. NeurIPS. https://arxiv.org/abs/1804.09170
- Locatello, F. et al. (2019). *Challenging Common Assumptions in the Unsupervised Learning of Disentangled Representations*. ICML. https://proceedings.mlr.press/v97/locatello19a.html
- Recht, B., Roelofs, R., Schmidt, L., & Shankar, V. (2019). *Do ImageNet Classifiers Generalize to ImageNet?* ICML. https://arxiv.org/abs/1902.10811
- Kapoor, S. & Narayanan, A. (2023). *Leakage and the reproducibility crisis in machine-learning-based science*. Patterns. https://arxiv.org/abs/2207.07048
- Theis, L., van den Oord, A., & Bethge, M. (2016). *A note on the evaluation of generative models*. ICLR. https://arxiv.org/abs/1511.01844
- van Engelen, J. E. & Hoos, H. H. (2020). *A survey on semi-supervised learning*. Machine Learning, 109(2). https://www.semanticscholar.org/paper/A-survey-on-semi-supervised-learning-Engelen-Hoos/3021b6dec80e7032fd995c0dcadf4c992b7d7506
- Balestriero, R. et al. (2023). *A Cookbook of Self-Supervised Learning*. https://arxiv.org/abs/2304.12210
- Marks, M. et al. (2023). *A Closer Look at Benchmarking Self-Supervised Pre-training with Image Classification*. https://arxiv.org/abs/2407.12210
