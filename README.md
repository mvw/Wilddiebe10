# Wilddiebe10
FaPra 1599 Uni Hagen

# General setup

        apt-get install ansible sshpass pandoc
        echo <vaultpw> > .vault-password

# Generate Docufiles
        make

or

        make pdf

or

        pandoc -s Wilddiebe10.mdwn -o Wilddiebe10.pdf

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

To get more involved read:

http://docs.ansible.com/ansible/playbooks_best_practices.html
