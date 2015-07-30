"""
@name:      PyHouse/src/Modules/Computer/Internet/test/xml_internet.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 8, 2014
@Summary:

"""

TESTING_INTERNET_LOCATE_URL_1 = 'http://snar.co/ip/'
TESTING_INTERNET_LOCATE_URL_2 = 'http://checkip.dyndns.com/'
TESTING_INTERNET_UPDATE_URL_1 = 'http://freedns.afraid.org/dynamic/update.php?12345'
TESTING_INTERNET_IPv4 = '65.35.48.61'
TESTING_INTERNET_IPv6 = '1234:5678::1'
TESTING_INTERNET_LAST_CHANGED = '2014-10-02T12:34:56'

L_INTERNET_LOCATE_URL_1 = '    <LocateUrl>' + TESTING_INTERNET_LOCATE_URL_1 + '</LocateUrl>'
L_INTERNET_LOCATE_URL_2 = '    <LocateUrl>' + TESTING_INTERNET_LOCATE_URL_2 + '</LocateUrl>'
L_INTERNET_UPDATE_URL_1 = '    <UpdateUrl>' + TESTING_INTERNET_UPDATE_URL_1 + '</UpdateUrl>'
L_INTERNET_IPv4 = '    <ExternalIPv4>' + TESTING_INTERNET_IPv4 + '</ExternalIPv4>'
L_INTERNET_IPv6 = '    <ExternalIPv6>' + TESTING_INTERNET_IPv6 + '</ExternalIPv6>'
L_INTERNET_LAST_CHANGED = '    <LastChanged>' + TESTING_INTERNET_LAST_CHANGED + '</LastChanged>'

XML_LOCATER_URL = '\n'.join([
    '<LocaterUrlSection>',
        L_INTERNET_LOCATE_URL_1,
        L_INTERNET_LOCATE_URL_2,
    '</LocaterUrlSection>'
])
XML_UPDATER_URL = '\n'.join([
    '<UpdaterUrlSection>',
        L_INTERNET_UPDATE_URL_1,
    '</UpdaterUrlSection>'
])
XML_INTERNET = '\n'.join([
    '<InternetSection>',
        XML_LOCATER_URL,
        XML_UPDATER_URL,
        L_INTERNET_IPv4,
        L_INTERNET_IPv6,
        L_INTERNET_LAST_CHANGED,
    '</InternetSection>'
])


INTERNET_XSD = """
<xs:schema
    attributeFormDefault="unqualified"
    elementFormDefault="qualified"
    xmlns:xs="http://www.w3.org/2001/XMLSchema">

  <xs:element name="InternetSection">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="LocaterUrlSection">
          <xs:complexType>
            <xs:sequence>
              <xs:element type="xs:anyURI" name="LocateUrl" maxOccurs="unbounded" minOccurs="0"/>
            </xs:sequence>
          </xs:complexType>
        </xs:element>
        <xs:element name="UpdaterUrlSection">
          <xs:complexType>
            <xs:sequence>
              <xs:element type="xs:anyURI" name="UpdateUrl" maxOccurs="unbounded" minOccurs="0"/>
            </xs:sequence>
          </xs:complexType>
        </xs:element>
        <xs:element type="xs:string" name="ExternalIPv4"/>
        <xs:element type="xs:string" name="ExternalIPv6"/>
        <xs:element type="xs:dateTime" name="LastChanged"/>
      </xs:sequence>
    </xs:complexType>
  </xs:element>

</xs:schema>
"""
# ## END DBK
