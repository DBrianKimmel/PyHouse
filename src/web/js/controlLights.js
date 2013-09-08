/* controlLights.js
 * 
 * Displays the schedules
 */

// import Nevow.Athena
// import globals
// import helpers


helpers.Widget.subclass(controlLights, 'ControlLightsWidget').methods(

	function __init__(self, node) {
		controlLights.ControlLightsWidget.upcall(self, '__init__', node);
	},

	/**
	 * 
	 * @param self is    <"Instance" of undefined.controlLights.ControlLightsWidget>
	 * @returns a deferred
	 */
	function ready(self) {
		
		function cb_widgetready(res) {
			// do whatever initialization needs here, 'show' for the widget is handled in superclass
			//Divmod.debug('---', 'controlLights.cb_widgready() was called. res = ' + res);
			self.hideControlLights();
		}
	
		//Divmod.debug('---', 'controlLights.ready() was called. ' + self);
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},

	/**
	 * This sends a message to the server to get the servers time.
	 * when the callback returns the time, it displays the time and schedules itself in 1 second. 
	 * 
	 * @param self
	 */
	function hideControlLights(self) {

		function cb_hideControlLights(p_json) {
			//Divmod.debug('---', 'controlLights.cb_hideControlLights() was called.');
			//var l_node = self.node;
			//console.log("l_node   %O", l_node);
			self.node.style.display = 'none';
		}
	
		//Divmod.debug('---', 'controlLights.hideControlLights() was called.');
		var l_defer = self.callRemote('getControlLights');
		l_defer.addCallback(cb_hideControlLights);
	}

);
