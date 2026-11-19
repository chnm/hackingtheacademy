"""Rebuild Hacking the Academy's contributions as Hugo page bundles.

Reads the flattened WordPress section pages (the static copy of the site),
treats every link in them as one contribution, captures that contribution's
text from the Wayback Machine snapshot nearest the book week (May 21-28, 2010),
falling back to the live page, and writes content/<section>/<slug>/index.md.

    .venv/bin/python scripts/capture.py ~/work/chnm/hackingtheacademy-src/hackingtheacademy.org

Fetches are cached in cache/, so a rerun only regenerates the Markdown.
"""
import concurrent.futures as cf
import csv
import hashlib
import html
import io
import json
import re
import sys
import time
import unicodedata
from pathlib import Path
from urllib.parse import urljoin, urlparse

import requests
import trafilatura
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent.parent
CACHE = ROOT / "cache"
CONTENT = ROOT / "content"
BOOK_WEEK = "20100528"
SECTIONS = [
    "lectures-classrooms-and-the-curriculum",
    "educational-technology",
    "scholarly-societies-and-conferences",
    "scholarship-and-scholarly-communication",
    "academic-employment-tenure-and-scholarly-identity",
    "departments-and-disciplines",
    "libraries",
    "more-hacking",
    "criticisms-of-this-book",
]
# Pages that are a single image; the capture is the image itself.
IMAGE_HOSTS = re.compile(r"//(?:www\.)?(?:twitpic\.com|flickr\.com)/")
# Text that means the snapshot is not the piece (login walls, bot checks,
# Internet Archive chrome, Flash players).
JUNK = re.compile(r"This site is currently private|request is being verified|Can You Chip In\?"
                  r"|requires a more recent version of the Adobe Flash Player")
UA = {"User-Agent": "Mozilla/5.0 (compatible; RRCHNM archive rebuild)"}
http = requests.Session()
http.headers.update(UA)


def get(url, tries=5):
    """GET with a disk cache and backoff; returns (status, content_type, bytes, final_url)."""
    key = CACHE / hashlib.sha1(url.encode()).hexdigest()
    if key.with_suffix(".json").exists():
        meta = json.loads(key.with_suffix(".json").read_text())
        return meta["status"], meta["type"], key.read_bytes(), meta["url"]
    for n in range(tries):
        try:
            r = http.get(url, timeout=60)
        except requests.RequestException:
            r = None
        if r is not None and r.status_code not in (429, 502, 503, 504):
            break
        time.sleep(5 * 2**n)
    if r is None:
        return None, "", b"", url  # not cached, so a rerun tries again
    CACHE.mkdir(exist_ok=True)
    key.write_bytes(r.content)
    meta = {"status": r.status_code, "type": r.headers.get("content-type", ""), "url": r.url}
    key.with_suffix(".json").write_text(json.dumps(meta))
    return r.status_code, meta["type"], r.content, r.url


def snapshot(url):
    """Timestamp of the 200 capture nearest the book week, or None."""
    status, _, body, _ = get(
        "https://web.archive.org/cdx/search/cdx?output=json&fl=timestamp"
        f"&filter=statuscode:200&url={requests.utils.quote(url, safe='')}"
    )
    if status != 200 or not body.strip():
        return None
    stamps = [row[0] for row in json.loads(body)[1:]]
    return min(stamps, key=lambda t: abs(int(t[:8]) - int(BOOK_WEEK)), default=None)


def redirect_target(url):
    """Where an archived redirect of url pointed (nearest the book week), or None."""
    status, _, body, _ = get(
        "https://web.archive.org/cdx/search/cdx?output=json&fl=timestamp"
        f"&filter=statuscode:3..&url={requests.utils.quote(url, safe='')}"
    )
    if status != 200 or not body.strip():
        return None
    stamps = [row[0] for row in json.loads(body)[1:]]
    if not stamps:
        return None
    ts = min(stamps, key=lambda t: abs(int(t[:8]) - int(BOOK_WEEK)))
    _, _, _, final = get(f"https://web.archive.org/web/{ts}id_/{url}")
    m = re.search(r"/web/\d+(?:id_)?/(https?://.+)", final)
    target = m and re.sub(r"^(https?://[^/]+):80/", r"\1/", m.group(1)).split("#")[0]
    return target if target and target.rstrip("/") != url.rstrip("/") else None


def slugify(text, limit=70):
    text = unicodedata.normalize("NFKD", text).encode("ascii", "ignore").decode()
    slug = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return slug[:limit].rstrip("-") or "untitled"


def split_authors(text):
    text = " ".join(text.split()).strip(" ,“”\"(")
    if not text:
        return []
    return [a.strip() for a in re.split(r"\s+(?:&|and)\s+", text) if a.strip()]


def parse_section(path):
    """One entry per link in the section's content div."""
    soup = BeautifulSoup(path.read_text(), "html.parser")
    entries = []
    for p in soup.select("div.content p"):
        links = p.find_all("a")
        if not links:
            continue  # an unlinked line stays in the section page as written; no page of its own
        before = "".join(str(s) for s in links[0].previous_siblings)
        after = "".join(str(s) for s in links[-1].next_siblings)
        authors = split_authors(BeautifulSoup(before, "html.parser").get_text())
        note = BeautifulSoup(after, "html.parser").get_text(" ", strip=True)
        for a in links:
            entries.append({
                "authors": authors,
                "title": " ".join(a.get_text().split()),
                "url": a["href"].strip(),
                "note": note,
            })
    return entries


# Sites whose pages are a player plus clutter: embed the work, never capture
# the page as text.
MEDIA_HOSTS = re.compile(r"//(?:www\.)?(?:vimeo\.com|slideshare\.net|scribd\.com|issuu\.com)/")
# SlideShare and Scribd answer scripts with a bot check, so these embeds were
# looked up and checked in a browser (2026-11-19).
EMBEDS = {
    "http://www.slideshare.net/leighblackall/teaching-is-dead":
        "https://www.slideshare.net/slideshow/embed_code/key/dt3eJPq3DVMq6H",
    "http://www.slideshare.net/leighblackall/the-disconnect-between-learning-and-education-429513":
        "https://www.slideshare.net/slideshow/embed_code/key/jdELH0Q2nVeHOE",
    "http://www.scribd.com/doc/9293620/LIBR200FinalPaperDraftPRINT-Millenials-vs-Xers-Yers-and-Boomers-Info-Usage-120508":
        "https://www.scribd.com/embeds/9293620/content",
    "http://www.scribd.com/doc/19367583/LIBR25611EAD-Online-Access-Tools-FINISHED-Final-BlackPRNT5109":
        "https://www.scribd.com/embeds/19367583/content",
}


def media(entry, url):
    """Embed a work on a media host; a Vimeo channel is only linked; else lost."""
    if src := EMBEDS.get(url):
        entry["source"] = "embed"
        entry["body"] = (f'<iframe src="{src}" width="640" height="520" '
                         f'title="{html.escape(entry["title"])}" allowfullscreen></iframe>')
    elif m := re.search(r"vimeo\.com/(\d+)", url):
        status, _, _, _ = get(f"https://vimeo.com/api/oembed.json?url=https://vimeo.com/{m.group(1)}")
        if status == 200:
            entry["source"] = "embed"
            entry["body"] = f"{{{{< vimeo {m.group(1)} >}}}}"
    elif "vimeo.com/channels/" in url:
        status, _, _, _ = get(url)
        if status == 200:
            entry["source"] = "external"
    return entry


def youtube_id(url):
    m = re.search(r"(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]{11})", url)
    return m and m.group(1)


def capture(entry):
    """Fill entry with archive info and the captured body; returns entry."""
    url = entry["url"]
    entry.update(archived=None, archive_url=None, source=None, body="", files={}, date=None)
    if not url:
        return entry
    if m := re.match(r"https?://(?:www\.)?archive\.org/details/([^/?#]+)", url):
        entry["source"] = "archive.org"
        entry["body"] = (f'<iframe src="https://archive.org/embed/{m.group(1)}" width="640" height="480" '
                         f'title="{html.escape(entry["title"])}" allowfullscreen></iframe>')
        return entry
    if MEDIA_HOSTS.search(url):
        return media(entry, url)
    ts = snapshot(url)
    if not ts and (target := redirect_target(url)):
        # Moved posts and short links: capture where the archived redirect went.
        url, ts = target, snapshot(target)
    if ts:
        entry["archived"] = ts
        entry["archive_url"] = f"https://web.archive.org/web/{ts}/{url}"
    if vid := youtube_id(url):
        entry["source"] = "youtube"
        entry["body"] = f"{{{{< youtube {vid} >}}}}"
        return entry
    candidates = []
    if ts:
        candidates.append(("wayback", f"https://web.archive.org/web/{ts}id_/{url}"))
    candidates.append(("live", url))
    for source, fetch_url in candidates:
        status, ctype, data, final = get(fetch_url)
        if status != 200 or not data:
            continue
        if "pdf" in ctype or data[:5] == b"%PDF-":
            name = slugify(Path(urlparse(url).path).stem or "document") + ".pdf"
            entry.update(source=source, files={name: data})
            entry["body"] = f"[Download the PDF]({name})"
            return entry
        if "html" not in ctype:
            continue
        page = data.decode("utf-8", "replace")
        if m := re.search(r"/spreadsheets/d/([\w-]+)", final):
            if sheet := spreadsheet(m.group(1)):
                entry.update(source=source, body=sheet[0], files=sheet[1])
                return entry
            continue
        if m := re.search(r"var DOC_CONTENT = '(.*?)';\s*var DOC_REVISION", page, re.S):
            # The 2010 Google Docs editor carried the document as a JS string;
            # its bold-line headings are what an extractor drops, so keep the HTML.
            entry.update(source=source, body=clean_html(js_unescape(m.group(1))))
            return entry
        if IMAGE_HOSTS.search(url):
            if m := re.search(r'id="photo-display"[^>]+src="([^"]+)"', page) or re.search(
                    r'(?:property|name)="(?:og:image|twitter:image)[^"]*"[^>]+content="([^"]+)"', page):
                body, files = localize_images(f"![{entry['title']}]({m.group(1)})", url,
                                              ts if source == "wayback" else None)
                if files:
                    entry.update(source=source, body=body, files=files)
                    return entry
            continue
        text = trafilatura.extract(page, url=url, output_format="markdown", include_images=True,
                                   include_links=True, include_comments=False, favor_recall=True)
        if not text or len(text) < 40 or JUNK.search(text):
            continue
        # Captured text is third-party: keep footnote marks and simple inline
        # tags, escape any other raw HTML so it shows as text.
        # (<https://...> is Markdown's own syntax for links and addresses with spaces.)
        text = re.sub(r"<(?!/?(?:sup|sub|u|em|strong|strike|q)>)(?!https?://|mailto:)(?=[/a-zA-Z!?])",
                      "&lt;", text)
        meta = trafilatura.extract_metadata(page, default_url=url)
        entry["date"] = meta and meta.date
        entry["source"] = source
        body, entry["files"] = localize_images(text, url, ts if source == "wayback" else None)
        entry["body"] = hoist_figures(body)
        return entry
    return entry


def js_unescape(s):
    """Decode a JavaScript string literal's escapes (\\74, \\x3c, \\u003c, \\n, \\')."""
    simple = {"n": "\n", "t": "\t", "r": "\r", "b": "\b", "f": "\f", "v": "\v"}

    def one(m):
        e = m.group(1)
        if e[0] == "x" or e[0] == "u":
            return chr(int(e[1:], 16))
        if e[0] in "01234567":
            return chr(int(e, 8))
        return simple.get(e, e)

    return re.sub(r"\\(x[0-9a-fA-F]{2}|u[0-9a-fA-F]{4}|[0-3]?[0-7]{1,2}|.)", one, s, flags=re.S)


SAFE_TAGS = {"p", "br", "b", "strong", "i", "em", "u", "ul", "ol", "li", "a", "blockquote",
             "table", "tr", "td", "th", "h1", "h2", "h3", "h4", "sup", "sub"}


def clean_html(doc):
    """A document's body reduced to SAFE_TAGS, no attributes but http(s) hrefs."""
    soup = BeautifulSoup(doc, "html.parser")
    body = soup.body or soup
    for tag in body.find_all(["script", "style"]):
        tag.decompose()
    for tag in body.find_all(True):
        if tag.name == "div":
            tag.append(soup.new_tag("br"))
            tag.unwrap()
        elif tag.name not in SAFE_TAGS:
            tag.unwrap()
        else:
            href = tag.get("href", "")
            tag.attrs = {"href": href} if tag.name == "a" and re.match(r"https?://", href) else {}
    out = body.decode_contents() if body is not soup else str(body)
    out = re.sub(r"(?:\s*<br/?>\s*){3,}", "<br/><br/>", out.replace("\xa0", " "))
    out = re.sub(r"\n\s*\n", "\n", out).strip()  # a blank line would end the Markdown HTML block
    return f'<div class="gdoc">\n{out}\n</div>'


def spreadsheet(key):
    """A public Google Sheet as its CSV plus the csv shortcode; None if not public."""
    status, ctype, data, _ = get(f"https://docs.google.com/spreadsheets/d/{key}/export?format=csv")
    if status != 200 or "csv" not in ctype:
        return None
    rows = list(csv.reader(io.StringIO(data.decode("utf-8", "replace"))))
    # Drop columns that are only links, numeric ids or blank (avatars, user ids).
    keep = [i for i in range(len(rows[0]))
            if not all(re.fullmatch(r"(https?://\S*|\d*)", r[i].strip()) for r in rows[1:] if i < len(r))]
    columns = ",".join(rows[0][i].replace('"', "") for i in keep)
    body = (f'{{{{< csv file="spreadsheet.csv" columns="{columns}" >}}}}\n\n'
            "[Download the spreadsheet (CSV)](spreadsheet.csv)")
    return body, {"spreadsheet.csv": data}


# Blog furniture that extraction picks up as images: theme/plugin icons,
# Blogger's edit pencil. Dropped, not reported missing.
CHROME_IMG = re.compile(r"/wp-content/(?:themes|plugins)/|blogblog\.com/img/|/icons?/|/Banners/")


def localize_images(text, base, ts):
    """Download Markdown images into the bundle and point the Markdown at them.

    An image no copy survives of becomes a missing-image shortcode."""
    files = {}

    def fetch_image(src):
        bare = src.split("?")[0]  # WordPress resize queries are often not archived
        stamp = ts or BOOK_WEEK
        for u in dict.fromkeys([f"https://web.archive.org/web/{stamp}im_/{src}",
                                f"https://web.archive.org/web/{stamp}im_/{bare}", src, bare]):
            status, ctype, data, _ = get(u)
            if status == 200 and ctype.startswith("image/") and data:
                return ctype, data
        return None, None

    def swap(m):
        alt, src = m.group(1), urljoin(base, html.unescape(m.group(2)))
        if CHROME_IMG.search(src):
            return ""
        if SMILEY.search(src):
            return alt
        ctype, data = fetch_image(src)
        if not data:
            alt = alt.replace("\\", "").replace("`", "'")
            return f"{{{{< missing-image alt=`{alt}` src=`{src.replace('`', '%60')}` >}}}}"
        ext = "." + ctype.split("/")[1].split(";")[0].replace("jpeg", "jpg").replace("svg+xml", "svg")
        name = f"image-{len(files) + 1}{ext}"
        files[name] = data
        alt = re.sub(r"\\(.)", r"\1", alt).replace("`", "'")  # Markdown escapes, as plain text
        return f"{{{{< figure src=\"{name}\" alt=`{alt}` >}}}}"

    return re.sub(r"!\[([^\]]*)\]\(([^)\s]+)[^)]*\)", swap, text), files


FIGURE = re.compile(r"\{\{< figure [^\n]*?>\}\}")
SMILEY = re.compile(r"/smilies/|/images/smiley|/emoji/")
PLAIN_START = re.compile(r"[^#>*|{\-\d\s]")  # not a heading, quote, list, table or shortcode


def hoist_figures(md):
    """Give every figure its own block. One that sat inside a paragraph moves
    just before it, classed "wrap" so the text flows around it, and a sentence
    the extractor split at the image is joined back up."""
    paras = md.split("\n\n")
    out, i = [], 0
    while i < len(paras):
        para = paras[i]
        figs = FIGURE.findall(para)
        rest = re.sub(r"(?<=\S)  +(?=\S)", " ", FIGURE.sub("", para)).strip()
        if not figs or not rest:
            out.append(para)
            i += 1
            continue
        out += [f.replace(" >}}", ' class="wrap" >}}') for f in figs]
        if (para.rstrip().endswith(">}}") and not re.search(r"[.!?:;\"”)\]*]$", rest)
                and i + 1 < len(paras) and PLAIN_START.match(paras[i + 1])):
            rest = f"{rest} {paras[i + 1]}"
            i += 1
        out.append(rest)
        i += 1
    return "\n\n".join(out)


def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)


def write(section, weight, entry, used):
    """Write the bundle; returns its URL path, or None for a lost piece (no page)."""
    if not entry["source"]:
        return None
    base = slugify(f"{(entry['authors'] or [''])[0]} {entry['title']}")
    slug, n = base, 2
    while slug in used:
        slug, n = f"{base}-{n}", n + 1
    used.add(slug)
    bundle = CONTENT / section / slug
    bundle.mkdir(parents=True, exist_ok=True)
    fm = [
        "---",
        f"title: {yaml_str(entry['title'])}",
        f"authors: {yaml_str(entry['authors'])}",
        f"weight: {weight}",
    ]
    if entry["note"]:
        fm.append(f"note: {yaml_str(entry['note'])}")
    if entry["url"]:
        fm.append(f"original_url: {yaml_str(entry['url'])}")
    if entry["archive_url"]:
        fm.append(f"archive_url: {yaml_str(entry['archive_url'])}")
    if entry["date"]:
        fm.append(f"published: {entry['date']}")
    fm.append(f"captured_from: {entry['source'] or 'none'}")
    fm.append("---")
    (bundle / "index.md").write_text("\n".join(fm) + "\n\n" + entry["body"].strip() + "\n")
    for name, data in entry["files"].items():
        (bundle / name).write_bytes(data)
    return f"/{section}/{slug}/"


def write_section(site, section, paths):
    """The section page keeps the original list as written, linked to the captures.

    A lost piece keeps its title, unlinked, with a "(lost)" label."""
    soup = BeautifulSoup((site / section / "index.html").read_text(), "html.parser")
    title = soup.select_one("div.post h1").get_text(strip=True)
    content = soup.select_one("div.content")
    for a, path in zip(content.find_all("a"), paths):
        if path:
            a["href"] = path
            continue
        label = soup.new_tag("span", attrs={"class": "lost"})
        label.string = "(lost)"
        a.insert_after(" ", label)
        a.unwrap()
    body = "".join(str(c) for c in content.children).strip()
    weight = SECTIONS.index(section) + 1
    (CONTENT / section / "_index.html").write_text(
        f"---\ntitle: {yaml_str(title)}\nweight: {weight}\n---\n\n{body}\n")


def main(site):
    site = Path(site).expanduser()
    jobs = [(s, i + 1, e) for s in SECTIONS for i, e in enumerate(parse_section(site / s / "index.html"))]
    print(f"{len(jobs)} contributions", file=sys.stderr)
    with cf.ThreadPoolExecutor(4) as ex:
        done = list(ex.map(lambda j: capture(j[2]), jobs))
    used = {s: set() for s in SECTIONS}
    paths = {s: [] for s in SECTIONS}
    for (section, weight, _), entry in zip(jobs, done):
        paths[section].append(write(section, weight, entry, used[section]))
    for section in SECTIONS:
        write_section(site, section, paths[section])
    tally = {}
    for e in done:
        tally[e["source"]] = tally.get(e["source"], 0) + 1
    print(tally, file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1])
