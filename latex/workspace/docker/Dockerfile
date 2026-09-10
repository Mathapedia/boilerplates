# TeX Live toolchain for this paper.
#
# Starts from the official TeX Live image (medium scheme, multi-arch) and adds
# what the PSTricks -> dvips -> ps2pdf pipeline and a typical paper need.
# `latexmk`, `dvisvgm`, `chktex`, `latexindent`, `biber` and Ghostscript are
# already in the base image. Builds in ~2 minutes; the result is ~3.5 GB.
#
# Rebuild with `make image`. Add packages with TLMGR_EXTRA, e.g.
#   docker build --build-arg TLMGR_EXTRA="minted algorithm2e" -t <image> docker
# or switch TEXLIVE_TAG to latest-full if you would rather have everything.
ARG TEXLIVE_TAG=latest-medium
FROM texlive/texlive:${TEXLIVE_TAG}

ARG TLMGR_EXTRA=""
RUN tlmgr update --self >/dev/null 2>&1 || true \
 && tlmgr install \
      collection-pstricks \
      cleveref \
      ieeetran \
      pgfplots \
      tikz-cd \
      tcolorbox \
      mdframed \
      csquotes \
      multirow \
      todonotes \
      standalone \
      fontawesome5 \
      ${TLMGR_EXTRA} \
 && tlmgr path add \
 && rm -rf /usr/local/texlive/*/tlpkg/backups /tmp/*

WORKDIR /work
