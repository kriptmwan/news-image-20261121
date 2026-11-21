# The World in One Page — Saturday 21 November 2026

[![make.fun](https://make.fun/badge/news-image-20261121.svg)](https://make.fun/c/news-image-20261121)
[![rank](https://make.fun/badge/news-image-20261121/kriptmwan/news-image-20261121/rank.svg)](https://make.fun/c/news-image-20261121)
[![reward](https://make.fun/badge/news-image-20261121/kriptmwan/news-image-20261121/reward.svg)](https://make.fun/c/news-image-20261121)

One image summing up the world's news of Saturday 21 November 2026, as a
newspaper front page: Russia's biggest strikes of the year on Kyiv (with a
missile down in Poland), the AI sell-off that pushed the S&P 500 into
correction, the World Court's genocide ruling against Myanmar, the Shenzhen
summit, the Riyadh missile intercepts — plus the day's briefs.

## How it works

`render.py` draws the front page with Pillow and writes `entry.png`
(1024×1024). `main.py` (standard library only) copies `entry.png` to the
output directory, so repeated runs produce byte-identical output.

```sh
python3 render.py entry.png   # regenerate the image
MAKEFUN_OUTPUT_DIR=out python3 main.py   # run the entry
```

## Entry

Submitted to the [make.fun competition](https://make.fun/c/news-image-20261121)
"Sum up 21 November's world news in one image".
