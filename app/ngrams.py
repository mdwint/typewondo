import string
from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
from typing import Iterator


def ngrams(text: str, n: int = 2) -> Iterator[tuple[str, ...]]:
    return zip(*(text[i:] for i in range(n)))


def top_ngrams(
    paths: list[Path],
    n: int = 2,
    top: int = 100,
    with_punctuation: bool = False,
) -> list[str]:
    c = Counter(
        ngram
        for path in paths
        if not any(part.startswith(".") for part in path.parts)
        for word in path.read_text().split()
        for ngram in ngrams(word, n)
        if not with_punctuation or any(char in ngram for char in string.punctuation)
    )
    return ["".join(ngram) for ngram, _ in c.most_common(top)]


def build_args_parser() -> ArgumentParser:
    p = ArgumentParser()
    p.add_argument("paths", type=Path, nargs="+")
    p.add_argument("-n", type=int, default="2", help="ngram length (2, 3, 4, ...)")
    p.add_argument("--top", type=int, default=100, help="x most common (default: 100)")
    p.add_argument("--with-punctuation", action="store_true")
    return p


def main() -> None:
    args = build_args_parser().parse_args()
    for ngram in top_ngrams(args.paths, args.n, args.top, args.with_punctuation):
        print(ngram)


if __name__ == "__main__":
    main()
