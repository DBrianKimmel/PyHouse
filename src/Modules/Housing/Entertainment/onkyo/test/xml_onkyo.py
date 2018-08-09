"""
-*- test-case-name: /home/briank/workspace/PyHouse/src/Modules/Housing/Entertainment/onkyo/test/xml_onkyo.py -*-

@name:      /home/briank/workspace/PyHouse/src/Modules/Housing/Entertainment/onkyo/test/xml_onkyo.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2018-2018 by D. Brian Kimmel
@note:      Created on Mar 19, 2018
@license:   MIT License
@summary:

<EntertainmentSection>
    <OnkyoSection Active="True">
        <Device Active="True" Key="0" Name="L/R Receiver TX-555">
            <UUID>Onkyo...-0000-0000-0000-0123456789ab</UUID>
            <Comment>Tx-555 Receiver</Comment>
            <IPv4>192.168.1.138</IPv4>
            <Port>60128</Port>
            <RoomName>Living Room</RoomName>
            <RoomUUID>Room....-0000-0000-0000-0123456789ab</RoomUUID>
            <Type>Receiver</Type>
        </Device>
        <Device Active="False" Key="1" Name="Receiver T2 = X-555">
            <UUID>Onkyo...-0000-0001-0001-0123456789ab</UUID>
            <Comment>Tx-555 Receiver_2</Comment>
            <IPv4>192.168.1.139</IPv4>
            <Port>60128</Port>
            <RoomName>Living Room</RoomName>
            <RoomUUID>Room....-0000-0000-0000-0123456789ab</RoomUUID>
            <Type>Receiver</Type>
        </Device>
    </OnkyoSection>
</EntertainmentSection>
"""

__updated__ = '2018-08-08'

TESTING_ONKYO_SECTION = 'OnkyoSection'
TESTING_DEVICE = 'Device'
TESTING_ONKYO_ACTIVE = 'True'

L_ONKYO_SECTION_START = '<' + TESTING_ONKYO_SECTION + ' Active="' + TESTING_ONKYO_ACTIVE + '">'
L_ONKYO_SECTION_END = '</' + TESTING_ONKYO_SECTION + '>'
L_DEVICE_END = '</' + TESTING_DEVICE + '>'

TESTING_ONKYO_DEVICE_NAME_0 = 'L/R Receiver TX-555'
TESTING_ONKYO_DEVICE_KEY_0 = '0'
TESTING_ONKYO_DEVICE_ACTIVE_0 = 'True'
TESTING_ONKYO_DEVICE_UUID_0 = 'Onkyo...-0000-0000-0000-0123456789ab'
TESTING_ONKYO_DEVICE_COMMENT_0 = 'Tx-555 Receiver'
TESTING_ONKYO_DEVICE_IPV4_0 = '192.168.1.138'
TESTING_ONKYO_DEVICE_PORT_0 = '60128'
TESTING_ONKYO_DEVICE_ROOM_NAME_0 = 'Living Room'
TESTING_ONKYO_DEVICE_ROOM_UUID_0 = 'Room....-0000-0000-0000-0123456789ab'
TESTING_ONKYO_DEVICE_TYPE_0 = 'Receiver'

L_ONKYO_DEVICE_START_0 = \
    '<' + TESTING_DEVICE + \
    ' Name="' + TESTING_ONKYO_DEVICE_NAME_0 + \
    '" Key="' + TESTING_ONKYO_DEVICE_KEY_0 + \
    '" Active="' + TESTING_ONKYO_DEVICE_ACTIVE_0 + \
    '">'
L_ONKYO_UUID_0 = '<UUID>' + TESTING_ONKYO_DEVICE_UUID_0 + '</UUID>'
L_ONKYO_COMMENT_0 = '<Comment>' + TESTING_ONKYO_DEVICE_COMMENT_0 + '</Comment>'
L_ONKYO_IPV4_0 = '<IPv4>' + TESTING_ONKYO_DEVICE_IPV4_0 + '</IPv4>'
L_ONKYO_PORT_0 = '<Port>' + TESTING_ONKYO_DEVICE_PORT_0 + '</Port>'
L_ONKYO_ROOM_NAME_0 = '<RoomName>' + TESTING_ONKYO_DEVICE_ROOM_NAME_0 + '</RoomName>'
L_ONKYO_ROOM_UUID_0 = '<RoomUUID>' + TESTING_ONKYO_DEVICE_ROOM_UUID_0 + '</RoomUUID>'
L_ONKYO_TYPE_0 = '<Type>' + TESTING_ONKYO_DEVICE_TYPE_0 + '</Type>'

L_ONKYO_DEVICE_0 = '\n'.join([
    L_ONKYO_DEVICE_START_0,
    L_ONKYO_UUID_0,
    L_ONKYO_COMMENT_0,
    L_ONKYO_IPV4_0,
    L_ONKYO_PORT_0,
    L_ONKYO_ROOM_NAME_0,
    L_ONKYO_ROOM_UUID_0,
    L_ONKYO_TYPE_0,
    L_DEVICE_END
])

TESTING_ONKYO_DEVICE_NAME_1 = 'Receiver T2 = X-555'
TESTING_ONKYO_DEVICE_KEY_1 = '1'
TESTING_ONKYO_DEVICE_ACTIVE_1 = 'False'
TESTING_ONKYO_DEVICE_UUID_1 = 'Onkyo...-0000-0001-0001-0123456789ab'
TESTING_ONKYO_DEVICE_COMMENT_1 = 'Tx-555 Receiver_2'
TESTING_ONKYO_DEVICE_IPV4_1 = '192.168.1.139'
TESTING_ONKYO_DEVICE_PORT_1 = '60128'
TESTING_ONKYO_DEVICE_ROOM_NAME_1 = 'Living Room'
TESTING_ONKYO_DEVICE_ROOM_UUID_1 = 'Room....-0000-0000-0000-0123456789ab'
TESTING_ONKYO_DEVICE_TYPE_1 = 'Receiver'

L_ONKYO_DEVICE_START_1 = \
    '<' + TESTING_DEVICE + \
    ' Name="' + TESTING_ONKYO_DEVICE_NAME_1 + \
    '" Key="' + TESTING_ONKYO_DEVICE_KEY_1 + \
    '" Active="' + TESTING_ONKYO_DEVICE_ACTIVE_1 + \
    '">'
L_ONKYO_UUID_1 = '<UUID>' + TESTING_ONKYO_DEVICE_UUID_1 + '</UUID>'
L_ONKYO_COMMENT_1 = '<Comment>' + TESTING_ONKYO_DEVICE_COMMENT_1 + '</Comment>'
L_ONKYO_IPV4_1 = '<IPv4>' + TESTING_ONKYO_DEVICE_IPV4_1 + '</IPv4>'
L_ONKYO_PORT_1 = '<Port>' + TESTING_ONKYO_DEVICE_PORT_1 + '</Port>'
L_ONKYO_ROOM_NAME_1 = '<RoomName>' + TESTING_ONKYO_DEVICE_ROOM_NAME_1 + '</RoomName>'
L_ONKYO_ROOM_UUID_1 = '<RoomUUID>' + TESTING_ONKYO_DEVICE_ROOM_UUID_1 + '</RoomUUID>'
L_ONKYO_TYPE_1 = '<Type>' + TESTING_ONKYO_DEVICE_TYPE_1 + '</Type>'

L_ONKYO_DEVICE_1 = '\n'.join([
    L_ONKYO_DEVICE_START_1,
    L_ONKYO_UUID_1,
    L_ONKYO_COMMENT_1,
    L_ONKYO_IPV4_1,
    L_ONKYO_PORT_1,
    L_ONKYO_ROOM_NAME_1,
    L_ONKYO_ROOM_UUID_1,
    L_ONKYO_TYPE_1,
    L_DEVICE_END
])

XML_ONKYO_SECTION = '\n'.join([
    L_ONKYO_SECTION_START,
    L_ONKYO_DEVICE_0,
    L_ONKYO_DEVICE_1,
    L_ONKYO_SECTION_END
])

# ## END DBK
