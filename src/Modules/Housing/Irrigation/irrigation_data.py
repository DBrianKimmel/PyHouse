"""
-*- test-case-name: PyHouse/src/Modules/Housing/Irrigation/irrigation_data.py -*-

@name:      PyHouse/src/Modules/Housing/Irrigation/irrigation_data.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2018-2018 by D. Brian Kimmel
@note:      Created on Feb 9, 2018
@license:   MIT License
@summary:

"""

__updated__ = '2018-02-11'

#  Import system type stuff

#  Import PyMh files and modules.
from Modules.Core.data_objects import BaseObject, BaseUUIDObject


class IrrigationData(BaseObject):
    """ Info about any/all irrigation systems for a house.

    ==> PyHouse.House.Irrigation.xxx as in the def below
    """

    def __init__(self):
        super(IrrigationData, self).__init__()
        self.Systems = {}  # IrrigationSystemData()


class IrrigationSystemData(BaseUUIDObject):
    """ Info about an irrigation system (may have many zones).

    ==> PyHouse.House.Irrigation.Systems.xxx as in the def below
    """

    def __init__(self):
        super(IrrigationSystemData, self).__init__()
        self.FirstZone = None
        self.UsesMasterValve = False  # Master valve
        self.UsesPumpStartRelay = False
        self.Type = None
        self.Zones = {}  # IrrigationZoneData()


class IrrigationZoneData(BaseObject):
    """ Detailed Info about an irrigation zone

    ==> PyHouse.House.Irrigation.Systems.Zones.xxx as in the def below
    """

    def __init__(self):
        super(IrrigationZoneData, self).__init__()
        self.Duration = 0  # On time in hh:mm:ss
        self.EmitterCount = 1
        self.EmitterType = 'Rotor'
        self.Next = 0
        self.Previous = -1
        self.Rate = 0  # Litres per Minute  = GPH * 0.0630901964
        self.StartTime = None

# ## END DBK
