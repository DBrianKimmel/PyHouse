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

### END DBK
