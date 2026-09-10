# Everything runs inside Docker; no local TeX install is needed.
#
#   make            build the PDF            -> build/main.pdf
#   make watch      rebuild on every save
#   make preview    watch + browser preview  -> http://localhost:8000
#   make svg        one SVG per page         -> build/svg/
#   make figures    Mermaid *.mmd -> EPS     -> build/figures/
#   make lint       chktex
#   make fmt        latexindent (in place)
#   make shell      bash inside the TeX Live container
#   make image      build a local image from docker/Dockerfile (extra packages)
#   make clean      remove build/

DOC   ?= main
# Published from https://github.com/Mathapedia/docker
IMAGE ?= mathapedia/latex:latest
MODE  ?= -pdfps          # -pdfps: latex->dvips->ps2pdf (PSTricks). -pdf: pdflatex.
PORT  ?= 8000
MERMAID_IMAGE ?= minlag/mermaid-cli:11.4.2

TEX_DIR   := tex
BUILD_DIR := build
MAIN      := $(TEX_DIR)/$(DOC).tex
PDF       := $(BUILD_DIR)/$(DOC).pdf

# Interactive TTY only when we have one (CI does not).
TTY := $(shell [ -t 0 ] && echo -it || echo -i)
RUN := docker run --rm $(TTY) \
	--user "$(shell id -u):$(shell id -g)" \
	-v "$(CURDIR)":/work -w /work \
	-e HOME=/tmp \
	$(IMAGE)

LATEXMK := latexmk -r latexmkrc $(MODE) -cd

# Page SVGs come from the DVI (dvisvgm renders PSTricks specials via
# Ghostscript); run from tex/ so \includegraphics paths resolve.
DVISVGM := cd $(TEX_DIR) && TEXINPUTS=.:../$(BUILD_DIR)/figures: \
	dvisvgm --page=1- --font-format=woff2 --exact-bbox \
	-o ../$(BUILD_DIR)/svg/$(DOC)-%p.svg ../$(BUILD_DIR)/$(DOC).dvi

MMD_SRC := $(wildcard $(TEX_DIR)/figures/*.mmd)
MMD_EPS := $(patsubst $(TEX_DIR)/figures/%.mmd,$(BUILD_DIR)/figures/%.eps,$(MMD_SRC))

.PHONY: all build watch preview svg figures lint fmt shell image image-if-missing clean

all: build

build: image-if-missing figures
	$(RUN) $(LATEXMK) $(MAIN)
	@echo "==> $(PDF)"

watch: image-if-missing figures
	$(RUN) $(LATEXMK) -pvc $(MAIN)

# Full-fidelity browser preview: latexmk -pvc rebuilds on save, dvisvgm turns
# each page into SVG, preview/index.html polls and reloads. Needs MODE=-pdfps.
preview: image-if-missing figures
	@mkdir -p $(BUILD_DIR)/svg
	@echo "==> http://localhost:$(PORT)/preview/"
	docker run --rm $(TTY) \
		--user "$(shell id -u):$(shell id -g)" \
		-v "$(CURDIR)":/work -w /work -e HOME=/tmp -p $(PORT):$(PORT) \
		$(IMAGE) sh -c '\
		  python3 -m http.server $(PORT) --bind 0.0.0.0 >/dev/null 2>&1 & \
		  $(LATEXMK) -pvc -e "\$$success_cmd = q(cd /work && $(DVISVGM) && date +%s > /work/$(BUILD_DIR)/svg/stamp)" $(MAIN)'

svg: build
	@mkdir -p $(BUILD_DIR)/svg
	$(RUN) sh -c '$(DVISVGM)'
	@echo "==> $(BUILD_DIR)/svg/"

# Mermaid -> PDF (mermaid-cli) -> EPS (Ghostscript), so the DVI route can
# \includegraphics it. Only runs for sources newer than their EPS.
figures: $(MMD_EPS)

$(BUILD_DIR)/figures/%.eps: $(TEX_DIR)/figures/%.mmd | image-if-missing
	@mkdir -p $(BUILD_DIR)/figures
	docker run --rm --user "$(shell id -u):$(shell id -g)" \
		-v "$(CURDIR)":/work -w /work $(MERMAID_IMAGE) \
		-i $< -o $(BUILD_DIR)/figures/$*.pdf -b transparent
	$(RUN) gs -q -dNOPAUSE -dBATCH -dSAFER -sDEVICE=eps2write -dEPSCrop \
		-sOutputFile=$@ $(BUILD_DIR)/figures/$*.pdf

lint: image-if-missing
	$(RUN) sh -c 'cd $(TEX_DIR) && chktex -q -n 1 -n 8 -n 13 -n 24 -n 29 -n 36 $(DOC).tex'

fmt: image-if-missing
	$(RUN) sh -c 'cd $(TEX_DIR) && find . -name "*.tex" -exec latexindent -s -w -m -l -c ../build/ {} +'

shell: image-if-missing
	$(RUN) bash

# Extend the published image (e.g. extra apt/tlmgr packages), then run with
# `make IMAGE=<name>` or set IMAGE at the top of this file.
image:
	docker build -t $(IMAGE) docker

image-if-missing:
	@docker image inspect $(IMAGE) >/dev/null 2>&1 || docker pull $(IMAGE)

clean:
	rm -rf $(BUILD_DIR)
