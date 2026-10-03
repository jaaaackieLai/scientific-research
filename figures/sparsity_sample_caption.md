# Sparsity sample

**Illustrative data only.** The curves are generated from deterministic formulas to demonstrate the figure-making style; they are not experimental results or values digitized from the reference image.

Suggested caption: Relative test accuracy change as sparsity increases, with sparsity applied to (a) the first convolutional layer or (b) all convolutional layers. Relative change is defined as `100 × (A(s) − A(0)) / A(0)`, where `A(s)` denotes test accuracy at sparsity `s`; higher values indicate better accuracy retention. Both panels use the same y-axis range, which extends below zero to show accuracy reductions. These illustrative curves have no repeated runs or uncertainty estimates, so no error bands are shown.

Demo assumptions: TiltDiff is the proposed method; SANE_sub is a baseline. Use deep red for TiltDiff and light blue for SANE_sub in both panels. Preserve sparsity tick labels because they identify the experimental conditions. Distinguish methods additionally with solid/circular versus dashed/square styling. No claim about actual method performance follows from this sample.

Style: 32 pt axis labels, 28 pt ticks and legends, 36 pt panel labels, 24 pt demo notice, 5 pt lines, 10 pt markers, 300 dpi PNG. TiltDiff's line and markers use zorder 3, above SANE_sub's zorder 2, independent of plotting order. Canvas: 24 × 9 inches, including panel labels and the demo notice.

The input data is in `figures/data/sparsity_sample.csv`; the plot script reads that file and preserves it on later runs. Regenerate the figure by running `figures/src/sparsity_sample.py` with the project's Python environment. Output paths are independent of the current working directory.
