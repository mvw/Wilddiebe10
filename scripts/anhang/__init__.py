import yaml

def _print_line(output):
        print "  - %s" % output 

def get_present_groups(vars_file='ansible/group_vars/file_server/public', key='k1599_users_present_groups'):
    content = yaml.load(open(vars_file))
    for group in content.get(key):
        _print_line(group)

def get_present_users(vars_file='ansible/group_vars/file_server/public', key='k1599_users_present_users'):
    content = yaml.load(open(vars_file))
    users = content.get(key)
    for user in users:
        _print_line(user['name'])

def get_samba_users(vars_file, key='samba_users'):
    content = yaml.load(open(vars_file))
    if content.has_key(key):
        users = content.get(key)
        for user in users:
            _print_line(user['name'])

def get_allowed_tcp_ports(vars_file, key='firewall_allowed_tcp_ports'):
    content = yaml.load(open(vars_file))
    if content.has_key(key):
        ports = content.get(key)
        for port in ports:
            number = port['number']
            try:
                interfaces = port['interfaces']
                for interface in interfaces:
                    line = "%s: %s" % (interface, number)
            except KeyError:
                line = "all: %s" % number

            _print_line(line)
