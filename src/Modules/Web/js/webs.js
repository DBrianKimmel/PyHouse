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

	// ============================================================================
	/**
     * Place the widget in the workspace.
	 * 
	 * @param self is    <"Instance" of undefined.logs.LogsWidget>
	 * @returns a deferred
	 */
	function ready(self) {
		function cb_widgetready(res) {
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
		//Divmod.debug('---', 'webs.showWidget() was called.');
		self.node.style.display = 'block';
	},
	function hideDataEntry(self) {
		self.nodeById('WebEntryDiv').style.display = 'none';		
	},
	function showDataEntry(self) {
		self.nodeById('WebEntryDiv').style.display = 'block';		
	},

	// ============================================================================
	/**
	 * Called from the root menu screen when the Web Server button was clicked.
	 */
	function startWidget(self) {
		function cb_startWidget(p_json) {
			//Divmod.debug('---', 'webs.cb_startWidget() was called.  JSON = ' + p_json);
			var l_obj = JSON.parse(p_json);
			self.fillEntry(l_obj);
		}
		function eb_startWidget(res) {
			Divmod.debug('---', 'webs.eb_startWidget() was called. ERROR = ' + res);
		}
		//Divmod.debug('---', 'webs.startWidget() was called.');
		self.showWidget()
        var l_defer = self.callRemote("getWebsData");  // call server @ web_webs.py
		l_defer.addCallback(cb_startWidget);
		l_defer.addErrback(eb_startWidget);
        return false;  // Stops the resetting of the server.
	},
	function fillEntry(self, p_obj) {
		//Divmod.debug('---', 'webs.fillEntry(1) was called.  Self:' + self);
		//console.log("webs.fillEntry() - Obj = %O", p_obj);
        self.nodeById('PortDiv').innerHTML = buildTextWidget('PortName', p_obj.WebPort);
		self.nodeById('WebEntryButtonsDiv').innerHTML = buildEntryButtons('handleDataOnClick', 'NoDelete');
	},
	function fetchEntry(self) {
		//Divmod.debug('---', 'webs.fetchEntry() was called. ');
        var l_data = {
            Port : fetchTextWidget(self, 'PortName'),
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
			//Divmod.debug('---', 'webs.cb_handleDataOnClick() was called.');
			self.showWidget();
		}
		function eb_handleDataOnClick(res){
			Divmod.debug('---', 'webs.eb_handleDataOnClick() was called. ERROR =' + res);
		}
		var l_ix = p_node.name;
		//Divmod.debug('---', 'webs.handleDataOnClick() was called. Node:' + l_ix);
		switch(l_ix) {
		case '10003':  // Change Button
	    	var l_json = JSON.stringify(self.fetchEntry());
			//Divmod.debug('---', 'webs.handleDataOnClick(Change) was called. JSON:' + l_json);
	        var l_defer = self.callRemote("saveWebData", l_json);  // @ web_lights
			l_defer.addCallback(cb_handleDataOnClick);
			l_defer.addErrback(eb_handleDataOnClick);
			break;
		case '10002':  // Back button
			//Divmod.debug('---', 'webs.handleDataOnClick(Back) was called.  ');
			self.hideWidget();
			var l_node = findWidgetByClass('RootMenu');
			l_node.startWidget();
			break;
		default:
			Divmod.debug('---', 'webs.handleDataOnClick(Default) was called. l_ix:' + l_ix);
			break;			
		}
        return false;  // false stops the chain.
	}
);
// ### END DBK
