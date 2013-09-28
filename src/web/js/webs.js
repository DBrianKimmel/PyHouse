/**
 * webs.js
 * 
 * version 1.00
 * 
 * D. Brian Kimmel
 * 
	ret = ret + '<form method="post" action="_submit!!post" enctype="multipart/form-data">\n';
	ret = ret +	'  Web Port:';
	ret = ret +	'    <input type = "text" name = "WebPort" value = "' + p_port + '" /><br />\n';
	ret = ret +	'  <br />\n';
	ret = ret + '  <input type="submit" name="post_btn" value="Change_Web Port" />\n';
	ret = ret + '</form>\n';
 */

// import Nevow.Athena
// import globals
// import helpers

/**
 * The Logs widget.
 * 
 */

helpers.Widget.subclass(webs, 'WebsWidget').methods(
		
	function __init__(self, node) {
		webs.WebsWidget.upcall(self, '__init__', node);
	},

	/**
     * Place the widget in the workspace.
	 * 
	 * @param self is    <"Instance" of undefined.logs.LogsWidget>
	 * @returns a deferred
	 */
	function ready(self) {
		
		function cb_widgetready(res) {
			// do whatever initialization needs here, 'show' for the widget is handled in superclass
			//Divmod.debug('---', 'webs.cb_widgready() was called.');
			self.hideWidget();
		}
		//Divmod.debug('---', 'webs.ready() was called. ' + self);
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},
	
	function showWidget(self) {
		Divmod.debug('---', 'webs.showWidget() was called.');
		self.node.style.display = 'block';
		//self.fetchScheduleData(self, globals.SelectedHouse.Ix);
	}
);
// ### END DBK
