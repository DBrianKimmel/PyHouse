"""
@name:      PyHouse/src/Modules/Housing/test/xml_rooms.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 22, 2014
@Summary:

"""


ROOMS_XML = """
<RoomSection>
    <Room Active="True" Key="0" Name="Master Bath">
        <Comment>Test Comment</Comment>
        <Corner>0.50, 10.50</Corner>
        <Size>14.00, 13.50</Size>
    </Room>
    <Room Active="True" Key="1" Name="Master Bed Closet 1">
        <Comment />
        <Corner>0.83, 24.58</Corner>
        <Size>6.91, 8.91</Size>
    </Room>
    <Room Active="False" Key="2" Name="Master Bedroom">
        <Comment />
        <Corner>0.83, 25.08</Corner>
        <Size>14.00, 18.00</Size>
    </Room>
    <Room Active="False" Key="3" Name="Master Sitting Room">
        <Comment />
        <Corner>0.83, 54.16</Corner>
        <Size>14.00, 8.00</Size>
    </Room>
</RoomSection>
"""


ROOMS_XSD = """
<xs:schema
    attributeFormDefault="unqualified"
    elementFormDefault="qualified"
    xmlns:xs="http://www.w3.org/2001/XMLSchema">

  <xs:element name="RoomSection">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="Room" maxOccurs="unbounded" minOccurs="0">
          <xs:complexType>
            <xs:sequence>
              <xs:element type="xs:string" name="Comment"/>
              <xs:element type="xs:string" name="Corner"/>
              <xs:element type="xs:string" name="Size"/>
            </xs:sequence>
            <xs:attribute type="xs:string" name="Active" use="optional"/>
            <xs:attribute type="xs:byte" name="Key" use="optional"/>
            <xs:attribute type="xs:string" name="Name" use="optional"/>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>

</xs:schema>
"""
# ## END DBK