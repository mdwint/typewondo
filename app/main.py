import json
from pathlib import Path
from textwrap import dedent

import config
from ngrams import build_args_parser, top_ngrams


def main():
    args = build_args_parser().parse_args()
    ngrams = top_ngrams(args.paths, args.n, args.top, args.with_punctuation)

    build_dir = Path("build")
    build_dir.mkdir(exist_ok=True)

    index_html = render_index(ngrams)
    (build_dir / "index.html").write_text(index_html)
    print(f"Wrote {build_dir}")


def render_index(ngrams: list[str]) -> str:
    layout = "colemak_dh"
    keymap = "\n".join(
        f'<div class="layer">{dedent(config.keymap[layer]).strip()}</div>'
        for layer in ("symbols", layout, "numbers")
    ).replace("·", '<span class="dim">·</span>')

    template = (Path(__file__).parent / "index.html").read_text()
    return template.replace("{keymap}", keymap, 1).replace(
        "NGRAMS", json.dumps(ngrams), 1
    )


if __name__ == "__main__":
    main()
