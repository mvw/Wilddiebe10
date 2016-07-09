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

# Run Ansible

        ansible-playbook -i inventory site.yml --vault-password-file=.vault-password -u root -k


or do a

        ssh-copy-id 138.201.175.250
        ansible-playbook -i inventory site.yml --vault-password-file=.vault-password -u root

The length of the commands above depends to your ~/.ssh/config

        Host fileserver fapra_1599
        HostName 138.201.175.250
        User root

and your local ~/.ansible.cfg

        [ssh_connection]
        ssh_args = -o StrictHostKeyChecking=no

# Generate a new password for the vault file

        mkpasswd --method=des

# More

To get more involved read:

http://docs.ansible.com/ansible/playbooks_best_practices.html
