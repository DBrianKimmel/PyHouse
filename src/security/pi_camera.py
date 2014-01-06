'''
Created on Nov 18, 2013

@author: briank

if this node is a raspberry pi and it has a camera attached, this will provide surveillance
videos and alerts.

If motion above a threshold is detected, it will trigger an alert and create a time lapse video
'''

# Motion detection settings:
# Threshold (how much a pixel has to change by to be marked as "changed")
# Sensitivity (how many changed pixels before capturing an image)
# ForceCapture (whether to force an image to be captured every forceCaptureTime seconds)
FRAME_INTERVAL = 1000  # mili-seconds
MIN_PIXELS = 25
THRESHOLD = 10
SENSITIVITY = 20

import StringIO
import subprocess
import os
import time
from datetime import datetime
from PIL import Image

forceCapture = True
forceCaptureTime = 60 * 60  # Once an hour

# File settings
saveWidth = 1280
saveHeight = 960
diskSpaceToReserve = 400 * 1024 * 1024  # Keep 400 mb free on disk

# Capture a small test image (for motion detection)
def capture_test_image():
    command = "raspistill -w %s -h %s -t 0 -e bmp -o -" % (100, 75)
    imageData = StringIO.StringIO()
    imageData.write(subprocess.check_output(command, shell = True))
    imageData.seek(0)
    im = Image.open(imageData)
    buffer = im.load()
    imageData.close()
    return im, buffer

# Save a full size image to disk
def save_image(width, height, diskSpaceToReserve):
    keep_disk_space_free(diskSpaceToReserve)
    time = datetime.now()
    filename = "capture-%04d%02d%02d-%02d%02d%02d.jpg" % (time.year, time.month, time.day, time.hour, time.minute, time.second)
    subprocess.call("raspistill -w 1296 -h 972 -t 0 -e jpg -q 15 -o %s" % filename, shell = True)
    print "Captured %s" % filename

# Keep free space above given level
def keep_disk_space_free(bytesToReserve):
    if (get_free_space() < bytesToReserve):
        for filename in sorted(os.listdir(".")):
            if filename.startswith("capture") and filename.endswith(".jpg"):
                os.remove(filename)
                print "Deleted %s to avoid filling disk" % filename
                if (get_free_space() > bytesToReserve):
                    return

# Get available disk space
def get_free_space():
    st = os.statvfs(".")
    du = st.f_bavail * st.f_frsize
    return du

# Get first image
image1, buffer1 = capture_test_image()

# Reset last capture time
lastCapture = time.time()

while (True):

    # Get comparison image
    image2, buffer2 = capture_test_image()

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
        save_image(saveWidth, saveHeight, diskSpaceToReserve)

    # Swap comparison buffers
    image1 = image2
    buffer1 = buffer2

# ## END DBK
