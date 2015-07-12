"""
@name:      PyHouse/src/Modules/Irrigation/test/xml_irrigation.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c)  2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 30, 2015
@Summary:

"""


IRRIGATION_XML = """
<IrrigationSection>
    <IrrigationSystem Name="LawnSystem" Key="0" Active="True">
        <Comment>Main yard system with Well Relay and 13 zones</Comment>
        <Zone Name="Front Rotors # 1" Key="0" Active="True">
            <Comment>Rotors on the West corner of the yard,</Comment>
            <Duration>2700</Duration>
        </Zone>
        <Zone Name="Front Rotors # 2" Key="1" Active="True">
            <Comment>Rotors on the driveway side of the yard,</Comment>
            <Duration>2700</Duration>
        </Zone>
        <Zone Name="Front Rotors # 3" Key="2" Active="True">
        </Zone>
        <Zone Name="Front Rotors # 4" Key="3" Active="True">
        </Zone>
        <Zone Name="Front Rotors # 5" Key="4" Active="True">
        </Zone>
        <Zone Name="Front Rotors # 6" Key="5" Active="True">
        </Zone>
        <Zone Name="Front Rotors # 7" Key="6" Active="True">
        </Zone>
    </IrrigationSystem>
    <IrrigationSystem Name="Lanai Drip" Key="1" Active="True">
        <Comment>Lanai area system</Comment>
        <Zone Name="Flower Drips" Key="0" Active="True">
        </Zone>
        <Zone Name="Pool Filler" Key="1" Active="True">
        </Zone>
        <Zone Name="UnUsed" Key="2" Active="True">
        </Zone>
    </IrrigationSystem>
</IrrigationSection>
"""


IRRIGATION_XSD = """
<xs:schema
    attributeFormDefault="unqualified"
    elementFormDefault="qualified"
    xmlns:xs="http://www.w3.org/2001/XMLSchema">

  <xs:element name="IrrigationSection">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="IrrigationSystem" maxOccurs="unbounded" minOccurs="0">
          <xs:complexType>
            <xs:sequence>
                <xs:element type="xs:string" name="Comment"/>
                <xs:element type="xs:string" name="Corner"/>
                xs:element type="xs:string" name="Size"/>
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
