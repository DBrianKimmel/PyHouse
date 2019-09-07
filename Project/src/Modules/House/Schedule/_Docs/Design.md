* Name:      Modules/Housing/Schedules/_Docs/Design.md
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2019 by D. Brian Kimmel
* Created:   2018-10-16
* Updated:   2019-01-11
* License:   MIT License
* Summary:   This is the design documentation for the Schedules Module of PyHouse.


# Schedules

Pyhouse maintains the series of events to be done in a house.
They include lights turning on and off, Thermostat settings, Irrigation Schedules, Pool pump on and off times and many others

Active schedules are shared throughout the house.


## Schedule

## Sunrise / Sunset

Originally I wrote a lot of complicated code to compute sunrise and sunset but then I found Astral.
I switched to astral and the code is now gone.  Hurrah!

## Time
Now every day at 10:00 AM a series of timers are calculated (this accounts for daylight savings time).
They are noon, solar noon, midnight, dusk, dawn, sunrise, sunset.
The Master node transmits the time messages.

## Master Node
At noon, each node checks to see if it is the master and if so transmits Mqtt messages as each time is reached.
If a node has not gotten a noon message by 12:01 PM it adds a random delay of a minute and schedules a transmit time of master node message.

## Mqtt

.../schedule/<Command>
- status
- control

The Mqtt message is the new way to execute a schedule.  Each node executes a schedule and sends a message ot all othefr nodes.
If the node receiving the message has a controller capable of acting on the message it does so by sending the proper commands to the controller


### XML

```xml
<Schedule Active="True" Key="0" Name="Schedule 0">
	<UUID>Schedule-0000-0000-0000-0123456789ab</UUID>
	<Comment>Description</Comment>
	<ScheduleType>Lighting</ScheduleType>
	<LightName>Light, Insteon (xml_lights) </LightName>
	<LightUUID>Light...-0000-0000-0000-0123456789ab</LightUUID>
	<Level>100</Level>
	<Rate>0</Rate>
	<RoomName>Master Bath (xml_lights)</RoomName>
	<RoomUUID>Light...-Room-0000-0000-123458b6eb6f</RoomUUID>
	<Time>13:34</Time>
	<DayOfWeek>127</DayOfWeek>
	<ScheduleMode>Home</ScheduleMode>
</Schedule>
```

### status

This is a schedule object published.

### Object

The Schedule object entry:

```python

```

DOW is a bitmask (0-127) of days the time is valid {mon=1, tue=2, wed=4, thu=8, fri=16, sat=32, sun=64}
-    0 is no days of the week
-    1 is valid on Monday
-    2 is valid on Tuesday
-    4 is valid on Wednesday
-    8 is valid on Thrsday
-   16 is valid on Friday
-   32 is valid on Saturday
-   64 is valid on Sunday

```python

```


#### DOW

DOW is a bitmask (0-127) of days the time is valid {mon=1, tue=2, wed=4, thu=8, fri=16, sat=32, sun=64}
-    0 is no days of the week
-    1 is valid on Monday
-    2 is valid on Tuesday
-    4 is valid on Wednesday
-    8 is valid on Thrsday
-   16 is valid on Friday
-   32 is valid on Saturday
-   64 is valid on Sunday


#### Light Status

This is the idealized light status info.
This class contains all the reportable and controllable information a light might have.

```python

class BaseObject(object):
        self.Name = 'undefined baseobject'
        self.Key = 0
        self.Active = False
        self.Comment = ''
        self.LastUpdate = None
class BaseUUIDObject(BaseObject):
        self.UUID = None
class DeviceInformation(BaseUUIDObject):
        self.DeviceFamily = 'Null'
        self.DeviceType = 0  # 0 = Controllers, 1 = Lighting, 2 = HVAC, 3 = Security, 4 = Bridge
        self.DeviceSubType = 0
        self.RoomCoords = None  # CoordinateInformation()
        self.RoomName = ''
        self.RoomUUID = None
class CoreLightingData(DeviceInformation):
        # self. Lighting Type = ''  # VALID_LIGHTING_TYPE = Button | Light | Controller
class LightData(CoreLightingData):
        self.BrightnessPct = 0  # 0% to 100%
        self.Hue = 0  # 0 to 65535
        self.Saturation = 0  # 0 to 255
        self.ColorTemperature = 0  # degrees Kelvin - 0 is not supported
        self.RGB = 0xffffff
        self.TransitionTime = 0  # 0 to 65535 ms = time to turn on or off (fade Time or Rate)
        self.State = State.UNKNOWN
        self.IsDimmable = False
        self.IsColorChanging = False
```

### END DBK
