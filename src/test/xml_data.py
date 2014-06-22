"""
@name: PyHouse/src/test/xml_data.py
@author: D. Brian Kimmel
@contact: <d.briankimmel@gmail.com
@Copyright (c) 2010-2014 by D. Brian Kimmel
@license: MIT License
@note: Created on Jan 20, 2010
@summary: Handle all of the information for all houses.

XML to define the PyHouse.xml file

used for testing
"""

# Missing
XML_MISSING = ''


# No sections
XML_EMPTY = """
<PyHouse>
</PyHouse>
"""


# Everything as expected in a running system.
XML_LONG = """
<PyHouse Version='2'>
    <ComputerDivision>
        <LogSection>
            <Debug>/var/log/pyhouse/debug</Debug>
            <Error>/var/log/pyhouse/error</Error>
        </LogSection>
        <WebSection>
            <WebPort>8580</WebPort>
        </WebSection>

<!-- Tested to here -->

        <InternetSection>
            <Internet Name="Connection-1" Key="0" Active="True" UUID='123'>
                <ExternalUrl>http://snar.co/ip</ExternalUrl>
                <ExternalDelay>28800</ExternalDelay>
                <ExternalIP>65.35.48.61</ExternalIP>
                <DynamicDnsSection>
                    <DynamicDNS Active="True" Key="0" Name="Afraid">
                        <UpdateUrl>http://freedns.afraid.org/dynamic/update.php?VDZtSkE2MzFVMVVBQVd5QXg2MDo5MjU1MzYw</UpdateUrl>
                        <UpdateInterval>21600</UpdateInterval>
                    </DynamicDNS>
                </DynamicDnsSection>
            </Internet>
        </InternetSection>

        <NodeSection>
            <Node Name='pi-01' Key='0' Active='True'>
                <UUID>87654321-1001-11e3-b583-082e5f899999</UUID>
                <ConnectionAddressV4>192.168.1.123</ConnectionAddressV4>
                <InterfaceSection>
                    <Interface Name='eth0' Key="0" Active="True">
                        <UUID>87654321-1001-11e3-b583-012300001111</UUID>
                        <MacAddress>01:02:03:04:05:06</MacAddress>
                        <IPv4Address>192.168.1.11</IPv4Address>
                        <IPv6Address>2000:1D::1, 2000:1D::101</IPv6Address>
                    </Interface>
                    <Interface Name='wlan0' Key="1" Active="True">
                        <UUID>87654321-1001-11e3-b583-012300002222</UUID>
                        <MacAddress>01:02:03:04:05:06</MacAddress>
                        <IPv4Address>192.168.1.22</IPv4Address>
                        <IPv6Address>2000:1D::2, 2000:1D::202</IPv6Address>
                    </Interface>
                    <Interface Name='lo' Key="2" Active="True">
                        <MacAddress>01:02:03:04:05:06</MacAddress>
                        <IPv4Address>192.168.1.33</IPv4Address>
                        <IPv6Address>2000:1D::3, 2000:1D::303</IPv6Address>
                    </Interface>
                </InterfaceSection>
            </Node>
        </NodeSection>
    </ComputerDivision>

    <HouseDivision Active="True" Key="0" Name="Test House 1">
        <UUID>12345678-1002-11e3-b583-082e5f8cdfd2</UUID>
        <Location>
            <Street>Test Street 1</Street>
            <City>Test City 1</City>
            <State>Florida</State>
            <ZipCode>12345</ZipCode>
            <Phone>(800) 555-1212</Phone>
            <Latitude>28.938448</Latitude>
            <Longitude>-82.517208</Longitude>
            <TimeZone>-240.0</TimeZone>
            <SavingTime>60.0</SavingTime>
        </Location>
        <Rooms>
            <Room Active="True" Key="0" Name="Test Living Room">
                <UUID>12341234-1003-11e3-82b3-082e5f8cdfd2</UUID>
                <Comment>Test Comment</Comment>
                <Corner>0.50, 10.50</Corner>
                <Size>14.00, 13.50</Size>
            </Room>
            <Room Active="True" Key="1" Name="Dining Room">
                <UUID>12341234-1003-11e3-4444-123455789abc</UUID>
                <Comment>This is room 2</Comment>
                <Corner>3.50, 13.50</Corner>
                <Size>24.00, 23.50</Size>
            </Room>
        </Rooms>
        <Lights>
            <Light Active="True" Key="0" Name="Test LR Overhead">
                <Comment>SwitchLink On/Off</Comment>
                <Coords>['0', '0']</Coords>
                <Dimmable>False</Dimmable>
                <Family>Insteon</Family>
                <Room>Test Living Room</Room>
                <Type>Light</Type>
                <UUID>ec9d9930-89c9-11e3-a1ab-082e5f8cdfd2</UUID>
                <Address>11.22.33</Address>
                <Controller>True</Controller>
                <DevCat>3140</DevCat>
                <GroupList>All_Lights|Outside|Foyer(0;0)</GroupList>
                <GroupNumber>0</GroupNumber>
                <Master>0</Master>
                <ProductKey>30.1A.35</ProductKey>
                <Responder>True</Responder>
            </Light>
            <Light Active="True" Key="1" Name="outside_gar">
                <Comment>SwitchLink On/Off</Comment>
                <Coords>['0', '0']</Coords>
                <Dimmable>False</Dimmable>
                <Family>Insteon</Family>
                <Room>Dining Room</Room>
                <Type>Light</Type>
                <UUID>ec9d9931-89c9-11e3-8fd7-082e5f8cdfd2</UUID>
                <Address>17.47.A1</Address>
                <Controller>True</Controller>
                <DevCat>0x0</DevCat>
                <GroupList>All_Lights|Outside|Garage(0;0)</GroupList>
                <GroupNumber>2</GroupNumber>
                <Master>True</Master>
                <ProductKey>0</ProductKey>
                <Responder>True</Responder>
            </Light>
        </Lights>
        <Controllers>
            <Controller Active="False" Key="0" Name="PLM_1">
                <Comment>Dongle using serial converter 067B:2303</Comment>
                <Coords>None</Coords>
                <Dimmable>True</Dimmable>
                <Family>Insteon</Family>
                <Room>Office</Room>
                <Type>Controller</Type>
                <UUID>ec97a5c3-89c9-11e3-ab54-082e5f8cdfd2</UUID>
                <Address>AA.AA.AA</Address>
                <Controller>True</Controller>
                <DevCat>0x0</DevCat>
                <GroupList />
                <GroupNumber>0</GroupNumber>
                <Master>False</Master>
                <ProductKey>0</ProductKey>
                <Responder>True</Responder>
                <Interface>Serial</Interface>
                <Port>/dev/ttyUSB0</Port>
                <BaudRate>19200</BaudRate>
                <ByteSize>8</ByteSize>
                <Parity>N</Parity>
                <StopBits>1.0</StopBits>
                <Timeout>1.0</Timeout>
                <DsrDtr>False</DsrDtr>
                <RtsCts>False</RtsCts>
                <XonXoff>False</XonXoff>
            </Controller>
            <Controller Active="False" Key="1" Name="PowerLink">
                <Comment>2413UH Powerlink Controller</Comment>
                <Coords>None</Coords>
                <Dimmable>True</Dimmable>
                <Family>Insteon</Family>
                <Room>Office</Room>
                <Type>Controller</Type>
                <UUID>ec99a18f-89c9-11e3-b271-082e5f8cdfd2</UUID>
                <Address>17.03.B2</Address>
                <Controller>True</Controller>
                <DevCat>0x0</DevCat>
                <GroupList />
                <GroupNumber>0</GroupNumber>
                <Master>False</Master>
                <ProductKey>0</ProductKey>
                <Responder>True</Responder
                ><Interface>Serial</Interface>
                <Port>/dev/ttyUSB0</Port>
                <BaudRate>19200</BaudRate>
                <ByteSize>8</ByteSize>
                <Parity>N</Parity>
                <StopBits>1.0</StopBits>
                <Timeout>1.0</Timeout>
                <DsrDtr>False</DsrDtr>
                <RtsCts>False</RtsCts>
                <XonXoff>False</XonXoff>
            </Controller>
            <Controller Active="False" Key="2" Name="UPB_PIM">
                <Comment>UPB PIM  using USB connection</Comment>
                <Coords>None</Coords>
                <Dimmable>True</Dimmable>
                <Family>UPB</Family>
                <Room>Master Bath</Room>
                <Type>Controller</Type>
                <UUID>ec9bc470-89c9-11e3-8f15-082e5f8cdfd2</UUID>
                <NetworkID>0</NetworkID>
                <Password>0</Password>
                <UnitID>255</UnitID>
                <Interface>USB</Interface>
                <Port>None</Port>
                <Vendor>6109</Vendor>
                <Product>21760</Product>
            </Controller>
        </Controllers>
        <Buttons>
            <Button Active="False" Key="0" Name="kpl_1_A">
                <Comment>KeypadLink Button A</Comment>
                <Coords>None</Coords>
                <Dimmable>False</Dimmable>
                <Family>Insteon</Family>
                <Room>Master Bath</Room>
                <Type>Button</Type>
                <UUID>ec97308f-89c9-11e3-a78b-082e5f8cdfd2</UUID>
                <Address>16.E5.B6</Address>
                <Controller>True</Controller>
                <DevCat>0x0</DevCat>
                <GroupList>All_Lights|MasterBedroom(0;0)</GroupList>
                <GroupNumber>1</GroupNumber>
                <Master>0</Master>
                <ProductKey>0</ProductKey>
                <Responder>True</Responder>
            </Button>
            <Button Active="False" Key="1" Name="kpl_1_B">
                <Comment>KeypadLink Button B</Comment>
                <Coords>None</Coords>
                <Dimmable>False</Dimmable>
                <Family>Insteon</Family>
                <Room />
                <Type>Button</Type>
                <UUID>ec97579e-89c9-11e3-832c-082e5f8cdfd2</UUID>
                <Address>16.E5.B6</Address>
                <Controller>True</Controller>
                <DevCat>0</DevCat>
                <GroupList>All_Buttons</GroupList>
                <GroupNumber>2</GroupNumber>
                <Master>False</Master>
                <ProductKey>0</ProductKey>
                <Responder>True</Responder>
            </Button>
        </Buttons>
        <Schedules>
            <Schedule Active="True" Key="0" Name="Evening">
                <Level>100</Level>
                <LightName>lr_cans</LightName>
                <LightNumber>10</LightNumber>
                <Rate>0</Rate>
                <RoomName>Living Room</RoomName>
                <Time>sunset - 00:06</Time>
                <Type>Device</Type>
                <UUID>ec95d100-89c9-11e3-90cb-082e5f8cdfd2</UUID>
            </Schedule>
            <Schedule Active="True" Key="1" Name="Evening">
                <Level>100</Level>
                <LightName>lr_rope</LightName>
                <LightNumber>7</LightNumber>
                <Rate>0</Rate>
                <RoomName>Living Room</RoomName>
                <Time>sunset - 00:08</Time>
                <Type>Device</Type>
                <UUID>ec95d101-89c9-11e3-bb08-082e5f8cdfd2</UUID>
            </Schedule>
            <Schedule Active="True" Key="2" Name="Evening">
                <Level>100</Level><LightName>outside_gar</LightName><LightNumber>1</LightNumber>
                <Rate>0</Rate><RoomName>Garage</RoomName><Time>sunset - 00:02</Time>
                <Type>Device</Type><UUID>ec95d102-89c9-11e3-abe6-082e5f8cdfd2</UUID>
            </Schedule>
            <Schedule Active="True" Key="3" Name="Evening">
                <Level>100</Level><LightName>outside_front</LightName>
                <LightNumber>0</LightNumber><Rate>0</Rate><RoomName>Foyer</RoomName>
                <Time>sunset</Time><Type>Device</Type>
                <UUID>ec95d103-89c9-11e3-8567-082e5f8cdfd2</UUID>
            </Schedule>
            <Schedule Active="True" Key="4" Name="Evening">
            <Level>100</Level><LightName>wet_bar</LightName><LightNumber>8</LightNumber>
                <Rate>0</Rate><RoomName>Living Room</RoomName>
                <Time>sunset - 00:04</Time><Type>Device</Type>
                <UUID>ec95d104-89c9-11e3-b921-082e5f8cdfd2</UUID>
            </Schedule>
            <Schedule Active="False" Key="5" Name="Night xxx">
                <Level>60</Level>
                <LightName>mbr_rope</LightName><LightNumber>6</LightNumber>
                <Rate>0</Rate><RoomName>Master Bedroom</RoomName>
                <Time>22:00</Time><Type>Device</Type>
                <UUID>ec95d105-89c9-11e3-8b11-082e5f8cdfd2</UUID>
            </Schedule>
            <Schedule Active="True" Key="6" Name="Night">
                <Level>0</Level><LightName>outside_gar</LightName>
                <LightNumber>1</LightNumber>
                <Rate>0</Rate><RoomName>Garage</RoomName><Time>23:00</Time>
                <Type>Device</Type><UUID>ec95f811-89c9-11e3-a802-082e5f8cdfd2</UUID>
            </Schedule>
            <Schedule Active="True" Key="7" Name="Night">
                <Level>0</Level><LightName>outside_front</LightName><LightNumber>0</LightNumber>
                <Rate>0</Rate><RoomName>Foyer</RoomName><Time>23:00</Time>
                <Type>Device</Type><UUID>ec95f812-89c9-11e3-931a-082e5f8cdfd2</UUID>
            </Schedule>
            <Schedule Active="True" Key="8" Name="Evening">
                <Level>60</Level><LightName>mbr_rope</LightName>
                <LightNumber>6</LightNumber><Rate>0</Rate><RoomName>Master Bedroom</RoomName>
                <Time>22:10</Time><Type>Device</Type><UUID>ec95f813-89c9-11e3-a132-082e5f8cdfd2</UUID>
            </Schedule>
            <Schedule Active="True" Key="9" Name="Night">
                <Level>0</Level><LightName>lr_rope</LightName><LightNumber>7</LightNumber>
                <Rate>0</Rate><RoomName>Living Room</RoomName>
                <Time>23:30</Time>
                <Type>Device</Type><UUID>ec95f814-89c9-11e3-91e0-082e5f8cdfd2</UUID>
            </Schedule>
            <Schedule Active="True" Key="10" Name="Night">
                <Level>0</Level><LightName>lr_cans</LightName>
                <LightNumber>10</LightNumber><Rate>0</Rate><RoomName>Living Room</RoomName>
                <Time>23:31</Time><Type>Device</Type><UUID>ec95f815-89c9-11e3-b6de-082e5f8cdfd2</UUID>
            </Schedule>
            <Schedule Active="True" Key="11" Name="Night">
                <Level>0</Level><LightName>wet_bar</LightName><LightNumber>8</LightNumber>
                <Rate>0</Rate><RoomName>Living Room</RoomName><Time>00:15</Time>
                <Type>Device</Type><UUID>ec95f816-89c9-11e3-b338-082e5f8cdfd2</UUID>
            </Schedule>
            <Schedule Active="True" Key="12" Name="Morning">
                <Level>0</Level><LightName>mbr_rope</LightName>
                <LightNumber>6</LightNumber><Rate>0</Rate>
                <RoomName>Master Bedroom</RoomName>
                <Time>sunrise + 00:30</Time><Type>Device</Type>
                <UUID>ec95f817-89c9-11e3-9bc6-082e5f8cdfd2</UUID>
            </Schedule>
            <Schedule Active="False" Key="13" Name="Testing">
                <Level>100</Level><LightName>lr_rope</LightName><LightNumber>7</LightNumber>
                <Rate>0</Rate><RoomName>Office</RoomName><Time>10:06</Time>
                <Type>Device</Type><UUID>ec961f21-89c9-11e3-a428-082e5f8cdfd2</UUID>
            </Schedule>
            <Schedule Active="False" Key="14" Name="Testing">
                <Level>0</Level>
                <LightName>lr_rope</LightName><LightNumber>7</LightNumber><Rate>0</Rate><RoomName>Office</RoomName>
                <Time>10:31</Time><Type>Device</Type><UUID>ec961f22-89c9-11e3-a510-082e5f8cdfd2</UUID>
            </Schedule>
            <Schedule Active="False" Key="15" Name="Testing">
                <Level>0</Level><LightName>test_lamp1</LightName><LightNumber>9</LightNumber><Rate>0</Rate>
                <RoomName>Breakfast Nook</RoomName><Time>10:24</Time>
                <Type>Device</Type><UUID>ec961f23-89c9-11e3-af9e-082e5f8cdfd2</UUID>
            </Schedule>
            <Schedule Active="False" Key="16" Name="Testing">
                <Level>0</Level><LightName>kitchen_counter</LightName>
                <LightNumber>11</LightNumber><Rate>0</Rate>
                <RoomName>Kitchen</RoomName>
                <Time>21:56</Time><Type>Device</Type><UUID>ec961f24-89c9-11e3-ae3a-082e5f8cdfd2</UUID>
            </Schedule>
        </Schedules>
        <Hvac>
            <Thermostats>
                <Thermostat Name="Test Thermostat 1" Active="True" Key="0">
                </Thermostat>
                <Thermostat Name="Test 2 Thermostat" Active="True" Key="1">
                </Thermostat>
           </Thermostats>
        </Hvac>
        <Pools>
            <Pool Name="Main Pool" Active="True" Key="0">
            </Pool>
            <Pool Name="Hot Tub" Active="True" Key="1">
            </Pool>
        </Pools>
        <Internet ExternalDelay="28800" ExternalIP="None" ExternalUrl="http://snar.co/ip">
            <DynamicDNS Active="True" Key="0" Name="Afraid">
                <Interval>21600</Interval>
                <Url>http://freedns.afraid.org/dynamic/update.php?VDZtSkE2MzFVMVVBQVd5QXg2MDo5MjU1MzYw</Url>
            </DynamicDNS>
        </Internet>
    </HouseDivision>

</PyHouse>
"""



XML_SHORT = """
<PyHouse Version='2'>
    <Web>
    </Web>
    <Nodes>
        <Node Name='PiNode-1' Key='0' Active='True'>
            <UUID>ec955bcf-89c9-11e3-b583-082e5f8cdfd2</UUID>
        </Node>
    </Nodes>
    <Houses>
        <House Name='House_1' Key='0' Active='True'>
            <Controllers>
                <Controller Name='Serial_1' Key='0' Active='True'>
                    <Interface>Serial</Interface>
                    <BaudRate>19200</BaudRate>
                    <ByteSize>8</ByteSize>
                    <DsrDtr>False</DsrDtr>
                    <Parity>N</Parity>
                    <RtsCts>False</RtsCts>
                    <StopBits>1.0</StopBits>
                    <Timeout>0</Timeout>
                    <XonXoff>False</XonXoff>
                </Controller>
                <Controller Name='USB_1' Key='1' Active='True'>
                    <Interface>USB</Interface>
                    <Vendor>12345</Vendor>
                    <Product>9876</Product>
                </Controller>
            </Controllers>
        </House>
    </Houses>
</PyHouse>
"""

# ## END DBK
