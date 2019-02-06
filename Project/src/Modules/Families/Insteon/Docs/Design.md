* Name:      PyHouse/Project/src/Modules/Families/Insteon/Docs/Design
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2019-2019 by D. Brian Kimmel
* Created:   2019-01-20
* Updated:   2019-01-20
* License:   MIT License
* Summary:   This is the design for Insteon..

#Insteon

Insteon is / was the 3rd family of lighting control devices I used.
It is beginning to show its age in 2018.

When switching to Raspberry Pis as control nodes, it became possible to have several Insteon PLMs in a house.
Then came the HTTP device, the Insteon Link???
Then came the Insteon Hub which is/was a cloud type device with perhaps some local control.

# Design

There will only be one active PLM per node.


```python
class InsteonData:
    def __init__(self):
        self.DevCat = 0  # DevCat and SubCat (2 bytes)
        self.EngineVersion = 2
        self.FirmwareVersion = 0
        self.GroupList = ''
        self.GroupNumber = 0
        self.InsteonAddress = 0  # Long integer internally - '1A.B3.3C' for external reaability
        self.ProductKey = ''  # 3 bytes
        self.Links = {}
```

## Types

Insteon devices are of many different types

- Controllers
- Lights
- Buttons
- Switches
- Thermostats
- Garage Door Sensor/controller
- motion detector
- camera
- door sensor
- waterleak detectors

### END DBK