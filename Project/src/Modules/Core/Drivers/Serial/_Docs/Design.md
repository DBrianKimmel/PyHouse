* Name:      PyHouse/Project/src/Modules/Drivers/Serial/Docs/README.md
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2019-2019 by D. Brian Kimmel
* Created:   2019-02-12
* Updated:   2019-02-12
* License:   MIT License
* Summary:   This is the design documentation for the Serial Driver.

# Serial

This is the interface for devices connected to to this computer that use the serial protocol to exchange information.

The device will have created a /dev/ttyUSBx port when it was plugged in or rebooted.

In order to make the usb more reliable, 

## Opening

When the device is found and open successfully, a Mqtt Message is sent to announce the fact.

### END DBK
