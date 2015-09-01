"""
@name:      PyHouse/src/Modules/Computer/Pi/pi_gpio.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2015 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Aug 30, 2015
@Summary:

This needs to wait for a new GPIO package that does not require root priveliges.

"""

# Import system type stuff

# Import PyMh files and modules.
try:
    import RPi.GPIO as GPIO
except:
    GPIO = None

IRRIGATION_PIN = 14

GPIO.setmode(GPIO.BOARD)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)

while True:
    GPIO.wait_for_edge(23, GPIO.RISING)
    print("Button 1 Pressed")
    GPIO.wait_for_edge(23, GPIO.FALLING)
    print("Button 1 Released")
    GPIO.wait_for_edge(24, GPIO.FALLING)
    print("Button 2 Pressed")
    GPIO.wait_for_edge(24, GPIO.RISING)
    print("Button 2 Released")
GPIO.cleanup()


class API(object):
    """
    """

    def __init__(self, p_pyhouse_obj):
        self.m_pyhouse_obj = p_pyhouse_obj

    def Start(self):
        if GPIO == None:
            return

    def RelayOn(self, p_pin):
        if GPIO == None:
            return
        GPIO.setup(p_pin, GPIO.OUT)
        GPIO.output(p_pin, GPIO.HIGH)

    def RelayOff(self, p_pin):
        if GPIO == None:
            return
        GPIO.setup(p_pin, GPIO.OUT)
        GPIO.output(p_pin, GPIO.LOW)

# ## END DBK
