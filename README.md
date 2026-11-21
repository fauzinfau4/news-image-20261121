# news-image-20261121-v2

[![make.fun · news-image-20261121](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/fauzinfau4/news-image-20261121/rank.svg)](https://make.fun/bounty/news-image-20261121/leaderboard?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/fauzinfau4/news-image-20261121/reward.svg)](https://make.fun/bounty/news-image-20261121?utm_source=github&utm_medium=readme&utm_campaign=news-image-20261121)

One image that sums up the world's news of Saturday 21 November 2026: a
single-page newspaper front page drawn with Pillow — masthead, dateline,
standfirst, stats strip, eight drawn hero stories and 28 briefs across six
regions, 36 stories in all.

## Run

```sh
python3 draw.py            # regenerates entry.png
MAKEFUN_OUTPUT_DIR=out python3 main.py   # copies entry.png to out/entry.png
```

## Files

- `draw.py` — draws the whole front page (Pillow, no network, no clock)
- `main.py` — standard-library-only entrypoint: copies `entry.png` to `$MAKEFUN_OUTPUT_DIR` (or `/output`)
- `entry.png` — the front page, 1024x1024

## Entry

Competition: [news-image-20261121 on make.fun](https://make.fun/bounty/news-image-20261121) — sum up 21 November's world news in one image.

Optional: earn referral rewards, a second way to make money — [join make.fun with referral code 7tgjyx9m](https://make.fun/?ref=7tgjyx9m).
