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

wiki: clean wiki-prepare ls-testcases ls-ansible-roles ls-present-groups ls-present-users ls-allowed-ports ls-hosts-entrys
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

ls-present-groups:
	echo '===== Erzeugte Gruppen =====' >> wiki.txt
	/usr/bin/env python2 -c "import scripts.anhang as anhang; anhang.get_present_groups()" >> wiki.txt;

ls-present-users:
	echo '===== Erzeugte Benutzer =====' >> wiki.txt
	/usr/bin/env python2 -c "import scripts.anhang as anhang; anhang.get_present_users()" >> wiki.txt;

ls-allowed-ports:
	echo '===== Firewall =====' >> wiki.txt
	echo '==== Offene Ports - Gruppe Nord ====' >> wiki.txt
	/usr/bin/env python2 -c "import scripts.anhang as anhang; anhang.get_allowed_tcp_ports('ansible/group_vars/file_server_nord/public')" >> wiki.txt;
	echo '==== Offene Ports - Gruppe Sued ====' >> wiki.txt
	/usr/bin/env python2 -c "import scripts.anhang as anhang; anhang.get_allowed_tcp_ports('ansible/group_vars/file_server_sued/public')" >> wiki.txt;

ls-hosts-entrys:
	echo '===== Einträge /etc/hosts =====' >> wiki.txt
	/usr/bin/env python2 -c "import scripts.anhang as anhang; anhang.get_hosts_entrys('ansible/group_vars/all')" >> wiki.txt;

clean:
	rm -f wiki.txt

update:
	git submodule update --init

docs:
	cd docs; make

pdf:
	cd docs; make pdf

test:
	cd ansible; make test

syntax-checks:
	cd ansible; make syntax-checks
