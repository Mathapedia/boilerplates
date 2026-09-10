# Agent guide

- Build with `make` (Docker required, nothing else). Output is `build/main.pdf`.
  Check the tail of `build/main.log` when it fails; latexmk halts on the first
  error with `file:line: message` output.
- Sections live in `tex/sections/`, one file per `\section`, `\input` from
  `tex/main.tex`. Figures live in `tex/figures/` and are `\input` from sections.
- Packages go in `tex/headers/preamble.tex`. Keep `hyperref` last and
  `cleveref` after it. Use `\cref` for references.
- The build route is `latex -> dvips -> ps2pdf` because of PSTricks. That means
  `\includegraphics` takes EPS only; generate EPS from other sources in
  `make figures` rather than committing binaries.
- PSTricks figures that should also render in the browser must stay inside the
  LaTeX2JS subset listed in README.md and keep commands at column 0 inside
  `pspicture`.
- Never commit anything under `build/`.
- `make lint` (chktex) and `make fmt` (latexindent) before opening a PR.
