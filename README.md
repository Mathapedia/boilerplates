# Mathapedia boilerplates

Templates for LaTeX papers and interactive math publications, scaffolded with
[pgpm](https://github.com/constructive-io/constructive/tree/main/pgpm).

```sh
npm i -g pgpm
pgpm init workspace --repo Mathapedia/boilerplates
cd <your-paper> && make
```

Docker is the only thing you need installed to build.

## Templates

| path              | what you get                                                                                                                                                       |
| ----------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------------ |
| `latex/workspace` | A paper: `tex/` skeleton (sections, headers, figures, bib), Dockerized TeX Live, `latexmk` DVI→PS→PDF pipeline for PSTricks + TikZ, Mermaid→EPS, live SVG preview, chktex/latexindent, GitHub Actions PDF artifacts + tagged releases, VS Code / devcontainer config. |

See [`latex/workspace/README.md`](latex/workspace/README.md) for the workflow
inside a generated paper, and [`docs/evaluation.md`](docs/evaluation.md) for why
it is built the way it is (what was taken from the RLS / Hyperweb whitepapers,
what LaTeX2JS can and cannot render, roadmap).

## Non-interactive scaffolding (CI, agents)

```sh
pgpm init workspace --repo Mathapedia/boilerplates --no-tty \
  --name my-paper --title "My Paper" \
  --fullName "Ada Lovelace" --email ada@example.com \
  --repoName my-paper --username ada --license MIT
```

Question names are the `____placeholder____` names from
`latex/workspace/.boilerplate.json` with the underscores stripped.

## Authoring a template

Same layout as [pgpm-boilerplates](https://github.com/constructive-io/pgpm-boilerplates):
`.boilerplates.json` at the root points at the template directory; each template
has a `.boilerplate.json` with its `type` and `questions`; placeholders are
`____name____` in file contents and paths. Keep templates text-only — the
placeholder pass reads every file as a string, so binaries (PDF, PNG, EPS) belong
in `build/`, generated from committed sources.
