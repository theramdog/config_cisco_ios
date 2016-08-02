#!/usr/bin/env python

#Script requires installation of the following on the host it will be executed from: python3-paramiko (via package manager), python-logilab-common (aka pytest, package manager), python-scp (via package manager), python-pip (via package manager), pysnmp (via pip), and netmiko (via pip)
#Script syntax: python configios.py config.txt verify.txt
#config.txt and verify.txt will feed the script commands to execute much like a copy/paste from a text editor to the cli would

from netmiko import ConnectHandler
from getpass import getpass
from datetime import datetime
from sys import argv

script, config_file, verify_file = argv

def config(net_connect, start_time):
    print('------------------------------------')
    print('Issuing configuration commands...')
    print('------------------------------------')
    config_output = net_connect.send_config_from_file(config_file)
    print(config_output)
    verify(net_connect, start_time)

def verify(net_connect, start_time):
    print('------------------------------------')
    print('Verifying configuration...')
    print('------------------------------------')
    verify_output = net_connect.send_config_from_file(verify_file)
    print(verify_output)
    end_time = datetime.now()
    total_time = end_time - start_time
    print('------------------------------------')
    print('Time to complete: %s') % total_time
    print('------------------------------------')
    commit(net_connect)

def commit(net_connect):
    commit_choice = raw_input('Would you like to commit the configuration (y/n)?: ')
    if commit_choice == 'y' in commit_choice or 'Y' in commit_choice or 'yes' in commit_choice or 'YES' in commit_choice:
        commit_command = ('wr')
        commit_output = net_connect.send_command(commit_command)
        print('------------------------------------')
        print(commit_output)
        print('------------------------------------')
        print('------------------------------------')
        print('Configuration has been committed')
        print('------------------------------------')
    else:
        print('------------------------------------')
        print('Configuration has NOT been committed')
        print('------------------------------------')

def main():
    ip_address = raw_input('Enter IP address: ')
    device = {
        'device_type' : 'cisco_ios',
        'ip' : ip_address,
        'username' : raw_input('Enter username: '),
        'password' : getpass(),
    }
    net_connect = ConnectHandler(**device)
    start_time = datetime.now()
    config(net_connect, start_time)

if __name__ == "__main__":
    main()

quit()
