"""

@name:      PyHouse/src/Modules/Security/pi_camera.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2013_2016 by D. Brian Kimmel
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

# Import system type stuff
import StringIO
import subprocess
import os
import time
from datetime import datetime
# from PIL import Image

# Import PyMh files
from Modules.Computer import logging_pyh as Logger
LOG = Logger.getLogger('PyHouse.SecurityCamera ')


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


class Image(object):
    """
    """

    # Capture a small test image (for motion detection)
    def capture_test_image(self):
        command = "raspistill -w %s -h %s -t 0 -e bmp -o -" % (100, 75)
        imageData = StringIO.StringIO()
        imageData.write(subprocess.check_output(command, shell = True))
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
        subprocess.call("raspistill -w 1296 -h 972 -t 0 -e jpg -q 15 -o %s" % filename, shell = True)

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
        image1, buffer1 = self.capture_test_image()

        # Reset last capture time
        lastCapture = time.time()

        while (True):

            # Get comparison image
            image2, buffer2 = self.capture_test_image()

            # Count changed pixels
            changedPixels = 0
            for x in xrange(0, 100):
                for y in xrange(0, 75):
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
            image1 = image2
            buffer1 = buffer2


class API(object):
    """ Initialize the cameras
    """

    def __init__(self, p_pyhouse_obj):
        """
        """
        self.m_pyhouse_obj = p_pyhouse_obj
        LOG.info('Initialized')

    def LoadXml(self, _p_pyhouse_obj):
        LOG.info('Loaded XML')

    def Start(self):
        LOG.info("Started.")

    def SaveXml(self, p_xml):
        LOG.info("Saved XML.")
        return p_xml

    def Stop(self):
        LOG.info("Stopped.")

# ## END DBK
