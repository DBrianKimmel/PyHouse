* Name:      PyHouse/Project/Docs/PyHouse.md
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2018 by D. Brian Kimmel
* Created:   2019-07-23
* Updated:   2019-07-23
* License:   MIT License
* Summary:   This is the design documentation of PyHouse.

# PyHouse

PyHouse is my (our) attempt to automate virtually every aspect about home life from within the house.
We recently lost Internet connectivity for 5 days and it pointed out how much is lost when disconnected.

There are a number of fundamental concepts to be addresses by PyHouse.

The first concept here is to have several small (think Raspberry Pi) computers communicating
with each other (via Mqtt) and doing all the things you want to do to make household life better.
Several of these computers should be running a Mqtt broker for redundancy.

Another concept is to virtualize the devices you want to control.
You want to turn a light, or a group of lights, on, off, brighter or dimmer and don't care if the
control is an insteon switch or a Hue bulb or some other type of light.

There should be multiple ways of issuing commands to the various devices within the house.
The earliest control we had was to walk up to the device and perform the desired action; we don't want to lose that ability.
Then we had remote controllers with a lot of buttons but devices usually only had one controller per device and we don't want that limitation.
Then along came smart phones and we were encouraged to download an 'app' for each device.
Well hundreds of devices (and apps) later and we spend much time switching between apps and turning on a Hue light, and then an Insteon light
and then turning on the electric tea kettle, turning down the volume on the tv, etc.

Then there was voice.




### END DBK