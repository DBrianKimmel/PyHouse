"""
@name:      PyHouse/src/Modules/Computer/Internet/test/xml_internet.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 8, 2014
@Summary:

"""

__updated__ = '2016-10-19'

L_INTERNET_SECTION_START = '<InternetSection>'
L_INTERNET_SECTION_END = '</InternetSection>'
L_INTERNET_LOCATE_URL_SECTION_START = '<LocateUrlSection>'
L_INTERNET_LOCATE_URL_SECTION_END = '</LocateUrlSection>'
L_INTERNET_UPDATE_URL_SECTION_START = '<UpdateUrlSection>'
L_INTERNET_UPDATE_URL_SECTION_END = '</UpdateUrlSection>'

TESTING_INTERNET_LOCATE_URL_0 = 'http://snar.co/ip/'
TESTING_INTERNET_LOCATE_URL_1 = 'http://checkip.dyndns.com/'
TESTING_INTERNET_UPDATE_URL_0 = 'http://freedns.afraid.org/dynamic/update.php?12345'
TESTING_INTERNET_UPDATE_URL_1 = 'http://freedns.afraid.org/dynamic/update.php?ABCDE'
TESTING_INTERNET_IPv4 = '65.35.48.61'
TESTING_INTERNET_IPv6 = '2001:db8::1'
TESTING_INTERNET_LAST_CHANGED = '2014-10-02T12:34:56'
TESTING_INTERNET_UPDATE_INTERVAL_0 = '86400'

L_INTERNET_LOCATE_URL_0 = '    <LocateUrl>' + TESTING_INTERNET_LOCATE_URL_0 + '</LocateUrl>'
L_INTERNET_LOCATE_URL_1 = '    <LocateUrl>' + TESTING_INTERNET_LOCATE_URL_1 + '</LocateUrl>'
L_INTERNET_UPDATE_URL_0 = '    <UpdateUrl>' + TESTING_INTERNET_UPDATE_URL_0 + '</UpdateUrl>'
L_INTERNET_UPDATE_URL_1 = '    <UpdateUrl>' + TESTING_INTERNET_UPDATE_URL_1 + '</UpdateUrl>'
L_INTERNET_IPv4 = '    <ExternalIPv4>' + TESTING_INTERNET_IPv4 + '</ExternalIPv4>'
L_INTERNET_IPv6 = '    <ExternalIPv6>' + TESTING_INTERNET_IPv6 + '</ExternalIPv6>'
L_INTERNET_LAST_CHANGED = '    <LastChanged>' + TESTING_INTERNET_LAST_CHANGED + '</LastChanged>'
L_INTERNET_UPDATE_INTERVAL = '    <UpdateInterval>' + TESTING_INTERNET_UPDATE_INTERVAL_0 + '</UpdateInterval>'

XML_LOCATER_URL = '\n'.join([
    L_INTERNET_LOCATE_URL_SECTION_START,
        L_INTERNET_LOCATE_URL_0,
        L_INTERNET_LOCATE_URL_1,
    L_INTERNET_LOCATE_URL_SECTION_END
])

XML_UPDATER_URL = '\n'.join([
    L_INTERNET_UPDATE_URL_SECTION_START,
        L_INTERNET_UPDATE_URL_0,
        L_INTERNET_UPDATE_URL_1,
    L_INTERNET_UPDATE_URL_SECTION_END
])

XML_INTERNET = '\n'.join([
    L_INTERNET_SECTION_START,
        XML_LOCATER_URL,
        XML_UPDATER_URL,
        L_INTERNET_IPv4,
        L_INTERNET_IPv6,
        L_INTERNET_LAST_CHANGED,
        L_INTERNET_UPDATE_INTERVAL,
    L_INTERNET_SECTION_END
])

# ## END DBK
