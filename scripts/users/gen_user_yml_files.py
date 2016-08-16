#!/usr/bin/env python
#-*- coding: UTF-8 -*-


import os
import sys
import subprocess

import argparse
import csv
import jinja2
import yaml


TEMPLATE_FILE = 'mail_template.j2'

REPLACE_UMLAUTS = {
    u"ö" : 'oe',
    u"ü" : 'ue',
    u"ä" : 'ae',
    u"ß" : 'ss',
}

GROUPS = {
    1 : 'web-nord',
    2 : 'mail-nord',
    3 : 'netz-nord',
    4 : 'cert-nord',
    5 : 'file-nord',
    6 : 'web-sued',
    7 : 'mail-sued',
    8 : 'netz-sued',
    9 : 'cert-sued',
    10 : 'file-sued',
    11 : 'sshusers',
    12 : 'fapra1599',
}


def _replace_umlauts(str2rep):
    string2return = str2rep
    for key, value in REPLACE_UMLAUTS.iteritems():
        string2return = string2return.replace(key, value)
    return string2return

def get_csv_content_from_file(fname):

    content = []

    with open(fname, 'rb') as csvfile:
        lines = csv.reader(csvfile, delimiter=',', quotechar='"')
        for line in lines:
            content.append(line)

    return content

def gen_user_data_dict_from_csv(csv_data, dict_name='k1599_users_present_users'):
    users = {}
    dict_from_csv = {dict_name : users}

    for line in csv_data:
        if line[0] == '' or line[0] == 'matrikelnr':
            continue

        name = "%s%s" % (line[2][0].lower().decode('utf-8'), line[1].lower().decode('utf-8'))
        name = _replace_umlauts(name).encode('ascii', 'ignore')


        lastname = line[1].lower().decode('utf-8')
        lastname = _replace_umlauts(lastname).encode('ascii', 'ignore')
        firstname = line[2].lower().decode('utf-8')
        firstname = _replace_umlauts(firstname).encode('ascii', 'ignore')

        password = gen_plain_password()
        cpassword = convert_plain_to_crypt_password(password)
        passwords = {'plain': password, 'crypt' : cpassword}

        matnr = line[0].lower()
        email = line[3].lower()
        group = line[4].lower()

        users[name] = {}
        users[name]['firstname'] = firstname
        users[name]['lastname'] = lastname
        users[name]['passwords'] = passwords
        users[name]['email'] = email
        users[name]['group'] = group
        users[name]['matnr'] = matnr

    group_users = _gen_group_user_data()
    users.update(group_users)

    return dict_from_csv

def _gen_group_user_data():
    users = {}

    for key in GROUPS.keys():
        name = GROUPS[key]
        group_index = key

        if group_index > 10:
            continue

        groups = []
        groups.append('fapra1599')
        groups.append(GROUPS[key])

        plain_password = gen_plain_password()
        crypt_password = convert_plain_to_crypt_password(plain_password)
        passwords = {}
        passwords['crypt'] = crypt_password
        passwords['plain'] = plain_password

        users[name] = {}
        users[name]['passwords'] = passwords
        users[name]['group'] = key
        users[name]['groups'] = ','.join(groups)

    return users

def gen_user_vault_dict(name, dict_from_csv, pw_type='plain'):
    dict_name = dict_from_csv.keys()[0]
    users = {}
    vault_dict = {name : users}

    for key in dict_from_csv[dict_name].keys():
        users[key] = dict_from_csv[dict_name][key]['passwords'][pw_type]


    return vault_dict

def gen_user_group_dict(dict_of_groups):
    name = 'k1599_users_present_groups'
    groups = []
    group_dict = {name : groups}

    for key in dict_of_groups.keys():
        groups.append(dict_of_groups[key])

    return group_dict

def gen_plain_password(length=10):

    cmd = "pwgen -n1 %s" % length
    call = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    password = call.stdout.read()

    return password.rstrip()

def convert_plain_to_crypt_password(pw_string):
    password = subprocess.Popen(['echo', pw_string], stdout=subprocess.PIPE)
    cmd = ['mkpasswd', '-s', '--method=des']
    call = subprocess.Popen(cmd, stdin=password.stdout, stdout=subprocess.PIPE)
    cpassword = call.communicate()[0]

    return cpassword.rstrip()

def print_out_yaml(input_dict):
    output = get_yaml_data(input_dict)
    print output

def get_yaml_data(input_dict):
    output = yaml.dump(input_dict, default_flow_style=False, explicit_start=True)
    return output

def gen_user_dict(dict_from_csv):
    dict_name = dict_from_csv.keys()[0]

    users = []

    for key in dict_from_csv[dict_name].keys():
        group_index = 0
        name = key

        passwords = {}
        passwords['crypt'] = '{{ _vault_user_crypt_password["%s"] }}' % key
        passwords['plain'] = '{{ _vault_user_crypt_password["%s"] }}' % key

        groups = []
        if 'group' in dict_from_csv[dict_name][key]:
            group_index = int(dict_from_csv[dict_name][key]['group'])

            if group_index == 5 or group_index == 10:
                groups.append('sudo')
                groups.append('sshusers')

            groups.append(GROUPS[group_index])

        groups.append('fapra1599')

        dict_from_csv[dict_name][key]['groups'] = ','.join(groups)

        user = {}
        user['name'] = name
        if 'firstname' in dict_from_csv[dict_name][key]:
            user['firstname'] = dict_from_csv[dict_name][key]['firstname']
            user['lastname'] = dict_from_csv[dict_name][key]['lastname']

        user['passwords'] = passwords
        user['groups'] = ','.join(groups)

        users.append(user)

    return users

def write_mail_data_files(dict_from_csv):

    template_loader = jinja2.FileSystemLoader(searchpath="./data/")
    template_env = jinja2.Environment(loader=template_loader)
    mail_template = template_env.get_template(TEMPLATE_FILE)

    dirname = 'mail'

    try:
        os.stat(dirname)
    except OSError:
        os.mkdir(dirname)

    key = dict_from_csv.keys()[0]
    data = dict_from_csv[key]

    for key in data.keys():
        user_name = key
        if user_name in GROUPS.values():
            continue

        user_password = data[key]['passwords']['plain']
        email = data[key]['email']
        group_index = int(data[key]['group'])
        group_name = GROUPS[group_index]
        group_password = data[group_name]['passwords']['plain']

        mail_text = mail_template.render(
            user_name=user_name,
            group_name=group_name,
            group_password=group_password,
            user_password=user_password)

        filename = '/'.join([dirname, email])
        with open(filename, 'w') as wfile:
            wfile.write(mail_text.encode('utf-8'))

def write_data(name, data):
    dirname = 'yaml'

    try:
        os.stat(dirname)
    except OSError:
        os.mkdir(dirname)

    filename = '/'.join([dirname, name])
    with open(filename, 'w') as wfile:
        wfile.writelines(data)


def main(argv):
    parser = argparse.ArgumentParser()
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="print out file content")

    parser.add_argument("-f", "--csv-file", type=str, dest='groupfile',
                        help="csv file to parse the user from")
    args = parser.parse_args(argv)

    if not args.groupfile:
        print "Please provide a csv file as parameter."
        sys.exit(1)
    else:
        data_from_csv = get_csv_content_from_file(args.groupfile)

    dict_of_groups = gen_user_group_dict(GROUPS)
    dict_from_csv = gen_user_data_dict_from_csv(data_from_csv)
    dict_user_data = gen_user_dict(dict_from_csv)
    dict_plain_vault = gen_user_vault_dict('_vault_user_plain_password', dict_from_csv)
    dict_crypt_vault = gen_user_vault_dict('_vault_user_crypt_password', dict_from_csv, 'crypt')

    write_data('user_groups.yml', get_yaml_data(dict_of_groups))
    write_data('plain_password_vault.yml', get_yaml_data(dict_plain_vault))
    write_data('crypt_password_vault.yml', get_yaml_data(dict_crypt_vault))
    write_data('full_user_data.yml', get_yaml_data(dict_from_csv))
    write_data('k1599_users_present_users.yml', get_yaml_data(dict_user_data))

    write_mail_data_files(dict_from_csv)

    if args.verbose:
        print_out_yaml(dict_of_groups)
        print_out_yaml(dict_user_data)
        print_out_yaml(dict_plain_vault)
        print_out_yaml(dict_crypt_vault)


if __name__ == "__main__":
    main(sys.argv[1:])
