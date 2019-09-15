* Name:      PyHouse/Project/src/Modules/Families/Insteon/_Docs/InsteonHub.md
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2019-2019 by D. Brian Kimmel
* Created:   2019-03-31
* Updated:   2019-09-14
* License:   MIT License
* Summary:   This is the documentation for the Insteon Hub.


# Hub 

Hub II - 2245.222

The hub is required for Alexa voice control of Insteon devices.

## Config

The hub is enabled by adding a line in bridges.yaml

```yaml
Insteon:
    Hub:
        Model: 2245-222
        Address: 53.54.55
        Mac: 00:01:02:53:54:55
        Rev: 3.3
        Date: 2219
        Interface:
            Type: Ethernet
            Host: insteon-ct
            Port: from the label
        Security:
            User: !user from the label
            Password: !password from the label
```

### END DBK
