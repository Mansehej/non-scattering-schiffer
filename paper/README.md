# Paper source

Build the focused research article with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
```

Build the verification supplement with:

```bash
latexmk -pdf -interaction=nonstopmode -halt-on-error supplement.tex
```

Both documents use `references.tex` directly and therefore require neither
BibTeX nor Biber.  They compile on arXiv without shell escape or external
fonts.
