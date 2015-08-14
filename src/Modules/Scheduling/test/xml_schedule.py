"""
@name:      PyHouse/src/Modules/Scheduling/test/xml_schedule.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014=2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 7, 2014
@Summary:

"""

TESTING_SCHEDULE_NAME_1 = 'Evening 1'
TESTING_SCHEDULE_KEY_1 = '0'
TESTING_SCHEDULE_ACTIVE_1 = 'True'
TESTING_SCHEDULE_LEVEL_1 = '100'
TESTING_SCHEDULE_LIGHT_NAME_1 = 'lr_cans'
TESTING_SCHEDULE_RATE_1 = '0'
TESTING_SCHEDULE_ROOM_NAME_1 = 'Living Room'
TESTING_SCHEDULE_TIME_1 = '12:34'
TESTING_SCHEDULE_TYPE_1 = 'LightingDevice'
TESTING_SCHEDULE_MODE_1 = 'Home'
TESTING_SCHEDULE_DOW_1 = '127'

XML_SCHEDULE = """
<ScheduleSection>
    <Schedule Name="Evening 1" Key="0" Active="True">
        <Level>100</Level>
        <LightName>lr_cans</LightName>
        <Rate>0</Rate>
        <RoomName>Living Room</RoomName>
        <Time>13:57</Time>
        <ScheduleType>LightingDevice</ScheduleType>
    </Schedule>
    <Schedule Active="True" Key="1" Name="Evening 2">
        <Level>100</Level>
        <LightName>lr_rope</LightName>
        <Rate>0</Rate>
        <RoomName>Living Room</RoomName>
        <Time>13:57</Time>
        <ScheduleType>LightingDevice</ScheduleType>
    </Schedule>
    <Schedule Active="True" Key="2" Name="Evening 3">
        <Level>100</Level>
        <LightName>outside_gar</LightName>
        <Rate>0</Rate>
        <RoomName>Garage</RoomName>
        <Time>sunset - 00:02</Time>
        <ScheduleType>LightingDevice</ScheduleType>
    </Schedule>
    <Schedule Active="True" Key="3" Name="Evening 4">
        <Level>100</Level>
        <LightName>outside_front</LightName>
        <Rate>0</Rate>
        <RoomName>Foyer</RoomName>
        <Time>sunset</Time>
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
</xs:schema>
"""
# ## END DBK
