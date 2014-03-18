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

	// ============================================================================
	/**
     * Place the widget in the workspace.
	 * 
	 * @param self is    <"Instance" of undefined.logs.LogsWidget>
	 * @returns a deferred
	 */
	function ready(self) {
		function cb_widgetready(res) {
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
		//Divmod.debug('---', 'logs.showWidget() was called.');
		self.node.style.display = 'block';
	},
	function hideEntry(self) {
		self.nodeById('LogEntryDiv').style.display = 'none';		
	},
	function showEntry(self) {
		self.nodeById('LogEntryDiv').style.display = 'block';		
	},

	// ============================================================================
	/**
	 * Called from the root menu screen when the Logs button was clicked.
	 */
	function startWidget(self) {
		function cb_startWidget(p_json) {
			//Divmod.debug('---', 'logs.cb_startWidget() was called.  JSON = ' + p_json);
			var l_obj = JSON.parse(p_json);
			self.fillEntry(l_obj);
		}
		function eb_startWidget(res) {
			Divmod.debug('---', 'logs.eb_startWidget() was called. ERROR = ' + res);
		}
		//Divmod.debug('---', 'logs.startWidget() was called.');
		self.showWidget()
        var l_defer = self.callRemote("getLogData");  // call server @ web_logs.py
		l_defer.addCallback(cb_startWidget);
		l_defer.addErrback(eb_startWidget);
        return false;  // Stops the resetting of the server.
	},
	function fillEntry(self, p_obj) {
		//Divmod.debug('---', 'logs.fillEntry() was called. ');
		//console.log("logs.fillEntry() - Obj = %O", p_obj);
        self.nodeById('DebugDiv').innerHTML = buildTextWidget('LogDebug', p_obj.Debug);
        self.nodeById('ErrorDiv').innerHTML = buildTextWidget('LogError', p_obj.Error);
		self.nodeById('LogEntryButtonsDiv').innerHTML = buildEntryButtons('handleDataOnClick', 'NoDelete');
	},
	function fetchEntry(self) {
		Divmod.debug('---', 'lights.fetchEntry() was called. ');
        var l_data = {
                Debug : fetchTextWidget('LogDebug'),
                Error : fetchTextWidget('LogError'),
            }
		return l_data;
	},

	// ============================================================================
	/**
	 * Event handler for buttons at bottom of the data entry portion of this widget.
	 * Get the possibly changed data and send it to the server.
	 */
	function handleDataOnClick(self, p_node) {
		function cb_handleDataOnClick(p_json) {
			//Divmod.debug('---', 'logs.cb_handleDataOnClick() was called.');
			self.showWidget();
		}
		function eb_handleDataOnClick(res){
			Divmod.debug('---', 'logs.eb_handleDataOnClick() was called. ERROR =' + res);
		}
		var l_ix = p_node.name;
		//Divmod.debug('---', 'logs.handleDataOnClick() was called. Node:' + l_ix);
		switch(l_ix) {
		case '10003':  // Change Button
	    	var l_json = JSON.stringify(self.fetchEntry());
			//Divmod.debug('---', 'logs.handleDataOnClick(Change) was called. JSON:' + l_json);
	        var l_defer = self.callRemote("saveLogData", l_json);  // @ web_lights
			l_defer.addCallback(cb_handleDataOnClick);
			l_defer.addErrback(eb_handleDataOnClick);
			break;
		case '10002':  // Back button
			//Divmod.debug('---', 'logs.handleDataOnClick(Back) was called.  ');
			self.hideWidget();
			var l_node = findWidgetByClass('RootMenu');
			l_node.startWidget();
			break;
		default:
			Divmod.debug('---', 'logs.handleDataOnClick(Default) was called. l_ix:' + l_ix);
			break;			
		}
        return false;  // false stops the chain.
	}
);
/* ### END */
