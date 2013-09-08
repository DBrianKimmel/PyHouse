/* buttons.js
 * 
 * Displays the buttons
 */

// import Nevow.Athena
// import globals
// import helpers


helpers.Widget.subclass(buttons, 'ButtonsWidget').methods(

	function __init__(self, node) {
		buttons.ButtonsWidget.upcall(self, '__init__', node);
	},

	/**
	 * 
	 * @param self is    <"Instance" of undefined.buttons.ButtonsWidget>
	 * @returns a deferred
	 */
	function ready(self) {
		
		function cb_widgetready(res) {
			// do whatever initialization needs here, 'show' for the widget is handled in superclass
			//Divmod.debug('---', 'buttons.cb_widgready() was called. res = ' + res);
			self.hideButtons();
		}
	
		//Divmod.debug('---', 'buttons.ready() was called. ' + self);
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},

	function hideButtons(self) {
		//Divmod.debug('---', 'buttons.hideButtons() was called.');
		self.node.style.display = 'none';
	}

);
