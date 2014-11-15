"""
@name: C:/Users/briank/Documents/GitHub/PyHouse/src/Modules/Scheduling/test/xml_schedule.py
@author: D. Brian Kimmel
@contact: D.BrianKimmel@gmail.com
@Copyright: (c)  2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Nov 7, 2014
@Summary:

"""
SCHEDULE_XML = """
<ScheduleSection>
    <Schedule Name="Evening 1" Key="0" Active="True">
        <Level>100</Level>
        <LightName>lr_cans</LightName>
        <Rate>0</Rate>
        <RoomName>Living Room</RoomName>
        <Time>13:57</Time>
        <ScheduleType>LightingDevice</ScheduleType>
    </Schedule>
    <Schedule Active="True" Key="1" Name="Evening">
        <Level>100</Level>
        <LightName>lr_rope</LightName>
        <LightNumber>7</LightNumber>
        <Rate>0</Rate>
        <RoomName>Living Room</RoomName>
        <Time>13:57</Time>
        <ScheduleType>LightingDevice</ScheduleType>
    </Schedule>
    <Schedule Active="True" Key="2" Name="Evening">
        <Level>100</Level><LightName>outside_gar</LightName><LightNumber>1</LightNumber><Rate>0</Rate>
        <RoomName>Garage</RoomName>
        <Time>sunset - 00:02</Time>
        <ScheduleType>LightingDevice</ScheduleType>
    </Schedule>
    <Schedule Active="True" Key="3" Name="Evening">
        <Level>100</Level><LightName>outside_front</LightName>
        <LightNumber>0</LightNumber><Rate>0</Rate><RoomName>Foyer</RoomName><Time>sunset</Time>
        <ScheduleType>LightingDevice</ScheduleType>
    </Schedule>
    <Schedule Active="True" Key="4" Name="Evening">
        <Level>100</Level>
        <LightName>wet_bar</LightName>
        <LightNumber>8</LightNumber>
        <Rate>0</Rate>
        <RoomName>Living Room</RoomName>
        <Time>sunset - 00:04</Time>
        <ScheduleType>LightingDevice</ScheduleType>
    </Schedule>
    <Schedule Active="False" Key="5" Name="Night xxx">
        <Level>60</Level><LightName>mbr_rope</LightName>
        <LightNumber>6</LightNumber><Rate>0</Rate><RoomName>Master Bedroom</RoomName>
        <Time>22:00</Time>
        <ScheduleType>LightingDevice</ScheduleType>
    </Schedule>
    <Schedule Active="True" Key="6" Name="Night">
        <Level>0</Level>
        <LightName>outside_gar</LightName>
        <LightNumber>1</LightNumber>
        <Rate>0</Rate>
        <RoomName>Garage</RoomName>
        <Time>23:00</Time>
        <ScheduleType>LightingDevice</ScheduleType>
    </Schedule>
</ScheduleSection>
"""

SCHEDULE_XSD = """
<xs:schema
    attributeFormDefault="unqualified"
    elementFormDefault="qualified"
    xmlns:xs="http://www.w3.org/2001/XMLSchema">

  <xs:element name="ScheduleSection">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="Schedule" maxOccurs="unbounded" minOccurs="0">
          <xs:complexType>
            <xs:sequence>
              <xs:element type="xs:byte" name="Level"/>
              <xs:element type="xs:string" name="LightName"/>
              <xs:element type="xs:byte" name="Rate"/>
              <xs:element type="xs:string" name="RoomName"/>
              <xs:element type="xs:string" name="Time"/>
              <xs:element type="xs:string" name="ScheduleType"/>
            </xs:sequence>
            <xs:attribute type="xs:string" name="Name" />
            <xs:attribute type="xs:integer" name="Key"/>
            <xs:attribute type="xs:boolean" name="Active"/>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>

</xs:schema>"""
# ## END DBK
