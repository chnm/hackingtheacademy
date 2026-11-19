# Hacking the Academy

Hugo source for [hackingtheacademy.org](https://hackingtheacademy.org/). Dan Cohen and Tom Scheinfeldt crowdsourced the book at RRCHNM in one week, May 21–28, 2010. The [edited volume](https://doi.org/10.3998/dh.12172434.0001.001) came out from the University of Michigan Press in 2013.

The original WordPress site only linked to the contributions, and by 2026 about 40% of those links were dead. This rebuild keeps a copy of each contribution on the site. Every copy links back to where the piece first appeared and to the Internet Archive snapshot it came from.

## Layout

- `content/<section>/_index.html` is a section page: the original list, exactly as written, with each link pointing at its captured copy. Pieces with no surviving copy anywhere keep their title, unlinked, labelled "(lost)", and get no page.
- `content/<section>/<slug>/index.md` is one contribution, as a page bundle that holds its images and PDFs. Front matter:

  | param | |
  |---|---|
  | `title`, `authors` | from the section list; `authors` is a taxonomy (`/authors/`) |
  | `weight` | position in the original list |
  | `note` | the list's trailing note, e.g. "(nominated by Matt Gold)", "(video)" |
  | `original_url` | the link as it appeared on the 2010 site |
  | `archive_url` | the Wayback snapshot nearest May 28, 2010 |
  | `published` | the post's own date, when the capture has one |
  | `captured_from` | `wayback`, `live` (the original page, fetched in 2026), `youtube` or `archive.org` (embedded) |

- `content/news/` holds the site's three posts, and `content/what-this-is-and-how-to-contribute.html` is the call for contributions, recovered from Wayback. The posts keep their old URLs, with the `/2010/MM/` WordPress paths as aliases.
- `static/theme/` is Jeremy Boggs's 2010 theme with WCAG fixes (focus outline, contrast, reflow) and its Adler font, recovered from Wayback.

Where a link had no archived copy, the script follows an archived redirect (moved blogs, bit.ly links) and captures its target. 2010 Google Docs are decoded from the editor page Wayback saved, and a still-public Google Sheet is kept as `spreadsheet.csv` and shown with the `csv` shortcode (`{{< csv file="spreadsheet.csv" columns="A,B" caption="..." >}}`).

## Rebuilding the captures

```bash
uv run scripts/capture.py ~/work/chnm/hackingtheacademy-src/hackingtheacademy.org
```

The script declares its Python version and dependencies inline ([PEP 723](https://peps.python.org/pep-0723/)), so [uv](https://docs.astral.sh/uv/) sets up its environment on the first run.

The argument is a mirror of the 2026 static site (`wget -m https://hackingtheacademy.org/`). Fetches are cached in `cache/` (gitignored), so a rerun only regenerates the files. The script overwrites `content/<section>/`, so make hand edits after the last run, or carry them over.

## Build

```bash
hugo server
```

## License

The code (`scripts/`, `layouts/`, `assets/`, the configuration) is MIT-licensed; see [LICENSE](LICENSE). It doesn't cover the content: the contributions under `content/` are their authors' work, republished from the 2010 book week with links to where each first appeared. The Adler web font in `static/theme/fonts/` is a third-party font under its own terms.
