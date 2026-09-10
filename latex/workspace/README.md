# ____title____

[![build](https://github.com/____username____/____repoName____/actions/workflows/build.yml/badge.svg)](https://github.com/____username____/____repoName____/actions/workflows/build.yml)

LaTeX paper scaffolded from [Mathapedia/boilerplates](https://github.com/Mathapedia/boilerplates).
The only local dependency is Docker.

```sh
make            # build/main.pdf
make preview    # browser editor (left) + live page preview (right) at http://localhost:8000/preview/
```

## Layout

```
tex/
  main.tex              document root: title, abstract, \input of sections
  headers/preamble.tex  packages (pstricks, tikz, hyperref, cleveref, ...)
  headers/colors.tex    palette
  headers/listings.tex  code listing languages/styles
  sections/*.tex        one file per section
  figures/*.tex         PSTricks / TikZ figures, \input from sections
  figures/*.mmd         Mermaid sources, compiled to EPS by `make figures`
  references.bib
docker/Dockerfile       optional extension of mathapedia/latex
latexmkrc               build recipe: latex -> dvips -> ps2pdf, output in build/
preview/index.html      split-pane editor + SVG page preview (layout from the LaTeX2JS playground)
preview/server.py       static server + save endpoint used by `make preview`
build/                  generated, git-ignored
```

## Commands

| command        | what it does                                                             |
| -------------- | ------------------------------------------------------------------------ |
| `make`         | `latexmk -pdfps` in Docker → `build/main.pdf`                            |
| `make watch`   | same, rebuilding whenever a file under `tex/` changes                   |
| `make preview` | editor + `watch` + `dvisvgm` page SVGs at `localhost:8000/preview/`; edits under `tex/` autosave and rebuild |
| `make svg`     | one SVG per page in `build/svg/` (what Mathapedia ingests)               |
| `make figures` | `tex/figures/*.mmd` → `build/figures/*.eps` via mermaid-cli + Ghostscript |
| `make lint`    | `chktex` on the document                                                 |
| `make fmt`     | `latexindent -w` over `tex/`                                             |
| `make shell`   | bash inside the TeX Live container (`kpsewhich …`, `apt list texlive-*`)   |
| `make image`   | build a local image from `docker/Dockerfile` (extra packages)            |
| `make clean`   | `rm -rf build/`                                                          |

Variables: `DOC=main` (root file name), `IMAGE=mathapedia/latex:latest`,
`MODE=-pdfps` (use `MODE=-pdf` for plain pdflatex if the paper has no
PSTricks), `PORT=8000`.

## Graphics

| kind                    | PDF build | browser (LaTeX2JS / Mathapedia) | notes                                           |
| ----------------------- | --------- | ------------------------------- | ----------------------------------------------- |
| PSTricks (subset below) | yes       | yes, interactive                | write commands at column 0 inside `pspicture`   |
| PSTricks (anything else)| yes       | no                              | pst-3dplot, pst-node, pscustom paths, …         |
| TikZ / pgfplots         | yes       | no                              |                                                 |
| Mermaid `.mmd`          | via EPS   | as SVG                          | only the source is committed                    |
| `\includegraphics`      | EPS only  | n/a                             | the DVI route cannot embed PNG/JPG/PDF directly |

LaTeX2JS subset: `pspicture`, `psline`, `pspolygon`, `psframe`, `pscircle`,
`psellipse`, `psarc`, `pswedge`, `psbezier`, `pscurve`, `psccurve`, `psecurve`,
`psdots`, `psgrid`, `psaxes`, `psplot`, `pscustom`, `rput`, `psset`, plus the
interactive `\userline` and `\slider`. Figures in `tex/figures/` that stay
inside that subset render identically in the PDF and in the browser.

## Adding a TeX package

The image is [`mathapedia/latex`](https://github.com/Mathapedia/docker) on Docker Hub
(Ubuntu TeX Live: pstricks, pictures/TikZ, latex-extra, science, publishers,
bibtex-extra, latexmk, chktex, latexindent, biber, dvisvgm). If something is
missing, either open a PR there, or extend locally: put the Debian package in
`APT_EXTRA` in `docker/Dockerfile`, `make image IMAGE=my-paper`, and use
`make IMAGE=my-paper` (or change the `IMAGE` default in the Makefile).

## Releases

Pushing a tag `v*` builds the PDF in CI and attaches it to a GitHub release.
Every push and PR uploads the PDF and page SVGs as a workflow artifact.

## License

____license____
