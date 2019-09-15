* Name:      PyHouse/Project/_Docs/Design.md
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2018 by D. Brian Kimmel
* Created:   2018-10-11
* Updated:   2018-10-11
* License:   MIT License
* Summary:   This is the design documentation of PyHouse.

# Project

This is the top level design of the PyHouse Project.

See PyHouse/Project/src/_Docs/Design.md 

This is the top design document for the PyHouse project.

# PyHouse

The PyHouse system requires several Raspberry Pi Computers called 'Nodes'.

## House server
The first of these nodes is the house server.
It would be wise to have a backup house server if at all possible.

The house server runs several critical services to enable PyHouse to be self sufficient.

### Mqtt Broker
The house server runs mosquitto Mqtt broker.

### DNS
The house server runs a dns service for the house.

### DDNS Updater
```bash
sudo apt install ddclient
```

### IPV6 Tunnel

### VPN

### VNC



## Lighting Controller

## Pandora Controller

## Node red servers



# Installation

See Install.md in this directory.



### END DBK
