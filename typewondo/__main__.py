import json
import random
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from textwrap import dedent

from . import config
from .ngrams import build_args_parser, find_ngrams


def main() -> None:
    p = build_args_parser()
    p.add_argument(
        "--layout",
        choices=config.layouts,
        default=config.layouts[0],
        help="Layout to display keymap for",
    )
    p.add_argument("--port", type=int, default=8000, help="HTTP port")
    args = p.parse_args()

    all_ngrams = find_ngrams(args.paths, args.n, args.with_punctuation)
    print(
        f"Found {len(all_ngrams)} ngrams in {len(args.paths)} files. "
        f"Selecting top {args.top}."
    )
    ngrams = [g for g, _ in all_ngrams.most_common(args.top)]
    random.shuffle(ngrams)

    index_html = render_index(args.layout, ngrams).encode()

    class Handler(BaseHTTPRequestHandler):
        def do_GET(self):
            if self.path == "/":
                self.send_response(HTTPStatus.OK)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                self.wfile.write(index_html)
            else:
                self.send_response(HTTPStatus.NOT_FOUND)
                self.end_headers()

    host, port = "127.0.0.1", args.port
    with HTTPServer((host, port), Handler) as httpd:
        print(f"Serving on http://{host}:{port}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            pass


def render_index(layout: str, ngrams: list[str]) -> str:
    keymap = "\n".join(
        f'<div class="layer">{dedent(layer).strip()}</div>'
        for name, layer in config.keymap.items()
        if name == layout or name not in config.layouts
    ).replace("·", '<span class="dim">·</span>')

    template = (Path(__file__).parent / "index.html").read_text()
    return template.replace("{keymap}", keymap, 1).replace(
        "NGRAMS", json.dumps(ngrams), 1
    )


if __name__ == "__main__":
    main()
