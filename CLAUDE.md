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
4. Refresh the study-assistant sources: run `node tools/notebook_sources.mjs` (needs a local server on port 8769 serving the repo, and Playwright with `/opt/pw-browsers/chromium`). It writes `notebook/lecture-NN.html`. After pushing, add the new lecture page as a **Website** source in the NotebookLM notebook "MBA Platform · مساعد مادة الفاينانس" (https://notebook.google.com/notebook/bc0daf56-8425-4185-8a30-b8250d51d2c7), and refresh the existing sources if their content changed. The notebook also holds the lecture slide PDFs (the lecturer is fine with it, per Mohamed on 2026-10-21), so remind Mohamed to upload the new lecture's PDF there too.
5. Commit and push to `main`. GitHub Pages redeploys within about a minute.
6. Mirror the change to the Claude artifact copy if one exists in the conversation.

## Backlog: add with the next lecture

Clear each item once it has shipped.

- (empty)

## Content style (agreed with Mohamed)

- Each section starts in English, MBA style: definitions, formulas, worked numbers.
- It then moves straight into an Egyptian Arabic explanation of the practical logic, written as an experienced Egyptian lecturer would say it. There are **no** headings such as "Arabic intuition" or "Medical analogy".
- Examples and analogies come from **medicine and hospitals** and from **marketing**, woven into the sentence itself. Do not use ready-mix concrete or plant examples: Mohamed is the only one in the cohort from that field.
- Arabic is a first-class audience (students on the Arabic track): every section gets an Egyptian Arabic explanation after it, every issue heading has an Arabic subtitle (`<span class="h-ar">`), and every card and formula has an Arabic name (`tAr`).
- Every abbreviation shows its full name where it first appears (headings, tool tiles, card fronts), not only inside the explanation.
- Any section with a formula gets a worked numeric example and a slow explanation of each part, not just a definition.
- Quiz questions are scenario-based, with step-by-step working and a reason why each wrong option is wrong.
- Stay faithful to the slides. Where a slide looks wrong (for example slide 17 of lecture 2, "horizontal" listed under vertical analysis), flag it in a note instead of silently fixing it.
- On screen, call each lecture page a **Lecture** ("Lecture 03"), never an "Issue". The code still uses `issue` names (`ISSUES`, `data-issue`, `issueTag`); leave those as they are.
- Never reproduce slides verbatim. Never present the platform as an official Academy publication; the footer disclaimer stays.
