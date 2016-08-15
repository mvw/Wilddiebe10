#!/usr/bin/env python
#-*- coding: UTF-8 -*-

import argparse
import copy
import csv
import sys
import subprocess
import yaml

REPLACE_UMLAUTS = {
    u"ö" : 'oe',
    u"ü" : 'ue',
    u"ä" : 'ae',
    u"ß" : 'ss',
}

GROUPS = {
    '1' : 'web-nord',
    '2' : 'mail-nord',
    '3' : 'netz-nord',
    '4' : 'cert-nord',
    '5' : 'file-nord',
    '6' : 'web-sued',
    '7' : 'mail-sued',
    '8' : 'netz-sued',
    '9' : 'cert-sued',
    '10' : 'file-sued',
    '11' : 'sshusers',
    '12' : 'fapra1599',
}


def _replace_umlauts(str2rep):
    string2return = str2rep
    for key, value in REPLACE_UMLAUTS.iteritems():
        string2return = string2return.replace(key, value)
    return string2return

def get_content(fname):

    content = []

    with open(fname, 'rb') as csvfile:
        lines = csv.reader(csvfile, delimiter=',', quotechar='"')
        for line in lines:
            content.append(line)

    return content

def get_user_data(csv_data, dict_name='k1599_users_present_users'):
    users = {}
    dict_from_csv = {dict_name : users}

    for line in csv_data:
        if line[0] == '' or line[0] == 'matrikelnr':
            continue

        name = "%s%s" % (line[2][0].lower().decode('utf-8'), line[1].lower().decode('utf-8'))
        name = _replace_umlauts(name).encode('ascii', 'ignore')

        password = get_plain_password()
        cpassword = get_crypt_password(password)
        passwords = {'plain': password, 'crypt' : cpassword}

        email = line[3].lower()
        group = line[4].lower()
        matnr = line[0].lower()

        users[name] = {}
        users[name]['passwords'] = passwords
        users[name]['email'] = email
        users[name]['group'] = group
        users[name]['matnr'] = matnr
    return dict_from_csv


def get_user_vault(name, dict_from_csv, pw_type='plain'):
    dict_name = dict_from_csv.keys()[0]
    users = {}
    vault_dict = {name : users}

    for key in dict_from_csv[dict_name].keys():
        users[key] = dict_from_csv[dict_name][key]['passwords'][pw_type]

    return vault_dict

def get_user_groups(dict_of_groups):
    name = 'k1599_users_present_groups'
    groups = []
    group_dict = {name : groups}

    for key in dict_of_groups.keys():
        groups.append(dict_of_groups[key])

    return group_dict

def get_plain_password(length=10):

    cmd = ['pwgen', str(length), '-n1']
    call = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE)
    password = call.stdout.read()

    return password.rstrip()

def get_crypt_password(pw_string):
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

def filter_user_data(dict_from_csv):
    clean_dict = copy.deepcopy(dict_from_csv)
    dict_name = clean_dict.keys()[0]

    for key in clean_dict[dict_name].keys():
        clean_dict[dict_name][key]['passwords']['crypt'] = '{{ _vault_user_crypt_password["%s"] }}' % key
        clean_dict[dict_name][key]['passwords']['plain'] = '{{ _vault_user_plain_password["%s"] }}' % key
        if 'email' in clean_dict[dict_name][key]:
            del clean_dict[dict_name][key]['email']

        if 'matnr' in clean_dict[dict_name][key]:
            del clean_dict[dict_name][key]['matnr']

        if 'group' in clean_dict[dict_name][key]:
            group_index = clean_dict[dict_name][key]['group']
            del clean_dict[dict_name][key]['group']

        groups = []
        if group_index == '5' or group_index == '10':
            groups.append('sudo')
            groups.append('sshusers')
        groups.append('fapra1599')
        groups.append(GROUPS[group_index])

        clean_dict[dict_name][key]['groups'] = ','.join(groups)

    return clean_dict

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
        data_from_csv = get_content(args.groupfile)

    dict_of_groups = get_user_groups(GROUPS)

    dict_from_csv = get_user_data(data_from_csv)
    dict_user_data = filter_user_data(dict_from_csv)
    dict_plain_vault = get_user_vault('_vault_user_plain_password', dict_from_csv)
    dict_crypt_vault = get_user_vault('_vault_user_crypt_password', dict_from_csv, 'crypt')

    with open('user_groups.yml', 'w') as wfile:
        data = get_yaml_data(dict_of_groups)
        wfile.writelines(data)

    with open('plain_password_vault.yml', 'w') as wfile:
        data = get_yaml_data(dict_plain_vault)
        wfile.writelines(data)

    with open('crypt_password_vault.yml', 'w') as wfile:
        data = get_yaml_data(dict_crypt_vault)
        wfile.writelines(data)

    with open('full_user_data.yml', 'w') as wfile:
        data = get_yaml_data(dict_from_csv)
        wfile.writelines(data)

    with open('k1599_users_present_users.yml', 'w') as wfile:
        data = get_yaml_data(dict_user_data)
        wfile.writelines(data)

    if args.verbose:
        print_out_yaml(dict_of_groups)
        print_out_yaml(dict_user_data)
        print_out_yaml(dict_plain_vault)
        print_out_yaml(dict_crypt_vault)


if __name__ == "__main__":
    main(sys.argv[1:])
