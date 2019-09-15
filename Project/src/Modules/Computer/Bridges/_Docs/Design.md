* Name:      Modules/Computer/Bridges/_Docs/Design.md
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2019-2019 by D. Brian Kimmel
* Created:   2019-09-14
* Updated:   2019-09-14
* License:   MIT License
* Summary:   This is the design for Bridges.

# Bridges

This module allows PyHouse to load information for Bridges.

Bridges are devices that allow PyHouse send and receive information to foreign devices.
Manufactures may call these devices Hubs or Bridges.
Some examples are the "Philips Hue Hub", the "Insteon Hub" and the "Accurite Bridge".

They are separate devices that do not plug in to a computer directly.
They are ganerally network connection devices.

## Configuration

Bridges are configured in "/etc/pyhouse/Computer/bridges.yaml".

```yaml
---
# Name:      /etc/pyhouse/computer/bridges.yaml
# Author:    D. Brian Kimmel
# Contact:   D.BrianKimmel@gmail.com
# Copyright: (c)2019-2019 by D. Brian Kimmel
# Created:   Jun 24, 2019
# Updated:   Jun 26, 2019
# License:   MIT License
# Summary:   This is for PyHouse

Bridges:
   # Insteon: !include insteon.yaml
   # AcuRite: !include acurite.yaml
   Hue: !include hue.yaml

### END DBK
```

Note that this file only defines the presence of the bridges.


### END DBK
