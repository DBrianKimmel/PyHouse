#!/usr/bin/python

"""
Insteon HVAC module.

Adds HVAC (Heating Ventilation Air Conditioning) to the Insteon suite.
Specifically developed for the Venstar 1-day programmable digital thermostat.
This contains an Insteon modem.

Models 2491T1E and 2491T7E = (2491TxE)

0x6E and 0x6F are old commands
"""

class ihvac_utility(object):

    def decode_50_record(self, p_obj, p_cmd1, p_cmd2):
        """
        @param p_obj: is the Device (light, thermostat...) we are decoding.
        @param p_cmd1: is the Command 1 field in the message we are decoding.
        @param p_cmd2: is the Command 2 field in the message we are decoding.
        """
        l_ret = 'Thermostat - Command1: {0:#X},  Command2:{1:#X}'.format(p_cmd1, p_cmd2)
        if p_cmd1 == 0x6e:
            l_ret = 'Thermostat temp = {0:}'.format(p_cmd2)
            return l_ret
        return l_ret

# ## END DBK
