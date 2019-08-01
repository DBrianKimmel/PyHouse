"""
@name:      PyHouse/Project/src/Modules/Housing/Irrigation/_test/xml_irrigation.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2015-2019 by D. Brian Kimmel
@license:   MIT License
@note:      Created on Jun 30, 2015
@Summary:

"""

__updated__ = '2019-05-09'

# The major XML sections
TESTING_IRRIGATION_SECTION = 'IrrigationSection'
TESTING_IRRIGATION_SYSTEM = 'System'
TESTING_IRRIGATION_ZONE = 'Zone'

L_IRRIGATION_SECTION_START = '<' + TESTING_IRRIGATION_SECTION + '>'
L_IRRIGATION_SECTION_END = '</' + TESTING_IRRIGATION_SECTION + '>'

L_IRRIGATION_SYSTEM_END = '</' + TESTING_IRRIGATION_SYSTEM + '>'
L_IRRIGATION_ZONE_END = '</' + TESTING_IRRIGATION_ZONE + '>'

######################
# System 0
######################

TESTING_IRRIGATION_SYSTEM_NAME_0 = 'LawnSystem'
TESTING_IRRIGATION_SYSTEM_KEY_0 = '0'
TESTING_IRRIGATION_SYSTEM_ACTIVE_0 = 'True'
TESTING_IRRIGATION_SYSTEM_UUID_0 = 'Irrigate-0000-0000-0000-0123456789ab'
TESTING_IRRIGATION_SYSTEM_COMMENT_0 = 'Main yard system with Well Relay and 13 zones'
TESTING_IRRIGATION_SYSTEM_FIRST_ZONE_0 = '0'
TESTING_IRRIGATION_SYSTEM_MASTER_VALVE_0 = 'False'
TESTING_IRRIGATION_SYSTEM_PUMP_RELAY_0 = 'True'
TESTING_IRRIGATION_SYSTEM_TYPE_0 = 'Multi'

L_IRRIGATION_SYSTEM_START_0 = \
        '<' + TESTING_IRRIGATION_SYSTEM + ' ' + \
        'Name="' + TESTING_IRRIGATION_SYSTEM_NAME_0 + '" ' \
        'Key="' + TESTING_IRRIGATION_SYSTEM_KEY_0 + '" ' + \
        'Active="' + TESTING_IRRIGATION_SYSTEM_ACTIVE_0 + '" ' + \
        '>'
L_IRRIGATION_SYSTEM_UUID_0 = '<UUID>' + TESTING_IRRIGATION_SYSTEM_UUID_0 + '</UUID>'
L_IRRIGATION_SYSTEM_COMMENT_0 = '<Comment>' + TESTING_IRRIGATION_SYSTEM_COMMENT_0 + '</Comment>'
L_IRRIGATION_SYSTEM_FIRST_ZONE_0 = '<FirstZone>' + TESTING_IRRIGATION_SYSTEM_FIRST_ZONE_0 + '</FirstZone>'
L_IRRIGATION_SYSTEM_MASTER_VALVE_0 = '<MasterValve>' + TESTING_IRRIGATION_SYSTEM_MASTER_VALVE_0 + '</MasterValve>'
L_IRRIGATION_SYSTEM_PUMP_RELAY_0 = '<PumpRelay>' + TESTING_IRRIGATION_SYSTEM_PUMP_RELAY_0 + '</PumpRelay>'
L_IRRIGATION_SYSTEM_TYPE_0 = '<Type>' + TESTING_IRRIGATION_SYSTEM_TYPE_0 + '</Type>'

#---------------------
# Zone 0
#---------------------

TESTING_IRRIGATION_ZONE_NAME_0_0 = 'Front Rotors # 1'
TESTING_IRRIGATION_ZONE_KEY_0_0 = '0'
TESTING_IRRIGATION_ZONE_ACTIVE_0_0 = 'True'
TESTING_IRRIGATION_ZONE_UUID_0_0 = 'Irrigate-Zone-0000-0000-0123456789ab'
TESTING_IRRIGATION_ZONE_COMMENT_0_0 = 'Rotors on the West corner of the yard'
TESTING_IRRIGATION_ZONE_DURATION_0_0 = '00:45:00'
TESTING_IRRIGATION_ZONE_EMITTER_COUNT_0_0 = '6'
TESTING_IRRIGATION_ZONE_EMITTER_TYPE_0_0 = 'Rotor'
TESTING_IRRIGATION_ZONE_NEXT_0_0 = '1'
TESTING_IRRIGATION_ZONE_PREV_0_0 = '-1'
TESTING_IRRIGATION_ZONE_RATE_0_0 = '1.2345'
TESTING_IRRIGATION_ZONE_START_TIME_0_0 = '11:22:33'

L_IRRIGATION_ZONE_START_0_0 = \
        '<' + TESTING_IRRIGATION_ZONE + ' ' + \
        'Name="' + TESTING_IRRIGATION_ZONE_NAME_0_0 + '" ' + \
        'Key="' + TESTING_IRRIGATION_ZONE_KEY_0_0 + '" ' + \
        'Active="' + TESTING_IRRIGATION_ZONE_ACTIVE_0_0 + '" ' + \
        '>'
L_IRRIGATION_ZONE_UUID_0_0 = '<UUID>' + TESTING_IRRIGATION_ZONE_UUID_0_0 + '</UUID>'
L_IRRIGATION_ZONE_COMMENT_0_0 = '<Comment>' + TESTING_IRRIGATION_ZONE_COMMENT_0_0 + '</Comment>'
L_IRRIGATION_ZONE_DURATION_0_0 = '<Duration>' + TESTING_IRRIGATION_ZONE_DURATION_0_0 + '</Duration>'
L_IRRIGATION_ZONE_EMITTER_COUNT_0_0 = '<EmitterCount>' + TESTING_IRRIGATION_ZONE_EMITTER_COUNT_0_0 + '</EmitterCount>'
L_IRRIGATION_ZONE_EMITTER_TYPE_0_0 = '<EmitterType>' + TESTING_IRRIGATION_ZONE_EMITTER_TYPE_0_0 + '</EmitterType>'
L_IRRIGATION_ZONE_NEXT_0_0 = '<NextZone>' + TESTING_IRRIGATION_ZONE_NEXT_0_0 + '</NextZone>'
L_IRRIGATION_ZONE_PREV_0_0 = '<PrevZone>' + TESTING_IRRIGATION_ZONE_PREV_0_0 + '</PrevZone>'
L_IRRIGATION_ZONE_RATE_0_0 = '<Rate>' + TESTING_IRRIGATION_ZONE_RATE_0_0 + '</Rate>'
L_IRRIGATION_ZONE_START_TIME_0_0 = '<StartTime>' + TESTING_IRRIGATION_ZONE_START_TIME_0_0 + '</StartTime>'

L_IRRIGATION_ZONE_0_0 = '\n'.join([
    L_IRRIGATION_ZONE_START_0_0,
    L_IRRIGATION_ZONE_UUID_0_0,
    L_IRRIGATION_ZONE_COMMENT_0_0,
    L_IRRIGATION_ZONE_DURATION_0_0,
    L_IRRIGATION_ZONE_EMITTER_COUNT_0_0,
    L_IRRIGATION_ZONE_EMITTER_TYPE_0_0,
    L_IRRIGATION_ZONE_NEXT_0_0,
    L_IRRIGATION_ZONE_PREV_0_0,
    L_IRRIGATION_ZONE_RATE_0_0,
    L_IRRIGATION_ZONE_START_TIME_0_0,
    L_IRRIGATION_ZONE_END
])

#---------------------
# Zone 1
#---------------------

TESTING_IRRIGATION_ZONE_NAME_0_1 = 'Front Rotors # 2'
TESTING_IRRIGATION_ZONE_KEY_0_1 = '1'
TESTING_IRRIGATION_ZONE_ACTIVE_0_1 = 'True'
TESTING_IRRIGATION_ZONE_UUID_0_1 = 'Irrigate-Zone-0001-0001-0123456789ab'
TESTING_IRRIGATION_ZONE_COMMENT_0_1 = 'Sprayers at the Back of the yard'
TESTING_IRRIGATION_ZONE_DURATION_0_1 = '00:45:00'
TESTING_IRRIGATION_ZONE_EMITTER_COUNT_0_1 = '13'
TESTING_IRRIGATION_ZONE_EMITTER_TYPE_0_1 = 'Sprayer'
TESTING_IRRIGATION_ZONE_NEXT_0_1 = '-1'
TESTING_IRRIGATION_ZONE_PREV_0_1 = '0'
TESTING_IRRIGATION_ZONE_RATE_0_1 = '2.2345'
TESTING_IRRIGATION_ZONE_START_TIME_0_1 = '00:00:00'

L_IRRIGATION_ZONE_START_0_1 = '<Zone Name="' + TESTING_IRRIGATION_ZONE_NAME_0_1 + \
        '" Key="' + TESTING_IRRIGATION_ZONE_KEY_0_1 + \
        '" Active="' + TESTING_IRRIGATION_ZONE_ACTIVE_0_1 + \
        '">'
L_IRRIGATION_ZONE_UUID_0_1 = '<UUID>' + TESTING_IRRIGATION_ZONE_UUID_0_1 + '</UUID>'
L_IRRIGATION_ZONE_COMMENT_0_1 = '<Comment>' + TESTING_IRRIGATION_ZONE_COMMENT_0_1 + '</Comment>'
L_IRRIGATION_ZONE_DURATION_0_1 = '<Duration>' + TESTING_IRRIGATION_ZONE_DURATION_0_1 + '</Duration>'
L_IRRIGATION_ZONE_EMITTER_COUNT_0_1 = '<EmitterCount>' + TESTING_IRRIGATION_ZONE_EMITTER_COUNT_0_1 + '</EmitterCount>'
L_IRRIGATION_ZONE_EMITTER_TYPE_0_1 = '<EmitterType>' + TESTING_IRRIGATION_ZONE_EMITTER_TYPE_0_1 + '</EmitterType>'
L_IRRIGATION_ZONE_NEXT_0_1 = '<NextZone>' + TESTING_IRRIGATION_ZONE_NEXT_0_1 + '</NextZone>'
L_IRRIGATION_ZONE_PREV_0_1 = '<PrevZone>' + TESTING_IRRIGATION_ZONE_PREV_0_1 + '</PrevZone>'
L_IRRIGATION_ZONE_RATE_0_1 = '<Rate>' + TESTING_IRRIGATION_ZONE_RATE_0_1 + '</Rate>'
L_IRRIGATION_ZONE_START_TIME_0_1 = '<StartTime>' + TESTING_IRRIGATION_ZONE_START_TIME_0_1 + '</StartTime>'

L_IRRIGATION_ZONE_0_1 = '\n'.join([
    L_IRRIGATION_ZONE_START_0_1,
    L_IRRIGATION_ZONE_UUID_0_1,
    L_IRRIGATION_ZONE_COMMENT_0_1,
    L_IRRIGATION_ZONE_DURATION_0_1,
    L_IRRIGATION_ZONE_EMITTER_COUNT_0_1,
    L_IRRIGATION_ZONE_EMITTER_TYPE_0_1,
    L_IRRIGATION_ZONE_NEXT_0_1,
    L_IRRIGATION_ZONE_PREV_0_1,
    L_IRRIGATION_ZONE_RATE_0_1,
    L_IRRIGATION_ZONE_START_TIME_0_1,
    L_IRRIGATION_ZONE_END
])

L_IRRIGATION_SYSTEM_0 = '\n'.join([
    L_IRRIGATION_SYSTEM_START_0,
    L_IRRIGATION_SYSTEM_UUID_0,
    L_IRRIGATION_SYSTEM_COMMENT_0,
    L_IRRIGATION_SYSTEM_FIRST_ZONE_0,
    L_IRRIGATION_SYSTEM_MASTER_VALVE_0,
    L_IRRIGATION_SYSTEM_PUMP_RELAY_0,
    L_IRRIGATION_SYSTEM_TYPE_0,
    L_IRRIGATION_ZONE_0_0,
    L_IRRIGATION_ZONE_0_1,
    L_IRRIGATION_SYSTEM_END
])

######################
# System 1
######################

TESTING_IRRIGATION_SYSTEM_NAME_1 = 'Lanai Drip'
TESTING_IRRIGATION_SYSTEM_KEY_1 = '1'
TESTING_IRRIGATION_SYSTEM_ACTIVE_1 = 'True'
TESTING_IRRIGATION_SYSTEM_UUID_1 = 'Irrigate-0001-0001-0001-0123456789ab'

L_IRRIGATION_SYSTEM_START_1 = '<' + TESTING_IRRIGATION_SYSTEM + \
        ' Name="' + TESTING_IRRIGATION_SYSTEM_NAME_1 + '" ' \
        ' Key="' + TESTING_IRRIGATION_SYSTEM_KEY_1 + '" ' + \
        ' Active="' + TESTING_IRRIGATION_SYSTEM_ACTIVE_1 + '"' + \
        '>'
L_IRRIGATION_SYSTEM_UUID_1 = '<UUID>' + TESTING_IRRIGATION_SYSTEM_UUID_1 + '</UUID>'

#---------------------
# Zone 0
#---------------------

TESTING_IRRIGATION_ZONE_NAME_1_0 = 'Front Rotors # 1'
TESTING_IRRIGATION_ZONE_KEY_1_0 = '0'
TESTING_IRRIGATION_ZONE_ACTIVE_1_0 = 'True'
TESTING_IRRIGATION_ZONE_UUID_1_0 = 'Irrigate-Zone-0000-0000-0123456789ab'
TESTING_IRRIGATION_ZONE_COMMENT_1_0 = 'Rotors on the West corner of the yard'
TESTING_IRRIGATION_ZONE_DURATION_1_0 = '00:45:00'

L_IRRIGATION_ZONE_START_1_0 = '<Zone Name="' + TESTING_IRRIGATION_ZONE_NAME_1_0 + \
        '" Key="' + TESTING_IRRIGATION_ZONE_KEY_1_0 + \
        '" Active="' + TESTING_IRRIGATION_ZONE_ACTIVE_1_0 + \
        '">'
L_IRRIGATION_ZONE_UUID_1_0 = '<UUID>' + TESTING_IRRIGATION_ZONE_UUID_1_0 + '</UUID>'
L_IRRIGATION_ZONE_COMMENT_1_0 = '<Comment>' + TESTING_IRRIGATION_ZONE_COMMENT_1_0 + '</Comment>'
L_IRRIGATION_ZONE_DURATION_1_0 = '<Duration>' + TESTING_IRRIGATION_ZONE_DURATION_1_0 + '</Duration>'

L_IRRIGATION_ZONE_1_0 = '\n'.join([
    L_IRRIGATION_ZONE_START_1_0,
    L_IRRIGATION_ZONE_UUID_1_0,
    L_IRRIGATION_ZONE_COMMENT_1_0,
    L_IRRIGATION_ZONE_DURATION_1_0,
    L_IRRIGATION_ZONE_END
])

L_IRRIGATION_SYSTEM_1 = '\n'.join([
    L_IRRIGATION_SYSTEM_START_1,
    L_IRRIGATION_SYSTEM_UUID_1,
    L_IRRIGATION_ZONE_1_0,
    L_IRRIGATION_SYSTEM_END
])

######################
# System 2
######################
# ## Irrigation System 3 - Cannon trail drip system

TESTING_IRRIGATION_SYSTEM_NAME_2 = 'Cannon Trail Drip'
TESTING_IRRIGATION_SYSTEM_KEY_2 = '2'
TESTING_IRRIGATION_SYSTEM_ACTIVE_2 = 'True'
TESTING_IRRIGATION_SYSTEM_UUID_2 = 'Irrigate-0002-0002-0002-0123456789ab'

L_IRRIGATION_SYSTEM_START_2 = '<' + TESTING_IRRIGATION_SYSTEM + \
        ' Name="' + TESTING_IRRIGATION_SYSTEM_NAME_2 + '" ' \
        ' Key="' + TESTING_IRRIGATION_SYSTEM_KEY_2 + '" ' + \
        ' Active="' + TESTING_IRRIGATION_SYSTEM_ACTIVE_2 + '"' + \
        '>'
L_IRRIGATION_SYSTEM_UUID_2 = '<UUID>' + TESTING_IRRIGATION_SYSTEM_UUID_2 + '</UUID>'

#---------------------
# Zone 0
#---------------------

TESTING_IRRIGATION_ZONE_NAME_2_0 = 'Front Drip # 1'
TESTING_IRRIGATION_ZONE_KEY_2_0 = '0'
TESTING_IRRIGATION_ZONE_ACTIVE_2_0 = 'True'
TESTING_IRRIGATION_ZONE_UUID_2_0 = 'Irrigate-0002-0000-0000-0123456789ab'
TESTING_IRRIGATION_ZONE_COMMENT_2_0 = 'xxx'
TESTING_IRRIGATION_ZONE_DURATION_2_0 = '00:45:00'

L_IRRIGATION_ZONE_START_2_0 = '<Zone Name="' + TESTING_IRRIGATION_ZONE_NAME_2_0 + \
        '" Key="' + TESTING_IRRIGATION_ZONE_KEY_2_0 + \
        '" Active="' + TESTING_IRRIGATION_ZONE_ACTIVE_2_0 + \
        '">'
L_IRRIGATION_ZONE_UUID_2_0 = '<UUID>' + TESTING_IRRIGATION_ZONE_UUID_2_0 + '</UUID>'
L_IRRIGATION_ZONE_COMMENT_2_0 = '<Comment>' + TESTING_IRRIGATION_ZONE_COMMENT_2_0 + '</Comment>'
L_IRRIGATION_ZONE_DURATION_2_0 = '<Duration>' + TESTING_IRRIGATION_ZONE_DURATION_2_0 + '</Duration>'

L_IRRIGATION_ZONE_2_0 = '\n'.join([
    L_IRRIGATION_ZONE_START_2_0,
    L_IRRIGATION_ZONE_UUID_2_0,
    L_IRRIGATION_ZONE_COMMENT_2_0,
    L_IRRIGATION_ZONE_DURATION_2_0,
    L_IRRIGATION_ZONE_END
])

L_IRRIGATION_SYSTEM_2 = '\n'.join([
    L_IRRIGATION_SYSTEM_START_2,
    L_IRRIGATION_SYSTEM_UUID_2,
    L_IRRIGATION_ZONE_2_0,
    L_IRRIGATION_SYSTEM_END
])

# ## The final irrigation section

XML_IRRIGATION = '\n'.join([
    L_IRRIGATION_SECTION_START,
    L_IRRIGATION_SYSTEM_0,
    L_IRRIGATION_SYSTEM_1,
    L_IRRIGATION_SYSTEM_2,
    L_IRRIGATION_SECTION_END
])

# ## END DBK
