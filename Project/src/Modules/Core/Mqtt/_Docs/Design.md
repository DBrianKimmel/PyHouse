* Name:      PyHouse/Project/src/Modules/Computer/Mqtt/Docs/README.md
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2018 by D. Brian Kimmel
* Created:   2018-10-01
* Updated:   2019-04-04
* License:   MIT License
* Summary:   This is the design documentation for the Mqtt Module of PyHouse.

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

## Broker

This module connects to a MQTT broker using the 3.1.1 protocol.
The client name must start with 'PyH-'.
It uses straight TCP and will soon allow TLS.

## Design

This Mqtt module is accessed by every other module.

The API is setup from the computer module.
It initialized as the first thing in the computer setup so it can be called to post and decode messages early on.

### Topic

1. The topics all start out with pyhouse

==>pyhouse

1. The next section is the house name.
House names must be unique within the realm that the broker and backup brokers serve.
House names may include spaces

==>pyhouse/housename

The next section is the message category.

==>pyhouse/housename/category

Categories:
- computer
- entertainment
- hvac
- irrigation
- lighting
- pool
- room
- rule
- schedule
- security

The next section is the action field.

==>pyhouse/housename/lighting/action

Actions:
- status
- control
- delete
- add
- synchronize


### Payload

The playload is structured to carry the information

# References

[Certificates](http://www.steves-internet-guide.com/mosquitto-tls/)

### END DBK
