# myip

Disclaimer:
This script uses ipinfo api, which can be used for free up to 1000 queries a day.
For more information go to http://ipinfo.io/developers/terms-of-use .

Demo avaiable at https://asciinema.org/a/9jmu3058rtzvtwhf6ql8twk2n .

usage: myip.py [-h] [-c] [-l] [-i [IP]]

Simple script for getting your wan ip address, using ipinfo api or via dns

optional arguments:

  -h, --help          show this help message and exit
  
  -c, --copy          copy ip address to clipboard
  
  -l, --location      Show location information (currently working only with
                      ipinfo api)
                      
  -i [IP], --ip [IP]  Provide ip address instead
