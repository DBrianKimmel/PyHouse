"""
@name:      PyHouse/src/Modules/Core/test/xml_device.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 18, 2015
@Summary:

See PyHouse/src/test/xml_data.py for the entire hierarchy.

"""

# Import system type stuff

# Import PyMh files
# from Modules.Core.test.xml_device import xxx


TESTING_DEVICE_COMMENT = 'Test Comment Device 1234'
TESTING_DEVICE_FAMILY_INSTEON = 'Insteon'
TESTING_DEVICE_FAMILY_UPB = 'UPB'
TESTING_DEVICE_TYPE = '1'
TESTING_DEVICE_SUBTYPE = '2'
TESTING_DEVICE_ROOM_X = '3.4'
TESTING_DEVICE_ROOM_Y = '5.6'
TESTING_DEVICE_ROOM_Z = '1.2'
TESTING_DEVICE_ROOM_COORDS = '[' + TESTING_DEVICE_ROOM_X + ', ' + TESTING_DEVICE_ROOM_Y + ', ' + TESTING_DEVICE_ROOM_Z + ']'
TESTING_DEVICE_ROOM_NAME = "Testing Room Name ABDG"
TESTING_DEVICE_UUID = 'deadbeef-room-0001-0002-deadbeef1234'

L_COMMENT = "    <Comment>" + TESTING_DEVICE_COMMENT + "</Comment>"
L_DEVICE_FAMILY_INSTEON = "    <DeviceFamily>" + TESTING_DEVICE_FAMILY_INSTEON + "</DeviceFamily>"
L_DEVICE_FAMILY_UPB = "    <DeviceFamily>" + TESTING_DEVICE_FAMILY_UPB + "</DeviceFamily>"
L_DEVICE_TYPE = '    <DeviceType>' + TESTING_DEVICE_TYPE + '</DeviceType>'
L_DEVICE_SUBTYPE = '    <DeviceSubType>' + TESTING_DEVICE_SUBTYPE + '</DeviceSubType>'
L_ROOM_COORD = "    <RoomCoords>" + TESTING_DEVICE_ROOM_COORDS + "</RoomCoords>"
L_ROOM_NAME = "    <RoomName>" + TESTING_DEVICE_ROOM_NAME + "</RoomName>"
L_UUID = "    <UUID>" + TESTING_DEVICE_UUID + "</UUID>"

XML_DEVICE_INSTEON = '\n'.join([
    '    <!-- xml_device -->',
    L_COMMENT,
    L_DEVICE_FAMILY_INSTEON,
    L_DEVICE_TYPE,
    L_DEVICE_SUBTYPE,
    L_ROOM_COORD,
    L_ROOM_NAME,
    L_UUID
    ])

XML_DEVICE_UPB = '\n'.join([
    '    <!-- xml_device -->',
    L_COMMENT,
    L_DEVICE_FAMILY_UPB,
    L_DEVICE_TYPE,
    L_DEVICE_SUBTYPE,
    L_ROOM_COORD,
    L_ROOM_NAME,
    L_UUID
    ])

XML_DEVICE_INSTEON_1_3 = '\n'.join([
    '    <!-- xml device 1.3 -->',
    '<Coords>[1, 3]</Coords>'
    ])

# ## END DBK
