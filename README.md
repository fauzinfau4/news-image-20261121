[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/fauzinfau4/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/fauzinfau4/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

# The World in One Day — Saturday 21 November 2026

A one-page newspaper front page for Saturday 21 November 2026, drawn
entirely in code with Pillow shapes and text. No photos, no downloaded
assets, no network calls — every pixel comes from the scripts in this repo.

## What's on the page

36 stories from six regions, all of them events that happened, or were
first reported, on Saturday 21 November 2026:

- **Lead story — Russia's overnight strikes on Ukraine.** A double-tap
  strike on Kryvyi Rih killed two people, among them a seven-year-old,
  and hurt 42; two more died at Lviv's railway station; two Russian
  missiles came down in Poland.
- **COP31 runs into overtime in Antalya.** Two weeks of talks ended on
  Friday with no final text; a third draft is due on Saturday morning,
  after the last one dropped every mention of fossil fuels and the
  $120bn adaptation figure.
- **BepiColombo reaches Mercury tonight.** After eight years and
  10 billion km, Europe and Japan's twin orbiters fire their thrusters
  at 19:24 CET for a 37-minute capture burn — the first time two
  spacecraft enter orbit around Mercury at once.
- **Plus:** Cyclone Akvan's aftermath in Odisha (no deaths, 372,000
  moved), KL Rahul's century in Wellington, GTA VI's split verdict
  (critics 99, users 5.3), Russell fastest ahead of Las Vegas
  qualifying, the top four seeds into the Turin semi-finals, Hyundai's
  new Elantra, Estonia closing its Russia crossings, the Pannun-plot
  sentencing, the Haiti blast, California's Nvidia subpoena — and
  23 more briefs, with a numbered world map and a DATE CHECK box
  listing the 19–20 November stories this page deliberately leaves out.

## Layout

A cream paper masthead with the date, a six-number statistics strip, a
region bar, three hero cards (Ukraine, COP31, Mercury), ten smaller
drawn cards, a numbered world map beside the briefs, a date-check box
and a footer naming every source.

## Run it

Render the poster:

```bash
python3 draw.py
```

That writes `entry.png` (1024×1024). Then ship it the way the grader
does:

```bash
MAKEFUN_OUTPUT_DIR=/tmp/out python3 main.py
```

`main.py` only copies `entry.png` byte-for-byte into the output
directory; it does no rendering and no network access. Running it twice
produces identical bytes, and running `draw.py` twice produces an
identical `entry.png`.

## Files

- `draw.py` — draws the whole front page with Pillow primitives.
- `main.py` — copies `entry.png` to `$MAKEFUN_OUTPUT_DIR` (or `/output`).
- `entry.png` — the rendered 1024×1024 front page.
- `LICENSE` — MIT.

## Sources

Reuters, AP, AFP, IMD, ESA, ATP Tour, UN News, Asia Today,
Sky & Telescope, ComicBook, Fextralife, RacingNews365, ESPN,
Jagran Josh, AppiSToS. Scheduled events of the day (BepiColombo's
19:24 CET burn, Las Vegas qualifying at 04:00 UTC, the Turin
semi-finals) are shown as due that day, not as results. Disputed
claims are attributed on the page, not stated as fact.

---

Built with [make.fun](https://make.fun/?ref=7tgjyx9m)
