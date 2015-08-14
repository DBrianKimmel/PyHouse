"""
@name:      PyHouse/src/Modules/Housing/test/xml_location.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014_2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 22, 2014
@Summary:

Notice that only TZ name is stored in the xml - offsets are derived on XML Read since they never change for a run.

The Olson Time Zone names are used and supported.

"""

TESTING_LOCATION_STREET = '5191 N Pink Poppy Dr'
TESTING_LOCATION_CITY = 'Beverly Hills'
TESTING_LOCATION_STATE = 'Florida'
TESTING_LOCATION_ZIP_CODE = '34465'

L_LOCATION_STREET = '     <Street>' + TESTING_LOCATION_STREET + '</Street>'
L_LOCATION_CITY = '     <City>' + TESTING_LOCATION_CITY + '</City>'
L_LOCATION_STATE = '     <State>' + TESTING_LOCATION_CITY + '</State>'
L_LOCATION_ZIP_CODE = '     <ZipCode>' + TESTING_LOCATION_CITY + '</ZipCode>'

XML_LOCATION = '\n'.join([
    '  <LocationSection>',
    L_LOCATION_STREET,
    L_LOCATION_CITY,
    L_LOCATION_STATE,
    L_LOCATION_ZIP_CODE,
    """
    <Phone>(352) 270-8096</Phone>
    <Latitude>28.938448</Latitude>
    <Longitude>-82.517208</Longitude>
    <TimeZoneName>America/New_York</TimeZoneName>
""",
    '  </LocationSection>'
])


LOCATION_XSD = """
<xs:schema
    attributeFormDefault="unqualified"
    elementFormDefault="qualified"
    xmlns:xs="http://www.w3.org/2001/XMLSchema">

  <xs:element name="LocationSection">
    <xs:complexType>
      <xs:sequence>
        <xs:element type="xs:string" name="Street"/>
        <xs:element type="xs:string" name="City"/>
        <xs:element type="xs:string" name="State"/>
        <xs:element type="xs:int" name="ZipCode"/>
        <xs:element type="xs:string" name="Phone"/>
        <xs:element type="xs:float" name="Latitude"/>
        <xs:element type="xs:float" name="Longitude"/>
        <xs:element type="xs:string" name="TimeZoneName"/>
      </xs:sequence>
    </xs:complexType>
  </xs:element>

</xs:schema>


<xs:element name='LocationSection >
    <xs:complexType>
    </xs:complexType>
</xs:element name='LocationSection >

    <xs:sequence>
        <xs:element name='Street' type='xs:string' />
        <xs:element name='City' type='xs:string' />
        <xs:element name='State' type='xs:string' />
        <xs:element name='ZipCode' type='xs:string' />
        <xs:element name='Phone' type='xs:string' />
        <xs:element name='Latitude' type='xs:string' />
        <xs:element name='Longitude' type='xs:string' />
        <xs:element name='TimeZoneName' type='xs:string' />
    </xs:sequence>



<xs:complexType name="RoomSection">
    <xs:simpleContent>
    </xs:simpleContent>
    <xs:sequence>
        <xs:element name="Comment" type="xs:string"/>
        <xs:element name="Corner" type="xs:string"/>
        <xs:element name="Size" type="xs:string"/>
    </xs:sequence>
</xs:complexType>
"""


# ## END DBK
