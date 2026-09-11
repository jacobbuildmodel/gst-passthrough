# Handover brief for the website chat

You are placing files. You are not rewriting them. This brief is all you need; do not
ask for the research document behind it.

## Where each file goes

| From | To | Notes |
|---|---|---|
| `2026-09-08.md` | `content/economics/2026-09-08.md` | The article. Copy it, do not retype it. |
| `figs/fig1-signal-vs-noise.svg` | wherever the site serves post figures | Referenced as `fig1-signal-vs-noise.svg` |
| `figs/fig2-water-supply.svg` | same | Referenced as `fig2-water-supply.svg` |
| `figs/fig3-still-prices.svg` | same | Referenced as `fig3-still-prices.svg` |
| everything else in this directory | `github.com/jacobbuildmodel/gst-passthrough` | The analysis repo the article links to |

The article links to `github.com/jacobbuildmodel/gst-passthrough`. That repository has
to exist and be public before the draft flag comes off, or the link is dead.

## Rules

**Copy the article file rather than retyping or regenerating it.** Every number in it
has been checked against `number_manifest.csv`, which lists all 62 figures in the
prose with their source and the script that produced them. A retyping step silently
breaks that chain.

**Do not rewrite prose that reads oddly.** It is more likely deliberate than wrong.
Flag it and leave it. Three examples that look like errors and are not. Full
pass-through is written as 0.9346 per cent rather than 1 per cent, because a rise from
7 to 8 multiplies the price by 1.08/1.07. The word "significant" appears once, inside
a direct quotation from MAS, where it carries its ordinary meaning and not a p-value;
if the linter flags it, flag that back rather than editing a quotation. And several
sentences quote MAS verbatim in quotation marks: those are exact and must not be
paraphrased or reflowed in a way that changes what sits inside the quote marks.

**Do not clear `draft: true`.** A human does that.

**Do not substitute a guess for any placeholder link.** The GitHub URL is the only
external link in the body and it must point at the real repository.

**Front matter field names may not match this site's Hugo config.** The article uses
`title`, `date`, `draft`, `author`, `categories`, `description`. If the site uses
different keys, rename the keys and leave every value exactly as written. Do not
rewrite the description.

## What to verify after placing

1. **The asides render as collapsible blocks, not as literal text.** There is one
   aside, titled "What the pre-registered tests actually did". If `{{< aside >}}`
   is not the shortcode this site uses, say so rather than converting it to raw HTML;
   the publish gate strips raw HTML.
2. **Both figure shortcodes resolve and all three SVGs load.** The article uses
   `{{< figure src="..." caption="..." >}}`. If the site's figure shortcode takes
   different argument names, rename the arguments and leave the captions untouched.
3. **Dark mode does not break the figures.** Each SVG carries CSS custom properties
   with literal fallbacks and a `prefers-color-scheme` block. They were rendered in
   Chromium in both themes and checked for label collisions before shipping. Confirm
   they still look right in the site's own dark theme, which may set a different
   background.
4. **The markdown table in "Water is the one price that holds still" renders.** It is
   six rows and three columns. If the site's markdown renderer needs a different table
   syntax, convert the syntax and leave the contents.
5. **The linter passes.** The file is pure ASCII, contains no em dashes, no U+2212, no
   U+00D7, and no raw HTML. Linear read is 1,847 words, 47 over the 1,200 to 1,800
   default. That is deliberate and is explained in the note below. The word "significant" appears exactly once, inside a MAS quotation; if
   the linter's statistical-usage rule fires on it, flag that back rather than editing
   the quotation.
6. **Page renders at 390px phone width without horizontal scroll.** The figures use
   `viewBox` with `max-width:100%` and no fixed width. The three-column table in the
   water section is the likely offender if anything overflows.

## One deliberate departure, so you do not flag it as an error

The piece runs 1,847 words of linear read against a 1,200 to 1,800 default. The extra
47 words are in the paragraph about polytechnic fees, which reports that the
government-absorption prediction is confirmed in January 2023 and not in January 2024,
and gives the 2024 number. The shorter version reported only the year that confirmed
it. The number is visible in the public repository either way, so the longer and
honest version is the right one. Do not cut it back to fit the default.

## If something does not fit

Flag it back rather than solving it. The two most likely problems are the aside
shortcode and the figure shortcode, and both have safe answers: rename the wrapper,
keep the contents.
