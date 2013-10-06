/**
 * logs.js
 * 
 * version 1.00
 * 
 * D. Brian Kimmel
 * 
 * Displays the Logs
 * 
	ret = ret + '<form method="post" action="_submit!!post" enctype="multipart/form-data">\n';
	ret = ret +	'  Debug:';
	ret = ret +	'    <input type = "text" name = "Debug" value = "' + l_obj.Debug + '" /><br />\n';
	ret = ret +	'  Error:';
	ret = ret +	'    <input type = "text" name = "Error" value = "' + l_obj.Error + '" /><br />\n';
	ret = ret +	'  <br />\n';
	ret = ret + '  <input type="submit" name="post_btn" value="Change_Logs" />\n';
	ret = ret + '</form>\n';
 */

// import Nevow.Athena
// import globals
// import helpers

/**
 * The Logs widget.
 * 
 */

helpers.Widget.subclass(logs, 'LogsWidget').methods(
		
	function __init__(self, node) {
		logs.LogsWidget.upcall(self, '__init__', node);
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
			//Divmod.debug('---', 'logs.cb_widgready() was called.');
			self.hideWidget();
		}
		//Divmod.debug('---', 'logs.ready() was called. ' + self);
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},
	
	function showWidget(self) {
		Divmod.debug('---', 'logs.showWidget() was called.');
		self.node.style.display = 'block';
	}
);
/* ### END */
