#!/usr/bin/env  python
'''Simple script to check wan ip address
 or to get information for ip address'''
import ipaddress
import json
import sys
from argparse import ArgumentParser
from dns import resolver
from pyperclip import copy as pcopy
from requests import get as get_url


class NotDomain(Exception):
    pass

# Parsing command line arguments passed to script

parser = ArgumentParser(
                    description='Simple script for getting your wan ip address'
                    ' or info for an ip address or domain, '
                    'using ipinfo api or via dns')

parser.add_argument('-c', '--copy',
                    action='store_true',
                    help='copy ip address to clipboard')

parser.add_argument('-l', '--location',
                    action='store_true',
                    help='Show location information')

parser.add_argument('-i', '--ip',
                    nargs='?',
                    type=str,
                    default='myip.opendns.com',
                    help='Provide ip address instead')

parser.add_argument('-o', '--output',
                    nargs='+',
                    default='',
                    help='Output results to a file')

args = parser.parse_args()
# Setting up dns resolver
MY_RESOLVER = resolver.Resolver()
# Using open dns server
MY_RESOLVER.nameservers = ['208.67.222.222']


def is_valid_ipv4_address(address):
    # Validate ip address
    try:
        ipaddr = ipaddress.IPv4Address(address)
        return ipaddr.is_global
    except ipaddress.AddressValueError:
        return False


def copy_to_clipboard(ip, text):
    # Format text and copy it to clipboard#
    # If user provided ip address then copy hostname to clipboard
    # else copy resolved ip address
    if is_valid_ipv4_address(ip):
        pcopy(text['hostname'])
    else:
        pcopy(str(text['ip']))


def dns_info(domain):
    # Get ip info via dns, default(myip.opendns.com)
    try:
        my_answers = MY_RESOLVER.query(domain, "A")
    except:
        raise NotDomain
    else:
        my_ip = str(my_answers[0])
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
    if is_valid_ipv4_address(domain):
        my_ip = domain
    else:
        try:
            my_ip = dns_info(domain)
        except NotDomain:
            print("Couldn't resolve, check ip or domain")
            sys.exit(1)
    return my_ip


def print_location_info(data):
    # Format json result from ipinfo api and print it
    try:
        ip = data['ip']
        city = data['city']
        country = data['country']
        coordinates = data['loc']
        org = data['org']
        host = data['hostname']
        print('Location info:\n')
        print('IP Address {0}\n'
              'Hostname {4}\n'
              'Country : {1}\n'
              'City : {2}\n'
              'Coordinates {3}\n'
              'Organization'
              .format(ip, country, city, coordinates, org, host))
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
    pass


# We pass command line arguments to main function
def main(ip=args.ip, copy=args.copy, location=args.location, out=args.output):
    try:
        # Try to figure out if user passed ip or domain name,
        # either way get valid ip and pass it to ipinfo
        my_ip = get_ip(ip)
        my_ip_info = ipinfo(my_ip)
    except:
        print('Error occurred')
    # If everything went fine, check for flags
    else:
        if location:
            print_location_info(my_ip_info)
        else:
            if is_valid_ipv4_address(ip):
                print('Domain or hostname: ', my_ip_info['hostname'])
            else:
                print('IP address :', my_ip)
        if copy:
            copy_to_clipboard(ip, my_ip_info)
        if out != '':
            output_json(filename=out[0], data=my_ip_info)


main()
