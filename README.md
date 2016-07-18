# Wilddiebe10
FaPra 1599 Uni Hagen

# General setup

        apt-get install ansible sshpass pandoc
        echo <vaultpw> > .vault-password

# Generate Documentaion
To ease the generation of the documentation files inside the doc folder you
could use on of the commands below:

        make

or

        make pdf

If you won't to do that all the time use conttest.

        pip install conttest
        conttest make

That will generate the pdf all the time if something is changes inside the docs folder. 

# Run Ansibleq
Run Ansible via

        ansible-playbook -i inventory site.yml --vault-password-file=.vault-password -u root -k


or do a

        ssh-copy-id root@<hostip>
        ansible-playbook -i inventory site.yml --vault-password-file=.vault-password -u root

alternative you could use the commands 'make [ansible_with_password]' instead of the commands above.

The length of the commands above depends to your ~/.ssh/config

        Host fileserver fapra_1599
        HostName <hostip>
        User root

and your local ~/.ansible.cfg

        [ssh_connection]
        ssh_args = -o StrictHostKeyChecking=no

# Generate a new password for the vault file

        mkpasswd --method=des

# Edit vault files

        ansible-vault --vault-password-file=.vault-password edit group_vars/fileserver/vault

# More

## Ansible
To get more involved with Ansible take a look at:

  http://docs.ansible.com/ansible/playbooks_best_practices.html

## Pandoc
To get more involved with pandoc take a look at:

  http://pandoc.org/README.html

## Latex
  https://en.wikibooks.org/wiki/LaTeX
