"""
-*- test-case-name: /home/briank/PyHouse/src/Modules/Housing/Lighting/test/xml_garagedoors.py -*-

@name:      /home/briank/PyHouse/src/Modules/Housing/Lighting/test/xml_garagedoors.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2016 by D. Brian Kimmel
@note:      Created on Oct 11, 2016
@license:   MIT License
@summary:

"""

__updated__ = '2016-10-12'

# Import system type stuff

# Import PyMh files
from Modules.Families.Insteon.test.xml_insteon import XML_INSTEON_0


L_GARAGE_DOOR_SECTION_START = '<GarageDoorSection>'
L_GARAGE_DOOR_SECTION_END = '</GarageDoorSection>'
L_GARAGE_DOOR_END = '</GarageDoor>'

TESTING_GARAGE_DOOR_NAME_0 = "Garage Door 1"
TESTING_GARAGE_DOOR_KEY_0 = '0'
TESTING_GARAGE_DOOR_ACTIVE_0 = 'True'
TESTING_GARAGE_DOOR_UUID_0 = 'GarageDr-0000-0000-0000-0123456789ab'
TESTING_GARAGE_DOOR_COMMENT_0 = "I/O-Link Comment"
TESTING_GARAGE_DOOR_STATUS_0 = "Open"
TESTING_GARAGE_DOOR_DEVICE_FAMILY_0 = 'Insteon'
TESTING_GARAGE_DOOR_DEVICE_TYPE_0 = '1'
TESTING_GARAGE_DOOR_DEVICE_SUBTYPE_0 = '4'
TESTING_GARAGE_DOOR_ROOM_X = '1.23'
TESTING_GARAGE_DOOR_ROOM_Y = '4.56'
TESTING_GARAGE_DOOR_ROOM_Z = '7.89'
TESTING_GARAGE_DOOR_ROOM_COORDS_0 = '[1.23,4.56,7.89]'
TESTING_GARAGE_DOOR_ROOM_NAME_0 = 'Garage'
TESTING_GARAGE_DOOR_ROOM_UUID_0 = 'Garage..-Room-0000-0000-Room.8b6eb6f'

L_GARAGE_DOOR_START_0 = \
        '<GarageDoor Name="' + TESTING_GARAGE_DOOR_NAME_0 + \
        '" Key="' + TESTING_GARAGE_DOOR_KEY_0 + \
        '" Active="' + TESTING_GARAGE_DOOR_ACTIVE_0 + \
        '">'
L_GARAGE_DOOR_UUID_0 = '    <UUID>' + TESTING_GARAGE_DOOR_UUID_0 + '</UUID>'
L_GARAGE_DOOR_COMMENT_0 = '    <Comment>' + TESTING_GARAGE_DOOR_COMMENT_0 + '</Comment>'
L_GARAGE_DOOR_DEVICE_TYPE_0 = '    <DeviceType>' + TESTING_GARAGE_DOOR_DEVICE_TYPE_0 + '</DeviceType>'
L_GARAGE_DOOR_DEVICE_SUBTYPE_0 = '    <DeviceSubType>' + TESTING_GARAGE_DOOR_DEVICE_SUBTYPE_0 + '</DeviceSubType>'
L_GARAGE_DOOR_ROOM_COORDS_0 = '    <RoomCoords>' + TESTING_GARAGE_DOOR_ROOM_COORDS_0 + '</RoomCoords>'
L_GARAGE_DOOR_ROOM_NAME_0 = '    <RoomName>' + TESTING_GARAGE_DOOR_ROOM_NAME_0 + '</RoomName>'
L_GARAGE_DOOR_ROOM_UUID_0 = '    <RoomUUID>' + TESTING_GARAGE_DOOR_ROOM_UUID_0 + '</RoomUUID>'

L_GARAGE_DOOR_DEVICE_FAMILY_0 = "    <DeviceFamily>" + TESTING_GARAGE_DOOR_DEVICE_FAMILY_0 + "</DeviceFamily>"
L_GARAGE_DOOR_STATUS_0 = "    <Status>" + TESTING_GARAGE_DOOR_STATUS_0 + "</Status>"

L_GARAGE_DOOR_0 = '\n'.join([
    L_GARAGE_DOOR_START_0,
    L_GARAGE_DOOR_UUID_0,
    L_GARAGE_DOOR_COMMENT_0,
    L_GARAGE_DOOR_DEVICE_FAMILY_0,
    L_GARAGE_DOOR_DEVICE_TYPE_0,
    L_GARAGE_DOOR_DEVICE_SUBTYPE_0,
    L_GARAGE_DOOR_ROOM_NAME_0,
    L_GARAGE_DOOR_ROOM_COORDS_0,
    L_GARAGE_DOOR_ROOM_UUID_0,
    L_GARAGE_DOOR_STATUS_0,
    XML_INSTEON_0,
    L_GARAGE_DOOR_END
    ])




XML_GARAGE_DOOR_SECTION = '\n'.join([
    L_GARAGE_DOOR_SECTION_START,
    L_GARAGE_DOOR_0,
    L_GARAGE_DOOR_SECTION_END
    ])

# ## END DBK
