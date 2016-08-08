#
# Makefile to handle ansible runs and syntax tests
#
#
# Author: Sascha Girrulat <sascha@girrulat.de>
#
#

all: wiki

ansible:
	cd ansible; make

wiki: clean wiki-prepare ls-testcases ls-ansible-roles
	cat wiki.txt

wiki-prepare:
	echo '====== Anhang ======' > wiki.txt

ls-testcases:
	echo '===== Testfälle =====' >> wiki.txt;
	grep '#' .travis.yml | grep -E '(Check|Run)' | sed 's/#/-/g' >> wiki.txt

ls-ansible-roles:
	echo '===== Ansible Rollen =====' >> wiki.txt;
	echo '==== Eigene Rollen ====' >> wiki.txt; ls ansible/roles | sed 's/^/  - /g' >> wiki.txt;
	echo '==== Externe Rollen ====' >> wiki.txt; ls ansible/vendor | sed 's/^/  - /g' >> wiki.txt;

clean:
	rm -f wiki.txt

update:
	git submodule update --init

test:
	cd ansible; make test

syntax-checks:
	cd ansible; make syntax-checks
