* Name:      PyHouse/Project/src/Modules/Housing/Scheduling/Docs/Design
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2018-2018 by D. Brian Kimmel
* Created:   2018-10-16
* Updated:   2019-01-11
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

The Schedule object entry:

```python
class BaseObject(object):
        self.Name = 'undefined baseobject'
        self.Key = 0
        self.Active = False
        self.Comment = ''
        self.LastUpdate = None
class BaseUUIDObject(BaseObject):
        self.UUID = None
class ScheduleBaseData(BaseUUIDObject):
        self.DOW = None  # a bitmask (0-127) of days the time is valid {mon=1, tue=2, wed=4, thu=8, fri=16, sat=32, sun=64}
        self.ScheduleMode = 'Always'  # Always, Home, Away, Vacation, ...
        self.ScheduleType = ''  # Valid Schedule Type
        self.Time = None
        #  for use by web browser - not saved in xml
        self._AddFlag = False#### DOW
        self._DeleteFlag = False
class ScheduleLightData(ScheduleBaseData):
        self.ScheduleType = 'Lighting'  # For future expansion into scenes, entertainment etc.
        self.Level = 0
        self.LightName = None
        self.LightUUID = None
        self.Rate = 0
        self.RoomName = None
        self.RoomUUID = None
class ScheduleIrrigationData(ScheduleBaseData):
        self.ScheduleType = 'Irrigation'
        self.Duration = None
        self.System = None
        self.SystemUUID = None
        self.Zone = None
class ScheduleHvacData(ScheduleBaseData):
        self.ScheduleType = 'Hvac'

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
class ScheduleLightData(ScheduleBaseData):
        self.Level = 0
        self.LightName = None
        self.LightUUID = None
        self.Rate = 0
        self.RoomName = None
        self.RoomUUID = None
        self.ScheduleType = 'Lighting'  # For future expansion into scenes, entertainment etc.
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
    def __init__(self):
        self.Name = 'undefined baseobject'
        self.Key = 0
        self.Active = False
        self.Comment = ''
        self.LastUpdate = None

class BaseUUIDObject(BaseObject):
    def __init__(self):
        super(BaseUUIDObject, self).__init__()
        self.UUID = None

class DeviceData(BaseUUIDObject):
    def __init__(self):
        super(DeviceData, self).__init__()
        self.DeviceFamily = 'Null'
        self.DeviceType = 0  # 0 = Controllers, 1 = Lighting, 2 = HVAC, 3 = Security, 4 = Bridge
        self.DeviceSubType = 0
        self.RoomCoords = None  # CoordinateData()
        self.RoomName = ''
        self.RoomUUID = None

class CoreLightingData(DeviceData):
    def __init__(self):
        super(CoreLightingData, self).__init__()
        # self. Lighting Type = ''  # VALID_LIGHTING_TYPE = Button | Light | Controller
        pass

class LightData(CoreLightingData):
    def __init__(self):
        super(LightData, self).__init__()
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





- ## BaseObject()
- Name = 'undefined baseobject'
- Key = 0
- Active = False
- Comment = ''
- LastUpdate = None (datetime)
- ## BaseUUIDObject()
- UUID = None
- ## ScheduleBaseData()
- DOW = None  # a bitmask (0-127) of days the time is valid {mon=1, tue=2, wed=4, thu=8, fri=16, sat=32, sun=64}
- ScheduleMode = 'Always'  # Always, Home, Away, Vacation, ...
- ScheduleType = 'Lighting'  # Valid Schedule Type
- Time = None
- ** for use by web browser - not saved in xml
- _AddFlag = False
- _DeleteFlag = False
- ## ScheduleLightData()
- Level = 0
- LightName = None
- LightUUID = None
- Rate = 0
- RoomName = None
- RoomUUID = None
- ScheduleType = 'Lighting'  # For future expansion into scenes, entertainment etc.

- ## LightData()
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
