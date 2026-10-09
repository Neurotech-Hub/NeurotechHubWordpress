"""Local preview for WordPress block markup in experiments/.

Usage (from the repo root):
    python3 experiments/preview/serve.py            # serve on http://127.0.0.1:8765
    python3 experiments/preview/serve.py --refresh  # re-download the live page shells first

Open http://127.0.0.1:8765/home (or /about). Each request re-renders experiments/<page>.html
inside a cached copy of the live page, so edits to the markup or neurotechhub.css show on reload.

The renderer approximates what WordPress does on save/render: block comments are stripped,
layout classes are added, embeds become iframes, and dynamic blocks (latest posts, Formidable
forms) are lifted from the live page. Anything it cannot render shows as a dashed placeholder.
"""

import html
import http.server
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
EXPERIMENTS = ROOT / "experiments"
SHELLS = Path(__file__).resolve().parent / "shells"
PORT = 8765

# Live page each experiment is rendered inside (header, footer, theme CSS and scripts).
PAGES = {
    "home": "https://neurotechhub.wustl.edu/",
    "about": "https://neurotechhub.wustl.edu/about-us/",
}

# Extra live pages scanned only for dynamic block output (e.g. the Store's PPI list).
SNIPPET_SOURCES = {
    "store": "https://neurotechhub.wustl.edu/store/",
}

BLOCK_LIBRARY = "https://neurotechhub.wustl.edu/wp-includes/css/dist/block-library/style.min.css?ver=7.0.7"


def fetch_shells():
    SHELLS.mkdir(exist_ok=True)
    for name, url in {**PAGES, **SNIPPET_SOURCES}.items():
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        (SHELLS / f"{name}.html").write_bytes(urllib.request.urlopen(req).read())
        print(f"fetched {url}")


def balanced_div(src, start):
    """Return the end index of the <div> that opens at `start`."""
    depth = 0
    for m in re.compile(r"<div\b|</div>").finditer(src, start):
        depth += 1 if m.group(0) == "<div" else -1
        if depth == 0:
            return m.end()
    return len(src)


def split_shell(shell):
    open_tag = '<div class="page-content">'
    i = shell.index(open_tag) + len(open_tag)
    j = shell.index("</div><!-- .page-content -->", i)
    return shell[:i], shell[i:j], shell[j:]


def live_snippets(contents):
    """Dynamic block output that only the server can render, keyed for reuse."""
    snippets = {"ppi-lists": []}
    for content in contents:
        i = content.find("<div class='wp-block-latest-posts")
        if i != -1:
            snippets.setdefault("washu/latest-posts", content[i:balanced_div(content, i)])
        for m in re.finditer(r'<div class="frm_forms[^"]*" id="frm_form_(\d+)_container"', content):
            snippets.setdefault(f"formidable:{m.group(1)}", content[m.start():balanced_div(content, m.start())])
        for m in re.finditer(r"<div id='[^']+' class=\"ppi-list[^\"]*\" data-react-attributes='([^']*)'", content):
            attrs = json.loads(html.unescape(m.group(1)))
            snippets["ppi-lists"].append((attrs, content[m.start():balanced_div(content, m.start())]))
    return snippets


def ppi_list(attrs, snippets):
    """Reuse a live PPI list with the same type and categories, trimmed to postsToShow."""
    for live_attrs, markup in snippets["ppi-lists"]:
        if live_attrs.get("listType") == attrs.get("listType", "people") and live_attrs.get("categories") == attrs.get("categories"):
            limit = attrs.get("postsToShow", live_attrs.get("postsToShow", 10))
            cards = [m.start() for m in re.finditer(r'<div class="washu-ppi-card', markup)]
            if len(cards) > limit:
                end = balanced_div(markup, cards[limit - 1]) if limit else cards[0]
                last = balanced_div(markup, cards[-1])
                markup = markup[:end] + markup[last:]
            return markup
    return placeholder(f"washu-ppi/ppi-list {json.dumps(attrs)}")


def placeholder(label):
    return (
        '<div style="padding:24px;margin:1em 0;border:2px dashed #c8c8c8;border-radius:6px;'
        f'color:#888;text-align:center">Rendered by WordPress: {html.escape(label)}</div>'
    )


def youtube_iframe(url):
    m = re.search(r"(?:youtu\.be/|v=|embed/)([\w-]{11})", url)
    if not m:
        return placeholder(f"embed {url}")
    return (
        f'<iframe width="750" height="422" src="https://www.youtube.com/embed/{m.group(1)}?feature=oembed" '
        'frameborder="0" allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; '
        'picture-in-picture; web-share" referrerpolicy="strict-origin-when-cross-origin" allowfullscreen></iframe>'
    )


def add_classes(tag, classes):
    if not classes:
        return tag
    if 'class="' in tag:
        return tag.replace('class="', 'class="' + " ".join(classes) + " ", 1)
    return re.sub(r"^<(\w+)", lambda m: f'<{m.group(1)} class="{" ".join(classes)}"', tag)


JUSTIFY = {"left": "flex-start", "center": "center", "right": "flex-end", "space-between": "space-between"}


def layout_classes(name, attrs, css):
    """Classes (and per-container CSS) WordPress adds when rendering layout-aware blocks."""
    layout = attrs.get("layout", {})
    kind = layout.get("type")
    if name in ("columns", "buttons", "social-links") or kind == "flex":
        kind = "flex"
    elif name in ("group", "column", "cover", "media-text", "details") and not kind:
        kind = "flow"
    if not kind:
        return []
    classes = [f"is-layout-{kind}", f"wp-block-{name.split('/')[-1]}-is-layout-{kind}"]
    if kind != "flex":
        return classes
    rules = []
    if layout.get("orientation") == "vertical":
        classes.append("is-vertical")
        rules.append("flex-direction:column;align-items:flex-start")
    if layout.get("justifyContent") in JUSTIFY:
        classes.append(f"is-content-justification-{layout['justifyContent']}")
        rules.append(f"justify-content:{JUSTIFY[layout['justifyContent']]}")
    if layout.get("flexWrap") == "nowrap" or name == "columns":
        classes.append("is-nowrap")
        rules.append("flex-wrap:nowrap")
    if layout.get("verticalAlignment") in ("top", "center", "bottom", "stretch"):
        va = {"top": "flex-start", "center": "center", "bottom": "flex-end", "stretch": "stretch"}
        rules.append(f"align-items:{va[layout['verticalAlignment']]}")
    if rules:
        cls = f"wp-container-preview-{len(css)}"
        classes.append(cls)
        css.append(f".{cls}{{{';'.join(rules)}}}")
    return classes


BLOCK = re.compile(r"<!--\s+(/?)wp:([a-z0-9/-]+)(\s+\{.*?\})?\s*(/?)-->", re.S)


def render(markup, snippets):
    css = []
    cover_inner = []

    def self_closing(name, attrs):
        if name == "washu-ppi/ppi-list":
            return ppi_list(attrs, snippets)
        if name in snippets:
            return snippets[name]
        return placeholder(f"{name} {json.dumps(attrs) if attrs else ''}")

    out, pos = [], 0
    for m in BLOCK.finditer(markup):
        out.append(markup[pos:m.start()])
        pos = m.end()
        closing, name, raw, self_close = m.groups()
        attrs = json.loads(raw) if raw else {}
        if closing:
            continue
        if self_close:
            out.append(self_closing(name, attrs))
            continue
        short = name.split("/")[-1] if name.startswith("core/") else name
        tag_m = re.match(r"\s*(<[a-z][^>]*>)", markup[pos:])
        if not tag_m:
            continue
        tag = tag_m.group(1)
        classes = layout_classes(short, attrs, css)
        if short == "cover":
            # WordPress puts the cover's layout classes on its inner container.
            cover_inner.append(classes)
            classes = []
        if short == "paragraph":
            classes.append("wp-block-paragraph")
        new_tag = add_classes(tag, classes)
        out.append(markup[pos:pos + tag_m.start(1)] + new_tag)
        pos += tag_m.end(1)
    out.append(markup[pos:])
    body = "".join(out)

    inner_classes = iter(cover_inner)
    body = re.sub(
        r'class="wp-block-cover__inner-container',
        lambda m: 'class="' + " ".join(next(inner_classes, [])) + " wp-block-cover__inner-container",
        body,
    )

    body = re.sub(
        r'(<div class="wp-block-embed__wrapper">)\s*(https?://\S+)\s*(</div>)',
        lambda m: m.group(1) + youtube_iframe(m.group(2)) + m.group(3),
        body,
    )
    body = re.sub(
        r'<div>\s*\[formidable id="(\d+)"\]\s*</div>',
        lambda m: snippets.get(f"formidable:{m.group(1)}", placeholder(f"Formidable form {m.group(1)}")),
        body,
    )
    return body, "\n".join(css)


def build(page):
    if not all((SHELLS / f"{name}.html").exists() for name in {**PAGES, **SNIPPET_SOURCES}):
        fetch_shells()
    before, live_content, after = split_shell((SHELLS / f"{page}.html").read_text())
    others = [split_shell((SHELLS / f"{name}.html").read_text())[1] for name in {**PAGES, **SNIPPET_SOURCES} if name != page]
    body, container_css = render((EXPERIMENTS / f"{page}.html").read_text(), live_snippets([live_content, *others]))

    head_extra = (
        f"<link rel='stylesheet' id='preview-block-library-css' href='{BLOCK_LIBRARY}' media='all' />\n"
        f"<style id='preview-block-supports'>{container_css}</style>\n"
    )
    before = before.replace("<link rel='stylesheet' id='chauvenet-style-css'", head_extra + "<link rel='stylesheet' id='chauvenet-style-css'", 1)

    # The custom CSS loads from the footer widget; swap it for the local file in the same spot.
    page_html = before + "\n" + body + "\n" + after
    return re.sub(
        r'<link rel="stylesheet" href="https://cdn\.jsdelivr\.net/gh/Neurotech-Hub/NeurotechHubWordpress@[^"]+">',
        f'<link rel="stylesheet" href="/neurotechhub.css?v={int(time.time())}">',
        page_html,
    )


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    def do_GET(self):
        page = self.path.strip("/").split("?")[0]
        if page in PAGES:
            try:
                data = build(page).encode()
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
            except Exception as exc:  # surface render errors in the browser
                data = f"<pre>{html.escape(repr(exc))}</pre>".encode()
                self.send_response(500)
                self.send_header("Content-Type", "text/html; charset=utf-8")
            self.end_headers()
            self.wfile.write(data)
            return
        super().do_GET()

    def end_headers(self):
        self.send_header("Cache-Control", "no-store")
        super().end_headers()


if __name__ == "__main__":
    if "--refresh" in sys.argv:
        fetch_shells()
    # A just-stopped previous server can hold the port for a moment.
    for attempt in range(20):
        try:
            server = http.server.ThreadingHTTPServer(("127.0.0.1", PORT), Handler)
            break
        except OSError:
            if attempt == 19:
                raise
            time.sleep(0.5)
    print("Preview: " + ", ".join(f"http://127.0.0.1:{PORT}/{p}" for p in PAGES))
    server.serve_forever()
