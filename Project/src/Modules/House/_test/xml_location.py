"""
@name:      PyHouse/src/Modules/Housing/_test/xml_location.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014_2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 22, 2014
@Summary:

Notice that only TZ name is stored in the xml - offsets are derived on XML Read since they never change for a run.

The Olson Time Zone names are used and supported.

"""

__updated__ = '2019-06-13'

TESTING_LOCATION_SECTION = 'LocationSection'

L_LOCATION_SECTION_START = '  <' + TESTING_LOCATION_SECTION + '>'
L_LOCATION_SECTION_END = '  </' + TESTING_LOCATION_SECTION + '>'

TESTING_LOCATION_STREET = '1234 Nowhere Dr'
TESTING_LOCATION_CITY = 'Beverly Hills'
TESTING_LOCATION_STATE = 'Florida'
TESTING_LOCATION_ZIP_CODE = '34465'
# TESTING_LOCATION_REGION = 'America'
TESTING_LOCATION_PHONE = '(800) 555-1212'
TESTING_LOCATION_LATITUDE = '28.938448'  # 28 56 18
TESTING_LOCATION_LONGITUDE = '-82.517208'  # -82 31 00
TESTING_LOCATION_ELEVATION = '33.3'
TESTING_LOCATION_TIME_ZONE_NAME = 'America/New_York'

L_LOCATION_STREET = '     <Street>' + TESTING_LOCATION_STREET + '</Street>'
L_LOCATION_CITY = '     <City>' + TESTING_LOCATION_CITY + '</City>'
L_LOCATION_STATE = '     <State>' + TESTING_LOCATION_STATE + '</State>'
L_LOCATION_ZIP_CODE = '     <ZipCode>' + TESTING_LOCATION_ZIP_CODE + '</ZipCode>'
# L_LOCATION_REGION = '     <Region>' + TESTING_LOCATION_REGION + '</Region>'
L_LOCATION_PHONE = '     <Phone>' + TESTING_LOCATION_PHONE + '</Phone>'
L_LOCATION_LATITUDE = '     <Latitude>' + TESTING_LOCATION_LATITUDE + '</Latitude>'
L_LOCATION_LONGITUDE = '     <Longitude>' + TESTING_LOCATION_LONGITUDE + '</Longitude>'
L_LOCATION_ELEVATION = '     <Elevation>' + TESTING_LOCATION_ELEVATION + '</Elevation>'
L_LOCATION_TIME_ZONE_NAME = '     <TimeZoneName>' + TESTING_LOCATION_TIME_ZONE_NAME + '</TimeZoneName>'

XML_LOCATION = '\n'.join([
    L_LOCATION_SECTION_START,
    L_LOCATION_STREET,
    L_LOCATION_CITY,
    L_LOCATION_STATE,
    L_LOCATION_ZIP_CODE,
#    L_LOCATION_REGION,
    L_LOCATION_PHONE,
    L_LOCATION_LATITUDE,
    L_LOCATION_LONGITUDE,
    L_LOCATION_ELEVATION,
    L_LOCATION_TIME_ZONE_NAME,
    L_LOCATION_SECTION_END
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
