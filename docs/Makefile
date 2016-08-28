#
# Makefile to handle pdf generation and syntax checks
#
#
# Author: Sascha Girrulat <sascha@girrulat.de>
#
#

SOURCE=Projektdokumentation.tex
PDF=$(SOURCE:tex=pdf)
export TEXMFHOME=$(PWD)/texmf

all: docs 

docs: setup ${PDF}

SKIP_CLEANUP?=0

pdf: setup_tex ${PDF} clean

clean:
	test $(SKIP_CLEANUP) -ne 1 && $(RM) count *.blg *.fdb_latexmk *.dvi *.fls *.bbl *.log *.fdb *.glo *.tex~ *.ist *.toc *.run.xml *.bcf *.out *.aux || echo "Skip cleanup, pls do make clean manually."
	
setup:
	sudo apt-get install texlive-latex-recommended \
											texlive-extra-utils \
											texlive-latex-extra \
											texlive-lang-german \
											pandoc \
											texlive-latex-base \
											texlive-bibtex-extra \
											texlive-generic-extra \
											biber

setup_tex:
	texhash $(TEXMFHOME)
	sudo mktexlsr 

${PDF}: ${SOURCE} Makefile
	latexmk -f -bibtex -pdf -bibtex-cond ${SOURCE}

.PHONY: docs clean
