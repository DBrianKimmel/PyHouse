* Name:      PyHouse/Project/src/Modules/Computer/Mqtt/Docs/README.md
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2018 by D. Brian Kimmel
* Created:   2018-10-01
* Updated:   2019-09-24
* License:   MIT License
* Summary:   This is the design documentation for the Mqtt Module of PyHouse.

# MQTT

Mqtt is a messaging system that is used within PyHouse

## Broker

This module connects to a MQTT broker using the 3.1.1 protocol.
The client name must start with 'PyH-'.
It uses straight TCP and will someday allow TLS.

## Design

This Mqtt module is accessed by every other module.

The API is setup from the computer module.
It initialized as the first thing in the computer setup so it can be called to post and decode messages early on.

## Message

Mqtt messages consist of a Topic and a Payload.

### Topic

1. The topics all start out with "pyhouse".

==> pyhouse/

2. The next section is the house name.
House names must be unique within the realm that the broker and backup brokers serve.
House names may include spacesand should be capitalized such as "ManorHouse".

==> pyhouse/ManorHouse/

3. The next section is the message type.

==> pyhouse/ManorHouse/type/

Types:
- computer
- house

4. The next section is the message category and possibly subcategories.

==> pyhouse/ManorHouse/type/category/

Categories:
- entertainment
- hvac
- irrigation
- lighting
- pool
- room
- rule
- schedule
- security

4. The next section is the action field.

==> pyhouse/ManorHouse/house/lighting/action

Actions:
- status
- control
- add
- delete
- update
- request
- trigger

Status and control are command and response operation actions.
Status usually occurs when some external device changes state.
Control us used when this node wants to change the state of an external device.

Add, delete, update and request are maintenance actions.
They are meant to keep all the PyHouse nodes synchronized.
They may happen when a node restarts and once a day during normal operations.
Add and delete are used when ???

Trigger is a notification action telling all other PyHouse computers something that may require action on their part has happened.


### Payload

The playload is structured to carry the information


## Dispatch

# References

[Certificates](http://www.steves-internet-guide.com/mosquitto-tls/)

### END DBK
