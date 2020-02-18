* Name:      PyHouse/Project/src/_Docs/PyHouse-Data.md
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2019-2020 by D. Brian Kimmel
* Created:   2019-09-17
* Updated:   2020-02-17
* License:   MIT License

# PyHouse

```python

pyhouse_obj.								PyHouseInformation()			Modules/Core/__init__.py
    Core.									CoreInformation()				Modules/Core/__init__.py
        Mqtt.								MqttInformation()				Modules/Core/Mqtt/__init__.py
        	Brokers{}
        Futuremodules
        _Apis{}																Modules/Core/__init__.py
    Computer.								ComputerInformation()			Modules/Computer/computer.py
        Bridges{}							BridgeInformation()				Modules/Computer/Bridges/bridges.py
        Communication
        InternetConnection
        Nodes{}								NodeInformation()
        Weather
        Web
        ---
        Name
        Comment
        Primary
        Priority
    House.									HouseInformation()				Modules/House/house.py
    	Location							LocationInformation{}			Modules/House/Location.py
    	Floor{}								FloorInformation{}				Modules/House/Floor.py
    	Rooms{}								RoomsInformation{}				Modules/House/Rooms.py
    	-
        Lighting.							LightingInformation()			Modules/House/Lighting/lighting.py
        	Buttons.{}
        	Controllers.{}					ControllerInformation()			Modules/House/Lighting/controllers.py
        		Access{}
        		Family{}					FamilyInformation()
        		Interface{}
        	Lights.{}
        	Outlets.{}
        Hvac.
        Security.
        Irrigation.
        Pool.
        Rules.
        Schedule.
        Sync.
        Entertainment.
    	Family.								FamilyInformation{}				Modules/House/Family/family.py
        ---
        Name

```

### END DBK
