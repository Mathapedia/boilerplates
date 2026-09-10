# Optional local extension of the Mathapedia TeX Live image
# (https://github.com/Mathapedia/docker). You only need this if your paper
# requires packages the published image lacks:
#
#   docker build --build-arg APT_EXTRA="texlive-fonts-extra" -t my-paper docker
#   make IMAGE=my-paper
#
# or edit APT_EXTRA's default below, run `make image`, and set IMAGE in the
# Makefile to the same name.
ARG BASE=ghcr.io/mathapedia/latex:latest
FROM ${BASE}

ARG APT_EXTRA=""
RUN if [ -n "${APT_EXTRA}" ]; then \
      apt-get update \
   && apt-get install -y --no-install-recommends ${APT_EXTRA} \
   && apt-get clean && rm -rf /var/lib/apt/lists/*; \
    fi

WORKDIR /work
