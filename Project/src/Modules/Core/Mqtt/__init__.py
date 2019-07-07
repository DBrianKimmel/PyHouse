"""
This package is used for MQTT communications.

A section of the PyHouse Object (Mqtt) is reserved for holding the information.

Multiple Brokers.
-----------------

Passing broker information via Mqtt itself may allow for synchronization of the broker tree.

XML routines will read/write all brokers in the XML configuration file.

pyhouse/<HouseName>/***
    ***/computer/browser/login                Modules/Web/web_login.py (139)
    ***/computer/local                        Modules/Computer/Nodes/node_local.py (348)
    ***/computer/node/iam                     Modules/Computer/Nodes/node_sync.py (50)
    ***/computer/node/whoisthere              Modules/Computer/Nodes/node_sync.py (42)
    ***/computer/shutdown                     Modules/Core/setup_pyhouse.py (140)
    ***/computer/startup                      Modules/Computer/Mqtt/mqtt_client.py (213)

    ***/hvac/<DeviceName>/***                 Modules/Families/Insteon/Insteon_HVAC.py (121)

    ***/lighting/{}/info                      Modules/Families/Insteon/Insteon_decoder.py (136)
    ***/lighting/controller/{}/start          Modules/Families/UPB/UPB_device.py (57)
    ***/lighting/web/{}/control               Modules/Web/web_control.py (64)

"""
__updated__ = '2019-05-13'

# ## END DBK
