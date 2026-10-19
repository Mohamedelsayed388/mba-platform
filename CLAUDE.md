# MBA Platform: maintainer notes

MBA Platform is Mohamed Elsayed's installable study app (PWA) for his Executive MBA cohort, published on GitHub Pages at https://mohamedelsayed388.github.io/mba-platform/. The first course is **Finance for Non-Financial Managers** (lecturer: Dr. Ahmed Amin Hashim, Arab Academy for Management, Banking & Financial Sciences). After every lecture, a new **issue** is added and published within 48 hours.

## Files

- `src/hub.html` is the **only file to edit by hand**: the page markup, styles, issue articles and the data arrays.
- `tools/build.py` wraps `src/hub.html` into `index.html`, adding the app metadata, install button and offline worker registration. Run `python3 tools/build.py src/hub.html index.html` after every edit, and never edit `index.html` directly.
- `sw.js` is the offline cache. **Bump `VERSION`** (for example `mbap-v1` to `mbap-v2`) on every publish so installed phones pick up the new issue.
- `manifest.webmanifest` and the icon PNGs rarely change. `tools/icons.py` regenerates the icons.

## Adding a new lecture (the weekly task)

1. Read the new lecture slides in full, and any study guide Mohamed shares.
2. In `src/hub.html`:
   - Add an `ISSUES` entry `{n, title, sub}` and update `NEXT`.
   - Add an `<article data-issue-body="N">` in the Issues section, and a button `<button aria-pressed="false" data-issue="N">` in `#issue-seg`. The newest issue is the one shown by default (`aria-pressed="true"`, and the others `hidden`).
   - Update the masthead "Latest" card (`Latest · Issue NN`, title, 3 bullets, and the `data-open-issue` value).
   - Append to `CARDS` (`{i, t, full?, en, f?, ar}`; give every abbreviation a `full` name, and never rename an existing `t`, because saved progress is keyed on it), `QUIZ` (`{i, s, o:[[text, why, 1 for correct]], st, ar}`) and `FORMULAS` (`{i, t, f, r}`), tagging every item with the issue number `i`.
   - Update the CFO-task tree statuses and the course-part pillars if the lecture moves the course forward.
3. Build, bump the `sw.js` version, check that the page script parses (`node --check`) and do a single phone-width screenshot.
4. Commit and push to `main`. GitHub Pages redeploys within about a minute.
5. Mirror the change to the Claude artifact copy if one exists in the conversation.

## Backlog: add with the next lecture

Clear each item once it has shipped.

- (empty)

## Content style (agreed with Mohamed)

- Each section starts in English, MBA style: definitions, formulas, worked numbers.
- It then moves straight into an Egyptian Arabic explanation of the practical logic, written as an experienced Egyptian lecturer would say it. There are **no** headings such as "Arabic intuition" or "Medical analogy".
- Engineering or medical analogies are woven into the sentence itself, because the cohort is mostly engineers and doctors.
- Every abbreviation shows its full name where it first appears (headings, tool tiles, card fronts), not only inside the explanation.
- Any section with a formula gets a worked numeric example and a slow explanation of each part, not just a definition.
- Quiz questions are scenario-based, with step-by-step working and a reason why each wrong option is wrong.
- Stay faithful to the slides. Where a slide looks wrong (for example slide 17 of lecture 2, "horizontal" listed under vertical analysis), flag it in a note instead of silently fixing it.
- Never reproduce slides verbatim. Never present the platform as an official Academy publication; the footer disclaimer stays.
