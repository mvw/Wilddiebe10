#
# Makefile to handle pdf generation and syntax checks
#
#
# Author: Sascha Girrulat <sascha@girrulat.de>
#
#

SOURCE=Projektdokumentation.tex
PDF=$(SOURCE:tex=pdf)
PDFSLIDE=$(SOURCE:md=pdf)
REVEALJS=$(SOURCE:md=html)
PWD=$(shell pwd)
export TEXMFHOME=$(PWD)/texmf

all: setup ${PDF}

SKIP_CLEANUP?=0

pdf: ${PDF} clean

clean:
	test $(SKIP_CLEANUP) -ne 1 && $(RM) count *.log *.fdb *.glo *.tex~ *.ist *.toc *.run.xml *.bcf *.out *.aux || echo "Skip cleanup, pls do make clean manually."
	
setup:
	sudo apt-get install texlive-latex-recommended \
											texlive-extra-utils \
											texlive-latex-extra \
											texlive-lang-german \
											pandoc \
											texlive-latex-base \
											texlive-bibtex-extra \
											texlive-generic-extra
								
	texhash $(TEXMFHOME)
	sudo mktexlsr 

#slides: ${PDFSLIDE}

#${REVEALJS}: ${SOURCE} Makefile
#	pandoc -V transition=fade -V theme=sky -t revealjs -s ${SOURCE} -o ${REVEALJS} --slide-level 1
#
#${PDFSLIDE}: ${SOURCE} Makefile
#	pandoc -t beamer -s ${SOURCE} -o ${PDFSLIDE} --slide-level 2 -V theme:Hannover
#
${PDF}: ${SOURCE} Makefile
	pdflatex ${SOURCE}
