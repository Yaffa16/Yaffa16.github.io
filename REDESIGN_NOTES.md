# Weird With Code — light redesign notes (v2)

This replaces the earlier dark version. The register now: near-white ground
(#fafafa), micro-sized type, media doing the talking. The interaction set:
counter preloader, mouse-trail images on the intro, scroll-eased project feed,
hover-peek on the index, a contact overlay (Esc closes it), and soft page-fade
transitions. All original interaction code written for this site — nothing was
copied from anywhere.

The previous dark build is preserved alongside as `*_dark_backup.*` files if
you want to compare or revert.

---

## Same architecture, new skin

`assets/works.js` is still the single source of truth for all 22 projects —
edit only that file to add work. `wwc.css`, `wwc.js` and `project.css` kept
their filenames but were rewritten, which is why none of the 22 project pages
needed touching this round: they import by name.

## Interaction reference (new)

| Attribute | Effect |
|---|---|
| `data-veil` (on body) | Counter preloader, once per session |
| `data-trail` + `data-trail-srcs='[...]'` | Mouse-trail images in that zone |
| `data-rise` / `data-rise-group` | Soft fade-in reveals (unchanged API) |
| `data-drift` | Gentle scroll parallax on the img inside |
| `data-peek="img.jpg"` | Hover media following the pointer |
| `data-overlay-open` / `data-overlay-close` | Contact overlay controls |

Legacy dark-system attributes (`data-mag`, `data-say`, `data-lines`) are
tolerated and inert or equivalent, so the patched project pages run unmodified.

## Accessibility floor

Reduced motion: no preloader, no trail, no peek, no drift, no page fades —
content simply appears. Touch: trail, peek and the "Move" prompt are removed.
Overlay traps Esc, restores focus on close, and is aria-hidden when shut.

---

# Earlier notes (dark version, superseded)


Dark rebuild in the style you asked for: oversized condensed type, numbered
works index, cursor-driven interaction. Your neon green (`#39ff14`) is kept as
the accent, so the identity is still yours — it just moved onto a black ground
where it reads a lot harder.

---

## ONE MANUAL STEP

Rename this file in your repo — I renamed it in my copy but the video itself is
too large to ship in this zip:

```
work/2024/voice_Box.mp4   ->   work/2024/voice_box.mp4
```

`voice_box.html` references the lowercase name. This works on macOS (which is
case-insensitive) but **404s on GitHub Pages**, which is not. Pre-existing bug,
worth fixing while you're in there. In git:

```bash
git mv work/2024/voice_Box.mp4 work/2024/voice_box.mp4
```

---

## How to install

Unzip over your repo root, keeping the folder structure. Every path in here
matches your existing layout, so files land where they belong and overwrite the
old versions. Your `images/`, `work/*/` media, and `assets/Profile_Photo.jpg`
are untouched.

Nothing is deleted. The originals of the three rewritten pages are saved
alongside them as `*_original_backup.html` in my working copy — but since your
repo is under git, `git diff` is the better way to review.

---

## What's new

### `assets/` — the shared layer

| File | Does |
|---|---|
| `wwc.css` | Design tokens, cursor, reveals, the works-index row, header, marquee, footer |
| `wwc.js` | Cursor, magnetic hover, scroll reveals, hover preview, marquee, anchor scroll |
| `works.js` | **Single source of truth for all 22 projects** |
| `project.css` | Dark re-skin for the existing project-page template |

**To add a project**, edit `assets/works.js` only. Drop an object at the top of
the right year:

```js
{ t: 'Title', h: '2026/slug.html', i: '2026/slug.jpg',
  g: 'Tag · Tag', d: 'One-line description.', v: 'Commission' }
```

The homepage list, the works page, and the running 00–21 numbering all update
themselves. Previously this data was duplicated inside `work/work.html`, which
is why the homepage and works page could drift apart.

### Rewritten pages

- **`index.html`** — full-height type hero with line-by-line reveal, marquee,
  the 22-row works index, about, contact.
- **`work/work.html`** — works index grouped by year, with year filter chips.
- **`work.html`** (root) — same page, generated with corrected relative paths.
  44 links across your project pages point here, so it had to stay real rather
  than become a redirect.
- **`work/bio.html`** — about + facts strip + contact. Your dark-mode toggle is
  now a **light**-mode toggle (the site is dark by default) and still persists
  to `localStorage`.

### Patched automatically (22 files)

Every `work/<year>/*.html` got the shared CSS/JS injected, scroll reveals on
hero/sidebar/media blocks, magnetic nav links, and the dark override. Their old
inline cursor is hidden via CSS rather than deleted, so nothing was ripped out.

### Redirects (8 files)

`about.html`, `work/about.html`, `work/contact.html` and the whole `extras/`
folder were orphans — nothing linked to them, and they'd have loaded as
unstyled light pages for anyone with an old bookmark. They now redirect to the
canonical pages.

---

## Interaction reference

Add these attributes to any element on any page:

| Attribute | Effect |
|---|---|
| `data-mag="0.4"` | Magnetic pull toward the pointer (value = strength) |
| `data-rise` | Fade + rise when scrolled into view |
| `data-rise-group="90"` | Stagger the direct children, 90ms apart |
| `data-lines` | Split a heading on `<br>` and reveal line by line |
| `data-say="Open"` | Text that appears beside the cursor on hover |
| `data-peek="img.jpg"` | Image that trails the cursor |
| `data-marquee="0.55"` | Scrolling strip (value = px per frame) |

Delay any single reveal with inline `style="--d:400ms"`.

---

## Accessibility floor

- `prefers-reduced-motion` removes the custom cursor entirely (restoring the
  native one), disables the marquee, and shows all content immediately.
- Touch devices never get the hidden cursor or the hover preview.
- Keyboard focus is visible on every interactive element.
- The works rows are real `<a>` elements, so they tab and open normally.

---

## Verified

Rendered in Chromium at 1440px and 390px. 241 internal references checked, no
broken links. Cursor, magnetic hover, hover preview, line reveals, works
rendering, year filter, and all reduced-motion fallbacks pass.

**Note:** fonts were blocked in my test environment, so any screenshots you saw
rendered in Arial fallback. With Barlow Condensed the headlines will be
noticeably narrower and more condensed than they appeared.

---

## v2.1 — full-site pass ("make the entire website")

Every page is now on the light system, not just the core four:

- All 22 project pages: old header replaced with the unified corner nav
  (Projects / Index / Studio / Contact), the contact overlay injected, and
  the footer back-link retargeted to the canonical index page.
- The fixed header now uses white type with `mix-blend-mode: difference`,
  so it reads near-black on the paper ground and flips to white when dark
  project media scrolls underneath it. One rule, legible everywhere.
- All 8 legacy redirect stubs (about, contact, extras/*) restyled light so
  even a stale bookmark shows a consistent page for the split second before
  forwarding.

Whole-site link integrity re-checked after the pass: 231 internal
references, zero broken. Overlay, reveals, and Esc-close verified working
on project pages directly.

---

## v3 — the deck homepage

Rebuilt the homepage around a 3D cascading deck once real reference
screenshots were available: every project as a tilted pane receding along a
bottom-left -> top-right diagonal on white.

Interaction set (all original code):
- Wheel or drag scrubs through the deck; the front pane recycles to the
  back. After 400ms of stillness the deck snaps to the nearest whole card.
- Mouse position parallaxes the whole stack.
- Hovering a pane flattens it toward the viewer and shows the project
  title bottom-left; press-and-release on a pane opens the project (the
  panes animate every frame, so navigation keys off the pane captured at
  pointer-down rather than the browser's synthesized click, which can be
  swallowed when an element moves between press and release).
- Overview / Index toggle bottom-right switches between the deck and a
  flat list on the same page.
- The nav is now four bordered boxes top-left on every page.

Touch and reduced-motion users get the Index view directly; the deck
requires a fine pointer and motion.

---

## v3.1 — deck matched to the reference video

- Panes rescaled to ~40vw squares; the stack now runs corner to corner
  (front pane bleeds off the bottom-left, deep panes exit top-right).
- Milder depth shrink so far panes stay large, plus a white depth haze
  that thickens with distance.
- Drag scrubs near 1:1 along the diagonal (vertical drag counts too).
- Click on empty deck space advances one card; click on a pane opens it.
  Wheel scrubbing still works as well.
- Tuning knobs in index.html: STEP_X/STEP_Y/STEP_Z (path geometry),
  0.0058 (drag ratio), TILT (pane rotation), --cardw in wwc.css (size).

---

## v3.2 — mirrored deck, glass, hover-open

- Deck direction flipped: front pane now bleeds off the bottom-RIGHT,
  the stack recedes to the top-left; pane tilt mirrored to match.
- Glass treatment on every pane: slight image translucency, edge light,
  diagonal sheen, plus the depth haze.
- Hovering a pane shows a small popup at the cursor with the project
  name, number and year; the popup flips inward near screen edges.
- Hover-to-open: holding the hover ~0.9s (DWELL in index.html) opens the
  project. Click still opens instantly. Only the front ~3 panes are
  interactive — with panes covering most of the screen, hover-open on
  the whole stack would navigate whenever the cursor rested anywhere.
- Drag/click scrubbing unchanged; dwell never fires mid-drag, and a
  back/forward return resets the fade so the page is never stuck blank.

---

## v3.3 — diagonal direction settled

Front pane bottom-left, stack receding to the top-right, panes facing
left; sheen relit from the left edge to match. Glass, cursor popup,
dwell-open, front-pane gating, and drag/click scrubbing all unchanged
from v3.2.

---

## v3.4 — click-to-open fixed for real

Root cause found: the panes are links containing images, and the browser
starts a NATIVE image-drag the moment a pressed pointer moves a few
pixels. That native drag fires pointercancel and swallows the click —
so perfectly still clicks worked while every real trackpad click (which
always wobbles slightly) silently died.

Fixes:
- Native dragging disabled on panes (draggable=false, -webkit-user-drag:
  none, dragstart prevented) and pointercancel now clears drag state.
- Click slop widened to 14px so trackpad clicks classify as clicks.
- Movement under the slop no longer scrubs the deck.
- Hover-to-open (dwell) removed entirely: hover shows the name/year
  popup, CLICK opens the project. The self-firing timer raced real
  clicks and navigated pages on its own.

Verified: sloppy click opens, clean click opens, drag starting on a pane
scrubs without navigating, long hover never navigates.

---

## v3.5 — true glass, glitch fixed

- "Blurry/lazy" look fixed: images render at full opacity again. Glass
  now comes from a narrow light streak across the pane, a 1px inner
  edge light, and a faint thickness shade — not a white wash. The depth
  haze only begins ~2 panes back and caps at 0.30.
- Black-slab glitch fixed: the dark sheets were the panes' large soft
  box-shadows stacking up (22 rotated shadow rectangles), showing
  through the then-translucent images. Shadows are now tight contact
  shadows and images are opaque; verified clean after repeated
  full-speed scrub stress.
- Confirmed by script: all 22 deck panes use exactly their own
  <project_name>.jpg — one image per project, no extras.

---

## v3.6 — clicks open, never scroll; panes face left

- Click-to-advance removed entirely. Clicks on empty space now do
  nothing; scrubbing is drag/wheel only. This was also the root of
  "clicking an image scrolls": panes beyond the front few were inert,
  so clicks on them fell through to the empty-space advance.
- Every visible pane is now clickable and opens exactly the project
  under the cursor (hit-testing follows the rotated quad, so what you
  see is what you click).
- Pane tilt flipped (TILT = -55): panes face left. The glass streak and
  thickness shade were relit to match the new facing.

Verified: mid-stack pane click opens that pane's project; empty-space
click neither advances nor navigates; drag still scrubs.

---

## v3.7 — glass frames, gaps, hover slide-out

- Each pane now has a glassmorphism FRAME around the image: translucent
  white fill, backdrop blur, 1px light border, soft shadow, rounded
  corners; the image sits inset with its own smaller radius.
- Gaps widened (STEP_X 172 / STEP_Y 128 / STEP_Z 128) and panes sized
  down slightly so neighbours no longer touch and a slid-out pane has
  room to come forward.
- Hovering slides the pane out of the stack: mostly toward the viewer
  (+300 z), a modest 64px lateral shift, tilt eased ~55%. The lateral
  shift is deliberately small — a bigger slide moved the pane out from
  under the cursor, fired mouseleave, snapped it back, and made clicks
  land in the gap it left. Verified hover stays stable for 1.2s solid.
- The cursor popup with project name and year is unchanged and shows
  during the slide-out.

---

## v3.8 — every pane hoverable; own hit-testing; ghost fix

- Root cause of "most images don't respond": the browser's hit-testing
  on this deep preserve-3d stack only ever resolved the front ~2 panes
  (elementsFromPoint even returned empty stacks where panes visibly
  painted). The deck now does its OWN geometric hit-testing: each frame
  stores every pane's projected screen quad (deck parallax + perspective
  included) and hover/clicks resolve against those quads, nearest pane
  first. Panes are pointer-events: none; the stage handles everything.
- Resting angle more frontal (TILT -38).
- Hover pulls ANY pane to the same fixed near depth with its screen
  position perspective-compensated, so the slide-out is equally
  dramatic at every rank and the pane grows in place under the cursor;
  rotation lags the slide (slide, THEN turn, ending near face-on).
- Ghost-pane glitch (empty frosted frames during hover sweeps) was
  backdrop-filter on per-frame-animated 3D layers intermittently
  dropping the pane's own image in Chromium. backdrop-filter removed;
  fill/border/shadow carry the glass look.

Verified with a real-mouse sweep: 7 distinct panes hoverable at rest
(every pane with visible area; deeper ones become reachable as you
scrub), mid-stack hover slides out crisp with correct caption, click
opens the exact hovered project, drag never navigates.

---

## v3.9 — rectangles, smaller panes, slide-right-then-turn

- Panes are now 4:3 rectangles (was square), 30% smaller
  (--cardw clamp(224px, 25vw, 392px)); hit quads updated to match.
- Hover sequence per spec: NO rotation in place. The pane first slides
  RIGHT out of the stack (+96px with the depth pull); the turn only
  begins once the slide is ~40% done, then completes near face-on.
- Sticky hover added: while a pane slides away from a stationary
  cursor, an 18%-expanded quad keeps the hover (and the click target)
  alive — no flicker, no snap-back loops. Pointer-down does a fresh
  strict hit-test first and uses the sticky pane only if the press is
  really within its margin, so a stale hover can never hijack a click
  elsewhere.

Verified: hover stable through the whole slide, click after the slide
opens the exact captioned project, teleport-click on empty space is
inert, drag never navigates.

---

## v3.10 — glass panes (blurry edges, sharp centre); slide-only, immediate

- True glass-pane look without backdrop-filter (which ghosts on
  animated 3D layers): each pane stacks TWO copies of its image — a
  blurred underlay and a sharp top layer whose edges fade out via CSS
  mask (mask-composite: intersect). Result: glassy blurry borders,
  sharp centre. One sizing gotcha fixed on the way: absolutely
  positioned images don't stretch to an inset box (replaced elements
  keep natural size), so dimensions are explicit.
- Hover NEVER rotates the pane any more — tilt is constant; the pane
  only slides right out of the stack with the depth pull.
- The slide is immediate: hover response lerp raised 0.12 -> 0.34
  (~90% out within 130ms). Verified all rotations stay at TILT during
  hover, popup shows name/number/year, click opens the exact project.

---

## v3.11 — harder left turn, near-square panes, 10-12 on screen

- TILT -38 -> -52: panes turned noticeably further left.
- Aspect 4:3 -> 5:4 ("less rectangle"); hit quads updated.
- Path tightened (STEP_X 118 / STEP_Y 88 / STEP_Z 96): measured 11
  panes meaningfully on screen at 1280x768, inside the requested
  10-12 band. Glass edges, immediate slide-only hover, popup, and
  click-through all re-verified after the change.

---

## v3.12 — hover is a pure sideways slide

The pane no longer travels toward the viewer on hover (that near-depth
pull is what made it "come up" and grow). Hover now changes X only:
same z, same tilt, same size — the pane simply steps right out of the
sequence and back.

The world-space shift is scaled by (P - z) / P so the ON-SCREEN slide
is the same distance whether the pane is at the front or deep in the
stack. SLIDE (index.html, currently 96) is the on-screen distance in px.

Measured: hovered pane moved +89px horizontally with no meaningful
change in size; click still opens the exact hovered project.

---

## v3.13 — three frame formats, 40 degree tilt

- Panes now render in one of THREE frame formats, cycled across the
  deck (index % 3), proportioned from the reference dimensions and
  expressed as fractions of --cardw so they scale with the viewport:
    0.75 x 1.00  (680 x 905, tall portrait)
    1.00 x 0.61  (904 x 550, wide landscape)
    0.91 x 0.77  (820 x 700, moderate landscape)
  The shared `aspect-ratio` rule is gone; JS sets --cw / --ch per pane
  and the CSS centres each on its own dimensions.
- TILT is now -40 degrees (negative = facing left).
- Hit-testing is per-pane: each card caches its own half-width and
  half-height, invalidated on resize. A single shared quad would have
  mis-mapped clicks now that panes differ in shape.

Verified at 1280x768: three distinct rendered sizes present
(240x320 x8, 320x195 x7, 291x246 x7), every pane at exactly -40deg,
11 panes on screen, 10 hoverable, and a click on each of the three
frame shapes opened exactly the hovered project.

---

## v3.14 — half the border glass, true 3D glass pane

Border glass halved across the board:
- --frame clamp(10px,1.2vw,18px) -> clamp(5px,0.6vw,9px)
- blurred underlay blur(12px) -> blur(6px), scale 1.04 -> 1.02
- sharp layer's edge fade band 10%/90% -> 5%/95%
So the image reads crisp almost to the edge with a thin glassy rim.

3D glass pane (not a flat sprite):
- .uv-card is transform-style: preserve-3d with a ::before face pushed
  translateZ(-7px) behind it, giving the slab real thickness that shows
  as the deck rotates.
- Bevelled inner edges (bright inset from upper-left, soft inset shade
  opposite) plus an inner glow read as glass thickness; the outer
  shadow is the contact shadow.
- A crisp angled specular streak, a rim light on the leading edge and
  a faint shade on the trailing edge complete the slab.

Re-verified after the change: no ghosting after a hard hover sweep
(0 panes missing their image), hoverable panes unchanged, click opens
the hovered project, drag still scrubs without navigating.

---

## v3.15 — panes rebuilt as glass sheets (reference match)

Matched to the supplied reference screenshot of the deck interaction:

- The white frame is GONE. Each pane is now a sheet of glass holding a
  full-bleed image; the glass reads as a thin lit rim (bright top and
  leading edges), a bevel, and a specular sweep — not a border.
- Panes are TRANSLUCENT (image opacity .88), so overlapping sheets show
  through one another the way real stacked glass does. This is the
  main thing that makes the stack read as glass rather than as cards.
- The blurred-underlay edge treatment and the edge mask were removed:
  with no frame there is no border to frost, and the reference shows
  crisp images to the very edge.
- Sheets enlarged (--cardw clamp(340px, 39vw, 600px)) and the path
  spacing retuned (132/96/104) for the reference's heavier overlap.
- Slab thickness kept: ::before face at translateZ(-5px), tinted like
  glass; corner radius dropped to 2px (reference sheets are near-square
  cornered).

Verified: 11 panes on screen, 8 directly hoverable at rest, click opens
the exact hovered project, no console errors.

---

## v3.16 — real slab depth, fog cut to a third

- Every pane now has actual 3D thickness: a side face standing
  perpendicular to the sheet (extending back from its right edge,
  which the left-facing tilt turns toward the viewer) plus a bottom
  face, both lit like glass. --thick is 11px.
- IMPORTANT fix found while doing this: `will-change: opacity` on the
  pane forces the element to flatten, which collapsed the 3D side
  faces into the sheet's plane (they measured 1px wide). Changed to
  `will-change: transform`; the faces now project correctly (~6px).
  Deep-end opacity fading still works, it just isn't hinted.
- Fog reduced to one third: haze factor 0.035 -> 0.0117, cap
  0.30 -> 0.10. Deep panes stay legible instead of washing out.

Re-verified: hover, popup, click-to-open, drag-scrub and the deep-end
fade all still correct.

---

## v3.17 — click previews the image, then loads the project

Clicking a pane no longer jumps straight to the page. The clicked pane
travels to the centre of the screen, turns face-on and scales up while
every other pane fades to zero; the project page loads once the
preview has landed (FOCUS_MS 420, navigation at LEAVE_MS 640).

Two robustness fixes came out of building it:
- The focus animation is TIME-BASED, not per-frame. The frame loop can
  run slowly (in a headless test it managed roughly one update per
  450ms), and a frame-count animation would then still be mid-move
  when the navigation fired. Clock-driven easing always completes.
- The caption's offsetWidth/offsetHeight were being read every frame,
  forcing a layout 60x/second. They are now measured only when the
  caption text changes.

Input is ignored once a preview starts (wheel and pointerdown bail on
`navigating`), and returning via back/forward clears the focus state.

Measured: preview lands dead centre (638,389 vs centre 640,384),
rotation eases to -1.2deg (face-on), every other pane at opacity 0,
then the correct project page loads.

---

## v3.18 — clockwise roll on every pane

Added ROLL (rotateZ, currently 7 degrees clockwise) to the pane
transform, matching the reference's leaning sheets: the roll opens up
the glass face and edge instead of presenting the pane square-on.

The hit-testing quads roll with it. CSS applies rotateZ before
rotateY in the transform list, so each corner is rotated in the pane's
own plane first, then swung into the scene — otherwise the clickable
shape would stay upright while the pane leaned, and clicks near the
corners would miss.

The roll eases back to 0 during the click preview, so the focused image
still lands square and face-on.

Knobs: ROLL and TILT sit together near the top of the deck script.

---

## v3.19 — 2 second hold on the preview

LEAVE_MS 640 -> 2000. The clicked pane still lands centre-screen in
420ms (FOCUS_MS), then the preview holds so the image can actually be
looked at before the project page loads.

Timed end to end: still previewing at 1.2s, navigation fires at ~2.0s,
correct project page loads.

---

## v3.18 — shallower tilt, pause before leaving

- TILT -40 -> -27: panes tilted back toward the right, so they sit at
  the shallower, more frontal angle of the reference render instead of
  turning hard left. 11 panes on screen.
- Click preview now holds: FOCUS_MS 420 to travel centre-screen, then
  HOLD_MS 1000 of stillness on the enlarged image, then the project
  page loads (LEAVE_MS = FOCUS_MS + HOLD_MS = 1420). Both constants
  sit together at the top of the focus block in index.html.

Verified: every pane reports -27deg, preview still on screen at 700ms
after the click, navigation lands on the correct project page.

---

## v3.19 — the real cause of the "wrong angle": keystoning

The panes looked wrongly tilted not because TILT was wrong but because
the perspective was too SHORT. At perspective: 2100px with the stack
running corner to corner, panes far from the vanishing point were
keystoned: their vertical edges sheared into leaning parallelograms,
so the deck read as skewed rather than uniformly angled.

Fixes:
- perspective 2100px -> 5200px and perspective-origin 44% 42% -> 50% 46%.
  Vertical edges now stay vertical across the whole stack, matching the
  reference render.
- STEP_Z 104 -> 260: a long perspective compresses depth, so the z step
  had to grow to keep the same sense of recession.
- Mouse parallax softened (rotateY 5deg -> 2.2deg, rotateX 4deg -> 1.6deg);
  at the old strength the sway added visible shear.
- P / P3 in the JS updated to 5200 and the origin offsets to the new
  50%/46%, so the geometric hit-testing still matches what is drawn.

Verified: 39 hover probes, 38 matched the painted pane exactly (the one
miss is an overlap seam resolving to the nearer pane); click opened the
correct project after the 1.42s preview; drag still scrubs.

---

## v3.20 — deck rotation removed

The mouse-parallax rotation of the whole deck was tipping the stack
backwards (rotateX) and swaying it sideways (rotateY) as the cursor
moved. Both are gone: `deck.style.transform = 'none'`. The only
rotation left in the scene is each pane's own left-facing TILT (-27).

The geometric hit-testing had been undoing that same parallax when it
projected the pane quads; that term is removed too, so the projection
is now a straight perspective transform and stays in sync with what is
drawn.

Verified: deck transform reads 'none' at five different cursor
positions (no rotation anywhere on screen); 37 hover probes with 36
matching the painted pane; click opens the correct project; drag still
scrubs.

---

## v3.21 — geometry matched to the measured reference angles

Measured angles from the reference render (pane corners 88.4 / 94.9,
diagonal 46.2) were used as targets and the deck tuned against a
measuring script rather than by eye.

- Diagonal: STEP_X / STEP_Y set to 99 / 109, a 46deg ratio.
  Measured path angle now averages 46.1 (reference 46.2).
- Corner angles: perspective 5200 -> 9500px, which reduces keystoning.
  Corners now span 86.4 - 93.7 across the front six panes
  (reference spans 88.4 - 94.9), i.e. a 7.3deg spread vs their 6.5.
- STEP_Z raised to 430 so the longer perspective does not flatten the
  recession, and the step length shortened to keep 10 panes on screen.
- P / P3 in the JS follow the CSS perspective (9500) so the geometric
  hit-testing still matches what is drawn.

A measuring script (reads the live CSS perspective, projects each
pane's own box, reports corner angles and the path angle per step) is
the right tool if these ever need re-tuning; guessing at these values
does not converge.

Verified: 10 panes on screen, 34 hover probes with 33 matching the
painted pane, click opens the correct project, drag still scrubs.

---

## v3.22 — all rotation removed, panes SHEARED to the measured angles

Two rotations were in the scene and both are gone: TILT (rotateY -27)
and ROLL (rotateZ 7). The panes are now sheared instead:

    transform: translate3d(...) skewY(32deg)

A rectangle skewed by 32deg has corners of 90-32 and 90+32. Measured on
the running page: 58.0 / 122.0 / 58.0 / 122.0, summing to 360.

Note on the supplied measurements (124.0, 82.0, 57.9, 167.4): those four
sum to 431, and any quadrilateral must sum to 360, so they cannot all be
corners of one pane — 167.4 is nearly straight, so that vertex landed
along an edge rather than on a corner. The shear was fitted to the
57.9 / 124.0 pair, which is self-consistent (57.9 + 124.0 = 181.9, i.e.
adjacent corners of a parallelogram).

Knock-on changes:
- Hit quads now shear with the panes (y shifts with x by tan(SKEW))
  instead of rotating. 48 hover probes, 0 mismatches — better than the
  rotated version, since a shear has no depth ambiguity.
- The click preview un-shears the pane to 0deg as it centres.
- .uv-edge / .uv-edge-b (the slab's side and bottom faces) are hidden:
  a side face is only visible when the pane rotates, and nothing
  rotates now.

SKEW (index.html, one constant) is the only angle control left.

---

## v3.24 — rotation restored, scale and composition fixed

The pure skew of v3.22/23 matched the measured corner angles but looked
wrong: on a 1920 screen the panes were also hitting the 600px size cap,
so the deck filled the window with huge leaning parallelograms. Fixed:

- Rotation is back (TILT -30, rotateY). The reference's corner angles
  come from a rotated plane in perspective, not a flat shear; the shear
  reproduced the numbers while losing the foreshortening that makes the
  panes read as glass. SKEW is kept as a constant but set to 0.
- Panes resized: --cardw clamp(210px, 19vw, 375px), roughly 40% smaller
  than the version in the screenshot.
- Spacing is now DERIVED from pane width (STEP_X 0.42w, STEP_Y 0.45w,
  STEP_Z 0.42w, recomputed on resize) instead of fixed pixels, so the
  composition is the same on a 1280 laptop and a 1920 monitor.
- Depth step deliberately shallow: a deep one compressed the far end of
  the stack into the vanishing point and left the right of the frame
  empty.
- Slab side/bottom faces visible again (they need rotation to show).

Measured: 11 panes at 1920x1080, 12 at 1440x900 and 1280x768, stack
spanning 70-75% of width in each case.

---

## v3.25 — TILT -45, three rotation axes, legible spacing

- TILT is now -45 (base yaw).
- Three new rotation variables sit beside it in index.html and are
  applied to the pane AND to its hit-testing quad, in the same axis
  order as the CSS transform, so clicks stay on the panes at any value:
      ROT_X  pitch (tips the top toward/away)
      ROT_Y  extra yaw, added to TILT
      ROT_Z  roll (spins the pane in its own plane)
  All default to 0. Tested at ROT_X 10 / ROT_Y -8 / ROT_Z 6: transform
  read rotateX(10) rotateY(-53) rotateZ(6) and hit-testing held at
  29/30 probes.
- STEP_Y: the requested 0.25 packed 19 panes on screen at -45deg and
  the images stopped reading. Swept 0.25/0.32/0.36/0.40/0.45 and
  settled on 0.36 — the flatter, wider stack asked for, with every
  pane still showing a readable image (14 panes at 1920, 15 at 1280).

Note: the occlusion metric used during the sweep (unoccluded bounding
box area) rated 0.25 as fine, which was wrong — the problem at -45deg
is foreshortening and translucency, not box overlap. Screenshots
decided it.

---

## v3.26 — hover flicker between panes fixed

Symptom: with SLIDE raised to 300, resting the cursor between two panes
made the hover flick on and off (measured: 8 changes in 700ms).

Cause: a feedback loop. The hit-testing quad was built from the pane's
CURRENT position, which the hover slide changes. Hover a pane -> it
slides 300px right -> the cursor is no longer inside it -> hover drops
-> it slides back under the cursor -> hover fires again. Between two
panes it is worse, because each one sliding away exposes the other.
The 18% sticky margin covered a 96px slide but nowhere near 300px.

Fix: hover hit-testing now uses each pane's RESTING geometry, so what
the cursor is "over" can never be changed by the hover itself. The
painted position is still tracked separately (drawnQuad) and clicks
accept either, so a click on a pane that has slid far away still opens
it. Depth ordering also comes from the resting position, so the
front-most pane under the cursor stays stable.

Verified: 0 hover changes at the point that previously flickered 8
times, 0 anywhere in a full-screen sweep, click-through and drag-scrub
still correct.

---

## v3.27 — no cursor-following image in the Index view

The image that floated beside the pointer in the Index list came from
the `data-peek` attribute on each row: wwc.js sees it and spawns the
#wc-peek element that trails the cursor. That attribute is now dropped
from the rows built in index.html, so the Index view is a plain text
list and #wc-peek is never created at all.

The peek behaviour is untouched on work/work.html, whose rows still
carry data-peek. Removing the attribute (rather than the JS) keeps the
change confined to the homepage, which is what was asked for.

Verified: 22 rows still render, no #wc-peek element exists after
hovering four rows, no [data-peek] left on the page, rows still open
their project.

---

## v3.28 — hover image removed from the index pages too

v3.27 removed the cursor-following image from the homepage's Index
view only. The same image was still appearing on the real index pages,
so `data-peek` is now dropped from the rows built in work/work.html and
the root work.html as well. No page in the site carries the attribute
any more, so wwc.js never creates the #wc-peek element at all.

The peek code itself is left in wwc.js, inert: it bails out when no
[data-peek] exists. Re-adding the attribute to any row would bring the
behaviour back.

Verified on all three list views (index page, root works page, homepage
Index view): 22 rows each, no floating image element after hovering
five rows, zero data-peek attributes. Year filtering still works (2017
-> 3 rows), no image after re-render, and rows still open their
project.

---

## v3.29 — one header everywhere; contact overlay fixed

Header was inconsistent: the homepage folded "Projects" into the
wordmark, while every other page carried a SEPARATE Projects tab, so
the boxes shifted position from page to page. Now all 26 pages use the
identical four boxes, with the wordmark itself acting as Projects:

    Weird With Code(R) Projects | Index | Studio | Contact

The current page's box is marked .now so you can see where you are.

Contact overlay:
- The header no longer disappears. The overlay was z-index 2000 and the
  header 900, so the overlay painted over it; the header is now 2100
  and stays visible and usable while contact is open.
- The Close button moved to the LEFT and the overlay's top row gained
  86px of padding so it clears the fixed header instead of colliding
  with it.
- While the overlay is open, body.uv-contact highlights the Contact box
  in the header, so it reads as the active tab.

Verified on homepage, index page, studio, a project page and the root
works page: identical four tabs on every one. Overlay checked: header
visible above it, Close left of the label, top row below the header,
Contact tab highlighted, Esc still closes.

---

## v3.30 — the deck is the landing view on mobile too

Previously touch devices were sent straight to the Index list, because
the deck was treated as hover-dependent. That was the wrong model: drag
and tap are the core interactions and both work fine with a finger.
Only the slide-out is hover-driven, and it simply does not apply on
touch.

- The `(hover: none)` fallback is gone. Only prefers-reduced-motion
  still falls back to the list.
- `touch-action: none` on the stage, so dragging scrubs the deck
  instead of panning the page (verified: window.scrollY stays 0).
- CLICK_SLOP is 22px on touch vs 14px with a mouse: fingers wobble more,
  and a wobbling tap was being classified as a drag.
- With no cursor to follow, the caption is pinned above the toggle and
  always names the FRONT pane, updating as you scrub.
- Phone layout: --cardw drops to clamp(160px, 62vw, 300px) under 700px
  wide, and the stack starts nearer the middle (BASE_X/BASE_Y switch at
  the same breakpoint) instead of mostly off-frame.
- Mobile header fixed: the boxes were overflowing the screen with
  CONTACT cut off. They now wrap to a second row and share it equally.

One bug found and fixed on the way: inside frame(), `capY` is a local
holding the caption's y position, which shadows the caption's year
element of the same name — writing to it threw
"Cannot create property 'textContent' on number".

Verified: iPhone 390x844 lands on the deck with 6 panes, drag scrubs
without scrolling the page, the caption tracks the front pane, and a tap
opens that pane's project. Tablet 6, laptop 9, desktop 11 panes.
