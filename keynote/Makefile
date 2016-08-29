SOURCE=fileserver.md
PDF=$(SOURCE:md=pdf)
REVEALJS=$(SOURCE:md=html)

all: ${REVEALJS} ${PDF}

${REVEALJS}: ${SOURCE} Makefile
	pandoc -V transition=fade -V theme=sky -t revealjs -s ${SOURCE} -o ${REVEALJS} --slide-level 1

${PDF}: ${SOURCE} Makefile
	pandoc -t beamer -s ${SOURCE} -o ${PDF} --slide-level 3 -V theme:Szeged

clean:
	rm $(RM) count *.html *.pdf

