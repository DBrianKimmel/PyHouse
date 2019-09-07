"""
@name:      PyHouse/Project/src/Modules/Housing/_test/xml_rooms.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 22, 2014
@Summary:

"""

__updated__ = "2019-06-18"

import datetime

TESTING_ROOM_SECTION = 'RoomSection'

L_ROOM_SECTION_START = '<' + TESTING_ROOM_SECTION + '>'
L_ROOM_SECTION_END = '  </' + TESTING_ROOM_SECTION + '>'
L_ROOM_END = '  </Room>'

TESTING_ROOM_NAME_0 = 'Room_0'
TESTING_ROOM_KEY_0 = '0'
TESTING_ROOM_ACTIVE_0 = 'True'
TESTING_ROOM_UUID_0 = 'Room....-0000-0000-0000-0123456789ab'
TESTING_ROOM_COMMENT_0 = 'Room comment # 0'
TESTING_ROOM_CORNER_X_0 = '12.1'
TESTING_ROOM_CORNER_Y_0 = '14.2'
TESTING_ROOM_CORNER_Z_0 = '0.5'
TESTING_ROOM_CORNER_0 = '[' + TESTING_ROOM_CORNER_X_0 + \
                        ',' + TESTING_ROOM_CORNER_Y_0 + \
                        ',' + TESTING_ROOM_CORNER_Z_0 + \
                        ']'
TESTING_ROOM_FLOOR_0 = '1'
TESTING_ROOM_LAST_UPDATE_0 = datetime.datetime.now()
TESTING_ROOM_SIZE_X_0 = '8.15'
TESTING_ROOM_SIZE_Y_0 = '9.27'
TESTING_ROOM_SIZE_Z_0 = '2.54'
TESTING_ROOM_SIZE_0 = '[' + TESTING_ROOM_SIZE_X_0 + \
                        ',' + TESTING_ROOM_SIZE_Y_0 + \
                        ',' + TESTING_ROOM_SIZE_Z_0 + \
                        ']'
TESTING_ROOM_TYPE_0 = 'Room'

L_ROOM_START_0 = '   ' + \
        '<Room Name="' + TESTING_ROOM_NAME_0 + \
        '" Key="' + TESTING_ROOM_KEY_0 + \
        '" Active="' + TESTING_ROOM_ACTIVE_0 + \
        '">'
L_ROOM_UUID_0 = '    <UUID>' + TESTING_ROOM_UUID_0 + '</UUID>'
L_ROOM_COMMENT_0 = '  <Comment>' + TESTING_ROOM_COMMENT_0 + '</Comment>'
L_ROOM_CORNER_0 = '  <Corner>' + TESTING_ROOM_CORNER_0 + '</Corner>'
L_ROOM_FLOOR_0 = '    <Floor>' + TESTING_ROOM_FLOOR_0 + '</Floor>'
L_ROOM_LAST_UPDATE_0 = '    <LastUpdate>' + str(TESTING_ROOM_LAST_UPDATE_0) + '</LastUpdate>'
L_ROOM_SIZE_0 = '  <Size>' + TESTING_ROOM_SIZE_0 + '</Size>'
L_ROOM_TYPE_0 = '  <RoomType>' + TESTING_ROOM_TYPE_0 + '</RoomType>'

L_ROOM_0 = '\n'.join([
    L_ROOM_START_0,
    L_ROOM_UUID_0,
    L_ROOM_COMMENT_0,
    L_ROOM_CORNER_0,
    L_ROOM_FLOOR_0,
    L_ROOM_LAST_UPDATE_0,
    L_ROOM_SIZE_0,
    L_ROOM_TYPE_0,
    L_ROOM_END
])

TESTING_ROOM_NAME_1 = 'Room-1'
TESTING_ROOM_KEY_1 = '1'
TESTING_ROOM_ACTIVE_1 = 'True'
TESTING_ROOM_UUID_1 = 'Room....-0001-0001-0001-0123456789ab'
TESTING_ROOM_COMMENT_1 = 'Room comment # 1'
TESTING_ROOM_CORNER_1 = '[12.0,14.0,0.5]'
TESTING_ROOM_FLOOR_1 = '1'
TESTING_ROOM_LAST_UPDATE_1 = datetime.datetime(2001, 1, 1, 1, 1, 1)
TESTING_ROOM_SIZE_1 = '[3.0,5.5,3.0]'
TESTING_ROOM_TYPE_1 = 'Room'

L_ROOM_START_1 = '   ' + \
        '<Room Name="' + TESTING_ROOM_NAME_1 + \
        '" Key="' + TESTING_ROOM_KEY_1 + \
        '" Active="' + TESTING_ROOM_ACTIVE_1 + \
        '">'
L_ROOM_UUID_1 = '    <UUID>' + TESTING_ROOM_UUID_1 + '</UUID>'
L_ROOM_COMMENT_1 = '  <Comment>' + TESTING_ROOM_COMMENT_1 + '</Comment>'
L_ROOM_CORNER_1 = '  <Corner>' + TESTING_ROOM_CORNER_1 + '</Corner>'
L_ROOM_FLOOR_1 = '    <Floor>' + TESTING_ROOM_FLOOR_1 + '</Floor>'
L_ROOM_LAST_UPDATE_1 = '    <LastUpdate>' + str(TESTING_ROOM_LAST_UPDATE_1) + '</LastUpdate>'
L_ROOM_SIZE_1 = '  <Size>' + TESTING_ROOM_SIZE_1 + '</Size>'
L_ROOM_TYPE_1 = '  <RoomType>' + TESTING_ROOM_TYPE_1 + '</RoomType>'

L_ROOM_1 = '\n'.join([
    L_ROOM_START_1,
    L_ROOM_UUID_1,
    L_ROOM_COMMENT_1,
    L_ROOM_CORNER_1,
    L_ROOM_FLOOR_1,
    L_ROOM_LAST_UPDATE_1,
    L_ROOM_SIZE_1,
    L_ROOM_TYPE_1,
    L_ROOM_END
])

TESTING_ROOM_NAME_2 = 'Room-2'
TESTING_ROOM_KEY_2 = '2'
TESTING_ROOM_ACTIVE_2 = 'True'
TESTING_ROOM_UUID_2 = 'Room....-0002-0002-0002-0123456789ab'
TESTING_ROOM_COMMENT_2 = 'Room comment # 2'
TESTING_ROOM_CORNER_2 = '[12.0,14.0,0.5]'
TESTING_ROOM_FLOOR_2 = '1'
TESTING_ROOM_LAST_UPDATE_2 = datetime.datetime(2002, 2, 2, 2, 2, 2)
TESTING_ROOM_SIZE_2 = '[3.0,5.5,3.0]'
TESTING_ROOM_TYPE_2 = 'Room'

L_ROOM_START_2 = '   ' + \
        '<Room Name="' + TESTING_ROOM_NAME_2 + \
        '" Key="' + TESTING_ROOM_KEY_2 + \
        '" Active="' + TESTING_ROOM_ACTIVE_2 + \
        '">'
L_ROOM_UUID_2 = '    <UUID>' + TESTING_ROOM_UUID_2 + '</UUID>'
L_ROOM_COMMENT_2 = '  <Comment>' + TESTING_ROOM_COMMENT_2 + '</Comment>'
L_ROOM_CORNER_2 = '  <Corner>' + TESTING_ROOM_CORNER_2 + '</Corner>'
L_ROOM_FLOOR_2 = '    <Floor>' + TESTING_ROOM_FLOOR_2 + '</Floor>'
L_ROOM_LAST_UPDATE_2 = '    <LastUpdate>' + str(TESTING_ROOM_LAST_UPDATE_2) + '</LastUpdate>'
L_ROOM_SIZE_2 = '  <Size>' + TESTING_ROOM_SIZE_2 + '</Size>'
L_ROOM_TYPE_2 = '  <RoomType>' + TESTING_ROOM_TYPE_2 + '</RoomType>'

L_ROOM_2 = '\n'.join([
    L_ROOM_START_2,
    L_ROOM_UUID_2,
    L_ROOM_COMMENT_2,
    L_ROOM_CORNER_2,
    L_ROOM_FLOOR_2,
    L_ROOM_LAST_UPDATE_2,
    L_ROOM_SIZE_2,
    L_ROOM_TYPE_2,
    L_ROOM_END
])

TESTING_ROOM_NAME_3 = 'Room-3'
TESTING_ROOM_KEY_3 = '3'
TESTING_ROOM_ACTIVE_3 = 'True'
TESTING_ROOM_UUID_3 = 'Room....-0003-0003-0003-0123456789ab'
TESTING_ROOM_COMMENT_3 = 'Room comment # 3'
TESTING_ROOM_CORNER_X_3 = '32.1'
TESTING_ROOM_CORNER_Y_3 = '34.2'
TESTING_ROOM_CORNER_Z_3 = '3.5'
TESTING_ROOM_CORNER_3 = '[' + TESTING_ROOM_CORNER_X_3 + \
                        ',' + TESTING_ROOM_CORNER_Y_3 + \
                        ',' + TESTING_ROOM_CORNER_Z_3 + \
                        ']'
TESTING_ROOM_FLOOR_3 = '3'
TESTING_ROOM_LAST_UPDATE_3 = datetime.datetime(2003, 3, 3, 3, 3, 3)
TESTING_ROOM_SIZE_X_3 = '8.15'
TESTING_ROOM_SIZE_Y_3 = '9.27'
TESTING_ROOM_SIZE_Z_3 = '2.54'
TESTING_ROOM_SIZE_3 = '[' + TESTING_ROOM_SIZE_X_3 + \
                        ',' + TESTING_ROOM_SIZE_Y_3 + \
                        ',' + TESTING_ROOM_SIZE_Z_3 + \
                        ']'
TESTING_ROOM_TYPE_3 = 'Room'

L_ROOM_START_3 = '   ' + \
        '<Room Name="' + TESTING_ROOM_NAME_3 + \
        '" Key="' + TESTING_ROOM_KEY_3 + \
        '" Active="' + TESTING_ROOM_ACTIVE_3 + \
        '">'
L_ROOM_UUID_3 = '    <UUID>' + TESTING_ROOM_UUID_3 + '</UUID>'
L_ROOM_COMMENT_3 = '  <Comment>' + TESTING_ROOM_COMMENT_3 + '</Comment>'
L_ROOM_CORNER_3 = '  <Corner>' + TESTING_ROOM_CORNER_3 + '</Corner>'
L_ROOM_FLOOR_3 = '    <Floor>' + TESTING_ROOM_FLOOR_3 + '</Floor>'
L_ROOM_LAST_UPDATE_3 = '    <LastUpdate>' + str(TESTING_ROOM_LAST_UPDATE_3) + '</LastUpdate>'
L_ROOM_SIZE_3 = '  <Size>' + TESTING_ROOM_SIZE_3 + '</Size>'
L_ROOM_TYPE_3 = '  <RoomType>' + TESTING_ROOM_TYPE_3 + '</RoomType>'

L_ROOM_3 = '\n'.join([
    L_ROOM_START_3,
    L_ROOM_UUID_3,
    L_ROOM_COMMENT_3,
    L_ROOM_CORNER_3,
    L_ROOM_FLOOR_3,
    L_ROOM_LAST_UPDATE_3,
    L_ROOM_SIZE_3,
    L_ROOM_TYPE_3,
    L_ROOM_END
])

XML_ROOMS = '\n'.join([
    L_ROOM_SECTION_START,
    L_ROOM_0,
    L_ROOM_1,
    L_ROOM_2,
    L_ROOM_3,
    L_ROOM_SECTION_END
])

# ## END DBK
