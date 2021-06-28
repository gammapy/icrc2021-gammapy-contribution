.PHONY: main clean FORCE

main: poster.pdf

poster.pdf: FORCE
	latexmk -pdflatex='lualatex -interaction nonstopmode -shell-escape' -pdf poster.tex

clean:
	latexmk -pdf -C
