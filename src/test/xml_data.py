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
        <InternetSection>
            <Internet Name="Connection-1" Key="0" Active="True">
                <UUID>1234</UUID>
                <ExternalUrl>http://snar.co/ip</ExternalUrl>
                <ExternalDelay>28800</ExternalDelay>
                <ExternalIP>65.35.48.61</ExternalIP>
                <DynamicDnsSection>
                    <DynamicDNS Active="True" Key="0" Name="Afraid">
                        <UUID>6543</UUID>
                        <UpdateUrl>http://freedns.afraid.org/dynamic/update.php?VDZtSkE2MzFVMVVBQVd5QXg2MDo5MjU1MzYw</UpdateUrl>
                        <UpdateInterval>21600</UpdateInterval>
                    </DynamicDNS>
                </DynamicDnsSection>
            </Internet>
        </InternetSection>

<!-- Tested to here -->

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

    <HouseDivision Active="True" Key="0" Name="Pink Poppy">
        <UUID>12345678-1002-11e3-b583-333e5f8cdfd2</UUID>
        <LocationSection>
            <Street>5191 N Pink Poppy Dr</Street><City>Beverly Hills</City><State>Florida</State><ZipCode>34465</ZipCode><Phone>(352) 270-8096</Phone>
            <Latitude>28.938448</Latitude><Longitude>-82.517208</Longitude><TimeZone>-240.0</TimeZone><SavingTime>60.0</SavingTime>
        </LocationSection>
        <RoomSection>
            <Room Active="True" Key="0" Name="Master Bath">
                <Comment>Test Comment</Comment>
                <Corner>0.50, 10.50</Corner>
                <Size>14.00, 13.50</Size>
            </Room>
            <Room Active="True" Key="1" Name="Master Bed Closet 1">
                <Comment />
                <Corner>0.83, 24.58</Corner>
                <Size>6.91, 8.91</Size>
            </Room>
            <Room Active="False" Key="2" Name="Master Bedroom">
                <Comment />
                <Corner>0.83, 25.08</Corner>
                <Size>14.00, 18.00</Size>
            </Room>
            <Room Active="False" Key="3" Name="Master Sitting Room">
                <Comment />
                <Corner>0.83, 54.16</Corner>
                <Size>14.00, 8.00</Size>
            </Room>
        </RoomSection>
        <ScheduleSection>
            <Schedule Active="True" Key="0" Name="Evening">
                <Level>100</Level>
                <LightName>lr_cans</LightName>
                <Rate>0</Rate>
                <RoomName>Living Room</RoomName>
                <Time>sunset - 00:06</Time>
                <ScheduleType>LightingDevice</ScheduleType>
            </Schedule>
            <Schedule Active="True" Key="1" Name="Evening">
                <Level>100</Level>
                <LightName>lr_rope</LightName>
                <LightNumber>7</LightNumber>
                <Rate>0</Rate>
                <RoomName>Living Room</RoomName>
                <Time>sunset - 00:08</Time>
                <ScheduleType>LightingDevice</ScheduleType>
            </Schedule>
            <Schedule Active="True" Key="2" Name="Evening">
                <Level>100</Level><LightName>outside_gar</LightName><LightNumber>1</LightNumber><Rate>0</Rate><RoomName>Garage</RoomName>
                <Time>sunset - 00:02</Time>
                <ScheduleType>LightingDevice</ScheduleType>
            </Schedule>
            <Schedule Active="True" Key="3" Name="Evening">
                <Level>100</Level><LightName>outside_front</LightName>
                <LightNumber>0</LightNumber><Rate>0</Rate><RoomName>Foyer</RoomName><Time>sunset</Time>
                <ScheduleType>LightingDevice</ScheduleType>
            </Schedule>
            <Schedule Active="True" Key="4" Name="Evening">
                <Level>100</Level>
                <LightName>wet_bar</LightName>
                <LightNumber>8</LightNumber>
                <Rate>0</Rate>
                <RoomName>Living Room</RoomName>
                <Time>sunset - 00:04</Time>
                <ScheduleType>LightingDevice</ScheduleType>
            </Schedule>
            <Schedule Active="False" Key="5" Name="Night xxx">
                <Level>60</Level><LightName>mbr_rope</LightName>
                <LightNumber>6</LightNumber><Rate>0</Rate><RoomName>Master Bedroom</RoomName>
                <Time>22:00</Time>
                <ScheduleType>LightingDevice</ScheduleType>
            </Schedule>
            <Schedule Active="True" Key="6" Name="Night">
                <Level>0</Level>
                <LightName>outside_gar</LightName>
                <LightNumber>1</LightNumber>
                <Rate>0</Rate>
                <RoomName>Garage</RoomName>
                <Time>23:00</Time>
                <ScheduleType>LightingDevice</ScheduleType>
            </Schedule>
        </ScheduleSection>
        <LightSection>
            <Light Active="True" Key="0" Name="outside_front">
                <Comment>SwitchLink On/Off</Comment>
                <Coords>['0', '0']</Coords>
                <IsDimmable>False</IsDimmable>
                <ControllerFamily>Insteon</ControllerFamily>
                <RoomName>Foyer</RoomName>
                <LightingType>Light</LightingType>
                <Address>16.62.2D</Address>
                <IsController>True</IsController>
                <DevCat>02.0A</DevCat>
                <GroupList>All_Lights|Outside|Foyer(0;0)</GroupList>
                <GroupNumber>0</GroupNumber>
                <IsMaster>True</IsMaster>
                <ProductKey>30.1A.35</ProductKey>
                <IsResponder>True</IsResponder>
                <CurLevel>73</CurLevel>
            </Light>
            <Light Active="True" Key="1" Name="outside_gar">
                <Comment>SwitchLink On/Off</Comment><Coords>['0', '0']</Coords>
                <IsDimmable>False</IsDimmable><ControllerFamily>Insteon</ControllerFamily>
                <RoomName>Garage</RoomName><LightingType>Light</LightingType><Address>17.47.A1</Address>
                <IsController>True</IsController><DevCat>0x0</DevCat><GroupList>All_Lights|Outside|Garage(0;0)</GroupList>
                <GroupNumber>0</GroupNumber>
                <IsMaster>True</IsMaster>
                <ProductKey>0</ProductKey><IsResponder>True</IsResponder>
            </Light>
            <Light Active="True" Key="2" Name="dr_chand">
                <Comment>SwitchLink dimmer</Comment><Coords>['0', '0']</Coords>
                <IsDimmable>True</IsDimmable><ControllerFamily>Insteon</ControllerFamily>
                <RoomName>Dining Room</RoomName><LightingType>Light</LightingType><Address>16.C9.37</Address>
                <IsController>True</IsController><DevCat>0</DevCat><GroupList>All_Lights|DiningRoom(12;12)</GroupList>
                <GroupNumber>0</GroupNumber>
                <IsMaster>True</IsMaster>
                <ProductKey>F4.20.20</ProductKey>
                <IsResponder>True</IsResponder></Light>
            <Light Active="True" Key="3" Name="dr_chand_slave">
                <Comment>SwitchLink dimmer</Comment>
                <Coords>['0', '0']</Coords>
                <IsDimmable>True</IsDimmable>
                <ControllerFamily>Insteon</ControllerFamily>
                <RoomName>Dining Room</RoomName>
                <LightingType>Light</LightingType>
                <Address>16.C9.D0</Address>
                <IsController>True</IsController>
                <DevCat>8007</DevCat>
                <GroupList>All_Lights|Pantry(0;0)</GroupList>
                <GroupNumber>0</GroupNumber>
                <IsMaster>False</IsMaster>
                <ProductKey>EB.2A.A8</ProductKey>
                <IsResponder>True</IsResponder>
            </Light>
            <Light Active="True" Key="4" Name="nook_chand">
                <Comment>SwitchLink dimmer</Comment>
                <Coords>['0', '0']</Coords>
                <IsDimmable>True</IsDimmable>
                <ControllerFamily>Insteon</ControllerFamily>
                <RoomName>Breakfast Nook</RoomName>
                <LightingType>Light</LightingType>
                <Address>17.C2.72</Address>
                <IsController>True</IsController>
                <DevCat>0xc44</DevCat>
                <GroupList>All_Lights|Pantry(0;0)</GroupList>
                <GroupNumber>0</GroupNumber>
                <IsMaster>True</IsMaster>
                <ProductKey>0</ProductKey>
                <IsResponder>True</IsResponder>
            </Light>
        </LightSection>
        <ButtonSection>
            <Button Active="False" Key="0" Name="kpl_1_A">
                <Comment>KeypadLink Button A</Comment>
                <Coords />
                <IsDimmable>False</IsDimmable>
                <ControllerFamily>Insteon</ControllerFamily>
                <RoomName>Master Bath</RoomName>
                <LightingType>Button</LightingType>
                <Address>16.E5.B6</Address>
                <IsController>True</IsController>
                <DevCat>0x0</DevCat>
                <GroupList>All_Lights|MasterBedroom(0;0)</GroupList>
                <GroupNumber>1</GroupNumber>
                <IsMaster>True</IsMaster>
                <ProductKey>0</ProductKey>
                <IsResponder>True</IsResponder>
            </Button>
            <Button Active="False" Key="1" Name="kpl_1_B">
                <Comment>KeypadLink Button B</Comment>
                <Coords />
                <IsDimmable>False</IsDimmable>
                <ControllerFamily>Insteon</ControllerFamily>
                <Room />
                <LightingType>Button</LightingType>
                <Address>16.E5.B6</Address>
                <IsController>True</IsController>
                <DevCat>0</DevCat>
                <GroupList>All_Buttons</GroupList>
                <GroupNumber>2</GroupNumber>
                <IsMaster>False</IsMaster>
                <ProductKey>0</ProductKey>
                <IsResponder>True</IsResponder>
            </Button>
            <Button Active="False" Key="2" Name="kpl_1_C">
                <Comment>KeypadLink Button C</Comment>
                <Coords />
                <IsDimmable>False</IsDimmable>
                <ControllerFamily>Insteon</ControllerFamily>
                <Room />
                <LightingType>Button</LightingType>
                <Address>16.E5.B6</Address>
                <IsController>True</IsController>
                <DevCat>0</DevCat>
                <GroupList>All_Buttons</GroupList>
                <GroupNumber>3</GroupNumber>
                <IsMaster>False</IsMaster>
                <ProductKey>0</ProductKey>
                <IsResponder>True</IsResponder>
            </Button>
            <Button Active="False" Key="3" Name="kpl_1_D">
                <Comment>KeypadLink Button D</Comment>
                <Coords />
                <IsDimmable>False</IsDimmable>
                <ControllerFamily>Insteon</ControllerFamily>
                <Room />
                <LightingType>Button</LightingType>
                <Address>16.E5.B6</Address>
                <IsController>True</IsController>
                <DevCat>0</DevCat><GroupList>All_Buttons</GroupList><GroupNumber>4</GroupNumber>
                <IsMaster>False</IsMaster>
                <ProductKey>0</ProductKey>
                <IsResponder>True</IsResponder>
            </Button>
        </ButtonSection>
        <ControllerSection>
            <Controller Active="False" Key="0" Name="PLM_1">
                <Comment>Dongle using serial converter 067B:2303</Comment>
                <Coords />
                <IsDimmable>False</IsDimmable>
                <ControllerFamily>Insteon</ControllerFamily>
                <RoomName>Office</RoomName>
                <LightingType>Controller</LightingType>
                <Address>AA.AA.AA</Address>
                <IsController>True</IsController>
                <DevCat>0x0</DevCat><GroupList />
                <GroupNumber>0</GroupNumber>
                <IsMaster>False</IsMaster>
                <ProductKey>0</ProductKey>
                <IsResponder>True</IsResponder>
                <InterfaceType>Serial</InterfaceType>
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
            <Controller Active="True" Key="1" Name="PowerLink">
                <Comment>2413UH Powerlink Controller</Comment>
                <Coords />
                <IsDimmable>False</IsDimmable>
                <ControllerFamily>Insteon</ControllerFamily>
                <RoomName>Office</RoomName>
                <LightingType>Controller</LightingType>
                <Address>17.03.B2</Address>
                <IsController>True</IsController>
                <DevCat>0x0</DevCat>
                <GroupList />
                <GroupNumber>0</GroupNumber>
                <IsMaster>False</IsMaster>
                <ProductKey>0</ProductKey>
                <IsResponder>True</IsResponder>
                <InterfaceType>Serial</InterfaceType>
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
                <Coords />
                <IsDimmable>False</IsDimmable>
                <ControllerFamily>UPB</ControllerFamily>
                <RoomName>Master Bath</RoomName>
                <LightingType>Controller</LightingType>
                <UPBNetworkID>6</UPBNetworkID>
                <UPBPassword>1253</UPBPassword>
                <UPBAddress>255</UPBAddress>
                <InterfaceType>USB</InterfaceType>
                <Port>None</Port>
                <Vendor>6109</Vendor>
                <Product>21760</Product>
            </Controller>
        </ControllerSection>
        <ThermostatSection>
            <Thermostat Name='Test Thermostat One' Active='True' Key='0'>
                <ControllerFamily>Insteon</ControllerFamily>
                <CoolSetPoint>78.0</CoolSetPoint>
                <CurrentTemperature>76</CurrentTemperature>
                <HeatSetPoint>71.0</HeatSetPoint>
                <ThermostatMode>Cool</ThermostatMode>
                <ThermostatScale>F</ThermostatScale>
                <Address>18.C9.4A</Address>
            </Thermostat>
        </ThermostatSection>
        <EntertainmentSection />
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
                    <InterfaceType>Serial</InterfaceType>
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
                    <InterfaceType>USB</InterfaceType>
                    <Vendor>12345</Vendor>
                    <Product>9876</Product>
                </Controller>
            </Controllers>
        </House>
    </Houses>
</PyHouse>
"""

# ## END DBK
