"""
Set of functions used by myip
"""

from socket import gethostbyname as dns_query
from pyperclip import copy as pcopy
import ipaddress
import sys


class NotDomain(Exception):
    pass


def is_valid_ipv4_address(address):
    # Validate ip address
    try:
        ipaddr = ipaddress.IPv4Address(address)
        return ipaddr.is_global
    except ipaddress.AddressValueError:
        return False


def copy_info(ip, text):
    copy_data = {}
    if is_valid_ipv4_address(ip):
        copy_data[text['ip']] = text['hostname']
    else:
        copy_data[text['hostname']] = text['ip']
    return copy_data


def copy_to_clipboard(text):
    # Format text and copy it to clipboard
    # If user provided ip address then copy hostname to clipboard
    # else copy resolved ip address
    copy_data = ''
    for data in text:
        for name, ip in data.items():
            copy_data += name + ' : ' + ip + ' \n'
    pcopy(str(copy_data))


def dns_info(domain):
    # Get ip info via dns, default(myip.opendns.com)
    try:
        my_answers = dns_query(domain)
    except:
        raise NotDomain
    else:
        my_ip = str(my_answers)
    return my_ip


def get_ip(domain):
    # Resolve domain to ip or return ip if it's valid ipv4 address
    if is_valid_ipv4_address(domain):
        my_ip = domain
        return my_ip
    else:
        try:
            my_ip = dns_info(domain)
            return my_ip
        except NotDomain:
            print("Couldn't resolve {}, check ip or domain\n".format(domain))


def read_from_file(file):
    my_ips_list = []
    try:
        with open(file, mode = 'r') as f:
            for ip in f.readlines():
                my_ips_list.append(ip)
        my_ips_list = [i.strip() for i in my_ips_list]
    except IOError:
        print('Could not read file')
        sys.exit(1)
    return my_ips_list
