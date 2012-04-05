#!/usr/bin/env python

"""Handle the scenes component of the lighting system.
"""


Scene_Data = {}

class SceneData(object):
    """
    """


class SceneAPI(SceneData):
    """
    """

    def load_all_scenes(self):
        self.m_logger.info("Using Scenes.")
        l_dict = self.m_config.get_value('Scenes')
        for l_key, l_value in l_dict.iteritems():
            self.Scene_Data[l_key] = {}
            for l_par, l_var in l_value.iteritems():
                self.Scene_Data[l_key][l_par] = l_var
        return self.Scene_Data



### END
