#
# Makefile to handle ansible runs and syntax tests
#
#
# Author: Sascha Girrulat <sascha@girrulat.de>
#
#

all: syntax-checks update ansible_with_sudo

clean:
	rm -f site.retry
	rm -f docs/*.pdf

ansible_with_sudo:
	    ansible-playbook -i inventory site.yml --vault-password-file=.vault-password -s -K

ansible_with_key:
	    ansible-playbook -i inventory site.yml --vault-password-file=.vault-password -u root

test: syntax-checks
	    ansible-playbook -i inventory site.yml --vault-password-file=.vault-password -s -K -C --diff

ci:
	    ansible-playbook -i tests/inventory tests/test.yml --connection=local --sudo

update:
	git submodule update --init

syntax-checks: check-yaml check-jinja

check-yaml:
	for f in $$(find host_vars/ group_vars/ -regextype posix-egrep -type f -regex '[^.]+'); do \
	  /usr/bin/env python2 -c "import yaml; yaml.load(open('$$f'))"; \
	  if [ $$? -ne 0 ]; then \
	    echo "Syntax Error in file: $$f."; \
	    exit 1; \
	  fi; \
	done

	for f in $$(find . -name '*.yml'); do \
	  /usr/bin/env python2 -c "import yaml; yaml.load(open('$$f'))"; \
	  if [ $$? -ne 0 ]; then \
	    echo "Syntax Error in file: $$f."; \
	    exit 1; \
	  fi; \
	done

check-jinja:
	for f in $$(find host_vars/ group_vars/ -regextype posix-egrep -type f -regex '[^.]+'); do \
	  /usr/bin/env python2 -c "import jinja2; \
	    e=jinja2.Environment(loader=jinja2.FileSystemLoader('./')); \
	    e.filters['ipaddr'] = func=lambda:None; \
	    e.get_template('$$f')"; \
	  if [ $$? -ne 0 ]; then \
	    echo "Syntax Error in file: $$f."; \
	    exit 1; \
	  fi; \
	done

	for f in $$(find . -regextype posix-egrep -type f -regex '.*j2'); do \
	  /usr/bin/env python2 -c "import jinja2; \
	    e=jinja2.Environment(loader=jinja2.FileSystemLoader('./')); \
	    e.filters['ipaddr'] = func=lambda:None; \
	    e.get_template('$$f')"; \
	  if [ $$? -ne 0 ]; then \
	    echo "Syntax Error in file: $$f."; \
	    exit 1; \
	  fi; \
	done
