* Name:      PyHouse/Project/src/Modules/Housing/Docs/Design
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2018 by D. Brian Kimmel
* Created:   2018-09-30
* Updated:   2019-01-11
* License:   MIT License
* Summary:   This is the design documentation for the Entertainment Module of PyHouse.


# Housing

Under the PyHouse banner, a user has one or more houses to automate/control.

Each house has one or more Mqtt brokers running.
They usually operate ()as a controlling broker with redundant brokers for backup.

Mqtt came into the picture after PyHous was up and running, so not everything runs reom a message.

## Mode
The house has 3 modes: Home, Away and Vacation.
* Home is the normal operation Where everything operates on a normal schedule.
* Away is the operation where the house is unoccupied but wishes not to appear that way.
* Vacation is for short term where the house is unoccupied but you still want services running.

## Design

Nodes are removed if last used > 2 months ago.

## Rooms



```python
class BaseObject(object):
        self.Name = 'undefined baseobject'
        self.Key = 0
        self.Active = False
        self.Comment = ''
        self.LastUpdate = None
class BaseUUIDObject(BaseObject):
        self.UUID = None
class RoomData(BaseUUIDObject):
        self.Corner = ''  # CoordinateData()
        self.Floor = '1st'  # Outside | Basement | 1st | 2nd | 3rd | 4th | Attic | Roof
        self.Size = ''  # CoordinateData()
        self.RoomType = 'Room'
        self._AddFlag = False
        self._DeleteFlag = False
```

### END DBK
