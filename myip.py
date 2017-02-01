#!/usr/bin/env  python

from myip_func import *
from myip_class import *
import argparse


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


# We pass command line arguments to main function
def main(ips=args.ip, copy=args.copy, location=args.location, out=args.output, gmap=args.gmap, file=args.file):
    copy_data = []
    ip_check_list = []
    ip_list = {}
    # Create list of ip addresses to process
    if not ips and not file:
        ip_list['Your ip'] = ''
    if file:
        for f in file:
            ip_check_list = read_from_file(f)
    if ips:
        ip_check_list.extend(ips)

    for i in ip_check_list:
        ip = get_ip(i)
        if ip:
            ip_list[i] = ip

    for name, ip in ip_list.items():
        try:
            # Try to figure out if user passed ip or domain name,
            # either way get valid ip and pass it to ipinfo
            my_ip = Myip(name, ip)
            my_ip_info = my_ip.info
            copy_data.append(copy_info(name, my_ip_info))
        except:
            print('Something went wrong!')
        # If everything went fine, check for flags
        else:
            if location:
                print(my_ip)
            else:
                if is_valid_ipv4_address(name):
                    print('{} info: {}'.format(name, my_ip.hostname))
                else:
                    print('{} info: {}'.format(name, my_ip.ip))
            if out != '':
                my_ip.write_to_file(filename=out[0])
            if gmap:
                map_link = my_ip.google_maps()
                print('Google maps link for {}: {}\n'.format(name, map_link))
    if copy:
        copy_to_clipboard(copy_data)
main()
