"""
@name:      PyHouse/src/Modules/Housing/test/xml_rooms.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 22, 2014
@Summary:

"""

TESTING_ROOM_NAME_0 = 'Master Bath'
TESTING_ROOM_KEY_0 = '0'
TESTING_ROOM_ACTIVE_0 = 'True'
TESTING_ROOM_COMMENT_0 = 'Room comment # 0'
TESTING_ROOM_CORNER_0 = '[12.0,14.0,0.5]'
TESTING_ROOM_SIZE_0 = '[3.0,5.5,3.0]'

TESTING_ROOM_NAME_1 = 'Master Bed Closer'
TESTING_ROOM_KEY_1 = '0'
TESTING_ROOM_ACTIVE_1 = 'True'
TESTING_ROOM_COMMENT_1 = 'Room comment # 0'
TESTING_ROOM_CORNER_1 = '[12.0,14.0,0.5]'
TESTING_ROOM_SIZE_1 = '[3.0,5.5,3.0]'

TESTING_ROOM_NAME_2 = 'Master Bath'
TESTING_ROOM_KEY_2 = '0'
TESTING_ROOM_ACTIVE_2 = 'True'
TESTING_ROOM_COMMENT_2 = 'Room comment # 0'
TESTING_ROOM_CORNER_2 = '[12.0,14.0,0.5]'
TESTING_ROOM_SIZE_2 = '[3.0,5.5,3.0]'

TESTING_ROOM_NAME_3 = 'Master Bath'
TESTING_ROOM_KEY_3 = '0'
TESTING_ROOM_ACTIVE_3 = 'True'
TESTING_ROOM_COMMENT_3 = 'Room comment # 0'
TESTING_ROOM_CORNER_3 = '[12.0,14.0,0.5]'
TESTING_ROOM_SIZE_3 = '[3.0,5.5,3.0]'

L_ROOM_SECTION_START = '  <RoomSection>'
L_ROOM_SECTION_END = '  </RoomSection>'
L_ROOM_START_0 = '  <Room Name="' + TESTING_ROOM_NAME_0 + '" Key="' + TESTING_ROOM_KEY_0 + '" Active="' + TESTING_ROOM_ACTIVE_0 + '">'
L_ROOM_COMMENT_0 = '  <Comment>' + TESTING_ROOM_COMMENT_0 + '</Comment>'
L_ROOM_CORNER_0 = '  <Corner>' + TESTING_ROOM_CORNER_0 + '</Corner>'
L_ROOM_SIZE_0 = '  <Size>' + TESTING_ROOM_SIZE_0 + '</Size>'
L_ROOM_START_1 = '  <Room Name="' + TESTING_ROOM_NAME_1 + '" Key="' + TESTING_ROOM_KEY_1 + '" Active="' + TESTING_ROOM_ACTIVE_1 + '">'
L_ROOM_COMMENT_1 = '  <Comment>' + TESTING_ROOM_COMMENT_1 + '</Comment>'
L_ROOM_CORNER_1 = '  <Corner>' + TESTING_ROOM_CORNER_1 + '</Corner>'
L_ROOM_SIZE_1 = '  <Size>' + TESTING_ROOM_SIZE_1 + '</Size>'
L_ROOM_START_2 = '  <Room Name="' + TESTING_ROOM_NAME_2 + '" Key="' + TESTING_ROOM_KEY_2 + '" Active="' + TESTING_ROOM_ACTIVE_2 + '">'
L_ROOM_COMMENT_2 = '  <Comment>' + TESTING_ROOM_COMMENT_2 + '</Comment>'
L_ROOM_CORNER_2 = '  <Corner>' + TESTING_ROOM_CORNER_2 + '</Corner>'
L_ROOM_SIZE_2 = '  <Size>' + TESTING_ROOM_SIZE_2 + '</Size>'
L_ROOM_START_3 = '  <Room Name="' + TESTING_ROOM_NAME_3 + '" Key="' + TESTING_ROOM_KEY_3 + '" Active="' + TESTING_ROOM_ACTIVE_3 + '">'
L_ROOM_COMMENT_3 = '  <Comment>' + TESTING_ROOM_COMMENT_3 + '</Comment>'
L_ROOM_CORNER_3 = '  <Corner>' + TESTING_ROOM_CORNER_3 + '</Corner>'
L_ROOM_SIZE_3 = '  <Size>' + TESTING_ROOM_SIZE_3 + '</Size>'
L_ROOM_END = '  </Room>'

L_ROOM_0 = '\n'.join([
    L_ROOM_START_0,
    L_ROOM_COMMENT_0,
    L_ROOM_CORNER_0,
    L_ROOM_SIZE_0,
    L_ROOM_END
])
L_ROOM_1 = '\n'.join([
    L_ROOM_START_1,
    L_ROOM_COMMENT_1,
    L_ROOM_CORNER_1,
    L_ROOM_SIZE_1,
    L_ROOM_END
])
L_ROOM_2 = '\n'.join([
    L_ROOM_START_2,
    L_ROOM_COMMENT_2,
    L_ROOM_CORNER_2,
    L_ROOM_SIZE_2,
    L_ROOM_END
])
L_ROOM_3 = '\n'.join([
    L_ROOM_START_3,
    L_ROOM_COMMENT_3,
    L_ROOM_CORNER_3,
    L_ROOM_SIZE_3,
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

XML_ROOMS = '\n'.join([
    L_ROOM_SECTION_START,
    L_ROOM_0,
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
