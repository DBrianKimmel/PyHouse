"""
@name:      PyHouse/src/Modules/Scheduling/test/xml_schedule.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 7, 2014
@Summary:

"""
from Modules.Lighting.test.xml_lights import TESTING_LIGHT_NAME_0, TESTING_LIGHT_NAME_1

L_SCHEDULE_SECTION_START = '<ScheduleSection>'
L_SCHEDULE_SECTION_END = '</ScheduleSection>'
L_SCHEDULE_END = '</Schedule>'

TESTING_SCHEDULE_NAME_0 = 'Evening 1'
TESTING_SCHEDULE_KEY_0 = '0'
TESTING_SCHEDULE_ACTIVE_0 = 'True'
TESTING_SCHEDULE_LEVEL_0 = '100'
TESTING_SCHEDULE_LIGHT_NAME_0 = TESTING_LIGHT_NAME_0
TESTING_SCHEDULE_RATE_0 = '0'
TESTING_SCHEDULE_ROOM_NAME_0 = 'Living Room'
TESTING_SCHEDULE_DOW_0 = '127'
TESTING_SCHEDULE_MODE_0 = 'Home'
TESTING_SCHEDULE_TIME_0 = '13:34'
TESTING_SCHEDULE_TYPE_0 = 'Lighting'

L_SCHEDULE_START_0 = '<Schedule Name="' + TESTING_SCHEDULE_NAME_0 + '" Key="' + TESTING_SCHEDULE_KEY_0 + '" Active="' + \
    TESTING_SCHEDULE_ACTIVE_0 + '">'
L_SCHEDULE_LEVEL_0 = '<Level>' + TESTING_SCHEDULE_LEVEL_0 + '</Level>'
L_SCHEDULE_LIGHT_NAME_0 = '<LightName>' + TESTING_SCHEDULE_LIGHT_NAME_0 + '</LightName>'
L_SCHEDULE_RATE_0 = '<Rate>' + TESTING_SCHEDULE_RATE_0 + '</Rate>'
L_SCHEDULE_ROOM_NAME_0 = '<RoomName>' + TESTING_SCHEDULE_ROOM_NAME_0 + '</RoomName>'
L_SCHEDULE_TIME_0 = '<Time>' + TESTING_SCHEDULE_TIME_0 + '</Time>'
L_SCHEDULE_TYPE_0 = '<ScheduleType>' + TESTING_SCHEDULE_TYPE_0 + '</ScheduleType>'
L_SCHEDULE_DOW_0 = '<DOW>' + TESTING_SCHEDULE_DOW_0 + '</DOW>'
L_SCHEDULE_MODE_0 = '<ScheduleMode>' + TESTING_SCHEDULE_MODE_0 + '</ScheduleMode>'

L_SCHEDULE_0 = '\n'.join([
    L_SCHEDULE_START_0,
    L_SCHEDULE_LEVEL_0,
    L_SCHEDULE_LIGHT_NAME_0,
    L_SCHEDULE_RATE_0,
    L_SCHEDULE_ROOM_NAME_0,
    L_SCHEDULE_TIME_0,
    L_SCHEDULE_TYPE_0,
    L_SCHEDULE_DOW_0,
    L_SCHEDULE_MODE_0,
    L_SCHEDULE_END
])


TESTING_SCHEDULE_NAME_1 = 'Evening 2'
TESTING_SCHEDULE_KEY_1 = '1'
TESTING_SCHEDULE_ACTIVE_1 = 'True'
TESTING_SCHEDULE_LEVEL_1 = '100'
TESTING_SCHEDULE_LIGHT_NAME_1 = TESTING_LIGHT_NAME_1
TESTING_SCHEDULE_RATE_1 = '0'
TESTING_SCHEDULE_ROOM_NAME_1 = 'Living Room'
TESTING_SCHEDULE_TIME_1 = '13:34'
TESTING_SCHEDULE_TYPE_1 = 'LightingDevice'
TESTING_SCHEDULE_MODE_1 = 'Home'
TESTING_SCHEDULE_DOW_1 = '127'

L_SCHEDULE_START_1 = '<Schedule Name="' + TESTING_SCHEDULE_NAME_1 + '" Key="' + TESTING_SCHEDULE_KEY_1 + '" Active="' + \
    TESTING_SCHEDULE_ACTIVE_1 + '">'
L_SCHEDULE_LEVEL_1 = '<Level>' + TESTING_SCHEDULE_LEVEL_1 + '</Level>'
L_SCHEDULE_LIGHT_NAME_1 = '<LightName>' + TESTING_SCHEDULE_LIGHT_NAME_1 + '</LightName>'
L_SCHEDULE_RATE_1 = '<Rate>' + TESTING_SCHEDULE_RATE_1 + '</Rate>'
L_SCHEDULE_ROOM_NAME_1 = '<RoomName>' + TESTING_SCHEDULE_ROOM_NAME_1 + '</RoomName>'
L_SCHEDULE_TIME_1 = '<Time>' + TESTING_SCHEDULE_TIME_1 + '</Time>'
L_SCHEDULE_TYPE_1 = '<ScheduleType>' + TESTING_SCHEDULE_TYPE_1 + '</ScheduleType>'
L_SCHEDULE_DOW_1 = '<DOW>' + TESTING_SCHEDULE_DOW_1 + '</DOW>'
L_SCHEDULE_MODE_1 = '<ScheduleMode>' + TESTING_SCHEDULE_MODE_1 + '</ScheduleMode>'

L_SCHEDULE_1 = '\n'.join([
    L_SCHEDULE_START_1,
    L_SCHEDULE_LEVEL_1,
    L_SCHEDULE_LIGHT_NAME_1,
    L_SCHEDULE_RATE_1,
    L_SCHEDULE_ROOM_NAME_1,
    L_SCHEDULE_TIME_1,
    L_SCHEDULE_TYPE_1,
    L_SCHEDULE_DOW_1,
    L_SCHEDULE_MODE_1,
    L_SCHEDULE_END
])


TESTING_SCHEDULE_NAME_2 = 'Night 3'
TESTING_SCHEDULE_KEY_2 = '2'
TESTING_SCHEDULE_ACTIVE_2 = 'True'
TESTING_SCHEDULE_LEVEL_2 = '0'
TESTING_SCHEDULE_LIGHT_NAME_2 = TESTING_SCHEDULE_LIGHT_NAME_0
TESTING_SCHEDULE_RATE_2 = '0'
TESTING_SCHEDULE_ROOM_NAME_2 = 'Living Room'
TESTING_SCHEDULE_TIME_2 = '23:57'
TESTING_SCHEDULE_TYPE_2 = 'LightingDevice'
TESTING_SCHEDULE_MODE_2 = 'Home'
TESTING_SCHEDULE_DOW_2 = '127'

L_SCHEDULE_START_2 = '<Schedule Name="' + TESTING_SCHEDULE_NAME_2 + '" Key="' + TESTING_SCHEDULE_KEY_2 + \
        '" Active="' + TESTING_SCHEDULE_ACTIVE_2 + '">'
L_SCHEDULE_LEVEL_2 = '<Level>' + TESTING_SCHEDULE_LEVEL_2 + '</Level>'
L_SCHEDULE_LIGHT_NAME_2 = '<LightName>' + TESTING_SCHEDULE_LIGHT_NAME_2 + '</LightName>'
L_SCHEDULE_RATE_2 = '<Rate>' + TESTING_SCHEDULE_RATE_2 + '</Rate>'
L_SCHEDULE_ROOM_NAME_2 = '<RoomName>' + TESTING_SCHEDULE_ROOM_NAME_2 + '</RoomName>'
L_SCHEDULE_TIME_2 = '<Time>' + TESTING_SCHEDULE_TIME_2 + '</Time>'
L_SCHEDULE_TYPE_2 = '<ScheduleType>' + TESTING_SCHEDULE_TYPE_2 + '</ScheduleType>'
L_SCHEDULE_DOW_2 = '<DOW>' + TESTING_SCHEDULE_DOW_2 + '</DOW>'
L_SCHEDULE_MODE_2 = '<ScheduleMode>' + TESTING_SCHEDULE_MODE_2 + '</ScheduleMode>'

L_SCHEDULE_2 = '\n'.join([
    L_SCHEDULE_START_2,
    L_SCHEDULE_LEVEL_2,
    L_SCHEDULE_LIGHT_NAME_2,
    L_SCHEDULE_RATE_2,
    L_SCHEDULE_ROOM_NAME_2,
    L_SCHEDULE_TIME_2,
    L_SCHEDULE_TYPE_2,
    L_SCHEDULE_DOW_2,
    L_SCHEDULE_MODE_2,
    L_SCHEDULE_END
])


TESTING_SCHEDULE_NAME_3 = 'Night 4'
TESTING_SCHEDULE_KEY_3 = '3'
TESTING_SCHEDULE_ACTIVE_3 = 'True'
TESTING_SCHEDULE_LEVEL_3 = '0'
TESTING_SCHEDULE_LIGHT_NAME_3 = TESTING_SCHEDULE_LIGHT_NAME_1
TESTING_SCHEDULE_RATE_3 = '0'
TESTING_SCHEDULE_ROOM_NAME_3 = 'Living Room'
TESTING_SCHEDULE_TIME_3 = '23:30'
TESTING_SCHEDULE_TYPE_3 = 'LightingDevice'
TESTING_SCHEDULE_MODE_3 = 'Home'
TESTING_SCHEDULE_DOW_3 = '127'

L_SCHEDULE_START_3 = '<Schedule Name="' + TESTING_SCHEDULE_NAME_3 + '" Key="' + \
        TESTING_SCHEDULE_KEY_3 + '" Active="' + TESTING_SCHEDULE_ACTIVE_3 + '">'
L_SCHEDULE_LEVEL_3 = '<Level>' + TESTING_SCHEDULE_LEVEL_3 + '</Level>'
L_SCHEDULE_LIGHT_NAME_3 = '<LightName>' + TESTING_SCHEDULE_LIGHT_NAME_3 + '</LightName>'
L_SCHEDULE_RATE_3 = '<Rate>' + TESTING_SCHEDULE_RATE_3 + '</Rate>'
L_SCHEDULE_ROOM_NAME_3 = '<RoomName>' + TESTING_SCHEDULE_ROOM_NAME_3 + '</RoomName>'
L_SCHEDULE_TIME_3 = '<Time>' + TESTING_SCHEDULE_TIME_3 + '</Time>'
L_SCHEDULE_TYPE_3 = '<ScheduleType>' + TESTING_SCHEDULE_TYPE_3 + '</ScheduleType>'
L_SCHEDULE_DOW_3 = '<DOW>' + TESTING_SCHEDULE_DOW_3 + '</DOW>'
L_SCHEDULE_MODE_3 = '<ScheduleMode>' + TESTING_SCHEDULE_MODE_3 + '</ScheduleMode>'

L_SCHEDULE_3 = '\n'.join([
    L_SCHEDULE_START_3,
    L_SCHEDULE_LEVEL_3,
    L_SCHEDULE_LIGHT_NAME_3,
    L_SCHEDULE_RATE_3,
    L_SCHEDULE_ROOM_NAME_3,
    L_SCHEDULE_TIME_3,
    L_SCHEDULE_TYPE_3,
    L_SCHEDULE_DOW_3,
    L_SCHEDULE_MODE_3,
    L_SCHEDULE_END
])

XML_SCHEDULE = '\n'.join([
    L_SCHEDULE_SECTION_START,
    L_SCHEDULE_0,
    L_SCHEDULE_1,
    L_SCHEDULE_2,
    L_SCHEDULE_3,
    L_SCHEDULE_SECTION_END
])

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
