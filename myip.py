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
    # Check and create dictionary of valid ip addresses
    ip_list = create_ip_list(ips, file)
    # Go through dictionary and get information from ipinfo
    for name, ip in ip_list.items():
        try:
            # Create instance of Myip class
            my_ip = Myip(name, ip)
            my_ip.ipinfo(ip)
            # Create list of values to be copied into clipboard if needed
            copy_data.append(copy_info(name, my_ip.info))
        except:
            print('Something went wrong!')
        # If everything went fine, check for flags
        else:
            # Main print Function
            print_info(location, my_ip, name)
            # Check for other flags
            if out != '':
                # Write results to file
                my_ip.write_to_file(filename=out[0])
            if gmap:
                map_link = my_ip.google_maps()
                print('Google maps link for {}: {}\n'.format(name, map_link))
    if copy:
        copy_to_clipboard(copy_data)
main()
