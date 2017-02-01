#!/usr/bin/env  python
'''
Simple script to check wan ip address
or to get information for ip address
'''
import ipaddress
import json
import sys
import argparse
from socket import gethostbyname as dns_query
from pyperclip import copy as pcopy
from requests import get as get_url


class NotDomain(Exception):
    pass

# Parsing command line arguments passed to script

parser = argparse.ArgumentParser(
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
                    nargs='+',
                    default=[''],
                    help='Provide ip address instead')

parser.add_argument('-o', '--output',
                    nargs=1,
                    default='',
                    help='Output results to a file')

parser.add_argument('-g', '--gmap',
                    action='store_true',
                    help='Get google maps link')

parser.add_argument('-f', '--file',
                    nargs=1,
                    help='Read list of ip addresses from file')

args = parser.parse_args()


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


# We pass command line arguments to main function
def main(ips=args.ip, copy=args.copy, location=args.location, out=args.output, gmap=args.gmap, file=args.file):
    copy_data = []
    ip_list = []
    # Create list of ip addresses to process
    if file and ips!=['']:
        for f in file:
            ip_list = open_file(f)
        ip_list.extend(ips)
    elif file:
        for f in file:
            ip_list = open_file(f)
    else:
        ip_list = ips

    for ip in ip_list:
        try:
            # Try to figure out if user passed ip or domain name,
            # either way get valid ip and pass it to ipinfo
            my_ip = get_ip(ip)
            my_ip_info = ipinfo(my_ip)
            copy_data.append(copy_info(ip, my_ip_info))
        except:
            pass
        # If everything went fine, check for flags
        else:
            if location:
                if ip == 'myip.opendns.com':
                    ip = 'your ip'
                print_location_info(my_ip_info, ip)
            else:
                if ip == '':
                    print( 'Your IP : {}'.format(my_ip_info['ip']))
                elif is_valid_ipv4_address(ip):
                    print('Hostname of ip {}: {}'.format(ip, my_ip_info['hostname']))
                else:
                    print( 'IP address for {}: {}'.format(ip, my_ip))
            if out != '':
                output_json(filename=out[0], data=my_ip_info)
            if gmap:
                map_link = google_maps(my_ip_info['loc'])
                print('Google maps link for {}: {}\n'.format(ip, map_link))
    if copy:
        copy_to_clipboard(copy_data)
main()
