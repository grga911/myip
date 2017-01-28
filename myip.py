#!/usr/bin/python3
import re
import json
from requests import get as get_url
from argparse import ArgumentParser
from dns import resolver
from pyperclip import copy as pcopy

parser = ArgumentParser(description='Simple script for getting your wan ip address, using ipinfo api or via dns')

parser.add_argument('-c', '--copy', action='store_true', help='copy ip address to clipboard')
parser.add_argument('-d','--dns',action='store_true', help='Use dns instead of ipinfo api')
parser.add_argument('-l','--location',action='store_true',help='Show location information (currently working only with ipinfo api)')
parser.add_argument('-i','--ip',nargs='?',default='myip.opendns.com',help='Provide ip address instead')

args=parser.parse_args()
args=vars(args)

MY_RESOLVER=resolver.Resolver()
MY_RESOLVER.nameservers=['208.67.222.222']
DOMAIN_REGEX=re.compile(r'[a-zZ-a]')

def copy_to_clipboard(data):
	text=''
	for ip in data:
		text+=ip['ip']+'\n'
	pcopy(str(text))
# resolve my ip via dns
def dns_info(ip):
	if bool(DOMAIN_REGEX.search(ip)):
		my_ip=[]
		try:
			my_answers = MY_RESOLVER.query(ip, "A")
			for ip in my_answers:
				my_ip.append(str(ip))
		except:
			print("Couldn't resolve address")
	else:
		my_ip.append(ip)
		ipinfo(my_ip)
	return my_ip

def ipinfo(ips):
	data=[]
	for ip in ips:
		url = 'http://ipinfo.io/'+ip+'/json'
		response = get_url(url)
		data.append(response.json())
	return data

def location_info(json_data):	

	for data in json_data:
		IP=data['ip']
		city = data['city']
		country=data['country']
		coordinates=data['loc']
		org=data['org']
		print('Location info:\n')
		print('IP Address {0}\nCountry : {1} \nCity : {2}\nCoordinates {3}\nOrganization'.format(IP,country,city,coordinates,org))

def main(ip=args['ip'],copy=args['copy'],location=args['location'],dns=args['dns']):

	my_ip=dns_info(ip)
	json_data = ipinfo(my_ip)
	if location==True:
		location_data = location_info(json_data)
	if copy==True:
		copy_to_clipboard(json_data)
	for ip in json_data:
		print('IP Address: {}'.format(ip['ip']))


main()