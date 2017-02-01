"""
Set of functions used by myip
"""

from socket import gethostbyname as dns_query
from pyperclip import copy as pcopy
from requests import get as get_url
import ipaddress
import json
import sys

class NotDomain(Exception):
    pass

def google_maps(coordinate):
    # Get google maps url
    gmap_url = 'https://www.google.com/maps?q=%40'
    url = gmap_url + coordinate
    return url


def is_valid_ipv4_address(address):
    # Validate ip address
    try:
        ipaddr = ipaddress.IPv4Address(address)
        return ipaddr.is_global
    except ipaddress.AddressValueError:
        return False


def copy_info(ip, text):
    if is_valid_ipv4_address(ip):
        copy_data = (text['hostname'])
    else:
        copy_data = (str(text['ip']))
    return copy_data


def copy_to_clipboard(text):
    # Format text and copy it to clipboard
    # If user provided ip address then copy hostname to clipboard
    # else copy resolved ip address
    copy_data = ''
    for i in text:
        copy_data += i + ' \n'
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


def ipinfo(ip):
    # Get info from ipinfo api
    url = 'http://ipinfo.io/' + ip + '/json'
    response = get_url(url)
    try:
        data = response.json()
        return data
    except:
        print('Check your input')


def get_ip(domain):
    # Resolve domain to ip or return ip if it's valid ipv4 address
    if is_valid_ipv4_address(domain) or domain == '':
        my_ip = domain
    else:
        try:
            my_ip = dns_info(domain)
        except NotDomain:
            print("Couldn't resolve {}, check ip or domain\n".format(domain))
            sys.exit(1)
    return my_ip


def print_location_info(data, name):
    # Format json result from ipinfo api and print it
    try:
        ip = data['ip']
        city = data['city']
        country = data['country']
        coordinates = data['loc']
        org = data['org']
        host = data['hostname']
        print('Location info for {0}:\n\n'
              'IP Address {1}\n'
              'Hostname {2}\n'
              'Country : {3}\n'
              'City : {4}\n'
              'Coordinates {5}\n'
              'Organization{6}\n'
              .format(name, ip, host, country, city, coordinates, org))
    except:
        print('Not a valid json, check domain or ip address')


def output_json(filename, data):
    # Writing results as json to a file
    with open(filename, 'a+') as file:
        json.dump(data, file,
                  sort_keys=True,
                  indent=4,
                  separators=(',', ':'),
                  ensure_ascii=False)


def open_file(file):
    my_ips_list = []
    try:
        with open(file, mode = 'r') as f:
            for ip in f.readlines():
                my_ips_list.append(ip)
    except IOError:
        print('Could not read file')
        sys.exit(1)
    else:
        my_ips_list = [i.strip() for i in my_ips_list]
        return my_ips_list