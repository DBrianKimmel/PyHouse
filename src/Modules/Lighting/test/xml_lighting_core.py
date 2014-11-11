"""
@name: C:/Users/briank/Documents/GitHub/PyHouse/src/Modules/Lighting/test/xml_lighting.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Nov 9, 2014
@Summary:

"""


CONTROLLER_XSD = """
<xs:schema
    attributeFormDefault="unqualified"
    elementFormDefault="qualified"
    xmlns:xs="http://www.w3.org/2001/XMLSchema">

  <xs:element name="ControllerSection">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="Controller" maxOccurs="unbounded" minOccurs="0">
          <xs:complexType>
            <xs:sequence>
              <xs:element type="xs:string" name="Comment"/>
              <xs:element type="xs:string" name="Coords"/>
              <xs:element type="xs:string" name="IsDimmable"/>
              <xs:element type="xs:string" name="ControllerFamily"/>
              <xs:element type="xs:string" name="RoomName"/>
              <xs:element type="xs:string" name="LightingType"/>
            </xs:sequence>
            <xs:attribute type="xs:string" name="Active"/>
            <xs:attribute type="xs:byte" name="Key"/>
            <xs:attribute type="xs:string" name="Name"/>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>

</xs:schema>
"""
# ## END DBK
