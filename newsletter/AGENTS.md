# Neurotech Hub Monthly: newsletter guide

Ground rules for drafting the monthly newsletter in this folder and pasting it into Mailchimp.

**Latest full issue:** `202611/2026-11-the-ambidextrous-mind.html`. Use it as the working reference for layout, components and tone.

**Earlier reference:** `2026-10-curiosity-is-a-skill.html` (root). Keep past issues in the repo for content and style reference; do not delete them after sending.

**Folder layout**

- `AGENTS.md`, `brain.svg`, `brain-mark.png`, and the October HTML stay at the root of `newsletter/`.
- Each issue lives in `YYYYMM/` (for example `202611/`), named `YYYY-MM-short-title.html`.
- `archive/` holds Mailchimp exports and discarded masthead explorations. Do not paste those into campaigns.

## Workflow

1. Create or open the issue folder `YYYYMM/`. Copy the latest full issue (or its skeleton) and rename to `YYYY-MM-short-title.html`.
2. Preview the file in a browser at desktop width (about 700px) and phone width (about 390px).
3. Upload any new images to Mailchimp **Content Studio**, copy each absolute URL, and put that URL in every `src` before pasting into Mailchimp.
4. In Mailchimp's new builder, add one **Code** block and paste everything between the `BEGIN MAILCHIMP CODE BLOCK` and `END MAILCHIMP CODE BLOCK` comments. The `<html>`, `<head>` and `<body>` around those markers exist only for local preview.
5. Send a Mailchimp test email and check it in Gmail, Outlook and Apple Mail (desktop and phone) before scheduling.

Files in `archive/` saved from Mailchimp (for example `Neurotech Hub Monthly - October 2026.html`) are reference only. Ignore Mailchimp's wrapper: the share bar, translate menu and template scaffolding. The issue's real content is inside `<body id="archivebody">`, after the archive bar.

## What Mailchimp handles (do not duplicate)

- **Subject line and preview text.** Set them in the campaign settings, not in the HTML. Don't add a hidden preheader.
- **Legal footer.** Mailchimp's footer supplies the copyright, mailing address, "update your preferences" and "unsubscribe" links. Our HTML ends after the credit line.
- **Merge tags.** Merge tags work inside Code blocks. Use `*|ARCHIVE|*` for "View this email in your browser". In a local preview they show as literal text, which is expected.

## Images (Content Studio)

Mailchimp does **not** import or re-host images when you paste HTML into a Code block. Whatever absolute URL is in `src` is what recipients load.

- **Host everything in Content Studio.** Prefer Mailchimp over the WordPress media library so sent issues don't depend on the website staying put.
- **Upload → Copy URL → paste into `src`.** New photos, diagrams and the masthead mark all go through Content Studio. Reuse existing `https://mcusercontent.com/...` URLs from past issues when the asset already lives there.
- **No relative paths in the Code block you paste.** Local filenames are fine only while previewing in this folder.
- **No inline SVG.** Gmail, Outlook and Mailchimp's Code block strip or ignore SVG. Rasterize marks (PNG with transparency) and host the PNG.
- **Masthead mark.** Source SVG: `brain.svg`. Email PNG: `brain-mark.png` (brand red `#a51417`, transparent background). Uploaded once to Content Studio. Reuse this URL in every issue:

  ```
  Masthead mark Content Studio URL:
  `https://mcusercontent.com/6391f76836f7cfd6d42fd5c61/images/1e2b2008-8650-71c4-259a-f74d64499090.png`
  ```

- **Sizes.** Upload at about 2× display width so images stay sharp on high-resolution screens. Typical uploads: intro square ~600×600 (display 200px); tool / column thumbs 720×480, 3:2 (display ~176–180px); full-width screenshots ~1000–1120px wide (display 502–560px).
- **Borders.** Screenshots and UI captures usually get `border:1px solid #e3e3e3` so they don't dissolve into the white letter. Prefer a light border over `box-shadow` (Outlook often drops shadows).
- **File weight.** Prefer JPG for photos when transparency is not needed. Aim under ~300–500 KB per image when possible. GIFs animate in many clients, but Outlook on Windows shows only the first frame—make that frame readable on its own.

## Mailchimp Code block rules

From Mailchimp's [Code block tips](https://mailchimp.com/help/use-code-content-blocks-new-builder/#Code_block_tips):

- **No JavaScript.** Mailchimp strips it.
- **No word-processor HTML.** Write in a plain text editor or here, never Word or Publisher.
- **Inline CSS.** Every style that matters goes in a `style` attribute. A `<style>` block at the top of the Code block is only for media queries (mobile) and progressive extras. If a client drops it, the email must still read correctly.
- **Media queries for mobile.** Use a `<style>` block with `@media` rules; classes are allowed.
- **Supported elements only.** Mailchimp removes anything else. Stick to `table`, `tr`, `td`, `div`, `p`, `h1`–`h4`, `a`, `img`, `span`, `strong`, `em`, `ul`, `ol`, `li`, `br`, `hr`, `style` and `link`. No forms, video, iframes, SVG or embedded scripts.

## Email-safe HTML

- **Lay out with tables.** No flexbox, grid or `position`. Side-by-side content uses table cells that stack on phones through a media query (`.nth-col`, `.nth-col-gap`, `.nth-col-img`, `.nth-col-stack`, `.nth-hide-sm`).
- **Intro float (exception).** The intro square may use `float:right` so body copy wraps beside it. Clear with an empty `clear:both` div after the paragraphs. On phones, `.nth-float-img` sets `float:none` and full width above the text. Outlook on Windows ignores floats and shows the image above the copy—that fallback is acceptable.
- **Width.** The issue is fluid up to 640px wide (`width="100%"` plus `max-width:640px`), with 40px side padding on desktop (`.nth-pad`) and 20px on phones.
- **Images.** Every image gets an absolute `src`, a real `alt` that describes the picture, a numeric `width` attribute, and `style="display:block; width:100%; max-width:…; height:auto; border:0;"` (or the light `#e3e3e3` border when needed). Optional `border-radius:6px`. Keep text out of images where possible, because many clients block images by default.
- **Buttons.** Build buttons as a table cell with a background colour and a padded link inside, so they still render in Outlook.
- **Fonts.** Web fonts are a bonus. Gmail and Outlook ignore them, so every `font-family` needs a system fallback (Georgia for headings, Helvetica or Arial for body text).
- **Colour and contrast.** Body text stays dark on white. Never rely on a background image to carry meaning or contrast.
- **Links.** Every link uses a full `https://` URL (or `mailto:`). Check each one before sending.

## Content and voice

- **Keep the author's words.** Restyling or reformatting never changes the copy, links or facts without asking. Suggest phrasing fixes; don't silently rewrite.
- **Flag, don't fix silently.** Suspected typos, wrong links or mismatched alt text get listed in the summary for review, not changed quietly.
- **Voice.** First person ("I"), casual but professional. Use "we" when a project or tool is explicitly collaborative.
- **Structure.** Every issue has: view-in-browser → masthead → intro (+ optional square image) → body sections → sign-off + credit. Mailchimp's footer follows. No custom black closing band and no WashU / corporate header chrome.
- **Intro.** Short, standalone and philosophical. Hint at the month's theme without listing every section. Split into short, pithy paragraphs so a square image can sit beside the text. The last line may bring it back to the Hub or this month's issue.
- **Sign-off.** Casual closing that fits the month (holiday, travel, meet-up, thanks). Not a recycled "Thanks for staying curious" by default.

## Style

Editorial and crafted, not corporate. Use WashU red as an accent, not as a full-bleed brand chrome. Prefer character in typography and spacing over institutional header bars. Avoid full-width hairlines in the masthead; short red accent rules are preferred.

### Tokens

| Token | Value | Use |
| --- | --- | --- |
| Red | `#a51417` | Accent, eyebrows, links, buttons, italic title word, masthead mark, short rules |
| Ink | `#1a1a1a` | Titles, strong emphasis |
| Body | `#3d3d3d` | Body copy, italic sign-off |
| Muted | `#6b6b6b` | Captions, credit, masthead subtitle, view-in-browser, tool meta labels |
| Rule | `#c8c8c8` | Card border, placeholder dashes |
| Hairline | `#e3e3e3` | Section and list dividers, image borders |
| Surface | `#f9f9f9` | Event / callout card fill |
| Page | `#f2f2f2` | Preview / view-in-browser strip behind the white letter |
| Radius | `6px` | Cards, buttons, images |
| Serif | `'Libre Baskerville', Georgia, 'Times New Roman', serif` | Titles, masthead subtitle, sign-off |
| Sans | `'Source Sans 3', 'Source Sans Pro', 'Helvetica Neue', Helvetica, Arial, sans-serif` | Body, eyebrows, buttons, captions |

Load Libre Baskerville and Source Sans 3 via a Google Fonts `<link>` at the top of the Code block. Fallbacks must still look correct when the link is ignored.

### Masthead (approved A4)

Centered white masthead. Do not use a black or full-bleed red header, and no full-width hairlines in the masthead.

1. The red brain mark (`43×29` display size; PNG hosted in Content Studio; links to `https://neurotechhub.wustl.edu/`), flanked by short red rules: `56×2px`, `#a51417`, built as table cells with a background colour, `16px` gap to the mark.
2. Issue title in serif, ~46px / 54px (34px / 40px on phones). Emphasize one word when it fits with `<em style="font-style:italic; color:#a51417;">…</em>`.
3. Subtitle in grey italic serif, ~15px: `The Neurotech Hub Monthly · {Month Year}` ("Neurotech Hub" links to the site; the middle dot is red).
4. No rule under the masthead. Whitespace (36px) separates it from the intro.

### Recurring components

- **Eyebrow.** Red uppercase sans, 12px, letter-spacing `0.14em`, above each section `h2`. Partner / meta labels in three-up columns may use muted `#6b6b6b` instead.
- **Section title (`h2`).** Serif, 28px / 36px (24px / 31px on phones), ink.
- **Subsection title (`h3`).** Serif, ~19–22px, ink.
- **Body.** Sans, 17px / 27px, `#3d3d3d`. Links underlined in red. Tool blurbs may use 15–16px when space is tight.
- **Bold emphasis.** Use sparingly, only where emphasis really matters: at most one short phrase per paragraph, and not in every blurb. `<strong style="color:#1a1a1a;">…</strong>`.
- **Caption.** Sans, 14px / 21px, muted; leading strong label in body colour.
- **Numbered list.** Red serif numerals in a narrow left column; hairline borders between rows.
- **Event / callout card.** `#f9f9f9` fill, `#c8c8c8` border, `4px` red top border, `6px` radius. Eyebrow + title + copy + optional image + red button. Use for a primary CTA (event, guide), not every section.
- **Button.** Table cell, `#a51417` background, white bold sans label, `14px 28px` padding, `6px` radius.
- **Text CTA.** Bold sans, red, no underline: `Label&nbsp;&rarr;`.
- **Image + text row.** Two `.nth-col` cells (image ~180–200px); stacks on phones with `.nth-col-gap`. On phones, drop the duplicate top border on the text cell (`.nth-row-text { border-top: 0; }`).
- **Three-up columns.** Three equal cells with `.nth-hide-sm` spacers between them; stack with `.nth-col-stack` padding on phones. Keep blurbs similar in length so the row stays balanced.
- **Equal image pair.** Two `.nth-col` cells of equal width.
- **Section divider.** Single hairline `#e3e3e3` in a padded row between major sections (not in the masthead).
- **Sign-off.** Centered. A short red accent bar (`56×2px`, `#a51417`)—no brain mark here. Then italic serif outro at ~18px / 30px, centred, `max-width:460px`, body colour, with one short phrase in red when it fits. Then muted credit at ~13px: `This email was produced by Matt Gaidica, PhD (gaidica@wustl.edu), Director of Neuroscience Innovation and the Neurotech Hub.`

### Tone of layout

- One job per section: eyebrow, one headline, short supporting copy, then media.
- Prefer whitespace and short accent rules over boxes and full-width hairlines. Cards are for a primary call to action, not every section.
- Character comes from the serif titles, the red italic accent, the brain mark in the masthead, and a crafted sign-off—not from WashU header chrome or dark bands.
