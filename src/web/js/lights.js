/* lights.js
 * 
 * Browser side code.
 */

// import Nevow.Athena
// import globals
// import helpers

helpers.Widget.subclass(lights, 'LightsWidget').methods(

    function __init__(self, node) {
        lights.LightsWidget.upcall(self, "__init__", node);
    },

	function ready(self) {

		function cb_widgetready(res) {
			Divmod.debug('---', 'lights.js - cb_widgready was called. res = ' + res);
		}

		Divmod.debug('---', 'lights.js - ready was called.  self =' + self);
		var uris = collectIMG_src(self.node, null);
		var d = loadImages(uris);
		d.addCallback(cb_widgetready);
		return d;
	},  // ready

	function getAndShowLights(self) {

		function cb_showLogin(p_user) {
			Divmod.debug('---', 'lights.js - cb_showLogin was called. user = ' + p_user);
			self.node.innerHTML = 'Show Lights';
		}  // cb_showLights

        var l_logData = {
        		name : 'silly',
        		passwd : '123'
        };
    	var l_json = JSON.stringify(l_logData);
		Divmod.debug('---', 'lights.getAndShowLights() was called.');
    	var d = self.callRemote("lights", l_json);  // @ web_mainpage
		d.addCallback(cb_showLogin);
        return false;
	}
);

//### END DBK
