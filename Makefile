# Makefile ANTI_AI_SLOP_GUARD v4.0
PY ?= python
NASKAH ?= REVISI_*.md
LAMA ?= tulisan_lama/*.md

.PHONY: audit deep check calibrate snapshot all clean

audit:            ## Audit pola permukaan, register, ejaan, kalimat, densitas
	$(PY) tools/slop_audit.py $(NASKAH) --show 5

deep:             ## Audit lapis probabilitas token (perlu torch + transformers)
	$(PY) tools/deep_audit.py $(NASKAH) --topk 12

calibrate:        ## Bangun garis dasar gaya pribadi dari tulisan lama
	$(PY) tools/slop_audit.py --calibrate $(LAMA)

snapshot:         ## Simpan salinan sebelum disunting
	@mkdir -p .deslop
	@for f in $(NASKAH); do cp "$$f" ".deslop/$$(basename $$f .md).before.md"; done
	@echo "salinan tersimpan di .deslop/"

check:            ## Uji Kontrak Invarian terhadap salinan sebelum
	@for f in $(NASKAH); do \
		b=".deslop/$$(basename $$f .md).before.md"; \
		if [ -f "$$b" ]; then \
			$(PY) tools/invariant_check.py "$$b" "$$f" --terms tools/terms.json || exit 1; \
		fi; \
	done

all: audit check

clean:
	rm -rf .deslop
