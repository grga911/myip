# myip

usage: myip.py [-h] [-c] [-d] [-l] [-i [IP]]

Simple script for getting your wan ip address, using ipinfo api or via dns

optional arguments:
  -h, --help          show this help message and exit
  -c, --copy          copy ip address to clipboard
  -d, --dns           Use dns instead of ipinfo api
  -l, --location      Show location information (currently working only with
                      ipinfo api)
  -i [IP], --ip [IP]  Provide ip address instead
