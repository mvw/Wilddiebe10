# Makefile to handle pdf generation and syntax checks
#
#
# Author: Sascha Girrulat <sascha@girrulat.de>
#
#
# TODO: Add syntax checks for yml files

ansible_with_key:
	    ansible-playbook -i inventory site.yml --vault-password-file=.vault-password -u root

ansible_with_password:
	    ansible-playbook -i inventory site.yml --vault-password-file=.vault-password -u root -k

ansible: ansible_with_password
