* Name:      PyHouse/Project/src/Modules/Housing/Scheduling/Docs/Design
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2018 by D. Brian Kimmel
* Created:   2018-10-16
* Updated:   2018-10-16
* License:   MIT License
* Summary:   This is the design documentation for the Scheduling Module of PyHouse.


# Scheduling

Pyhouse maintains the series of events to be done in a house.
They include lights turning on and off, Thermostat settings, Irrigation Schedules, Pool pump on and off times and many others

## Schedule

## Sunrise / Sunset

Originally I wrote a lot of cpmplicated code to compute sunrise and sunset but then I found Astral.
I switched to astral and the code is now gone.  Hurrah!

## Mqtt

.../schedule/<Command>
- status
- control

The Mqtt message is the new way to execute a schedule.  Each node executes a schedule and sends a message ot all othefr nodes.
If the node receiving the message has a controller capable of acting on the message it does so by sending the proper commands to the controller


### status

This is a schedule object published.

### Object

#### BaseObject
- Name = 'undefined baseobject'
- Key = 0
- Active = False
- Comment = ''
- LastUpdate = None (datetime)
#### BaseUUIDObject
- UUID = None
#### ScheduleBaseData
- DOW = None  # a bitmask (0-127) of days the time is valid {mon=1, tue=2, wed=4, thu=8, fri=16, sat=32, sun=64}
- ScheduleMode = 'Always'  # Always, Home, Away, Vacation, ...
- ScheduleType = ''  # Valid Schedule Type
- Time = None
-   for use by web browser - not saved in xml
- _AddFlag = False
- _DeleteFlag = False
#### ScheduleLightData
- Level = 0
- LightName = None
- LightUUID = None
- Rate = 0
- RoomName = None
- RoomUUID = None
- ScheduleType = 'Lighting'  # For future expansion into scenes, entertainment etc.
#### LightData
- BrightnessPct = 0  # 0% to 100%
- Hue = 0  # 0 to 65535
- Saturation = 0  # 0 to 255
- ColorTemperature = 0  # degrees Kelvin - 0 is not supported
- RGB = 0xffffff
- TransitionTime = 0  # 0 to 65535 ms = time to turn on or off (fade Time or Rate)
- State = State.UNKNOWN
- IsDimmable = False
- IsColorChanging = False



### END DBK
