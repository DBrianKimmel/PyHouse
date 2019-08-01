"""
@name:      PyHouse/src/Modules/Computer/Internet/_test/xml_internet.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 8, 2014
@Summary:   Testing multiple internet connection structures.

InternetSection
  Internet Name Active Key
    ExternamIPv4
    ExternamIPv6
    LastChanged
    UpdateInterval
    LocateUrl
    UpdateUrl
"""

__updated__ = '2017-12-21'

L_INTERNET_SECTION_START = '<InternetSection>'
L_INTERNET_SECTION_END = '</InternetSection>'
L_INTERNET_END = '</Internet>'
L_INTERNET_LOCATE_URL_SECTION_START = '<LocateUrlSection>'
L_INTERNET_LOCATE_URL_SECTION_END = '</LocateUrlSection>'
L_INTERNET_UPDATE_URL_SECTION_START = '<UpdateUrlSection>'
L_INTERNET_UPDATE_URL_SECTION_END = '</UpdateUrlSection>'

TESTING_INTERNET_NAME_0 = 'InternetName0'
TESTING_INTERNET_KEY_0 = '0'
TESTING_INTERNET_ACTIVE_0 = 'True'

L_INTERNET_START_0 = \
        '<Internet Name="' + TESTING_INTERNET_NAME_0 + \
        '" Key="' + TESTING_INTERNET_KEY_0 + \
        '" Active="' + TESTING_INTERNET_ACTIVE_0 + \
        '">'

TESTING_INTERNET_IPv4_0 = '65.35.48.61'
TESTING_INTERNET_IPv6_0 = '2001:db8::1'
TESTING_INTERNET_LAST_CHANGED_0 = '2014-10-02 12:34:56'
TESTING_INTERNET_UPDATE_INTERVAL_0 = '86400'

L_INTERNET_IPv4_0 = '    <ExternalIPv4>' + TESTING_INTERNET_IPv4_0 + '</ExternalIPv4>'
L_INTERNET_IPv6_0 = '    <ExternalIPv6>' + TESTING_INTERNET_IPv6_0 + '</ExternalIPv6>'
L_INTERNET_LAST_CHANGED_0 = '    <LastChanged>' + TESTING_INTERNET_LAST_CHANGED_0 + '</LastChanged>'
L_INTERNET_UPDATE_INTERVAL_0 = '    <UpdateInterval>' + TESTING_INTERNET_UPDATE_INTERVAL_0 + '</UpdateInterval>'

TESTING_INTERNET_LOCATE_URL_0_0 = 'http://snar.co/ip/'
TESTING_INTERNET_LOCATE_URL_0_1 = 'http://ipv4bot.whatismyipaddress.com/'

L_INTERNET_LOCATE_URL_0_0 = '    <LocateUrl>' + TESTING_INTERNET_LOCATE_URL_0_0 + '</LocateUrl>'
L_INTERNET_LOCATE_URL_0_1 = '    <LocateUrl>' + TESTING_INTERNET_LOCATE_URL_0_1 + '</LocateUrl>'

XML_LOCATER_URL_0 = '\n'.join([
    L_INTERNET_LOCATE_URL_SECTION_START,
        L_INTERNET_LOCATE_URL_0_0,
        L_INTERNET_LOCATE_URL_0_1,
    L_INTERNET_LOCATE_URL_SECTION_END
])

TESTING_INTERNET_UPDATE_URL_0_0 = 'http://freedns.afraid.org/dynamic/update.php?12345'
TESTING_INTERNET_UPDATE_URL_0_1 = 'http://freedns.afraid.org/dynamic/update.php?ABCDE'

L_INTERNET_UPDATE_URL_0_0 = '    <UpdateUrl>' + TESTING_INTERNET_UPDATE_URL_0_0 + '</UpdateUrl>'
L_INTERNET_UPDATE_URL_0_1 = '    <UpdateUrl>' + TESTING_INTERNET_UPDATE_URL_0_1 + '</UpdateUrl>'

XML_UPDATER_URL_0 = '\n'.join([
    L_INTERNET_UPDATE_URL_SECTION_START,
        L_INTERNET_UPDATE_URL_0_0,
        L_INTERNET_UPDATE_URL_0_1,
    L_INTERNET_UPDATE_URL_SECTION_END
])

XML_INTERNET_0 = '\n'.join([
    L_INTERNET_START_0,
    L_INTERNET_IPv4_0,
    L_INTERNET_IPv6_0,
    L_INTERNET_LAST_CHANGED_0,
    L_INTERNET_UPDATE_INTERVAL_0,
    XML_LOCATER_URL_0,
    XML_UPDATER_URL_0,
    L_INTERNET_END
])

TESTING_INTERNET_NAME_1 = 'InternetName1'
TESTING_INTERNET_KEY_1 = '1'
TESTING_INTERNET_ACTIVE_1 = 'False'

L_INTERNET_START_1 = \
        '<Internet Name="' + TESTING_INTERNET_NAME_1 + \
        '" Key="' + TESTING_INTERNET_KEY_1 + \
        '" Active="' + TESTING_INTERNET_ACTIVE_1 + \
        '">'

TESTING_INTERNET_LOCATE_URL_1_0 = 'http://PyHouse.Org/ip/'

L_INTERNET_LOCATE_URL_1_0 = '    <LocateUrl>' + TESTING_INTERNET_LOCATE_URL_1_0 + '</LocateUrl>'

XML_LOCATER_URL_1 = '\n'.join([
    L_INTERNET_LOCATE_URL_SECTION_START,
        L_INTERNET_LOCATE_URL_1_0,
    L_INTERNET_LOCATE_URL_SECTION_END
])
XML_INTERNET_1 = '\n'.join([
    L_INTERNET_START_1,
    XML_LOCATER_URL_1,
    L_INTERNET_END
])

TESTING_INTERNET_IPv4_1 = '65.35.48.61'
TESTING_INTERNET_IPv6_1 = '2001:db8::1'
TESTING_INTERNET_LAST_CHANGED_1 = '2014-10-02T12:34:56'
TESTING_INTERNET_UPDATE_INTERVAL_1 = '86400'

L_INTERNET_IPv4_1 = '    <ExternalIPv4>' + TESTING_INTERNET_IPv4_1 + '</ExternalIPv4>'
L_INTERNET_IPv6_1 = '    <ExternalIPv6>' + TESTING_INTERNET_IPv6_1 + '</ExternalIPv6>'
L_INTERNET_LAST_CHANGED_1 = '    <LastChanged>' + TESTING_INTERNET_LAST_CHANGED_1 + '</LastChanged>'
L_INTERNET_UPDATE_INTERVAL_1 = '    <UpdateInterval>' + TESTING_INTERNET_UPDATE_INTERVAL_1 + '</UpdateInterval>'

XML_INTERNET_1 = '\n'.join([
    L_INTERNET_START_1,
    L_INTERNET_IPv4_1,
    L_INTERNET_IPv6_1,
    L_INTERNET_LAST_CHANGED_1,
    L_INTERNET_UPDATE_INTERVAL_1,
    L_INTERNET_END
])

XML_INTERNET = '\n'.join([
    L_INTERNET_SECTION_START,
    XML_INTERNET_0,
    XML_INTERNET_1,
    L_INTERNET_SECTION_END
])

# ## END DBK
