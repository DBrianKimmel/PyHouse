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

__updated__ = '2018-11-26'

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
TESTING_CONTROLLER_COMMENT = 'Controller Comment'
TESTING_CONTROLLER_COMMENT_0 = 'Device Comment 0'
TESTING_CONTROLLER_FAMILY_INSTEON = 'Insteon'
TESTING_CONTROLLER_INTERFACE_TYPE = 'Serial'
TESTING_CONTROLLER_TYPE = '1'
TESTING_CONTROLLER_SUBTYPE = '2'
TESTING_CONTROLLER_ROOM_X = '3.4'
TESTING_CONTROLLER_ROOM_Y = '5.6'
TESTING_CONTROLLER_ROOM_Z = '1.2'
TESTING_CONTROLLER_ROOM_COORDS = '[' + TESTING_CONTROLLER_ROOM_X + ', ' + TESTING_CONTROLLER_ROOM_Y + ', ' + TESTING_CONTROLLER_ROOM_Z + ']'
TESTING_CONTROLLER_ROOM_NAME = "Testing Room Name ABDG"
TESTING_CONTROLLER_ROOM_UUID = 'Device..-Room-0001-0002-deadbeef1234'

L_CONTROLLER_START_0 = '    ' + \
        '<Controller Name="' + TESTING_CONTROLLER_NAME_0 + \
        '" Key="' + TESTING_CONTROLLER_KEY_0 + \
        '" Active="' + TESTING_CONTROLLER_ACTIVE_0 + \
        '">'
L_CONTROLLER_UUID_0 = '    <UUID>' + TESTING_CONTROLLER_UUID_0 + '</UUID>'

L_CONTROLLER_0 = '\n'.join([
    L_CONTROLLER_START_0,
    L_CONTROLLER_UUID_0,
    XML_DEVICE_INSTEON,
    XML_INSTEON_1,
    L_SERIAL_INTERFACE,
    XML_SERIAL,
    L_CONTROLLER_END
    ])

TESTING_CONTROLLER_NAME_1 = 'UPB USB Controller'
TESTING_CONTROLLER_KEY_1 = '1'
TESTING_CONTROLLER_ACTIVE_1 = 'True'
TESTING_CONTROLLER_UUID_1 = 'Controlr-0001-0001-0001-2468acb6eb6f'

L_CONTROLLER_START_1 = '    ' + \
        '<Controller Name="' + TESTING_CONTROLLER_NAME_1 + \
        '" Key="' + TESTING_CONTROLLER_KEY_1 + \
        '" Active="' + TESTING_CONTROLLER_ACTIVE_1 + \
        '">'
L_CONTROLLER_UUID_1 = '    <UUID>' + TESTING_CONTROLLER_UUID_1 + '</UUID>'
L_CONTROLLER_1 = '\n'.join([
    L_CONTROLLER_START_1,
    L_CONTROLLER_UUID_1,
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
    L_CONTROLLER_SECTION_END
    ])

# ## END DBK
