* Name:      Modules/House/Family/Sonoff/_Docs/Flashing.md
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2019-2019 by D. Brian Kimmel
* Created:   2019-08-08
* Updated:   2019-08-08
* License:   MIT License
* Summary:   This is how to set up sonoff devices.

# Sonoff


## Software

Download the following software if you haven't already done so.

* esptool
* pip3 install netifaces flask

## Install

To directory /srv/sonoff:
* sonoff.bin
* sonoff-minimal.bin

* pip3 install netifaces flask

## Commands

Put the Sonoff in flash mode by holding down the button and connecting flasher device.
Continue holding button for 2-3 seconds after powering up.

* esptool --port /dev/ttyUSB0 write_flash -fs 1MB -fm dout 0x0 /srv/sonoff/sonoff.bin


## Initial Setup


# Configuration

## Setup



### END DBK
