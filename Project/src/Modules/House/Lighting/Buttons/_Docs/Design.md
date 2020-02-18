* Name:      Modules/House/Lighting/Buttons/_Docs/Design.md
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2020-2020 by D. Brian Kimmel
* Created:   2020-02-05
* Updated:   2020-02-05
* License:   MIT License
* Summary:   This is the design documentation for the Lighting Module of PyHouse.

# Buttons


## Config

```
Buttons:
    - Name: Living Room mini remote
      Comment: For Garage Door Pink Poppy
      Type: Remote
      Family:
          Name: Insteon
          Address: 33.33.33
          # Model: 2342-2
          # Date: 1518
          # Version: 1.7
      Button:
          - Name: GDO
            Comment: Garage Door Open/Close
            Group: 1
          - Name: B
            Group: 2
          - Name: C
            Group: 3
          - Name: Test
            Comment: Test Button
            Group: 4
    - Name: Brian Bedside mini remote
      Type: Remote
      Comment: For Lights
      Family:
          Name: Insteon
          Address: 44.44.44
          # Model: 2343-2
      Button:
          - Name: GDO
            Comment: TV Lights
            Group: 1
          - Name: B
            Comment: Brian Headboard
            Group: 2
          - Name: C
            Comment: Marcia Hedboard
            Group: 3
          - Name: D
            Group: 4
          - Name: E
            Group: 5
          - Name: F
            Group: 6
          - Name: G
            Group: 7
          - Name: H
            Group: 8
    - Name: Breakfast Nook Slave
      Type: Slave
      Family:
          Name: Insteon
          Address: 55.55.55
    - Name: Diningroom Slave
      Type: Slave
      Family:
          Name: Insteon
          Address: 66.66.66
```


### Insteon mini remote (button set)

### Instein slave

With Insteon dimmer switches, only one switch is connected to the light (Load).
The other switches in a N-way setup have nothing connected to the load wire.
They exist only to be a controller device to the master switch which is a responder.
There may be other brands that do this also.

These switches are arbitrarily categorized as buttons. since they do not directly control the load.

```
Buttons:
    - Name: Diningroom Slave
      Type: Slave
      Family:
          Name: Insteon
          Address: 66.66.66
```

Notice that they do not have a Button section since there is only one button on the switch.

### END DBK
