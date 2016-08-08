#
# Makefile to handle ansible runs and syntax tests
#
#
# Author: Sascha Girrulat <sascha@girrulat.de>
#
#

all: ls-testcases 

ansible: 
	cd ansible; make

ls-testcases:
	echo '====== Anhang ======' > testcases.txt; echo '===== Testfälle =====' >> testcases.txt;
	grep '#' .travis.yml | grep -E '(Check|Run)' | sed 's/#/-/g' >> testcases.txt
	cat testcases.txt

clean:
	rm testcases.txt

update:
	git submodule update --init

test:
	cd ansible; make test

syntax-checks:
	cd ansible; make syntax-checks
