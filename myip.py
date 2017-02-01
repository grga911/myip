#!/usr/bin/env  python
'''
Simple script to check wan ip address
or to get information for ip address
'''
from myip_func import *
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
