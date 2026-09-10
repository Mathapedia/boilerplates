# LaTeX workflow evaluation and plan

Source material: [rls-whitepaper](https://github.com/constructive-io/rls-whitepaper),
[hyperweb-whitepaper](https://github.com/constructive-io/hyperweb-whitepaper),
[LaTeX2JS](https://github.com/Mathapedia/LaTeX2JS), mathapedia.com.

## What the whitepapers do

Both repos are the same setup with a different root file (`rls.tex` / `hvm.tex`):

- **Pipeline**: `latex → bibtex → latex → dvips → ps2pdf`, hand-rolled in a
  Makefile as five chained commands inside `docker run`. The DVI route exists
  because the papers use **PSTricks** (`pspicture`, `pscircle`, `pswedge`,
  `psline`, `psdots`, `rput`), which needs PostScript. TikZ is also loaded and
  works fine on that route.
- **Image**: `pyramation/pstricks-latex`, built from `latex/Dockerfile` —
  Ubuntu 22.04 + `apt install texlive-*` + Ghostscript + Node. Big, amd64-only,
  no version pin, packages come from Ubuntu's TeX Live snapshot.
- **Structure**: `tex/` with `headers/` (colors, `listings` TypeScript language),
  `sections/`, per-section `images/*.tex` figures, `references.bib`. This part
  is good and was kept.
- **Graphics**: PSTricks figures as `.tex`; Mermaid `.mmd` sources with the
  generated PNG/PDF committed next to them; `\includegraphics` of those.
- **CI**: pull the image, run the same five commands, upload `tex/*.pdf`.
- **Pain points**: output lands in `tex/` next to sources (aux/log/ps/pdf all
  git-noise), no incremental rebuilds (always two full passes + bibtex), no
  watch mode, no lint, no preview short of opening the PDF, and the image is
  a one-off that has to be rebuilt by hand.

## What the template changes

| whitepapers                          | template                                                                                  |
| ------------------------------------ | ----------------------------------------------------------------------------------------- |
| five chained commands                | `latexmk -pdfps` with `latexmkrc`; reruns only what changed, handles bibtex/cleveref loops |
| output in `tex/`                     | everything in `build/` (git-ignored)                                                      |
| Ubuntu apt TeX Live, amd64           | official `texlive/texlive:latest-medium` + `tlmgr install` of what the pipeline needs; multi-arch; 90 s to build, 3.4 GB |
| committed PNG/PDF from Mermaid       | only `.mmd` committed; `make figures` renders to EPS via mermaid-cli (ghcr) + Ghostscript |
| no watch / preview                   | `make watch` (`latexmk -pvc`), `make preview` (dvisvgm page SVGs + tiny static page that live-reloads) |
| no lint                              | `make lint` (chktex, noisy rules off), `make fmt` (latexindent)                           |
| CI: pull prebuilt image              | CI builds the same Dockerfile with a GHA layer cache, uploads PDF + SVGs, attaches the PDF to `v*` releases |
| ad-hoc project setup                 | `pgpm init workspace --repo Mathapedia/boilerplates` with author/title/license questions   |

Image choice: `latest-full` is 9 GB and needs nothing installed; `latest-medium`
+ collections `latexextra`/`publishers`/`bibtexextra` came out at 7.6 GB and
22 minutes of `tlmgr` (rejected); `latest-medium` + `collection-pstricks` +
a short list of common packages is 3.4 GB / 90 s and built the RLS whitepaper
identically (42 pages). `TLMGR_EXTRA` and `TEXLIVE_TAG` build args cover the
rest.

## Graphics mapping: PDF vs browser

Everything renders in the PDF. The question for a Mathapedia/LaTeX2JS live
view is what renders *there*.

| construct                           | Docker PDF | LaTeX2JS in browser                          |
| ----------------------------------- | ---------- | -------------------------------------------- |
| text, sections, lists, tables       | yes        | yes (MathJax for math)                       |
| `pspicture` + the commands below    | yes        | yes, SVG, interactive `\userline`/`\slider`  |
| other PSTricks (pst-node, pst-3dplot, `\pscustom` paths, `psgrid` details) | yes | no |
| TikZ / pgfplots                     | yes        | no                                           |
| `\includegraphics{*.eps}`           | yes        | no (would need a pre-rendered SVG/PNG)        |
| `listings`                          | yes        | plain `verbatim` only                        |
| bibliography, `\cref`               | yes        | no                                           |

LaTeX2JS PSTricks subset (from `packages/pstricks/src`): `pspicture`, `psline`,
`pspolygon`, `psframe`, `pscircle`, `psellipse`, `psarc`, `pswedge`,
`psbezier`, `pscurve`, `psccurve`, `psecurve`, `psdots`, `psgrid`, `psaxes`,
`psplot`, `pscustom`, `rput`, `psset`, `userline`, `slider`.

Two practical constraints, both encoded in `tex/figures/*.tex`:

1. mathapedia.com's `normalizePspictureIndentation` strips leading whitespace
   inside `pspicture`; write PSTricks commands at column 0 so the source is
   identical in both renderers.
2. Keep each figure in its own file so it can be pasted into Mathapedia as-is
   or fed to `latex2react` without the surrounding paper.

Conclusion: LaTeX2JS is not a second renderer for the *paper* — it is the
renderer for *figures and interactive snippets*. The paper's canonical output
is the Docker PDF; the browser preview in the template is therefore
`dvisvgm` of the real DVI (full fidelity, ~0.4 s for three pages), not a
LaTeX2JS reimplementation.

## Editor: is it worth it?

Not yet, as a separate product. What the template ships instead:

- `make preview` — save in any editor, see the real rendering in a browser
  within a couple of seconds. This is the "small UI to see what you're typing"
  with zero fidelity gap.
- `.vscode/settings.json` + `.devcontainer/` — LaTeX Workshop with the same
  `latexmk` recipe, SyncTeX enabled, so click-to-source works.

A LaTeX2JS-based editor makes sense at the figure level, and mathapedia.com
already has the pieces (`tex-editor.tsx` CodeMirror component, `latex.tsx`
client-only `latex2react`). A worthwhile next step is a `make figure-preview`
/ small page that mounts `latex2react` on `tex/figures/*.tex` next to the
dvisvgm rendering of the same figure, so an author sees immediately whether a
figure is inside the browser-renderable subset. That is a separate, small
package; it should not gate the paper workflow.

## Roadmap

1. **Done** — `latex/workspace`: paper template, Docker image, latexmk, Mermaid,
   preview, lint/fmt, CI, pgpm scaffolding. Validated: `pgpm init --no-tty`,
   `make build` (PSTricks + TikZ + Mermaid EPS + bibtex), `make lint`,
   `make svg`, `make preview`.
2. Publish `ghcr.io/mathapedia/latex` from this Dockerfile so `make` and CI
   pull instead of build (set `IMAGE`), and pin by digest for reproducible
   papers.
3. Figure preview page using `latex2react` side by side with dvisvgm output;
   a `pgpm init` question or `latex/figure` template for standalone
   interactive figures.
4. Optional variants: `latex/beamer`, `latex/book`, and a `MODE=-pdf` /
   LuaLaTeX variant for papers without PSTricks that want OpenType fonts and
   `minted`.
5. Migrate the RLS and Hyperweb whitepapers onto the template (they compile
   unchanged against the image already; the move is Makefile + output dir).
