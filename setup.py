from setuptools import setup

setup(
	name = 'myip',
	version = '1.1',
	packages = [ 'myip' ],
	url = 'https://github.com/grga911',
	license = 'MIT',
	author = 'grga911',
	author_email = '',
	description = 'Simple scipt for getting your wan ip', install_requires = [ 'dnspython', 'pyperclip', 'requests' ]
)
