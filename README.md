# typewondo

Run `typewondo` on a collection of text files to start training your typing:

```console
$ poetry run typewondo ~/foo/**.py ~/bar/**.txt -n 4 --with-punctuation --layout colemak_dh
Found 66496 ngrams in 1319 files. Selecting top 100.
Serving on http://127.0.0.1:8000
```

![screenshot](/screenshot.png)
