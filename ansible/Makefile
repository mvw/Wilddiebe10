#
# Makefile to handle ansible runs and syntax tests
#
#
# Author: Sascha Girrulat <sascha@girrulat.de>
#
#

all: syntax-checks ansible_with_key

clean:
	rm -f site.retry
	rm -f docs/*.pdf

ansible_with_key:
	    ansible-playbook -i inventory site.yml --vault-password-file=.vault-password -u root

ansible_with_password:
	    ansible-playbook -i inventory site.yml --vault-password-file=.vault-password -u root -k

ansible: syntax-checks ansible_with_password

syntax-checks: check-yaml check-jinja

check-yaml:
	for f in $$(find host_vars/ group_vars/ -regextype posix-egrep -type f -regex '[^.]+'); do \
	  python -c "import yaml; yaml.load(open('$$f'))"; \
	done

	for f in $$(find . -name '*.yml'); do \
	  python -c "import yaml; yaml.load(open('$$f'))"; \
	done

check-jinja:
	for f in $$(find host_vars/ group_vars/ -regextype posix-egrep -type f -regex '[^.]+'); do \
	  python -c "import jinja2; \
	    e=jinja2.Environment(loader=jinja2.FileSystemLoader('./')); \
	    e.filters['ipaddr'] = func=lambda:None; \
	    e.get_template('$$f')"; \
	  if [ $$? -ne 0 ]; then \
	    echo "Syntax Error in file: $$f."; \
	  fi; \
	done

	for f in $$(find . -regextype posix-egrep -type f -regex '.*j2'); do \
	  python -c "import jinja2; \
	    e=jinja2.Environment(loader=jinja2.FileSystemLoader('./')); \
	    e.filters['ipaddr'] = func=lambda:None; \
	    e.get_template('$$f')"; \
	  if [ $$? -ne 0 ]; then \
	    echo "Syntax Error in file: $$f."; \
	  fi; \
	done

