#
# Makefile to handle pdf generation and syntax checks
#
#
# Author: Sascha Girrulat <sascha@girrulat.de>
#
#

SOURCE=Wilddiebe10.md
PDF=$(SOURCE:md=pdf)
PDFSLIDE=$(SOURCE:md=pdf)
REVEALJS=$(SOURCE:md=html)


all: ${PDF}

pdf: ${PDF}

#slides: ${PDFSLIDE}

#${REVEALJS}: ${SOURCE} Makefile
#	pandoc -V transition=fade -V theme=sky -t revealjs -s ${SOURCE} -o ${REVEALJS} --slide-level 1
#
#${PDFSLIDE}: ${SOURCE} Makefile
#	pandoc -t beamer -s ${SOURCE} -o ${PDFSLIDE} --slide-level 2 -V theme:Hannover
#
${PDF}: ${SOURCE} Makefile
	pandoc --number-sections -s ${SOURCE} -o ${PDF}
