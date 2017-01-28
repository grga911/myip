#!/usr/bin/env  python3
from argparse import ArgumentParser

from dns import resolver
from pyperclip import copy as pcopy
from requests import get as get_url

# Parsing command line arguments passed to script

parser = ArgumentParser( description = 'Simple script for getting your wan ip address, using ipinfo api or via dns' )

parser.add_argument( '-c', '--copy', action = 'store_true', help = 'copy ip address to clipboard' )
parser.add_argument( '-l', '--location', action = 'store_true', help = 'Show location information' )
parser.add_argument( '-i', '--ip', nargs = '?', default = 'myip.opendns.com', help = 'Provide ip address instead' )

args = parser.parse_args( )
# Creating dictionary from arguments
args = vars( args )
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
	for ip in ips:
		url = 'http://ipinfo.io/' + ip + '/json'
		response = get_url( url )
		data.append( response.json( ) )
	return data


def print_location_info( json_data ):
	'''Format json result from ipinfo api and print it'''
	for data in json_data:
		IP = data[ 'ip' ]
		city = data[ 'city' ]
		country = data[ 'country' ]
		coordinates = data[ 'loc' ]
		org = data[ 'org' ]
		print( 'Location info:\n' )
		print( 'IP Address {0}\nCountry : {1} \nCity : {2}\nCoordinates {3}\nOrganization'.format( IP, country, city,
		                                                                                           coordinates, org ) )

# We pass command line arguments to main function
def main( ip = args[ 'ip' ], copy = args[ 'copy' ], location = args[ 'location' ] ):
	# If location flag is off use dns_info and print_ips to print results
	if location == False:
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
		json_data = ipinfo( my_ip )
		print_location_info( json_data )
		if copy == True:
			copy_to_clipboard( json_data )


main( )
