# Püschel, *Small Guide to Giving Presentations* (summary)

Source: Markus Püschel, CMU ECE. Full PDF: `puschel-small-guide-to-giving-presentations.pdf` (49 pages, slide + notes per page). Page numbers below point to that PDF. This is a paraphrased summary; open the PDF for the original examples.

Where this guide conflicts with the user's own preferences, the user wins. Known conflict: the guide says bullets need not be full sentences; the user wants complete sentences on slides (see `text-density.md`).

## Six principles (p.47)

| Principle | Rule | Pages |
|---|---|---|
| Alignment | Every element aligns to something. Left-align when unsure; centered text looks weak. Applies to tables too. | 2, 5, 41 |
| Contrast | If two things should look different, make them clearly different. For text, change at least two of: weight, size, color, font. | 2, 5–6 |
| Layering | Decide what is foreground and push the rest back (gray, lighter, pastel). Maps are the model example. | 37, 41 |
| Consistency | Same font, same color for the same kind of thing across the whole talk. Break it only on purpose, for emphasis. | 29 |
| Visualization | Show problem statements, methods, algorithms, and results as pictures, not as text or equations. | 20–25 |
| Acknowledgment | Name co-authors aloud, credit borrowed figures on the slide, cite related work by name. | 8, 13, 27 |

## Content and structure

- Open with motivation: what, why, why it matters. Give a precise problem statement, visualized if possible. The first slide must not be text-only. (p.3, 15)
- Typical order: motivation and problem statement, background and related work, contribution, results, conclusions. (p.16)
- Overview slide after the motivation: talks over 25 min repeat it before each section; up to 20 min show it once; up to 10 min skip it. (p.15)
- Number of slides at most 2/3 of the minutes, counting every slide. (p.12)
- Communicate motivation, problem, main idea, main result. Do not try to get every detail across; going deep for a few slides is fine. (p.19)
- Repeat one or two key points throughout. Conclusions repeat the main messages, optionally with a key visual from the talk. (p.26–27, 48)
- Bring people back after a hard part: "I just explained ...; next ...". (p.27)
- Prepare backup slides for expected questions. (p.27)
- Common mistakes: too many slides, slides too packed, fearing that clear explanations look trivial. (p.26)

## Text on slides

- People cannot read and listen at the same time; text and speech compete, images and speech do not. (p.17)
- Minimize text. No two consecutive text-only slides; aim for no text-only slides except overviews. (p.18)
- Reveal many bullets one at a time while speaking. Define every acronym and use few. (p.18)

## Visual design

- Simple template, no logo clutter (logos only on first and last slides). Black on white, or bright on dark. (p.29)
- Sans-serif font (Calibri), at most two fonts; code in Courier New bold. (p.30)
- Math typeset with LaTeX, not the Office equation editor. (p.31)
- Colors: pick a few and keep them. Avoid fully saturated colors; desaturate (HSL). Red works for emphasized text; for filled boxes use pastel colors, optionally with a darker outline of the same hue; dark desaturated boxes with white text also work. (p.32–36)
- Slide numbers are fine but gray. (p.16)

## Plots (viewgraphs)

- Title and axis labels present, fonts large, enough contrast (no yellow on white), sensible number format (13.25, 20.3 µs, 100,000). (p.38)
- The plot type must make the message jump out. (p.38)
- Y-axis label horizontal above the axis; drop the y-axis line when gridlines suffice; gridlines in the background layer. (p.41)
- Prefer direct labels on the lines over a legend. (p.42)
- Presenting a plot aloud: say what is compared, what x and y show, whether higher is better, walk through one data point, then give the conclusion. (p.39)

## Delivery

- Introduce yourself, name co-authors, speak clearly and not too fast, look at the audience. (p.13)
- Watch other talks and practice putting into words why something works or not. (p.48)
