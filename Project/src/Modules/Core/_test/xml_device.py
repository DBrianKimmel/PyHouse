"""
@name:      PyHouse/src/Modules/Core/_test/xml_device.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2017 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jul 18, 2015
@Summary:

See PyHouse/src/_test/xml_data.py for the entire hierarchy.

"""

__updated__ = '2019-07-20'

# Import system type stuff

# Import PyMh files

TESTING_DEVICE_COMMENT_0 = 'Device Comment 0'
TESTING_DEVICE_FAMILY_INSTEON = 'Insteon'
TESTING_DEVICE_TYPE_0 = 'Lighting'
TESTING_DEVICE_SUBTYPE_0 = 'Controller'
TESTING_DEVICE_ROOM_X_0 = '3.4'
TESTING_DEVICE_ROOM_Y_0 = '5.6'
TESTING_DEVICE_ROOM_Z_0 = '1.2'
TESTING_DEVICE_ROOM_COORDS_0 = '[' + TESTING_DEVICE_ROOM_X_0 + ', ' + TESTING_DEVICE_ROOM_Y_0 + ', ' + TESTING_DEVICE_ROOM_Z_0 + ']'
TESTING_DEVICE_ROOM_NAME_0 = "Testing Room Name ABDG"
TESTING_DEVICE_ROOM_UUID_0 = 'Device..-Room-0001-0002-deadbeef1234'
TESTING_DEVICE_UUID_0 = 'Device..-Dev.-0001-0002-deadbeef1234'

L_COMMENT_0 = "<Comment>" + TESTING_DEVICE_COMMENT_0 + "</Comment>"
L_DEVICE_FAMILY_INSTEON = "<DeviceFamily>" + TESTING_DEVICE_FAMILY_INSTEON + "</DeviceFamily>"
L_DEVICE_TYPE_0 = '<DeviceType>' + TESTING_DEVICE_TYPE_0 + '</DeviceType>'
L_DEVICE_SUBTYPE_0 = '<DeviceSubType>' + TESTING_DEVICE_SUBTYPE_0 + '</DeviceSubType>'
L_ROOM_COORD_0 = "<RoomCoords>" + TESTING_DEVICE_ROOM_COORDS_0 + "</RoomCoords>"
L_ROOM_NAME_0 = "<RoomName>" + TESTING_DEVICE_ROOM_NAME_0 + "</RoomName>"
L_ROOM_UUID_0 = "<RoomUUID>" + TESTING_DEVICE_ROOM_UUID_0 + "</RoomUUID>"
L_UUID_0 = "<UUID>" + TESTING_DEVICE_UUID_0 + "</UUID>"

XML_DEVICE_INSTEON = '\n'.join([
    '    <!-- xml_device -->',
    L_COMMENT_0,
    L_DEVICE_FAMILY_INSTEON,
    L_DEVICE_TYPE_0,
    L_DEVICE_SUBTYPE_0,
    L_ROOM_COORD_0,
    L_ROOM_NAME_0,
    L_ROOM_UUID_0,
    L_UUID_0
    ])

TESTING_DEVICE_FAMILY_UPB = 'UPB'
TESTING_DEVICE_COMMENT_1 = 'Device Comment 1'
TESTING_DEVICE_TYPE_1 = '1'
TESTING_DEVICE_SUBTYPE_1 = '2'
TESTING_DEVICE_UUID_1 = 'Device..-Dev.-0002-0002-deadbeef5678'

L_DEVICE_FAMILY_UPB = "    <DeviceFamily>" + TESTING_DEVICE_FAMILY_UPB + "</DeviceFamily>"
L_DEVICE_COMMENT_1 = "<Comment>" + TESTING_DEVICE_COMMENT_1 + "</Comment>"
L_DEVICE_TYPE_1 = '<DeviceType>' + TESTING_DEVICE_TYPE_1 + '</DeviceType>'
L_DEVICE_SUBTYPE_1 = '<DeviceSubType>' + TESTING_DEVICE_SUBTYPE_1 + '</DeviceSubType>'
L_UUID_1 = "<UUID>" + TESTING_DEVICE_UUID_1 + "</UUID>"

XML_DEVICE_UPB = '\n'.join([
    '    <!-- xml_device -->',
    L_DEVICE_COMMENT_1,
    L_DEVICE_FAMILY_UPB,
    L_DEVICE_TYPE_1,
    L_DEVICE_SUBTYPE_1,
    L_ROOM_COORD_0,
    L_ROOM_NAME_0,
    L_ROOM_UUID_0,
    L_UUID_1
    ])

# ## END DBK
