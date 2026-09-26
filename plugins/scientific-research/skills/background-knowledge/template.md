# Format for new files

Each section only contains content that meets the inclusion criteria (easy to get wrong, controversial, has a fixed convention); if there is none, write "None". Every item comes with a source.

## Data types / training scenarios (`data/`, `settings/`)

```markdown
# <Domain name>

> Last verified: YYYY-MM-DD

## 1. Problem setting
What problem this domain solves, which subtasks it has, common notation.

## 2. Common datasets and known issues
Dataset names, sizes, issues already pointed out (label errors, duplicate samples, too easy).

## 3. Data splits and leakage risks
Standard split methods, and leakage paths specific to this domain.

## 4. Evaluation protocols and metrics
The community's current standard practice, and the limitations of each metric.

## 5. Baselines that must be compared
Methods without which a comparison does not hold up, including simple but strong baselines.

## 6. Common pitfalls
Mistakes papers often make and reviewers often catch.

## 7. Open controversies
Questions without consensus yet, listing each side's position and evidence.

## References
```

## Model architectures (`core/architectures/`)

```markdown
# <Architecture name>

> Last verified: YYYY-MM-DD

## 1. Versions and variants
Variants that change results, and cases where names are used interchangeably.

## 2. Details that affect results but papers often omit
E.g. position of normalization layers, type of positional encoding, initialization method.

## 3. Items to align for a fair comparison
Parameter count, compute, training budget, data augmentation, etc.

## 4. Known issues and controversies

## References
```
