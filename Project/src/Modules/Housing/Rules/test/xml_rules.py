"""
-*- test-case-name: /home/briank/workspace/Pyhouse/src/Modules/Housing/Rules/test/xml_rules.py -*-

@name:      /home/briank/workspace/Pyhouse/src/Modules/Housing/Rules/test/xml_rules.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2017-2017 by D. Brian Kimmel
@note:      Created on Feb 1, 2017
@license:   MIT License
@summary:

"""

__updated__ = '2017-02-02'


TESTING_RULES_SECTION = 'RulesSection'
TESTING_RULE = 'Rule'

L_RULES_SECTION_START = '<' + TESTING_RULES_SECTION + '>'
L_RULES_SECTION_END = '</' + TESTING_RULES_SECTION + '>'
L_RULE_END = '</' + TESTING_RULE + '>'

TESTING_RULE_NAME_0 = 'MBR Closet'
TESTING_RULE_KEY_0 = '0'
TESTING_RULE_ACTIVE_0 = 'True'
TESTING_RULE_UUID_0 = 'Rule....-0000-0000-0000-0123456789ab'
TESTING_RULE_COMMENT_0 = "Turn light off 15 minutes after it was turned on."

TESTING_RULE_DEVICE_UUID = 'Light...-Room-0000-0000-123458b6eb6f'
TESTING_RULE_CONDITION = 'On'
TESTING_RULE_TIME = '900'  # 15 minutes
TESTING_RULE_ACTION = 'Off'

L_RULE_START_0 = '' + \
    '<' + TESTING_RULE + ' ' + \
    'Name="' + TESTING_RULE_NAME_0 + '" ' + \
    'Key="' + TESTING_RULE_KEY_0 + '" ' + \
    'Active="' + TESTING_RULE_ACTIVE_0 + '" ' + \
    '>'
L_RULE_UUID_0 = '<UUID>' + TESTING_RULE_UUID_0 + '</UUID>'
L_RULE_COMMENT_0 = '<Comment>' + TESTING_RULE_COMMENT_0 + '</Comment>'

L_RULE_DEVICE_UUID = '<DeviceUUID>' + TESTING_RULE_DEVICE_UUID + '</DeviceUUID>'
L_RULE_CONDITION = '<Condition>' + TESTING_RULE_CONDITION + '</Condition>'
L_RULE_TIME = '<Time>' + TESTING_RULE_TIME + '</Time>'
L_RULE_ACTION = '<Action>' + TESTING_RULE_ACTION + '</Action>'

L_RULE_0 = '\n'.join([
    L_RULE_START_0,
    L_RULE_UUID_0,
    L_RULE_COMMENT_0,
    L_RULE_DEVICE_UUID,
    L_RULE_CONDITION,
    L_RULE_TIME,
    L_RULE_ACTION,
    L_RULE_END
    ])

XML_RULES_SECTION = '\n'.join([
    L_RULES_SECTION_START,
    L_RULE_0,
    L_RULES_SECTION_END
    ])

# ## END DBK
