* Name:      PyHouse/Project/src/_Docs/PyHouse-Data.md
* Author:    D. Brian Kimmel
* Contact:   D.BrianKimmel@gmail.com
* Copyright: (c) 2019-2019 by D. Brian Kimmel
* Created:   2019-09-17
* Updated:   2019-09-26
* License:   MIT License

# PyHouse

```python
pyhouse_obj.					PyHouseInformation()			Modules/Core/data_objects.py
    Core.						CoreInformation()				Modules/Core/data_objects.py
        Mqtt.					MqttInformation()
        	Brokers{}
    Computer.					ComputerInformation()			Modules/Computer/computer.py
        Bridges.{}				BridgeInformation()				Modules/Computer/Bridges/bridges.py
        Communication
        InternetConnection
        Nodes.{}				NodeInformation()
        Weather
        Web
        ---
        Name
        Comment
        Primary
        Priority
    House.						HouseInformation()				Modules/House/house.py
    	Family.					FamilyInformation{}				Modules/House/Family/family.py
        Lighting.				LightingInformation()			Modules/House/Lighting/lighting.py
        	Buttons.{}
        	Controllers.{}		ControllerInformation()			Modules/House/Lighting/controllers.py
        		Access{}
        		Family{}		FamilyInformation()
        		Interface{}
        	Lights.{}
        	Outlets.{}
        ---
        Name
```

### END DBK
