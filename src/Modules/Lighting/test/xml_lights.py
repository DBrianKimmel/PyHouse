"""
@name:      PyHouse/src/Modules/Lighting/test/xml_lights.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 22, 2014
@Summary:

See PyHouse/src/test/xml_data.py for the entire hierarchy.

"""

__updated__ = '2016-07-07'

# Import system type stuff

# Import PyMh files
from Modules.Families.Insteon.test.xml_insteon import XML_INSTEON
from Modules.Families.UPB.test.xml_upb import XML_UPB


L_LIGHT_SECTION_START = '<LightSection>'
L_LIGHT_SECTION_END = '</LightSection>'
L_LIGHT_END = '</Light>'

TESTING_LIGHT_NAME_0 = "Light, Insteon (xml_lights) "
TESTING_LIGHT_KEY_0 = '0'
TESTING_LIGHT_ACTIVE_0 = 'True'
TESTING_LIGHT_UUID_0 = 'Light...-0000-0000-0000-0123456789ab'
TESTING_LIGHT_COMMENT_0 = "SwitchLink On/Off Light Comment"
TESTING_LIGHT_CUR_LEVEL_0 = "42"
TESTING_LIGHT_DEVICE_FAMILY_0 = 'Insteon'
TESTING_LIGHT_DEVICE_TYPE_0 = '1853'
TESTING_LIGHT_DEVICE_SUBTYPE_0 = '23'
TESTING_LIGHT_IS_DIMMABLE_0 = 'True'
TESTING_LIGHT_ROOM_X = '1.23'
TESTING_LIGHT_ROOM_Y = '4.56'
TESTING_LIGHT_ROOM_Z = '7.89'
# TESTING_LIGHT_ROOM_COORDS = '[' + TESTING_LIGHT_ROOM_X + ', ' + TESTING_LIGHT_ROOM_Y + ', ' + TESTING_LIGHT_ROOM_Z + ']'
TESTING_LIGHT_ROOM_COORDS_0 = '[1.23,4.56,7.89]'
TESTING_LIGHT_ROOM_NAME_0 = 'Master Bath'
TESTING_LIGHT_ROOM_UUID_0 = 'Light...-Room-0000-0000-Room.8b6eb6f'
TESTING_LIGHT_TYPE_0 = 'Light'

L_LIGHT_START_0 = \
        '<Light Name="' + TESTING_LIGHT_NAME_0 + \
        '" Key="' + TESTING_LIGHT_KEY_0 + \
        '" Active="' + TESTING_LIGHT_ACTIVE_0 + \
        '">'
L_LIGHT_UUID_0 = '    <UUID>' + TESTING_LIGHT_UUID_0 + '</UUID>'
L_LIGHT_COMMENT_0 = '    <Comment>' + TESTING_LIGHT_COMMENT_0 + '</Comment>'
L_LIGHT_DEVICE_TYPE_0 = '    <DeviceType>' + TESTING_LIGHT_DEVICE_TYPE_0 + '</DeviceType>'
L_LIGHT_DEVICE_SUBTYPE_0 = '    <DeviceSubType>' + TESTING_LIGHT_DEVICE_SUBTYPE_0 + '</DeviceSubType>'
L_LIGHT_ROOM_COORDS_0 = '    <RoomCoords>' + TESTING_LIGHT_ROOM_COORDS_0 + '</RoomCoords>'
L_LIGHT_ROOM_NAME_0 = '    <RoomName>' + TESTING_LIGHT_ROOM_NAME_0 + '</RoomName>'
L_LIGHT_ROOM_UUID_0 = '    <RoomUUID>' + TESTING_LIGHT_ROOM_UUID_0 + '</RoomUUID>'

L_LIGHT_IS_DIMMABLE_0 = '    <IsDimmable>' + TESTING_LIGHT_IS_DIMMABLE_0 + '</IsDimmable>'
L_LIGHT_DEVICE_FAMILY_0 = "    <DeviceFamily>" + TESTING_LIGHT_DEVICE_FAMILY_0 + "</DeviceFamily>"
L_LIGHT_LEVEL_0 = "    <CurLevel>" + TESTING_LIGHT_CUR_LEVEL_0 + "</CurLevel>"
L_LIGHT_TYPE_0 = '    <LightingType>' + TESTING_LIGHT_TYPE_0 + '</LightingType>'

L_LIGHT_0 = '\n'.join([
    L_LIGHT_START_0,
    L_LIGHT_UUID_0,
    L_LIGHT_COMMENT_0,
    L_LIGHT_DEVICE_FAMILY_0,
    L_LIGHT_DEVICE_TYPE_0,
    L_LIGHT_DEVICE_SUBTYPE_0,
    L_LIGHT_ROOM_NAME_0,
    L_LIGHT_ROOM_COORDS_0,
    L_LIGHT_ROOM_UUID_0,
    L_LIGHT_IS_DIMMABLE_0,
    L_LIGHT_TYPE_0,
    L_LIGHT_LEVEL_0,
    XML_INSTEON,
    L_LIGHT_END
    ])


TESTING_LIGHT_NAME_1 = "UPB Light"
TESTING_LIGHT_KEY_1 = '1'
TESTING_LIGHT_ACTIVE_1 = 'True'
TESTING_LIGHT_UUID_1 = 'Light...-Lgt.-0000-0001-Light.b6eb6f'
TESTING_LIGHT_DIMMABLE_1 = 'True'
TESTING_LIGHT_CUR_LEVEL_1 = "12"
TESTING_LIGHT_FAMILY_1 = 'UPB'
TESTING_LIGHT_TYPE_1 = 'Light'

L_LIGHT_START_1 = \
        '<Light Name="' + TESTING_LIGHT_NAME_1 + \
        '" Key="' + TESTING_LIGHT_KEY_1 + \
        '" Active="' + TESTING_LIGHT_ACTIVE_1 + \
        '">'
L_LIGHT_UUID_1 = '    <UUID>' + TESTING_LIGHT_UUID_1 + '</UUID>'
L_LIGHT_TYPE_1 = '    <LightingType>' + TESTING_LIGHT_TYPE_1 + '</LightingType>'
L_LIGHT_DIMMABLE_1 = '    <IsDimmable>' + TESTING_LIGHT_DIMMABLE_1 + '</IsDimmable>'
L_LIGHT_CUR_LEVEL_1 = "    <CurLevel>" + TESTING_LIGHT_CUR_LEVEL_1 + "</CurLevel>"
L_LIGHT_FAMILY_1 = "    <DeviceFamily>" + TESTING_LIGHT_FAMILY_1 + "</DeviceFamily>"

L_LIGHT_1 = '\n'.join([
    L_LIGHT_START_1,
    L_LIGHT_UUID_1,
    L_LIGHT_DIMMABLE_1,
    L_LIGHT_FAMILY_1,
    L_LIGHT_TYPE_1,
    L_LIGHT_CUR_LEVEL_1,
    XML_UPB,
    L_LIGHT_END
    ])


XML_LIGHT_SECTION = '\n'.join([
    L_LIGHT_SECTION_START,
    L_LIGHT_0,
    L_LIGHT_1,
    L_LIGHT_SECTION_END
    ])

# ## END DBK
