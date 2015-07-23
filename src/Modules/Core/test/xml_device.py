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
TESTING_DEVICE_FAMILY = 'Insteon'
TESTING_DEVICE_TYPE = '1'
TESTING_DEVICE_SUBTYPE = '2'
TESTING_DEVICE_ROOM_X = '3.4'
TESTING_DEVICE_ROOM_Y = '5.6'
TESTING_DEVICE_ROOM_Z = '1.2'
TESTING_DEVICE_ROOM_COORDS = '[' + TESTING_DEVICE_ROOM_X + ', ' + TESTING_DEVICE_ROOM_Y + ', ' + TESTING_DEVICE_ROOM_Z + ']'
TESTING_DEVICE_ROOM_NAME = "Master Bath"
TESTING_DEVICE_UUID = 'd60b1521-2db1-11e5-a943-082e5f8cdfd2'

COMMENT = "    <Comment>" + TESTING_DEVICE_COMMENT + "</Comment>"
DEVICE_FAMILY = "    <DeviceFamily>" + TESTING_DEVICE_FAMILY + "</DeviceFamily>"
DEVICE_TYPE = '    <DeviceType>' + TESTING_DEVICE_TYPE + '</DeviceType>'
DEVICE_SUBTYPE = '    <DeviceSubType>' + TESTING_DEVICE_SUBTYPE + '</DeviceSubType>'
ROOM_COORD = "    <RoomCoords>" + TESTING_DEVICE_ROOM_COORDS + "</RoomCoords>"
ROOM_NAME = "    <RoomName>" + TESTING_DEVICE_ROOM_NAME + "</RoomName>"
UUID = "    <UUID>" + TESTING_DEVICE_UUID + "</UUID>"

XML_DEVICE = '\n'.join([
    '    <!-- xml_device -->',
    COMMENT,
    DEVICE_FAMILY,
    DEVICE_TYPE,
    DEVICE_SUBTYPE,
    ROOM_COORD,
    ROOM_NAME,
    UUID
])

XML_DEVICE_1_3 = '\n'.join([
    '    <!-- xml device 1.3 -->',
    '<Coords>[1, 3]</Coords>'
])

# ## END DBK
