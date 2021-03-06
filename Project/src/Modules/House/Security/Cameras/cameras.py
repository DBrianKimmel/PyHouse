"""
@name:      Modules/House/Security/cameras.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013_2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Nov 18, 2013
@Summary:

if this node is a raspberry pi and it has a camera attached, this will provide surveillance
videos and alerts.

If motion above a threshold is detected, it will trigger an alert and create a time lapse video
"""

# Motion detection settings:
# Threshold (how much a pixel has to change by to be marked as "changed")
# Sensitivity (how many changed pixels before capturing an image)
# ForceCapture (whether to force an image to be captured every forceCaptureTime seconds)

__updated__ = '2020-02-02'
__version_info__ = (19, 8, 1)
__version__ = '.'.join(map(str, __version_info__))

# Import system type stuff
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

import subprocess
import os
import time
from datetime import datetime
# from PIL import Image

# Import PyMh files
from Modules.Core.Config.config_tools import Api as configApi

from Modules.Core import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.Cameras        ')

CONFIG_NAME = 'cameras'

FRAME_INTERVAL = 1000  # mili-seconds
MIN_PIXELS = 25
THRESHOLD = 10
SENSITIVITY = 20

forceCapture = True
forceCaptureTime = 60 * 60  # Once an hour

# File settings
saveWidth = 1280
saveHeight = 960
diskSpaceToReserve = 400 * 1024 * 1024  # Keep 400 mb free on disk


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


class Image:
    """
    """

    # Capture a small _test image (for motion detection)
    def capture_test_image(self):
        command = "raspistill -w %s -h %s -t 0 -e bmp -o -" % (100, 75)
        imageData = StringIO.StringIO()
        imageData.write(subprocess.check_output(command, shell=True))
        imageData.seek(0)
        im = None  # Image.open(imageData)
        l_buffer = im.load()
        imageData.close()
        return im, l_buffer

    # Save a full size image to disk
    def save_image(self, _width, _height, diskSpaceToReserve):
        self.keep_disk_space_free(diskSpaceToReserve)
        time = datetime.now()
        filename = "capture-%04d%02d%02d-%02d%02d%02d.jpg" % (time.year, time.month, time.day, time.hour, time.minute, time.second)
        subprocess.call("raspistill -w 1296 -h 972 -t 0 -e jpg -q 15 -o %s" % filename, shell=True)

    # Keep free space above given level
    def keep_disk_space_free(self, bytesToReserve):
        if (self.get_free_space() < bytesToReserve):
            for filename in sorted(os.listdir(".")):
                if filename.startswith("capture") and filename.endswith(".jpg"):
                    os.remove(filename)
                    if (self.get_free_space() > bytesToReserve):
                        return

    # Get available disk space
    def get_free_space(self):
        st = os.statvfs_result(".")
        du = st.f_bavail * st.f_frsize
        return du

    def main(self):
        # Get first image
        _image1, buffer1 = self.capture_test_image()

        # Reset last capture time
        lastCapture = time.time()

        while (True):

            # Get comparison image
            image2, buffer2 = self.capture_test_image()

            # Count changed pixels
            changedPixels = 0
            for x in range(0, 100):
                for y in range(0, 75):
                    # Just check green channel as it's the highest quality channel
                    pixdiff = abs(buffer1[x, y][1] - buffer2[x, y][1])
                    if pixdiff > THRESHOLD:
                        changedPixels += 1

            # Check force capture
            if forceCapture:
                if time.time() - lastCapture > forceCaptureTime:
                    changedPixels = SENSITIVITY + 1

            # Save an image if pixels changed
            if changedPixels > SENSITIVITY:
                lastCapture = time.time()
                self.save_image(saveWidth, saveHeight, diskSpaceToReserve)

            # Swap comparison buffers
            _image1 = image2
            buffer1 = buffer2


class LocalConfig:
    """
    """

    m_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj
        self.m_config = configApi(p_pyhouse_obj)

    def _extract_one_camera(self, p_config) -> dict:
        """
        @param p_config: is the config fragment containing one button's information.
        @return: a ButtonInformation() obj filled in.
        """
        l_obj = CameraInformation()
        l_required = ['Name', 'Family']
        _l_groupfields = ['Family', 'Room']
        for l_key, l_value in p_config.items():
            if l_key == 'Family':
                l_obj.Family = self.m_config.extract_family_group(l_value)
            elif l_key == 'Room':
                l_obj.Room = self.m_config.extract_room_group(l_value)
                pass
            else:
                setattr(l_obj, l_key, l_value)
        # Check for required data missing from the config file.
        for l_key in [l_attr for l_attr in dir(l_obj) if not l_attr.startswith('_') and not callable(getattr(l_obj, l_attr))]:
            if getattr(l_obj, l_key) == None and l_key in l_required:
                LOG.warning('Location Yaml is missing an entry for "{}"'.format(l_key))
        LOG.info('Extracted Camera "{}"'.format(l_obj.Name))
        return l_obj

    def _extract_all_cameras(self, p_config):
        """ Get all of the button sets configured
        A Button set is a (mini-remote) with 4 or 8 buttons in the set
        The set has one insteon address and each button is in a group
        """
        l_dict = {}
        for l_ix, l_camera in enumerate(p_config):
            l_camera = self._extract_one_camera(l_camera)
            l_dict[l_ix] = l_camera
        return l_dict

    def load_yaml_config(self):
        """ Read the lights.yaml file if it exists.  No file = no lights.
        It must contain 'Lights:'
        All the lights are a list.
        """
        # LOG.info('Loading Config')
        l_yaml = self.m_config.read_config_file(CONFIG_NAME)
        if l_yaml == None:
            LOG.error('{}.yaml is missing.'.format(CONFIG_NAME))
            return None
        try:
            l_yaml = l_yaml['Cameras']
        except:
            LOG.warning('The config file does not start with "Cameras:"')
            return None
        l_cameras = self._extract_all_cameras(l_yaml)
        return l_cameras


class Api:
    """ Initialize the cameras
    """

    m_local_config = None
    m_pyhouse_obj = None

    def __init__(self, p_pyhouse_obj):
        """
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        self._add_storage()
        self.m_local_config = LocalConfig(p_pyhouse_obj)
        LOG.info('Initialized')

    def _add_storage(self) -> None:
        """
        """
        if not hasattr(self.m_pyhouse_obj.House, 'Security'):
            setattr(self.m_pyhouse_obj.House, 'Security', object())
        setattr(self.m_pyhouse_obj.House.Security, 'Cameras', {})

    def LoadConfig(self):
        """
        """
        LOG.info('Loading Config')
        self.m_pyhouse_obj.House.Security.Cameras = self.m_local_config.load_yaml_config()
        LOG.info('Loaded {} Cameras.'.format(len(self.m_pyhouse_obj.House.Security.Cameras)))

    def Start(self):
        pass

    def SaveConfig(self):
        pass

    def Stop(self):
        pass

# ## END DBK
