* Name:      PyHouse/Project/src/Modules/Housing/Lighting/Docs/Design
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2018 by D. Brian Kimmel
* Created:   2018-10-16
* Updated:   2018-10-16
* License:   MIT License
* Summary:   This is the design documentation for the Lighting Module of PyHouse.


# Lighting

Lighting was the first piece of PyHouse.

Turn on the Kithen Ceiling lights.
Turn off the Bedroom Ceiling lights.
Turn on the Outside lights.

## Lighting

Since I started using Insteon, the lighting module became 3 sub modules:
* Controllers
* Lights & Outlets
* Buttons

### Common

Common to Buttons, Controllers, Lights&Outlets.

```python
BaseObject():
        Name - The name the device is called.
        Key - 0
        Active - True/False
        Comment - A description of the device.
        LastUpdate - Date and time last changed
BaseUUIDObject(BaseObject):
        UUID - None
DeviceInformation(BaseUUIDObject):
        DeviceFamily - Insteon, Hue, ...
        DeviceType - 0 = Controllers, 1 = Lighting, 2 = HVAC, 3 = Security, 4 = Bridge
        DeviceSubType - 0
        RoomCoords - None  # CoordinateInformation()
        RoomName - The name of the room where the device is located.
        RoomUUID - None
CoreLightingData(DeviceInformation):
        Lighting Type = ''  # VALID_LIGHTING_TYPE = Button | Controller | Light
```


### Controllers

There are two different concepts called controllers.

The first is a device, connected to a computer, that sends commands from the computer to the device.
Insteon, UPB and X10 all have these controllers.  Other families may also have them also.
They connect to a serial port or a USB port on the computer side.

The second concept is a switch that 'controls' a responder.
A 'slave' switch, in a n-way group of switches, is the controller of the 'master' switch (which is wired to the fixture).
The 'master' switch responds to the 'controller' to send power to the fixture.

```python
BaseObject():
        Name = 'undefined baseobject'
        Key = 0
        Active = False
        Comment = ''
        LastUpdate = None
BaseUUIDObject(BaseObject):
        UUID = None
DeviceInformation(BaseUUIDObject):
        DeviceFamily = 'Null'
        DeviceType = 0  # 0 = Controllers, 1 = Lighting, 2 = HVAC, 3 = Security, 4 = Bridge
        DeviceSubType = 0
        RoomCoords = None  # CoordinateInformation()
        RoomName = ''
        RoomUUID = None
CoreLightingData(DeviceInformation):
        # Lighting Type = ''  # VALID_LIGHTING_TYPE = Button | Light | Controller
ControllerInformation(CoreLightingData):
        InterfaceType = ''  # Serial | USB | Ethernet
        LasuUsed = None  # Date time of successful start
        Node = None  # node the controller is connected to
        Port = ''
        Ret = None  # Return Code
        #  The following are not in XML config file
        self._isFunctional = True  # if controller is not working currently
        self._HandlerAPI = None  # PLM, PIM, etc (family controller device handler) API() address
        self._Data = bytearray()  # Rx InterfaceType specific data
        self._Message = bytearray()
        self._Queue = None
```
```
<Controller Active="False" Key="0" Name="PLM_1">
	<Comment>None</Comment>
	<LastUpdate>2019-05-12 12:25:34.277753</LastUpdate>
	<UUID>c1490758-092e-11e4-bffa-b827eb189eb4</UUID>
	<DeviceType>1</DeviceType>
	<DeviceSubType>2</DeviceSubType>
	<Interface>
		<Type>Serial</Type>
		<Port>/dev/ttyUSB0</Port>
		<Serial>
			<BaudRate>19200</BaudRate>
			<ByteSize>8</ByteSize>
			<DsrDtr>False</DsrDtr>
			<Parity>N</Parity>
			<RtsCts>False</RtsCts>
			<StopBits>1.0</StopBits>
			<Timeout>1.0</Timeout>
			<XonXoff>False</XonXoff>
		</Serial>
	<Family>
		<Name>Insteon</Name>
		<DevCat>01.20</DevCat>
		<EngineVersion>0</EngineVersion>
		<FirmwareVersion>0</FirmwareVersion>
		<GroupList>None</GroupList>
		<GroupNumber>0</GroupNumber>
		<InsteonAddress>AA.AA.AA</InsteonAddress>
		<ProductKey>00.00.00</ProductKey>
	</Family>
	<Room>
		<RoomCoords>[0.0,0.0,0.0]</RoomCoords>
		<RoomName>12</RoomName>
		<RoomUUID>c894ef92-b1e5-11e6-8a14-74da3859e09a</RoomUUID>
	</Room>
</Controller>
```

### Switch

This includes wall switches, Outdoor switches and outlet switches.

```python
class BaseObject(object):
        self.Name = 'undefined baseobject'
        self.Key = 0
        self.Active = False
        self.Comment = ''
        self.LastUpdate = None
class BaseUUIDObject(BaseObject):
        self.UUID = None
class DeviceInformation(BaseUUIDObject):
        self.DeviceFamily = 'Null'
        self.DeviceType = 0  # 0 = Controllers, 1 = Lighting, 2 = HVAC, 3 = Security, 4 = Bridge
        self.DeviceSubType = 0
        self.RoomCoords = None  # CoordinateInformation()
        self.RoomName = ''
        self.RoomUUID = None
```

### Buttons


### END DBK
