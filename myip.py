#!/usr/bin/python3
from requests import get as get_url
from argparse import ArgumentParser
from dns import resolver
from pyperclip import copy as pcopy

# Parsing command line arguments passed to script

parser = ArgumentParser(description='Simple script for getting your wan ip address, using ipinfo api or via dns')

parser.add_argument('-c', '--copy', action='store_true', help='copy ip address to clipboard')
parser.add_argument('-l','--location',action='store_true',help='Show location information')
parser.add_argument('-i','--ip',nargs='?',default='myip.opendns.com',help='Provide ip address instead')

args=parser.parse_args()
# Creating dictionary from arguments
args=vars(args)
#Setting up dns resolver
MY_RESOLVER=resolver.Resolver()
#Using open dns server
MY_RESOLVER.nameservers=['208.67.222.222']
#Copy results to clipboard
def copy_to_clipboard(data):
	text=''
	try:
		for ip in data:
			text+=ip['ip']+',\n'
	except:
		for ip in data:
			text+=ip
	pcopy(str(text))
#Function for printing ip addresses
def print_ips(ips):
	for ip in ips:
		print('IP Address: {}'.format(ip))
#Geting ip info from open dns via myip.opendns.com
def dns_info(ip):
	my_ip=[]
	#Try to resolve via dns
	try:
		my_answers = MY_RESOLVER.query(ip, "A")
		for ip in my_answers:
			my_ip.append(str(ip))
	#If you can't call ipinfo function
	except:
		print( "Couldn't resolve address, trying with ip info" )
		my_ip.append(ip)
		ipinfo(my_ip)
	return my_ip
#Getting ip info from ipinfo api
def ipinfo(ips):
	data=[]
	for ip in ips:
		url = 'http://ipinfo.io/'+ip+'/json'
		response = get_url(url)
		data.append(response.json())
	return data
#Function for printing json results from ipinfo api
def print_location_info(json_data):
	for data in json_data:
		IP=data['ip']
		city = data['city']
		country=data['country']
		coordinates=data['loc']
		org=data['org']
		print('Location info:\n')
		print('IP Address {0}\nCountry : {1} \nCity : {2}\nCoordinates {3}\nOrganization'.format(IP,country,city,coordinates,org))
# We pass command line arguments to main function
def main(ip=args['ip'],copy=args['copy'],location=args['location']):
	#If location flag is off use dns_info and print_ips to print results
	if location==False:
		# Query dns for ip information
		my_ip = dns_info( ip )
		print_ips(my_ip)
		if copy == True:
			copy_to_clipboard( my_ip )
	#else use ipinfo and print_location_info functions
	else:
	#Ipinfo doesn't require ip address, if left blank it would show wan ip
	#But since we can provide either ip or domain name we need dns_info
		my_ip=dns_info(ip)
		json_data = ipinfo( my_ip )
		print_location_info(json_data)
		if copy == True:
			copy_to_clipboard( json_data )

# Calling main function
main()
