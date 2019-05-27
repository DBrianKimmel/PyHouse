* Name:      PyHouse/Project/src/Modules/Housing/Rules/Docs/Design
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2019-2019 by D. Brian Kimmel
* Created:   2019-05-23
* Updated:   2019-05-23
* License:   MIT License
* Summary:   This is the design documentation for the Modules of PyHouse.

# Rules

This implements rules such as:
    If garage door opens between dusk and dawn, turn on the outside lights.
    If a closet light is on more than 30 minutes, turn it off.

There is a trigger event.
There is a action to be performed item
There is a delay section.

## Xml

```xml

<Event Name="Outside Lights" Key="0" Active="True">
    <><>
</Event>
```

### END DBK
