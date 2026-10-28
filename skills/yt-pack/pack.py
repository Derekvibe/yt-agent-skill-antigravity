#!/usr/bin/env python3
"""pack.py - keep one living Markdown file per video (a "video pack").

  python3 pack.py add  --root DIR --video "Title" --section script (--file F | --stdin | --text T) [--delete-source]
  python3 pack.py show --root DIR --video "Title"
  python3 pack.py list --root DIR

DIR is a folder in the user's own project, for example <project>/videos. Each video gets
DIR/<slug>/video-pack.md, and DIR/index.md lists every video. A section is replaced when the same
skill runs again, new sections slot into a fixed order, and anything the user typed outside the
marked blocks is left alone. Nothing here touches the network or any media file.

Sections: idea hooks script package seo chapters edit shorts retention comments viral plan audit notes
"""
import argparse, datetime, os, re, sys, tempfile, unicodedata

# Keep output safe on consoles whose default encoding is not UTF-8 (e.g. older Windows terminals).
try:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
except Exception:
    pass

SECTIONS = [
    ("idea", "Idea"), ("hooks", "Hooks"), ("script", "Script"),
    ("package", "Title and thumbnail"), ("seo", "Description and SEO"), ("chapters", "Chapters"),
    ("edit", "Edit list"), ("shorts", "Shorts"), ("retention", "Retention notes"),
    ("comments", "Comment replies"), ("viral", "Niche research"), ("plan", "Upload plan"),
    ("audit", "Channel audit"), ("notes", "Notes"),
]
ORDER = [k for k, _ in SECTIONS]
LABEL = dict(SECTIONS)
PACK = "video-pack.md"
HEADER = ("# {title}\n\nVideo pack. Each section is written by a yt-* skill and replaced when that skill "
          "runs again. Anything you write outside the marked blocks is kept.\n\n")


def fail(msg):
    print("error: " + msg, file=sys.stderr)
    sys.exit(1)


def slugify(title):
    s = unicodedata.normalize("NFKD", title).encode("ascii", "ignore").decode("ascii").lower()
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")[:60].strip("-")
    return s or "video"


def check_root(root):
    """Refuse to write inside the installed skills or the .gemini config folder."""
    real = os.path.normcase(os.path.realpath(root))
    skills_dir = os.path.normcase(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
    parts = real.replace("\\", "/").split("/")
    if real == skills_dir or real.startswith(skills_dir + os.sep) or ".gemini" in parts:
        fail("refusing to write inside the skills folder. Pass --root <your project folder>/videos")
    return os.path.realpath(root)


def read_text(a):
    if a.file:
        try:
            with open(a.file, encoding="utf-8-sig", errors="replace") as fh:
                return fh.read()
        except OSError as e:
            fail("cannot read %s (%s)" % (a.file, e))
    if a.stdin:
        return sys.stdin.buffer.read().decode("utf-8-sig", "replace")
    return a.text or ""


def write_atomic(path, text):
    d = os.path.dirname(path)
    fd, tmp = tempfile.mkstemp(dir=d, prefix=".pack-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.remove(tmp)


def make_block(key, body, stamp):
    body = body.strip().replace("<!-- yt:", "<!-- yt :")  # a section can never close itself early
    return "<!-- yt:begin %s -->\n## %s\n_Updated %s_\n\n%s\n<!-- yt:end %s -->\n" % (key, LABEL[key], stamp, body, key)


def upsert(text, key, block):
    pat = re.compile(r"<!-- yt:begin %s -->\n.*?<!-- yt:end %s -->\n?" % (key, key), re.S)
    if pat.search(text):
        return pat.sub(lambda m: block, text, count=1)
    later = [m.start() for k in ORDER[ORDER.index(key) + 1:]
             for m in [re.search(r"<!-- yt:begin %s -->" % k, text)] if m]
    if later:
        at = min(later)
        return text[:at] + block + "\n" + text[at:]
    return text.rstrip("\n") + "\n\n" + block


def pack_path(root, video):
    return os.path.join(root, slugify(video), PACK)


def rebuild_index(root):
    rows = []
    for name in sorted(os.listdir(root)):
        p = os.path.join(root, name, PACK)
        if not os.path.isfile(p):
            continue
        with open(p, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
        m = re.match(r"# (.+)", text)
        have = [k for k in ORDER if "<!-- yt:begin %s -->" % k in text]
        when = datetime.datetime.fromtimestamp(os.path.getmtime(p)).strftime("%Y-%m-%d %H:%M")
        rows.append("| [%s](%s/%s) | %s | %s |" % ((m.group(1) if m else name).replace("|", "/"),
                                                    name, PACK, ", ".join(have) or "-", when))
    body = "# Video packs\n\n| Video | Sections | Updated |\n| --- | --- | --- |\n" + "\n".join(rows) + "\n"
    write_atomic(os.path.join(root, "index.md"), body)


def cmd_add(a):
    if a.section not in LABEL:
        fail("unknown section '%s'. Use one of: %s" % (a.section, " ".join(ORDER)))
    if not (a.file or a.stdin or a.text):
        fail("give the content with --file, --stdin or --text")
    body = read_text(a)
    if not body.strip():
        fail("the content is empty, nothing saved")
    root = check_root(a.root)
    path = pack_path(root, a.video)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    text = ""
    if os.path.isfile(path):
        with open(path, encoding="utf-8", errors="replace") as fh:
            text = fh.read()
    if not text:
        text = HEADER.format(title=a.video.strip() or "Untitled video")
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    write_atomic(path, upsert(text, a.section, make_block(a.section, body, stamp)))
    rebuild_index(root)
    if a.delete_source and a.file:
        try:
            os.remove(a.file)
        except OSError:
            pass
    print("saved: %s  (section: %s)" % (path, a.section))


def cmd_show(a):
    path = pack_path(check_root(a.root), a.video)
    if not os.path.isfile(path):
        fail("no pack for '%s' yet" % a.video)
    with open(path, encoding="utf-8", errors="replace") as fh:
        print(fh.read())


def cmd_list(a):
    root = check_root(a.root)
    if not os.path.isdir(root):
        fail("no such folder: %s" % root)
    found = False
    for name in sorted(os.listdir(root)):
        p = os.path.join(root, name, PACK)
        if os.path.isfile(p):
            with open(p, encoding="utf-8", errors="replace") as fh:
                text = fh.read()
            have = [k for k in ORDER if "<!-- yt:begin %s -->" % k in text]
            print("%-40s %s" % (name, ", ".join(have) or "-"))
            found = True
    if not found:
        print("no video packs yet")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd")
    for name, fn in (("add", cmd_add), ("show", cmd_show), ("list", cmd_list)):
        p = sub.add_parser(name)
        p.add_argument("--root", required=True)
        if name != "list":
            p.add_argument("--video", required=True)
        if name == "add":
            p.add_argument("--section", required=True)
            p.add_argument("--file")
            p.add_argument("--stdin", action="store_true")
            p.add_argument("--text")
            p.add_argument("--delete-source", action="store_true")
        p.set_defaults(fn=fn)
    a = ap.parse_args()
    if not getattr(a, "fn", None):
        print(__doc__)
        sys.exit(1)
    a.fn(a)


if __name__ == "__main__":
    main()
