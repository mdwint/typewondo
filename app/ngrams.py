import string
from argparse import ArgumentParser
from collections import Counter
from pathlib import Path
from typing import Iterator


def ngrams(text: str, n: int = 2) -> Iterator[tuple[str, ...]]:
    return zip(*(text[i:] for i in range(n)))


def find_ngrams(
    paths: list[Path], n: int = 2, with_punctuation: bool = False
) -> Counter[str]:
    return Counter(
        "".join(ngram)
        for path in paths
        if not any(part.startswith(".") for part in path.parts)
        for word in path.read_text().split()
        for ngram in ngrams(word, n)
        if not with_punctuation or any(char in ngram for char in string.punctuation)
    )


def build_args_parser() -> ArgumentParser:
    p = ArgumentParser()
    p.add_argument("paths", type=Path, nargs="+")
    p.add_argument("-n", type=int, default="2", help="ngram length (2, 3, 4, ...)")
    p.add_argument("--top", type=int, default=100, help="x most common (default: 100)")
    p.add_argument("--with-punctuation", action="store_true")
    return p


def main() -> None:
    args = build_args_parser().parse_args()

    ngrams = find_ngrams(args.paths, args.n, args.with_punctuation)
    print(f"Found {len(ngrams)} ngrams in {len(args.paths)} files.")

    for ngram, count in ngrams.most_common(args.top):
        print(f"{ngram} ({count})")


if __name__ == "__main__":
    main()
