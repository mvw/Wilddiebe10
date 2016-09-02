#
# Makefile to handle ansible runs and syntax tests
#
#
# Author: Sascha Girrulat <sascha@girrulat.de>
#
#
DEST='docs/includes/appendix/ansible.tex'
all: anhang 

ansible:
	cd ansible; make

anhang: clean anhang-prepare ls-testcases ls-ansible-roles ls-present-groups ls-present-users ls-allowed-ports ls-hosts-entrys
	cat $(DEST)

anhang-prepare:
	echo '\section{Ansible}' > $(DEST)

ls-testcases:
	echo '\subsection{Testfälle}' >> $(DEST);
	/usr/bin/env python2 -c "import scripts.anhang as anhang; anhang.print_item_header()" >> $(DEST);
	grep '#' .travis.yml | grep -E '(Check|Run)' | sed 's/#/&/g' >> $(DEST)
	/usr/bin/env python2 -c "import scripts.anhang as anhang; anhang.print_item_footer()" >> $(DEST);

ls-ansible-roles:
	echo '\subsection{Ansible Rollen}' >> $(DEST);
	echo '\subsubsection{Eigene Rollen}' >> $(DEST);
	/usr/bin/env python2 -c "import scripts.anhang as anhang; anhang.print_item_header()" >> $(DEST);
	ls ansible/roles | sed 's/^/  & /g' | sed 's/_/\\_/g' >> $(DEST);
	/usr/bin/env python2 -c "import scripts.anhang as anhang; anhang.print_item_footer()" >> $(DEST);
	echo '\subsubsection{Externe Rollen}' >> $(DEST);
	/usr/bin/env python2 -c "import scripts.anhang as anhang; anhang.print_item_header()" >> $(DEST);
	ls ansible/vendor | sed 's/^/  & /g' | sed 's/_/\\_/g' >> $(DEST);
	/usr/bin/env python2 -c "import scripts.anhang as anhang; anhang.print_item_footer()" >> $(DEST);

ls-present-groups:
	echo '\subsection{Erzeugte Gruppen}' >> $(DEST)
	/usr/bin/env python2 -c "import scripts.anhang as anhang; anhang.get_present_groups()" >> $(DEST);

ls-present-users:
	echo '\subsection{Erzeugte Benutzer}' >> $(DEST)
	/usr/bin/env python2 -c "import scripts.anhang as anhang; anhang.get_present_users()" >> $(DEST);

ls-allowed-ports:
	echo '\subsection{Firewall}' >> $(DEST)
	echo '\subsubsection{Offene Ports - Gruppe Nord}' >> $(DEST)
	/usr/bin/env python2 -c "import scripts.anhang as anhang; anhang.get_allowed_tcp_ports('ansible/group_vars/file_server_nord/public')" >> $(DEST);
	echo '\subsubsection{Offene Ports - Gruppe Sued}' >> $(DEST)
	/usr/bin/env python2 -c "import scripts.anhang as anhang; anhang.get_allowed_tcp_ports('ansible/group_vars/file_server_sued/public')" >> $(DEST);

ls-hosts-entrys:
	echo '\subsection{Einträge /etc/hosts}' >> $(DEST)
	/usr/bin/env python2 -c "import scripts.anhang as anhang; anhang.get_hosts_entrys('ansible/group_vars/all')" >> $(DEST);

clean:
	rm -f $(DEST)

update:
	git submodule update --init

docs:
	cd docs; make docs

pdf:
	cd docs; make pdf

test:
	cd ansible; make test

syntax-checks:
	cd ansible; make syntax-checks

.PHONY: docs clean
