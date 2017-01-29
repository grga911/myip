#!/usr/bin/env  python3
import json
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


def copy_to_clipboard( data ):
	'''Format text and copy it to clipboard'''
	text = ''
	try:
		for ip in data:
			text += ip[ 'ip' ] + ',\n'
	except:
		for ip in data:
			text += ip
	pcopy( str( text ) )


def print_ips( ips ):
	'''Print ips'''
	for ip in ips:
		print( 'IP Address: {}'.format( ip ) )


def dns_info( ip ):
	'''Get ip info via dns, using myip.opendns.com'''
	my_ip = [ ]
	try:
		my_answers = MY_RESOLVER.query( ip, "A" )
		for ip in my_answers:
			my_ip.append( str( ip ) )
	except:
		print( "Couldn't resolve address, trying with ip info" )
		my_ip.append( ip )
		ipinfo( my_ip )
	return my_ip


def ipinfo( ips ):
	'''Get info from ipinfo api'''
	data = [ ]
	try:
		for ip in ips:
			url = 'http://ipinfo.io/' + ip + '/json'
			response = get_url( url )
			data.append( response.json( ) )
	except (RuntimeError, TypeError, NameError) as error:
		print( error )
	return data


def print_location_info( json_data ):
	'''Format json result from ipinfo api and print it'''
	try:
		json_data = json.loads( json_data )
		for data in json_data:
			IP = data[ 'ip' ]
			city = data[ 'city' ]
			country = data[ 'country' ]
			coordinates = data[ 'loc' ]
			org = data[ 'org' ]
			print( 'Location info:\n' )
			print(
				'IP Address {0}\nCountry : {1} \nCity : {2}\nCoordinates {3}\nOrganization'.format( IP, country, city,
		                                                                                           coordinates, org ) )
	except:
		print( 'Not a valid json, check domain or ip address' )


def output_file( filename, data ):
	'''Writing results as json to a file'''
	with open( filename, 'a+' ) as file:
		json.dump( data, file, sort_keys = True, indent = 4, separators = (',', ':'), ensure_ascii = False )
	pass
# We pass command line arguments to main function
def main( ip = args.ip, copy = args.copy, location = args.location, out = args.output ):
	# If location flag is off use dns_info and print_ips to print results
	if not location:
		# Query dns for ip information
		my_ip = dns_info( ip )
		print_ips( my_ip )
		if copy == True:
			copy_to_clipboard( my_ip )
	# else use ipinfo and print_location_info functions
	else:
		# Ipinfo doesn't require ip address, if left blank it would show wan ip
		# But since we can provide either ip or domain name we need dns_info
		my_ip = dns_info( ip )
		json_data = json.dumps( ipinfo( my_ip ), sort_keys = True )
		print_location_info( json_data )
		if out != '':
			output_file( filename = out[ 0 ], data = json.loads( json_data ) )
		if copy:
			copy_to_clipboard( json_data )


main( )
