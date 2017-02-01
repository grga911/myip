from requests import get as get_url
import json


class Myip:
    """
    Base class for ipinfo
    """
    def __init__(self, name, ip):
        self._name = name
        self.__info = self.__ipinfo(ip)
        self._ip = self.info['ip']
        self._hostname = self.info['hostname']
        self._loc = self.info['loc']
        self._org = self.info['org']
        self._city = self.info['city']
        self._country = self.info['country']

    def __str__(self):
        return 'Location info for {0} :\n'\
                'IP Address : {1}\n'\
                'Hostname : {2}\n'\
                'Country : {3}\n'\
                'City : {4}\n'\
                'Coordinates : {5}\n'\
                'Organization : {6}\n'\
                .format(self.name, self.ip, self.hostname, self.country, self.city, self.loc, self.org)

    def write_to_file(self, filename):
        data = self.info
        # Writing results as json to a file
        with open(filename, 'a+') as file:
            json.dump(
                      data, file,
                      sort_keys=True,
                      indent=4,
                      separators=(',', ':'),
                      ensure_ascii=False)

    def google_maps(self):
        # Get google maps url
        coordinate = str(self.info['loc'])
        gmap_url = 'https://www.google.com/maps?q=@'
        url = gmap_url + coordinate

        return str(url)

    @staticmethod
    def __ipinfo(ip):
        # Get info from ipinfo api
        url = 'http://ipinfo.io/' + ip + '/json'
        response = get_url(url)
        try:
            data = response.json()
            return data
        except:
            print('Check your input')

    @property
    def info(self):

        return self.__info

    @property
    def hostname(self):

        return self._hostname

    @property
    def loc(self):

        return self._loc

    @property
    def city(self):

        return self._city

    @property
    def country(self):

        return self._country

    @property
    def org(self):

        return self._org

    @property
    def name(self):

        return self._name

    @property
    def ip(self):

        return self._ip
