"""
@name: C:/Users/briank/Documents/GitHub/PyHouse/src/Modules/Computer/Internet/test/xml_internet.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Nov 8, 2014
@Summary:

"""



INTERNET_XML = """
        <InternetSection>
            <LocaterUrlSection>
                <LocateUrl>http://snar.co/ip/</LocateUrl>
                <LocateUrl>http://checkip.dyndns.com/</LocateUrl>
            </LocaterUrlSection>
            <UpdaterUrlSection>
                <UpdateUrl>http://freedns.afraid.org/dynamic/update.php?12345</UpdateUrl>
            </UpdaterUrlSection>
            <ExternalIPv4>65.35.48.61</ExternalIPv4>
            <ExternalIPv6>1234:5678::1</ExternalIPv6>
            <LastChanged>2014-10-02T12:34:56</LastChanged>
        </InternetSection>
"""



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
