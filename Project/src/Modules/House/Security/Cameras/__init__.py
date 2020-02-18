"""
@name:      Modules/House/Security/Cameras/cameras.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2020_2020 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Feb  1, 2020
@Summary:

if this node is a raspberry pi and it has a camera attached, this will provide surveillance
videos and alerts.

If motion above a threshold is detected, it will trigger an alert and create a time lapse video
"""


class CameraInformation:
    """

    ==> PyHouse.House.Security.Garage_Doors.xxx as in the def below
    """

    def __init__(self):
        self.Name = None
        self.Comment = None
        self.DeviceType = 'Security'
        self.DeviceSubType = 'Camera'
        self.Family = None  # FamilyInformation()
        self.Room = None  # RoomInformation()

# ## END DBK
