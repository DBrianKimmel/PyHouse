"""
@name:      PyHouse/src/Modules/Housing/test/xml_rooms.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2016 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 22, 2014
@Summary:

"""

L_ROOM_SECTION_START = '  <RoomSection>'
L_ROOM_SECTION_END = '  </RoomSection>'
L_ROOM_END = '  </Room>'

TESTING_ROOM_NAME_0 = 'Master Bath'
TESTING_ROOM_KEY_0 = '0'
TESTING_ROOM_ACTIVE_0 = 'True'
TESTING_ROOM_COMMENT_0 = 'Room comment # 0'
TESTING_ROOM_CORNER_X_0 = '12.1'
TESTING_ROOM_CORNER_Y_0 = '14.2'
TESTING_ROOM_CORNER_Z_0 = '0.5'
TESTING_ROOM_CORNER_0 = '[' + TESTING_ROOM_CORNER_X_0 + \
                        ',' + TESTING_ROOM_CORNER_Y_0 + \
                        ',' + TESTING_ROOM_CORNER_Z_0 + \
                        ']'
TESTING_ROOM_FLOOR_0 = '1'
TESTING_ROOM_SIZE_X_0 = '3.0'
TESTING_ROOM_SIZE_0 = '[3.0,5.5,3.0]'
TESTING_ROOM_TYPE_0 = 'Room'
TESTING_ROOM_UUID_0 = '51c03dcc-2e69-Room-0000-Room00000000'
L_ROOM_START_0 = '  <Room Name="' + TESTING_ROOM_NAME_0 + '" Key="' + TESTING_ROOM_KEY_0 + '" Active="' + \
        TESTING_ROOM_ACTIVE_0 + '">'
L_ROOM_COMMENT_0 = '  <Comment>' + TESTING_ROOM_COMMENT_0 + '</Comment>'
L_ROOM_CORNER_0 = '  <Corner>' + TESTING_ROOM_CORNER_0 + '</Corner>'
L_ROOM_FLOOR_0 = '    <Floor>' + TESTING_ROOM_FLOOR_0 + '</Floor>'
L_ROOM_SIZE_0 = '  <Size>' + TESTING_ROOM_SIZE_0 + '</Size>'
L_ROOM_TYPE_0 = '  <RoomType>' + TESTING_ROOM_TYPE_0 + '</RoomType>'
L_ROOM_UUID_0 = '    <UUID>' + TESTING_ROOM_UUID_0 + '</UUID>'

L_ROOM_0 = '\n'.join([
    L_ROOM_START_0,
    L_ROOM_UUID_0,
    L_ROOM_COMMENT_0,
    L_ROOM_CORNER_0,
    L_ROOM_FLOOR_0,
    L_ROOM_SIZE_0,
    L_ROOM_TYPE_0,
    L_ROOM_END
])

TESTING_ROOM_NAME_1 = 'Master Bed Closet'
TESTING_ROOM_KEY_1 = '0'
TESTING_ROOM_ACTIVE_1 = 'True'
TESTING_ROOM_COMMENT_1 = 'Room comment # 1'
TESTING_ROOM_CORNER_1 = '[12.0,14.0,0.5]'
TESTING_ROOM_FLOOR_1 = '1'
TESTING_ROOM_SIZE_1 = '[3.0,5.5,3.0]'
TESTING_ROOM_TYPE_1 = 'Room'
TESTING_ROOM_UUID_1 = '51c03dcc-2e69-Room-0001-Room11111111'

L_ROOM_START_1 = '  <Room Name="' + TESTING_ROOM_NAME_1 + '" Key="' + TESTING_ROOM_KEY_1 + '" Active="' + \
        TESTING_ROOM_ACTIVE_1 + '">'
L_ROOM_COMMENT_1 = '  <Comment>' + TESTING_ROOM_COMMENT_1 + '</Comment>'
L_ROOM_CORNER_1 = '  <Corner>' + TESTING_ROOM_CORNER_1 + '</Corner>'
L_ROOM_FLOOR_1 = '    <Floor>' + TESTING_ROOM_FLOOR_1 + '</Floor>'
L_ROOM_SIZE_1 = '  <Size>' + TESTING_ROOM_SIZE_1 + '</Size>'
L_ROOM_TYPE_1 = '  <RoomType>' + TESTING_ROOM_TYPE_1 + '</RoomType>'
L_ROOM_UUID_1 = '    <UUID>' + TESTING_ROOM_UUID_1 + '</UUID>'

L_ROOM_1 = '\n'.join([
    L_ROOM_START_1,
    L_ROOM_UUID_1,
    L_ROOM_COMMENT_1,
    L_ROOM_CORNER_1,
    L_ROOM_FLOOR_1,
    L_ROOM_SIZE_1,
    L_ROOM_TYPE_1,
    L_ROOM_END
])

TESTING_ROOM_NAME_2 = 'Sitting Room'
TESTING_ROOM_KEY_2 = '0'
TESTING_ROOM_ACTIVE_2 = 'True'
TESTING_ROOM_COMMENT_2 = 'Room comment # 2'
TESTING_ROOM_CORNER_2 = '[12.0,14.0,0.5]'
TESTING_ROOM_SIZE_2 = '[3.0,5.5,3.0]'
TESTING_ROOM_UUID_2 = '51c03dcc-2e69-Room-0002-Room22222222'

L_ROOM_START_2 = '  <Room Name="' + TESTING_ROOM_NAME_2 + '" Key="' + TESTING_ROOM_KEY_2 + '" Active="' + \
        TESTING_ROOM_ACTIVE_2 + '">'
L_ROOM_COMMENT_2 = '  <Comment>' + TESTING_ROOM_COMMENT_2 + '</Comment>'
L_ROOM_CORNER_2 = '  <Corner>' + TESTING_ROOM_CORNER_2 + '</Corner>'
L_ROOM_SIZE_2 = '  <Size>' + TESTING_ROOM_SIZE_2 + '</Size>'
L_ROOM_UUID_2 = '    <UUID>' + TESTING_ROOM_UUID_2 + '</UUID>'

L_ROOM_2 = '\n'.join([
    L_ROOM_START_2,
    L_ROOM_COMMENT_2,
    L_ROOM_CORNER_2,
    L_ROOM_SIZE_2,
    L_ROOM_UUID_2,
    L_ROOM_END
])

TESTING_ROOM_NAME_3 = 'Foyer'
TESTING_ROOM_KEY_3 = '0'
TESTING_ROOM_ACTIVE_3 = 'True'
TESTING_ROOM_COMMENT_3 = 'Room comment # 3'
TESTING_ROOM_CORNER_3 = '[12.0,14.0,0.5]'
TESTING_ROOM_FLOOR_3 = '1'
TESTING_ROOM_SIZE_3 = '[ 3.0,5.5,3.0]'
TESTING_ROOM_TYPE_3 = 'Room'
TESTING_ROOM_UUID_3 = 'Room.dcc-2e69-Room-0003-Room33333333'


XML_ROOMS = '\n'.join([
    L_ROOM_SECTION_START,
    L_ROOM_0,
    L_ROOM_1,
    L_ROOM_2,
    L_ROOM_SECTION_END
])


ROOMS_XSD = """
<xs:schema
    attributeFormDefault="unqualified"
    elementFormDefault="qualified"
    xmlns:xs="http://www.w3.org/2001/XMLSchema">

  <xs:element name="RoomSection">
    <xs:complexType>
      <xs:sequence>
        <xs:element name="Room" maxOccurs="unbounded" minOccurs="0">
          <xs:complexType>
            <xs:sequence>
              <xs:element type="xs:string" name="Comment"/>
              <xs:element type="xs:string" name="Corner"/>
              <xs:element type="xs:string" name="Size"/>
            </xs:sequence>
            <xs:attribute type="xs:string" name="Active" use="optional"/>
            <xs:attribute type="xs:byte" name="Key" use="optional"/>
            <xs:attribute type="xs:string" name="Name" use="optional"/>
          </xs:complexType>
        </xs:element>
      </xs:sequence>
    </xs:complexType>
  </xs:element>

</xs:schema>
"""
# ## END DBK
