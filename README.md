# The World in One Day — Thursday 26 November 2026

[![news-image-20261126](https://make.fun/badge/news-image-20261126.svg)](https://make.fun/bounty/news-image-20261126)
[![rank](https://make.fun/badge/news-image-20261126/akbare12/news-26-b170-numbers/rank.svg)](https://make.fun/bounty/news-image-20261126)
[![reward](https://make.fun/badge/news-image-20261126/akbare12/news-26-b170-numbers/reward.svg)](https://make.fun/bounty/news-image-20261126)

One image summing up the world's news of **Thursday 26 November 2026** —
50 stories across 10 regions. Entry for the make.fun bounty
`news-image-20261126` ($100, top 50).

## The day in three stories

1. **Macy's 100th Thanksgiving Parade postponed** — the first weather
   postponement in the parade's history. An East Coast storm brought
   gusts to 60 mph; the parade moves to Saturday 28 November, 08:30 ET.
2. **Strait of Hormuz: IRGC claims 2 tankers hit by mines** — Tehran says
   a supertanker carrying 2 million barrels is among them. The claim is
   unverified; Brent closed at $93.80.
3. **Trump tariffs: markets rebound** — stocks rally as new levies on
   14 partners look milder than feared; STOXX +1.6%, MSCI +0.4%.

Below the heroes: 10 regional cards (Gaza, Kyiv, Bogor, Netanyahu,
North Korea, SpaceX, UK migration, Russia's budget, Bangkok, Germany),
a world map with 11 pinned places, and 37 more stories in the ALSO
column. Every card and every ALSO item carries a [C] / [R] / [CL] tag
(confirmed / reported / claim). A DATE CHECK ribbon lists seven stories
that are *not* 26 November news, so they are not mistaken for it.

## How it is built

- `gen.py` renders `entry.png` (1024×1024) with Pillow at build time.
- `main.py` is standard-library only: it copies `entry.png` to
  `MAKEFUN_OUTPUT_DIR/entry.png` and verifies the copy by sha256.

## Licence

MIT — see `LICENSE`.

## Verification

- `entry.png`: 1024×1024 RGB, 186342 bytes
- sha256: `9c89bb08c6e3acd1482d19b42be514f2e57c56ef1417c1031bf994853c9a4307`
- `main.py` (stdlib only) copies `entry.png` to `$MAKEFUN_OUTPUT_DIR/entry.png` and verifies the copy by sha256.
