* Name:      PyHouse/Project/src/Modules/Housing/Entertainment/pioneer/Docs/Design
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2018 by D. Brian Kimmel
* Created:   2018-09-30
* Updated:   2018-10-10
* License:   MIT License
* Summary:   This is the design documentation for the Pioneer Module of PyHouse.


# Pioneer


## Design

The pioneer module (so far) is kind of a passive module.
It gets set up when the XML defines one or more Pioneer devices.

Then it sends out a Mqtt status message declaring the status when first connected to.]
It then waits for a control message.
Control messages can come from services sch as Pandora, or from a Node-Red dashboard triggering something.

The pioneer device I have does not wake up from a TCP connection.
Only one telnet session is allowed at any time.
Therefore, the telnet session will be released after three minutes of inactivity.

There is the possibility of having more than one pioneer devices in a house.
The name of the devide is used for the key.
Be sure to configure the name to be unique and reference the name in the services.


## XML / Config

```python
<PioneerSection Active="True">
	<Type>Component</Type>
	<Device Active="True" Key="0" Name="822-k">
		<Comment>X-822-K Receiver</Comment>
		<UUID>dc575f69-85ee-11e8-8a4d-a08cfd2fc483</UUID>
		<CommandSet>2015</CommandSet>
		<IPv4>192.168.9.121</IPv4>
		<Port>8102</Port>
		<Room>Living Room</Room>
		<Type>Receiver</Type>
	</Device>
</PioneerSection>
```

* CommandSet
   Which command set the device is using
* IPv4
* Port
* Room
* Type


## Messages

### Control



### Status


### END DBK
