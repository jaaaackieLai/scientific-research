# Checklist

Confirm item by item before delivering a figure you made; when reviewing the user's figure or code, also check item by item, and for each problem state the location, the reason, and the fix.

- The proposed method is identifiable at a glance: it is the only saturated color, and baseline methods are all light colors
- Gaps are visible: no row of bars at almost the same height
- Text in the figure keeps only the values the claim needs; other explanations go into suggested caption text
- Every number in the figure can be recomputed directly from the user's data; differences, cumulative values, proportions, and lead times are allowed, but no imputed values or arbitrary merging of different metrics
- Every axis has a name and unit, and metric direction is marked
- Very small or very large values use scientific notation according to the rules, keeping the coefficient `1 ×` before `10^n`
- The legend does not cover data, and labels do not overlap
- Subplots meant for comparing trends use the same y range; when the y axis does not start at 0, note it in the suggested caption
- What error bars and error bands represent (standard deviation, 95% confidence interval, number of runs) is explained at least in the legend area or the suggested caption
- Color mapping is consistent with other figures in the same paper
- After plotting, actually open the output PNG and look at it once
- Places where you decided on your own (method families, tick choices, etc.) are listed when delivering
