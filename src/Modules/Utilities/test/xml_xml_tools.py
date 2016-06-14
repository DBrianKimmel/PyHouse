"""
@name:      PyHouse/src/Modules/Utilities/test/xml_xml_tools.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: 2016-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 11, 2016
@summary:   This module is for testing XML tools.

"""

TESTING_XML_BOOL_0 = 'False'
TESTING_XML_BOOL_1 = 'True'
TESTING_XML_BOOL_2 = 'Howdy'
L_BOOL_0 = '<Bool0>' + TESTING_XML_BOOL_0 + '</Bool0>'
L_BOOL_1 = '<Bool1>' + TESTING_XML_BOOL_1 + '</Bool1>'
L_BOOL_2 = '<Bool2>' + TESTING_XML_BOOL_2 + '</Bool2>'

TESTING_XML_FLOAT_0 = '3.1415926535'
L_FLOAT_0 = '<Float0>' + TESTING_XML_FLOAT_0 + '</Float0>'

TESTING_XML_INT_0 = '137'
TESTING_XML_INT_1 = '319'
L_INT_0 = '<Int0>' + TESTING_XML_INT_0 + '</Int0>'
L_INT_1 = '<Int1>' + TESTING_XML_INT_1 + '</Int1>'

TESTING_XML_TEXT_0 = 'Test of text element'
TESTING_XML_TEXT_1 = 'Another text element'
L_TEXT_0 = '<Text0>' + TESTING_XML_TEXT_0 + '</Text0>'
L_TEXT_1 = '<Text1>' + TESTING_XML_TEXT_1 + '</Text1>'


TESTING_XML_IPV4_0 = '98.76.45.123'
TESTING_XML_IPV6_0 = '1234:dead::beef'
L_IPV4_0 = '<IpV40>' + TESTING_XML_IPV4_0 + '</IpV40>'
L_IPV6_0 = '<IpV60>' + TESTING_XML_IPV6_0 + '</IpV60>'

TESTING_XML_UUID_0 = '01234567-fedc-2468-7531-0123456789ab'
L_UUID_0 = '<UUID0>' + TESTING_XML_UUID_0 + '</UUID0>'

TESTING_XML_YEAR_0 = '2016'
TESTING_XML_MONTH_0 = '01'
TESTING_XML_DAY_0 = '23'
TESTING_XML_HOUR_0 = '05'
TESTING_XML_MINUTE_0 = '10'
TESTING_XML_SECOND_0 = '15'
TESTING_XML_DATE_TIME_0 = '2016-01-23 05:10:15'
L_DATE_TIME_0 = '<DateTime0>' + TESTING_XML_DATE_TIME_0 + '</DateTime0>'

TESTING_XML_ROOM_X_0 = '3.4'
TESTING_XML_ROOM_Y_0 = '5.6'
TESTING_XML_ROOM_Z_0 = '1.2'
TESTING_XML_ROOM_COORDS_0 = '[' + TESTING_XML_ROOM_X_0 + ', ' + TESTING_XML_ROOM_Y_0 + ', ' + TESTING_XML_ROOM_Z_0 + ']'
L_ROOM_COORDS_0 = '<RoomCoords0>' + TESTING_XML_ROOM_COORDS_0 + '</RoomCoords0>'

TESTING_XML_BOOL_A0 = 'True'
TESTING_XML_FLOAT_A0 = '2.123456789'
TESTING_XML_INT_A0 = '1931'
TESTING_XML_TEXT_A0 = 'Test of text attribute'
L_TEST_0_START = '<Test ' + \
    '  BoolA0="' + TESTING_XML_BOOL_A0 + \
    '" FloatA0="' + TESTING_XML_FLOAT_A0 + \
    '" IntA0="' + TESTING_XML_INT_A0 + \
    '" TextA0="' + TESTING_XML_TEXT_A0 + \
    '">'
L_TEST_0_END = '</Test>'

TESTING_XML_BOOL_A1 = 'False'
TESTING_XML_FLOAT_A1 = '3.1415926535'
TESTING_XML_INT_A1 = '279'
TESTING_XML_TEXT_A1 = 'Another text attribute'
L_TEST_A1_START = '<SubTest ' + \
    '  BoolA1="' + TESTING_XML_BOOL_A1 + \
    '" FloatA1="' + TESTING_XML_FLOAT_A1 + \
    '" IntA1="' + TESTING_XML_INT_A1 + \
    '" TextA1="' + TESTING_XML_TEXT_A1 + \
    '" />'
L_TEST_1_END = '</Test>'

XML_TEST = '\n'.join([
    L_TEST_0_START,
    L_BOOL_0,
    L_BOOL_1,
    L_BOOL_2,
    L_FLOAT_0,
    L_INT_0,
    L_TEXT_0,
    L_TEXT_1,
    L_TEST_A1_START,
    L_IPV4_0,
    L_IPV6_0,
    L_UUID_0,
    L_DATE_TIME_0,
    L_ROOM_COORDS_0,
    L_TEST_0_END
])

# ## END DBK
