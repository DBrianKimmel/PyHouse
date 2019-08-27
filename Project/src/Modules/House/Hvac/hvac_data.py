"""
@name:      Modules/House/Hvac/hvac_data.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2019-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 04, 2019
@Summary:

"""
#  Import system type stuff

#  Import PyMh files
from Modules.Core.data_objects import DeviceInformation


class XXXThermostatData(DeviceInformation):
    """

    ==> PyHouse.House.Hvac.Thermostats.xxx as in the def below
    """

    def __init__(self):
        super(XXXThermostatData, self).__init__()
        self.CoolSetPoint = 0
        self.CurrentTemperature = 0
        self.HeatSetPoint = 0
        self.ThermostatMode = 'Cool'  # Cool | Heat | Auto | EHeat
        self.ThermostatScale = 'F'  # F | C
        self.ThermostatStatus = 'Off'  # On
        self.UUID = None


class XXXThermostatStatus():
    """
    """

    def __init__(self):
        self.Name = None
        self.Status = None
        self.Fan = None
        self.Mode = None
        self.Family = 'insteon'
        self.BrightnessPct = None

# ## END DBK

