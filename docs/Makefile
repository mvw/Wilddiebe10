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
UNAME_S := $(shell uname -s)

all: docs 

docs: setup ${PDF}

SKIP_CLEANUP?=0

pdf: setup_tex ${PDF} clean

anhang:
	cd ../; make anhang

clean_all: clean
	rm $(RM) count *.pdf

clean:
	test $(SKIP_CLEANUP) -ne 1 && $(RM) count \
		*.blg \
		*.fdb_latexmk \
		*.dvi \
		*.fls \
		*.bbl \
		*.log \
		*.fdb \
		*.glo \
		*.tex~ \
		*.ist \
		*.toc \
		*.run.xml \
		*.bcf \
		*.out \
		includes/*.aux \
		*.aux || echo "Skip cleanup, pls do make clean manually."

setup:
ifeq ($(UNAME_S),Linux)
	sudo apt-get install texlive-latex-recommended \
											texlive-extra-utils \
											texlive-latex-extra \
											texlive-lang-german \
											pandoc \
											texlive-latex-base \
											texlive-bibtex-extra \
											texlive-generic-extra \
											biber
endif
ifeq ($(UNAME_S),FreeBSD)
	pkg install latex-mk
	pkg install latex-biber
	pkg install tex-dvipsk
endif

setup_tex:
	texhash $(TEXMFHOME)
	sudo mktexlsr 

${PDF}: ${SOURCE} Makefile
	latexmk -f -bibtex -pdf -bibtex-cond ${SOURCE}
	pdflatex AnwenderItRichtlinie.tex
	pdflatex Betriebshandbuch.tex 

.PHONY: docs clean
