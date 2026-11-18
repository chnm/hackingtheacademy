"""Rebuild Hacking the Academy's contributions as Hugo page bundles.

Reads the flattened WordPress section pages (the static copy of the site),
treats every link in them as one contribution, captures that contribution's
text from the Wayback Machine snapshot nearest the book week (May 21-28, 2010),
falling back to the live page, and writes content/<section>/<slug>/index.md.

    .venv/bin/python scripts/capture.py ~/work/chnm/hackingtheacademy-src/hackingtheacademy.org

Fetches are cached in cache/, so a rerun only regenerates the Markdown.
"""
import concurrent.futures as cf
import hashlib
import html
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
    """One entry per link (or per unlinked line) in the section's content div."""
    soup = BeautifulSoup(path.read_text(), "html.parser")
    entries = []
    for p in soup.select("div.content p"):
        links = p.find_all("a")
        if not links:
            text = p.get_text(" ", strip=True)
            if text:
                author, _, title = text.partition(",")
                entries.append({"authors": split_authors(author), "title": title.strip() or text, "url": None, "note": ""})
            continue
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


def youtube_id(url):
    m = re.search(r"(?:youtube\.com/watch\?v=|youtu\.be/)([\w-]{11})", url)
    return m and m.group(1)


def capture(entry):
    """Fill entry with archive info and the captured body; returns entry."""
    url = entry["url"]
    entry.update(archived=None, archive_url=None, source=None, body="", files={}, date=None)
    if not url:
        return entry
    ts = snapshot(url)
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
        text = re.sub(r"<(?!/?(?:sup|sub|u|em|strong|strike|q)>)(?=[/a-zA-Z!?])", "&lt;", text)
        meta = trafilatura.extract_metadata(page, default_url=url)
        entry["date"] = meta and meta.date
        entry["source"] = source
        entry["body"], entry["files"] = localize_images(text, url, ts if source == "wayback" else None)
        return entry
    return entry


def localize_images(text, base, ts):
    """Download Markdown images into the bundle and point the Markdown at them."""
    files = {}

    def swap(m):
        alt, src = m.group(1), urljoin(base, html.unescape(m.group(2)))
        fetch = f"https://web.archive.org/web/{ts}im_/{src}" if ts else src
        status, ctype, data, _ = get(fetch)
        if status != 200 or not ctype.startswith("image/"):
            return m.group(0).replace(m.group(2), src)
        ext = "." + ctype.split("/")[1].split(";")[0].replace("jpeg", "jpg").replace("svg+xml", "svg")
        name = f"image-{len(files) + 1}{ext}"
        files[name] = data
        return f"![{alt}]({name})"

    return re.sub(r"!\[([^\]]*)\]\(([^)\s]+)[^)]*\)", swap, text), files


def yaml_str(s):
    return json.dumps(s, ensure_ascii=False)


def write(section, weight, entry, used):
    """Write the bundle; returns its URL path."""
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
    """The section page keeps the original list as written, linked to the captures."""
    soup = BeautifulSoup((site / section / "index.html").read_text(), "html.parser")
    title = soup.select_one("div.post h1").get_text(strip=True)
    content = soup.select_one("div.content")
    for a, path in zip(content.find_all("a"), paths):
        a["href"] = path
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
        path = write(section, weight, entry, used[section])
        if entry["url"]:
            paths[section].append(path)
    for section in SECTIONS:
        write_section(site, section, paths[section])
    tally = {}
    for e in done:
        tally[e["source"]] = tally.get(e["source"], 0) + 1
    print(tally, file=sys.stderr)


if __name__ == "__main__":
    main(sys.argv[1])
