'''
Created on Nov 18, 2013

@author: briank

if this node is a raspberry pi and it has a camera attached, this will provide surveilance
videos and alerts.

If motion above a threshold is detected, it will trigger an alert and create a time lapse video
'''

FRAME_INTERVAL = 1000  # miliseconds
MIN_PIXELS = 25
