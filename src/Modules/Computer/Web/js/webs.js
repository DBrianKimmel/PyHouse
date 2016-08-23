/**
 * @name:      PyHouse/src/Modules/Computer/Web/js/web.js
 * @author:    D. Brian Kimmel
 * @contact:   D.BrianKimmel@gmail.com
 * @copyright: (c) 2014-2016 by D. Brian Kimmel
 * @license:   MIT License
 * @note:      Created on June 18, 2014
 * @summary:   Displays the Web element
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
			self.hideWidget();
		}
		function eb_widgetready(p_reason) {
			Divmod.debug('---', 'ERROR - webs.eb_widgetready() - ' + p_reason);
		}
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		l_defer.addErrback(eb_widgetready);
		return l_defer;
	},
	function startWidget(self) {
		self.node.style.display = 'block';
		self.fetchDataFromServer();
	},

// ============================================================================
	/**
	 * Called from the computer menu screen when the Web Server button was clicked.
	 */
	function fetchDataFromServer(self) {
		function cb_fetchDataFromServer(p_json) {
			var l_obj = JSON.parse(p_json);
			self.fillEntry(l_obj);
		}
		function eb_fetchDataFromServer(res) {
			Divmod.debug('---', 'webs.eb_fetchDataFromServer() was called. ERROR = ' + res);
		}
        var l_defer = self.callRemote("getWebsData");  // call server @ web_webs.py
		l_defer.addCallback(cb_fetchDataFromServer);
		l_defer.addErrback(eb_fetchDataFromServer);
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
            };
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
			self.startWidget();
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
			self.showWidget('ComputerMenu');
			break;
		default:
			Divmod.debug('---', 'webs.handleDataOnClick(Default) was called. l_ix:' + l_ix);
			break;			
		}
        return false;  // false stops the chain.
	}
);
// ### END DBK
