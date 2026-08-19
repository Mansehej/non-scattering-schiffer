.PHONY: all verify lean paper clean

all: verify lean paper

verify:
	cd verification && ./reproduce.sh

lean:
	cd formalization && python3 scripts/check_no_holes.py && lake build

paper:
	cd paper && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex
	cd paper && latexmk -pdf -interaction=nonstopmode -halt-on-error supplement.tex
	cp paper/main.pdf non_scattering_preprint.pdf
	cp paper/supplement.pdf non_scattering_verification_supplement.pdf

clean:
	cd paper && latexmk -C main.tex || true
	cd paper && latexmk -C supplement.tex || true
	rm -rf verification/rendered
