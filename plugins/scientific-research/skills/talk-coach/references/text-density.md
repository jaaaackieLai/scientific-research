# Text density on a slide

The user's default body size is 24 pt. Earlier decks often had slides that overflowed or looked empty. This file holds the measured capacity and the length rules; the rules are still being worked out, so add to the log at the bottom whenever the user corrects a slide.

## Measured capacity (`font-size-24-layout.png`)

The image is a 16:9 slide rendered at 1913 × 1071 px (about 2 px per pt). Template: gray section bar at the top with the section name right-aligned, title 44 pt bold, subtitle 24 pt bold underlined, body 24 pt, gray `n / N` page number bottom right.

| Item | Measurement |
|---|---|
| Body line, full width | about 85 characters including spaces, which is 13–15 words of technical English (17 short words in the image) |
| Body line, half width (figure on the other side) | about 40 characters, 6–7 words |
| Line pitch at 24 pt | about 29 pt (58 px) |
| Spacing before a bullet / sub-bullet | 12 pt / 6 pt |
| Title at 44 pt bold | about 50 characters on one line |
| Subtitle at 24 pt bold | about 80 characters on one line |
| Chinese at 24 pt | about 37 characters per full-width line |

The image holds 8 body lines (a 3-line paragraph, 3 bullets, 2 sub-bullets) under a title and subtitle, with room for about 2 more lines above the page number. **Hard limit: 10 body lines with a subtitle, 11 without.** Bullet spacing eats into this: every 2 extra bullets cost roughly 1 line.

## Counting lines

For each sentence: `lines = ceil(characters / 85)` at full width, `ceil(characters / 40)` at half width. Sum over the slide and add 1 line per 2 bullets for spacing. Report the total as `n / 10` with each slide.

## Length rules (current version)

- Body text is complete English sentences, one idea per sentence. This overrides Püschel's "bullets need not be sentences".
- One sentence per bullet; aim for one line (up to ~14 words), allow two. A sentence that needs three lines is two ideas: split it.
- Text-only slide: 5–8 lines. Under 4 looks empty; either add a figure or merge with a neighbouring slide. Over 10 overflows.
- Slide with a half-width figure: 3–4 sentences on the text side.
- Slide with a full-width figure: one takeaway sentence (subtitle or a line under the figure), nothing else.
- At most two bullet levels. A sub-bullet adds detail to its parent; it is not a new point.
- Keep what the speaker will explain off the slide. The slide states the claim; the script gives the reasoning.

## Correction log

Add one line per correction: date, what was wrong, the rule it implies.

- (empty)
