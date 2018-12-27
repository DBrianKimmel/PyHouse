* Name:      PyHouse/Project/src/Modules/Computer/Mqtt/Docs/README.md
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2018 by D. Brian Kimmel
* Created:   2018-10-01
* Updated:   2018-10-01
* License:   MIT License
* Summary:   This is the design documentation for the Mqtt Module of PyHouse.


# MQTT

## Design

This Mqtt module is accessed by every other module.

The API is setup from the computer module.
It initialized as the first thing in the computer setup so it can be called to post and decode messages early on.


### Topic

The topics all start out with pyhouse
==>pyhouse

The next section is the house name.
House names must be unique within the realm that the broker and backup brokers serve.
==>pyhouse/housename

The next section is the message category.
==>pyhouse/housename/lighting

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


### Payload

The playload is structured to carry the information


### END DBK
