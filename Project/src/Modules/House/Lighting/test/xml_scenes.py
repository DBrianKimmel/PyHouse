"""
@name:      PyHouse/src/Modules/Housing/Lighting/test/xml_scenes.py
@author:    D. Brian Kimmel
@contact:   D.BrianKimmel@gmail.com
@copyright: (c) 2018-2018 by D. Brian Kimmel
@note:      Created on Aug 24, 2018
@license:   MIT License
@summary:

<SceneSection>
    <Scene Name="MBR Evening" Key="0" Active="True">
        <Comment>Evening in the Master Bedroom</Comment>
        <Component Name="Brians Bed" Key="0" Active="True">
            <Level>35</Level>
        </Component
    </Scene>
</SceneSection>


"""

__updated__ = '2018-08-24'

# Import PyMh files

TESTING_SCENE_SECTION = 'SceneSection'

L_SCENE_SECTION_START = '<' + TESTING_SCENE_SECTION + '>'
L_SCENE_SECTION_END = '</' + TESTING_SCENE_SECTION + '>'

XML_SCENE = '\n'.join([
    L_SCENE_SECTION_START,
    L_SCENE_SECTION_END
])

# ## END DBK
