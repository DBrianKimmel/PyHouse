* Name:      PyHouse/Project/src/Modules/Housing/Entertainment/Docs/Design
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2018 by D. Brian Kimmel
* Created:   2018-09-30
* Updated:   2019-04-01
* License:   MIT License
* Summary:   This is the design documentation for the Entertainment Module of PyHouse.


# Entertainment


## Design

In order to preserve the XML, the entire entertainment section is loaded.
Only the active subsections have their modules loaded.

In a running instance of PyHouse only the sub-modules that are defined as active in the config file are loaded.
This makes it sort of a plugin system.
This lowers the memory footprint of the system, since there are a lot of different entertainment device modules,
this will be a big savings of memory.

This module is MQTT message driven.
A Mqtt message is sent to entertainment.py and it dispatches it to the appropriate module.
These messages have topics that begin with:

The modules may return a status message, control other submodules or ...


### Mqtt Messages

Mqtt messages have the topic:

```
		pyhouse/<house name>/entertainment/<device-or-service>/<action>
```

where <device-or-service> is one of the active submodules.


```python
===== _Connector ===== <class 'twisted.internet.tcp.Connector'>
Obj:_addressType            <class 'twisted.internet.address.IPv4Address'> .
Obj:_makeTransport          <bound method Connector._makeTransport of <twisted.internet.tcp.Connector object at 0x7f22669d5048>> .
Obj:bindAddress             None .
Obj:buildProtocol           <bound method BaseConnector.buildProtocol of <twisted.internet.tcp.Connector object at 0x7f22669d5048>> .
Obj:cancelTimeout           <bound method BaseConnector.cancelTimeout of <twisted.internet.tcp.Connector object at 0x7f22669d5048>> .
Obj:connect                 <bound method BaseConnector.connect of <twisted.internet.tcp.Connector object at 0x7f22669d5048>> .
Obj:connectionFailed        <bound method BaseConnector.connectionFailed of <twisted.internet.tcp.Connector object at 0x7f22669d5048>> .
Obj:connectionLost          <bound method BaseConnector.connectionLost of <twisted.internet.tcp.Connector object at 0x7f22669d5048>> .
Obj:disconnect              <bound method BaseConnector.disconnect of <twisted.internet.tcp.Connector object at 0x7f22669d5048>> .
Obj:factory                 <Modules.Housing.Entertainment.pioneer.pioneer.PioneerFactory object at 0x7f226af526d8> .
Obj:factoryStarted          1 .
Obj:getDestination          <bound method Connector.getDestination of <twisted.internet.tcp.Connector object at 0x7f22669d5048>> .
Obj:host                    192.168.9.121 .
Obj:port                    8102 .
Obj:reactor                 <twisted.internet.epollreactor.EPollReactor object at 0x7f226abfde80> .
Obj:state                   connecting .
Obj:stopConnecting          <bound method BaseConnector.stopConnecting of <twisted.internet.tcp.Connector object at 0x7f22669d5048>> .
Obj:timeout                 30 .
Obj:timeoutID               <DelayedCall 0x7f22669d5160 [29.99857497215271s] called=0 cancelled=0 _BaseBaseClient.failIfNotConnected(TimeoutError('',))> .
Obj:transport               <<class 'twisted.internet.tcp.Client'> to ('192.168.9.121', 8102) at 7f22669d50f0> .
```


### EntertainmentDeviceData

```python
super(EntertainmentDeviceData, self).__init__()
self.DeviceCount = 0
self._Factory = None  # The factory pointer for this device of an entertainment sub-section
self._Transport = None
self._Connector = None
```


### EntertainmentDeviceControl

Used to control a device.
All defaults are None - Only fill in what you need so inadvertent controls are not done.


* Channel   =  The channel or frequency (TV, Radio)
* Device    = The name of the device within a family (822-k)
* Direction = None  # F or R  - Foreward, Reverse (think Video play)
* Family    = The device family we are controlling (onkyo, pioneer, ...)
* From      = The node
* HostName  = None  # name of computer holding definitions
* Input     = None  # '01'  # Input ID
* Power     = None  # 'Off'  # On or Off which is standby
* Skip      = Skip the rest of this unit
* Volume    = None  # '0'  # 0-100 - Percent
* Zone      = None  # '1'  # For multi zone output

## XML

```xml
<EntertainmentSection>
    <OnkyoSection Active="True">
        <Type>Component</Type>
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
    <PanasonicSection Active="False">
    </PanasonicSection>
    <PandoraSection Active="True">
        <Type>Service</Type>
        <Device Active="True" Key="0" Name="On pi-06-ct ">
            <Comment>Living Room</Comment>
            <Host>192.168.9.16</Host>
            <Type>Service</Type>
            <ConnectionName>Pioneer</ConnectionName>
            <InputName>CD</InputName>
            <InputCode>01FN</InputCode>
            <Volume>47</Volume>
        </Device>
    </PandoraSection>
    <PioneerSection Active="True">
        <Device Active="True" Key="0" Name="L/R Receiver VSX-822-K">
            <UUID>Pioneer.-0000-0000-0000-0123456789ab</UUID>
            <Comment>VSX-822-K Receiver</Comment>
            <CommandSet>2015</CommandSet>
            <IPv4>192.168.9.121</IPv4>
            <Port>8102</Port>
            <RoomName>Living Room</RoomName>
            <RoomUUID>Room....-0000-0000-0000-0123456789ab</RoomUUID>
            <Status>On</Status>
            <Type>Receiver</Type>
            <Volume>75</Volume>
        </Device>
        <Device Active="True" Key="0" Name="Missing Device">
            <UUID>Pioneer.-0001-0000-0000-0123456789ab</UUID>
            <CommandSet>2015</CommandSet>
            <Comment>VSX-822-K Bogus</Comment>
            <IPv4>192.168.1.122</IPv4>
            <Port>8102</Port>
            <RoomName>Master Bedroom</RoomName>
            <RoomUUID>Room....-0001-0000-0000-0123456789ab</RoomUUID>
            <Type>Fake Receiver</Type>
        </Device>
    </PioneerSection>
    <SamsungSection Active="True">
        <Device Active="True" Key="0" Name="ct - L/R - TV 48abc1234">
            <UUID>Samsung.-0000-0000-0000-0123456789ab</UUID>
            <Comment>48in Smart-Tv  </Comment>
            <Installed>2016-07-29</Installed>
            <IPv4>192.168.9.118</IPv4>
            <Model>UN48J5201AFXZA</Model>
            <Port>55000</Port>
            <RoomName>Living Room</RoomName>
            <RoomUUID>Room....-0000-0000-0000-0123456789ab</RoomUUID>
            <Type>TV</Type>
        </Device>
    </SamsungSection>
</EntertainmentSection>
```

### END DBK
