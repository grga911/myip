#!/usr/bin/env  python3

import json
import pprint
from argparse import ArgumentParser
from dns import resolver
from pyperclip import copy as pcopy
from requests import get as get_url

# Parsing command line arguments passed to script

parser = ArgumentParser( description = 'Simple script for getting your wan ip address, using ipinfo api or via dns' )

parser.add_argument( '-c', '--copy', action = 'store_true', help = 'copy ip address to clipboard' )
parser.add_argument( '-l', '--location', action = 'store_true', help = 'Show location information' )
parser.add_argument( '-i', '--ip', nargs = '?', default = 'myip.opendns.com', help = 'Provide ip address instead' )
parser.add_argument( '-o', '--output', nargs = '+', default = '', help = 'Output results to a file' )

args = parser.parse_args( )
# Setting up dns resolver
MY_RESOLVER = resolver.Resolver( )
# Using open dns server
MY_RESOLVER.nameservers = [ '208.67.222.222' ]

class NotDomainError(Exception):
	def __init__(self, text="Not a domain error"):
		self.text= text
	def __str__(self):
		return repr(self.text)

def copy_to_clipboard( data ):
	'''Format text and copy it to clipboard'''
	text = ''
	try:
		text += data[ 'hostname' ]
	except:
		text += data
	pcopy( str( text ) )


def print_ips( ip ):
	'''Print ips'''
	print( 'IP Address: {}'.format( ip ) )


def dns_info( ip):
	'''Get ip info via dns, using myip.opendns.com'''
	try:
		my_answers = MY_RESOLVER.query( ip, "A" )
	except:
		raise Exception()
	my_ip = str( my_answers[ 0 ] )
	return my_ip


def ipinfo( ip ):
	'''Get info from ipinfo api'''
	try:
		url = 'http://ipinfo.io/' + ip + '/json'
		response = get_url( url )
		data = response.json()
		return data
	except (RuntimeError, TypeError, NameError) as error:
		print( error )

def get_ip(ip,loc,cp):
	try:
		my_ip=dns_info(ip)
		if cp:
			copy_to_clipboard(my_ip)
		if not loc:
			print_ips(my_ip)
	except:
		info=ipinfo(ip)
		my_ip=info['ip']
		if cp:
			copy_to_clipboard(info)
		if not loc:
				print('Domain Name', info['hostname'])
	return my_ip
def print_location_info( data ):
	'''Format json result from ipinfo api and print it'''
	try:
		IP = data[ 'ip' ]
		city = data[ 'city' ]
		country = data[ 'country' ]
		coordinates = data[ 'loc' ]
		org = data[ 'org' ]
		host = data['hostname']
		print( 'Location info:\n' )
		print('IP Address {0}\nHostname {4}\nCountry : {1} \nCity : {2}\nCoordinates {3}\nOrganization'.format( IP, country, city,coordinates, org, host ) )
	except:
		print( 'Not a valid json, check domain or ip address' )


def output_json( filename, data ):
	'''Writing results as json to a file'''
	with open( filename, 'a+' ) as file:
		json.dump( data, file, sort_keys = True, indent = 4, separators = (',', ':'), ensure_ascii = False )
	pass
# We pass command line arguments to main function
def main( ip = args.ip, copy = args.copy, location = args.location, out = args.output ):
	# If location flag is off use dns_info and print_ips to print results
		my_ip = get_ip( ip,location,copy)
		if location:
			print_location_info(ipinfo(my_ip))
		if out != '':
			out_json=ipinfo(my_ip)
			output_json( filename = out[0], data = out_json )

main( )
