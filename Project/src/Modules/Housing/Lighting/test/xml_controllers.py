"""
@name:      PyHouse/src/Modules/Lighting/test/xml_controllers.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2014-2018 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 22, 2014
@Summary:

There is a matrix of controllers to create here

<ControllerSection>
    <Controller Active="True" Key="0" Name="Insteon Serial Controller">
        <UUID>Controlr-0000-0000-0000-2468acb6eb6f</UUID>
        <Comment>Device Comment 0</Comment>
        <DeviceFamily>Insteon</DeviceFamily>
        <DeviceType>1</DeviceType>
        <DeviceSubType>2</DeviceSubType>
        <RoomCoords>[3.4, 5.6, 1.2]</RoomCoords>
        <RoomName>Testing Room Name ABDG</RoomName>
        <RoomUUID>Device..-Room-0001-0002-deadbeef1234</RoomUUID>
        <UUID>Device..-Dev.-0001-0002-deadbeef1234</UUID>
        <InsteonAddress>21.34.1F</InsteonAddress>
        <DevCat>01.1C</DevCat>
        <EngineVersion>1</EngineVersion>
        <FirmwareVersion>32</FirmwareVersion>
        <GroupNumber>5</GroupNumber>
        <GroupList>Insteon Group list 1</GroupList>
        <ProductKey>11.1A.DD</ProductKey>
        <InterfaceType>Serial</InterfaceType>
        <Port>/dev/ttyS0</Port>
        <Serial>
            <BaudRate>19200</BaudRate>
            <ByteSize>8</ByteSize>
            <Parity>N</Parity>
            <StopBits>1.0</StopBits>
            <Timeout>1.0</Timeout>
            <DsrDtr>False</DsrDtr>
            <RtsCts>False</RtsCts>
            <XonXoff>False</XonXoff>
        </Serial>
    </Controller>
    <Controller Active="True" Key="1" Name="UPB USB Controller">
        <UUID>Controlr-0001-0001-0001-2468acb6eb6f</UUID>
        <Comment>Device Comment 0</Comment>
        <DeviceFamily>UPB</DeviceFamily>
        <DeviceType>1</DeviceType>
        <DeviceSubType>2</DeviceSubType>
        <RoomCoords>[3.4, 5.6, 1.2]</RoomCoords>
        <RoomName>Testing Room Name ABDG</RoomName>
        <RoomUUID>Device..-Room-0001-0002-deadbeef1234</RoomUUID>
        <UUID>Device..-Dev.-0001-0002-deadbeef1234</UUID>
        <UPBAddress>255</UPBAddress>
        <UPBNetworkID>6</UPBNetworkID>
        <UPBPassword>1253</UPBPassword>
        <InterfaceType>USB</InterfaceType>
        <Port>/dev/ttyUSB0</Port>
        <USB>
            <Vendor>6109</Vendor>
            <Product>21760</Product>
        </USB>
    </Controller>
</ControllerSection>

"""

__updated__ = '2019-02-07'

# Import system type stuff

# Import PyMh files
from Modules.Core.test.xml_device import \
        XML_DEVICE_INSTEON, \
        XML_DEVICE_UPB
from Modules.Drivers.test.xml_interface import \
        XML_SERIAL_LINUX_INTERFACE, \
        XML_USB_INTERFACE
from Modules.Families.Insteon.test.xml_insteon import XML_INSTEON_1
from Modules.Families.UPB.test.xml_upb import \
        XML_UPB
from Modules.Drivers.Serial.test.xml_serial import \
        XML_SERIAL
from Modules.Drivers.USB.test.xml_usb import \
        XML_USB

TESTING_CONTROLLER_SECTION = 'ControllerSection'
TESTING_CONTROLLER = 'Controller'

L_SERIAL_INTERFACE = XML_SERIAL_LINUX_INTERFACE

L_CONTROLLER_SECTION_START = '<' + TESTING_CONTROLLER_SECTION + '>'
L_CONTROLLER_SECTION_END = '</' + TESTING_CONTROLLER_SECTION + '>'
L_CONTROLLER_END = '</' + TESTING_CONTROLLER + '>'

TESTING_CONTROLLER_NAME_0 = 'Insteon Serial Controller'
TESTING_CONTROLLER_KEY_0 = '0'
TESTING_CONTROLLER_ACTIVE_0 = 'True'
TESTING_CONTROLLER_UUID_0 = 'Controlr-0000-0000-0000-2468acb6eb6f'
TESTING_CONTROLLER_COMMENT_0 = 'Device Comment 0'
TESTING_CONTROLLER_FAMILY_0 = 'Insteon'
TESTING_CONTROLLER_INTERFACE_TYPE_0 = 'Serial'
TESTING_CONTROLLER_TYPE_0 = '1'
TESTING_CONTROLLER_SUBTYPE_0 = '2'
TESTING_CONTROLLER_ROOM_X_0 = '3.4'
TESTING_CONTROLLER_ROOM_Y_0 = '5.6'
TESTING_CONTROLLER_ROOM_Z_0 = '1.2'
TESTING_CONTROLLER_ROOM_COORDS_0 = '[' + TESTING_CONTROLLER_ROOM_X_0 + ', ' + TESTING_CONTROLLER_ROOM_Y_0 + ', ' + TESTING_CONTROLLER_ROOM_Z_0 + ']'
TESTING_CONTROLLER_ROOM_NAME_0 = "Testing Room Name Zero"
TESTING_CONTROLLER_ROOM_UUID_0 = 'Device..-Room-000o-0002-deadbeef1234'

L_CONTROLLER_START_0 = \
        '<' + TESTING_CONTROLLER + \
        '  Name="' + TESTING_CONTROLLER_NAME_0 + \
        '" Key="' + TESTING_CONTROLLER_KEY_0 + \
        '" Active="' + TESTING_CONTROLLER_ACTIVE_0 + \
        '">'

L_CONTROLLER_FAMILY_0 = "<DeviceFamily>" + TESTING_CONTROLLER_FAMILY_0 + "</DeviceFamily>"
L_CONTROLLER_TYPE_0 = '<DeviceType>' + TESTING_CONTROLLER_TYPE_0 + '</DeviceType>'
L_CONTROLLER_SUBTYPE_0 = '<DeviceSubType>' + TESTING_CONTROLLER_SUBTYPE_0 + '</DeviceSubType>'
L_CONTROLLER_ROOM_COORD_0 = "<RoomCoords>" + TESTING_CONTROLLER_ROOM_COORDS_0 + "</RoomCoords>"
L_CONTROLLER_ROOM_NAME_0 = "<RoomName>" + TESTING_CONTROLLER_ROOM_NAME_0 + "</RoomName>"
L_CONTROLLER_ROOM_UUID_0 = "<RoomUUID>" + TESTING_CONTROLLER_ROOM_UUID_0 + "</RoomUUID>"

L_CONTROLLER_COMMENT_0 = '<Comment>' + TESTING_CONTROLLER_COMMENT_0 + '</Comment>'
L_CONTROLLER_UUID_0 = '<UUID>' + TESTING_CONTROLLER_UUID_0 + '</UUID>'

L_CONTROLLER_ROOM_0 = '\n'.join([
    L_CONTROLLER_ROOM_NAME_0,
    L_CONTROLLER_ROOM_COORD_0,
    L_CONTROLLER_ROOM_UUID_0
    ])

L_CONTROLLER_0 = '\n'.join([
    L_CONTROLLER_START_0,
    L_CONTROLLER_UUID_0,
    L_CONTROLLER_FAMILY_0,
    L_CONTROLLER_TYPE_0,
    L_CONTROLLER_SUBTYPE_0,
    L_CONTROLLER_ROOM_0,

    XML_DEVICE_INSTEON,
    XML_INSTEON_1,
    L_SERIAL_INTERFACE,
    XML_SERIAL,
    L_CONTROLLER_END
    ])

TESTING_CONTROLLER_NAME_1 = 'UPB USB Controller'
TESTING_CONTROLLER_KEY_1 = '1'
TESTING_CONTROLLER_ACTIVE_1 = 'True'
TESTING_CONTROLLER_COMMENT_1 = 'Device Comment 1'
TESTING_CONTROLLER_UUID_1 = 'Controlr-0001-0001-0001-2468acb6eb6f'

L_CONTROLLER_START_1 = '    ' + \
        '<Controller Name="' + TESTING_CONTROLLER_NAME_1 + \
        '" Key="' + TESTING_CONTROLLER_KEY_1 + \
        '" Active="' + TESTING_CONTROLLER_ACTIVE_1 + \
        '">'
L_CONTROLLER_UUID_1 = '<UUID>' + TESTING_CONTROLLER_UUID_1 + '</UUID>'
L_CONTROLLER_COMMENT_1 = '<Comment>' + TESTING_CONTROLLER_COMMENT_1 + '</Comment>'

L_CONTROLLER_1 = '\n'.join([
    L_CONTROLLER_START_1,
    L_CONTROLLER_UUID_1,
    L_CONTROLLER_COMMENT_1,
    XML_DEVICE_UPB,
    XML_UPB,
    XML_USB_INTERFACE,
    XML_USB,
    L_CONTROLLER_END
    ])

TESTING_CONTROLLER_NAME_2 = 'Insteon Serial Controller'
TESTING_CONTROLLER_KEY_2 = '0'
TESTING_CONTROLLER_ACTIVE_2 = 'True'
TESTING_CONTROLLER_UUID_2 = 'Controlr-0000-0000-0000-2468acb6eb6f'
TESTING_CONTROLLER_COMMENT_2 = 'Device Comment 0'
TESTING_CONTROLLER_FAMILY_2 = 'Insteon'
TESTING_CONTROLLER_INTERFACE_TYPE_2 = 'Serial'
TESTING_CONTROLLER_TYPE = '1'
TESTING_CONTROLLER_SUBTYPE = '2'
TESTING_CONTROLLER_ROOM_NAME_2 = "Testing Room Name ABDG"
TESTING_CONTROLLER_ROOM_UUID_2 = 'Device..-Room-0001-0002-deadbeef1234'

L_CONTROLLER_START_2 = \
        '<' + TESTING_CONTROLLER + \
        '  Name="' + TESTING_CONTROLLER_NAME_2 + \
        '" Key="' + TESTING_CONTROLLER_KEY_2 + \
        '" Active="' + TESTING_CONTROLLER_ACTIVE_2 + \
        '">'
L_CONTROLLER_UUID_2 = '<UUID>' + TESTING_CONTROLLER_UUID_2 + '</UUID>'
L_CONTROLLER_FAMILY_2 = "<DeviceFamily>" + TESTING_CONTROLLER_FAMILY_2 + "</DeviceFamily>"

L_CONTROLLER_2 = '\n'.join([
    L_CONTROLLER_START_2,
    L_CONTROLLER_UUID_2,
    L_CONTROLLER_COMMENT_1,
    L_CONTROLLER_FAMILY_2,
    XML_DEVICE_UPB,
    XML_UPB,
    XML_USB_INTERFACE,
    XML_USB,
    L_CONTROLLER_END
    ])

XML_CONTROLLER_SECTION = '\n'.join([
    L_CONTROLLER_SECTION_START,
    L_CONTROLLER_0,
    L_CONTROLLER_1,
    L_CONTROLLER_2,
    L_CONTROLLER_SECTION_END
    ])

# ## END DBK
