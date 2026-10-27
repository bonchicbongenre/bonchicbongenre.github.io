"""The wall's numbers are measured, never typed.

Every tile on the wall states a size. A site's is its front page as served. The wall's
own names are all this page, the same bytes under each name, so theirs is this page's
own size -- a number that is part of what it counts.

  python3 .github/wall.py            check every stated size; exit 1 on any mismatch
  python3 .github/wall.py --live     also check each of the wall's names serves this page
  python3 .github/wall.py --fix [door repo dir ...]
                                     write the measured sizes in, solve this page's own
                                     size, date the measurement, and copy every file of
                                     this repo but CNAME into each door repo given

Standard library only. Runs from anywhere; the page is the one beside this directory.
"""
import datetime
import os
import pathlib
import re
import shutil
import sys
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parent.parent
PAGE = ROOT / "index.html"
UA = {"User-Agent": "wall-check/1.0 (+https://itsallinthe.name)"}
TILE = re.compile(r'<p class="t"><a href="https://([^"]+)">[^<]*</a></p>.*?<p class="d">([\d,]+) bytes</p>', re.S)
STAMP = re.compile(r"measured \d{4}-\d\d-\d\d \d\d:\d\d UTC(?: \([^)]*\))?")


def served(name):
    """the front page of a name as served, decompressed (urllib asks for no compression)"""
    with urllib.request.urlopen(urllib.request.Request("https://%s/" % name, headers=UA), timeout=30) as r:
        return r.read()


def wrong(what):
    """a failure, said so that GitHub shows it on the run's own page"""
    if os.environ.get("GITHUB_ACTIONS"):
        print("::error title=wall::" + what)
    return 1


def names_of(html):
    return re.search(r"var names=\[([^\]]*)\]", html).group(1).replace('"', "").split(",")


def own_size(html, names):
    """rewrite every name tile with a candidate size until the page's length is that size"""
    size = len(html.encode())
    for _ in range(8):
        stated = "{:,}".format(size)
        html = TILE.sub(lambda m: m.group(0) if m.group(1) not in names else
                        m.group(0)[:m.start(2) - m.start(0)] + stated + m.group(0)[m.end(2) - m.start(0):], html)
        if len(html.encode()) == size:
            return html, size
        size = len(html.encode())
    sys.exit("no fixed point for this page's own size")


def main():
    args = sys.argv[1:]
    html = PAGE.read_text()
    names = names_of(html)
    page = html.encode()
    bad = 0
    for m in TILE.finditer(html):
        name, stated = m.group(1), int(m.group(2).replace(",", ""))
        actual = len(page) if name in names else len(served(name))
        ok = stated == actual
        print("%-30s states %7s  %s %7s  %s" % (name, "{:,}".format(stated), "is its own" if name in names else "served",
                                                 "{:,}".format(actual), "ok" if ok else "WRONG"))
        if not ok:
            bad += wrong("%s states %s bytes; %s %s. Run: python3 .github/wall.py --fix <door repos>" % (
                name, "{:,}".format(stated), "the page is" if name in names else "it serves", "{:,}".format(actual)))
    if "--live" in args:
        for name in names:
            same = served(name) == page
            print("%-30s serves this page: %s" % (name, "yes" if same else "NO"))
            if not same:
                bad += wrong("%s does not serve this page" % name)
    if "--fix" in args:
        def measured(m):
            if m.group(1) in names:
                return m.group(0)
            n = "{:,}".format(len(served(m.group(1))))
            return m.group(0)[:m.start(2) - m.start(0)] + n + m.group(0)[m.end(2) - m.start(0):]
        html = TILE.sub(measured, html)
        now = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
        html = STAMP.sub("measured " + now, html)
        html, size = own_size(html, names)
        PAGE.write_text(html)
        print("wrote %s: %s bytes, measured %s" % (PAGE, "{:,}".format(size), now))
        files = [p for p in ROOT.iterdir() if p.is_file() and p.name not in ("CNAME", ".DS_Store")]
        for door in args[args.index("--fix") + 1:]:
            if door.startswith("--"):
                break
            for p in files:
                shutil.copy2(p, pathlib.Path(door) / p.name)
            print("copied %d files to %s" % (len(files), door))
        return
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    main()
