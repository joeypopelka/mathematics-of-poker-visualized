# Plan: Mathematics of Poker, Visualized

> **Status: executed** (Nov 2026). All phases complete; see the root README
> for the result. Kept for the record.

Consolidate the per-chapter *Mathematics of Poker* (Chen & Ankenman) exploration
projects into one repo and one GitHub Pages site, organized by game family, and
finish the remaining work.

## Target structure

```
mathematics-of-poker-visualized/
├── index.html            ← landing page (the hub)
├── .nojekyll, README.md, PLAN.md
├── akq/
│   ├── limit/            ← NEW: ch 13 intro (the gateway game)
│   └── nl/               ← ch 15 project (moved in)
├── zero-one/             ← "[0,1] family" (ch 11, 16–18; formerly the ch 17 folder)
├── jam-or-fold/          ← ch 12 project (git mv, history intact)
├── multi-street/         ← NEW: ch 14 + 19
├── risk/                 ← NEW: ch 22–25
├── tournaments/          ← ch 26–28 project (moved in)
└── multiway/             ← NEW (light): ch 29
```

Site navigation order (pedagogical, by family): AKQ (13 → 15) · [0,1]
(11, 16–18) · jam-or-fold (12) · multi-street (14, 19) · risk (22–25) ·
tournaments (26–28) · multiway (29).

## Phases

0. **Setup** — commit this plan; `gh repo rename mathematics-of-poker-visualized`
   (old repo URL redirects; Pages URL becomes
   `https://joeypopelka.github.io/mathematics-of-poker-visualized/`).
1. **Restructure** — `git mv` ch12 files → `jam-or-fold/`; copy in ch15 →
   `akq/nl/`, ch17 → `zero-one/`, ch26–28 → `tournaments/`; fix stale links;
   placeholder root index; verify Pages.
2. **Close out the [0,1] family** — sequence-form LP to settle game #11's
   x-side exactly; resolve game #12's finite-pot value; write the family
   README/REPORT; family hub page.
3. **Ch 13 limit AKQ intro** (`akq/limit/`) — α = 1/(P+1) gateway page.
4. **Multi-street games** (`multi-street/`, ch 14 + 19) — geometric pot growth,
   equal pot-fraction betting, NL bluff sizing; fidelity table; explorer.
5. **Risk** (`risk/`, ch 22–25) — risk of ruin (known and uncertain win rate),
   Kelly, game selection, backing agreements; fidelity table; explorer.
6. **Multiway, light** (`multiway/`, ch 29) — single modest page.
7. **The site** — landing hub, home-links on every explorer, monorepo README
   with the coverage map, link audit.
8. **Finish** — rename local folder, push, verify every page 200, then (with
   user confirmation) remove the redundant original folders.

## Standing rules

- Exact methods over approximation; strict-margin verification; every book
  number reproduced or flagged as an erratum in a per-project fidelity table.
- Explorers are self-contained single-page HTML (vanilla JS/Canvas, no external
  requests) — work on Pages, locally, and as claude.ai artifacts.
- Heavy data stays checked in (`equity.f32`, `sweep.npz`, …) so Python steps
  rerun without redoing enumeration.
