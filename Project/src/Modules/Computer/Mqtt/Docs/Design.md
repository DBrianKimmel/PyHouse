* Name:      PyHouse/Project/src/Modules/Computer/Mqtt/Docs/Design.md
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2019-2019 by D. Brian Kimmel
* Created:   2019-05-15
* Updated:   2019-05-23
* License:   MIT License
* Summary:   This is the design documentation for the Mqtt section of PyHouse.


# MQTT

Mqtt is a messaging system that is used within PyHouse

There are several general and nearly universal topic endings that are in use.
* /status
* /control
* /delete
* /update
* /trigger

```xml
<?xml version="1.0" ?>
<MqttSection>
	<Broker Active="True" Key="0" Name="CannonTrail">
		<UUID>Broker..-0000-0000-0000-0123456789ab</UUID>
		<BrokerHost>Mqtt-Ct</BrokerHost>
		<BrokerAddress>192.168.9.10</BrokerAddress>
		<BrokerPort>8883</BrokerPort>
		<BrokerUser>pyhouse</BrokerUser>
		<BrokerPassword>ChangeMe</BrokerPassword>
		<Class>Local</Class>
	</Broker>
	<Broker Active="True" Key="1" Name="PinkPoppy">
		<UUID>Broker..-0001-0001-0001-0123456789ab</UUID>
		<BrokerHost>Mqtt-pp</BrokerHost>
		<BrokerAddress>192.168.1.10</BrokerAddress>
		<BrokerPort>1883</BrokerPort>
		<BrokerUser>pyhouse</BrokerUser>
		<BrokerPassword>ChangeMe</BrokerPassword>
		<Class>Local</Class>
	</Broker>
</MqttSection>
```

### END DBK
