import yaml

def print_item_header():
        print '\\begin{itemize}'

def print_item_footer():
        print '\\end{itemize}'

def _print_line(output):
        print "  \item %s" % output

def get_present_groups(vars_file='ansible/group_vars/file_server/public', key='k1599_users_present_groups'):
    content = yaml.load(open(vars_file))
    print_item_header()
    for group in content.get(key):
        _print_line(group)
    print_item_footer()

def get_present_users(vars_file='ansible/group_vars/file_server/public', key='k1599_users_present_users'):
    content = yaml.load(open(vars_file))
    users = content.get(key)
    print_item_header()
    for user in users:
        _print_line(user['name'])
    print_item_footer()

def get_samba_users(vars_file, key='samba_users'):
    content = yaml.load(open(vars_file))
    if content.has_key(key):
        users = content.get(key)
        print_item_header()
        for user in users:
            _print_line(user['name'])

        print_item_footer()

def get_hosts_entrys(vars_file, key='k1599_common_hosts'):
    content = yaml.load(open(vars_file))
    if content.has_key(key):
        hosts = content.get(key)
        print_item_header()
        for host in hosts:
            if host['ip'].startswith('{'):
                continue
            try:
              _print_line("%s : %s %s" % (host['ip'], host['name'], host['fqdn']))
            except KeyError:
              _print_line("%s : %s" % (host['ip'], host['name']))
        print_item_footer()

def get_allowed_tcp_ports(vars_file, key='firewall_allowed_tcp_ports'):
    content = yaml.load(open(vars_file))
    if content.has_key(key):
        ports = content.get(key)
        print_item_header()
        for port in ports:
            number = port['number']
            try:
                interfaces = port['interfaces']
                for interface in interfaces:
                    line = "%s: %s" % (interface, number)
            except KeyError:
                line = "all: %s" % number

            _print_line(line)
        print_item_footer()
