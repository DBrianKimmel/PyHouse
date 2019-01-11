* Name:      PyHouse/Project/src/Modules/Housing/Docs/Design
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2018 by D. Brian Kimmel
* Created:   2018-09-30
* Updated:   2018-10-04
* License:   MIT License
* Summary:   This is the design documentation for the Entertainment Module of PyHouse.


# Housing

Under the PyHouse banner, a user has one or more houses to automate/control.

Each house has one or more Mqtt brokers running.
They usually operate as a controlling broker with redundant brokers for backup.

Mqtt came into the picture after PyHous was up and running, so not everything runs reom a message.


## Design

Nodes are removed if last used > 2 months

## Rooms

- Name = 'undefined baseobject'
- Key = 0
- Active = False
- Comment = ''
- LastUpdate = None

- UUID = None

- Corner = ''  # CoordinateData()
- Floor = '1st'  # Outside | Basement | 1st | 2nd | 3rd | 4th | Attic | Roof
- Size = ''  # CoordinateData()
- RoomType = 'Room'
- _AddFlag = False
- _DeleteFlag = False



### END DBK
