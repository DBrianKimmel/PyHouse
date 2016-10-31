"""
-*- test-case-name: /home/briank/PyHouse/src/Modules/Housing/Lighting/test/xml_motion.py -*-

@name:      /home/briank/PyHouse/src/Modules/Housing/Lighting/test/xml_motion.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2016-2016 by D. Brian Kimmel
@note:      Created on Oct 22, 2016
@license:   MIT License
@summary:

"""

__updated__ = '2016-10-27'

# Import system type stuff

# Import PyMh files
from Modules.Core.test.xml_device import XML_DEVICE_INSTEON
from Modules.Families.Insteon.test.xml_insteon import XML_INSTEON_2


L_LIGHTING_MOTION_SECTION_START = '<MotionDetectorSection>'
L_LIGHTING_MOTION_SECTION_END = '</MotionDetectorSection>'
L_LIGHTING_MOTION_END = '</Motion>'

TESTING_LIGHTING_MOTION_NAME_0 = 'Insteon Motion Detector'
TESTING_LIGHTING_MOTION_ACTIVE_0 = 'True'
TESTING_LIGHTING_MOTION_KEY_0 = '0'
TESTING_LIGHTING_MOTION_UUID_0 = 'Motion..-0000-0000-0000-0123456789ab'
TESTING_LIGHTING_MOTION_COMMENT_0 = "Motion Detector Comment"
TESTING_LIGHTING_MOTION_DEVICE_FAMILY_0 = 'Insteon'
TESTING_LIGHTING_MOTION_DEVICE_TYPE_0 = '1'
TESTING_LIGHTING_MOTION_DEVICE_SUBTYPE_0 = '5'
TESTING_LIGHTING_MOTION_ROOM_X = '1.23'
TESTING_LIGHTING_MOTION_ROOM_Y = '4.56'
TESTING_LIGHTING_MOTION_ROOM_Z = '7.89'
TESTING_LIGHTING_MOTION_ROOM_COORDS_0 = '[1.23, 4.56, 7.89]'
TESTING_LIGHTING_MOTION_ROOM_NAME_0 = 'LivingRoom'
TESTING_LIGHTING_MOTION_ROOM_UUID_0 = 'LR......-Room-0000-0000-Room.8b6eb6f'

L_LIGHTING_MOTION_START_0 = \
        '<Motion Name="' + TESTING_LIGHTING_MOTION_NAME_0 + \
        '" Key="' + TESTING_LIGHTING_MOTION_KEY_0 + \
        '" Active="' + TESTING_LIGHTING_MOTION_ACTIVE_0 + \
        '">'
L_LIGHTING_MOTION_UUID_0 = '    <UUID>' + TESTING_LIGHTING_MOTION_UUID_0 + '</UUID>'
L_LIGHTING_MOTION_COMMENT_0 = '    <Comment>' + TESTING_LIGHTING_MOTION_COMMENT_0 + '</Comment>'
L_LIGHTING_MOTION_DEVICE_TYPE_0 = '    <DeviceType>' + TESTING_LIGHTING_MOTION_DEVICE_TYPE_0 + '</DeviceType>'
L_LIGHTING_MOTION_DEVICE_SUBTYPE_0 = '    <DeviceSubType>' + TESTING_LIGHTING_MOTION_DEVICE_SUBTYPE_0 + '</DeviceSubType>'
L_LIGHTING_MOTION_ROOM_COORDS_0 = '    <RoomCoords>' + TESTING_LIGHTING_MOTION_ROOM_COORDS_0 + '</RoomCoords>'
L_LIGHTING_MOTION_ROOM_NAME_0 = '    <RoomName>' + TESTING_LIGHTING_MOTION_ROOM_NAME_0 + '</RoomName>'
L_LIGHTING_MOTION_ROOM_UUID_0 = '    <RoomUUID>' + TESTING_LIGHTING_MOTION_ROOM_UUID_0 + '</RoomUUID>'

L_LIGHTING_MOTION_DEVICE_FAMILY_0 = "    <DeviceFamily>" + TESTING_LIGHTING_MOTION_DEVICE_FAMILY_0 + "</DeviceFamily>"



L_LIGHTING_MOTION_BODY = '\n'.join([
    XML_DEVICE_INSTEON,
    ])

XML_INSTEON_MOTION = '\n'.join([
    L_LIGHTING_MOTION_START_0,
    L_LIGHTING_MOTION_BODY,
    XML_INSTEON_2,
    L_LIGHTING_MOTION_END
    ])

XML_LIGHTING_MOTION_SECTION = '\n'.join([
    L_LIGHTING_MOTION_SECTION_START,
    XML_INSTEON_MOTION,
    L_LIGHTING_MOTION_SECTION_END
    ])

# ## END DBK
