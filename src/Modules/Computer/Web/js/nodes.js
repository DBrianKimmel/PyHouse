/**
 * @name: PyHouse/src/Modules/Web/js/nodes.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @copyright: (c) 2012-2017 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created about 2012
 * @summary: Displays the Nodes element
 * 
 */

helpers.Widget.subclass(nodes, 'NodesWidget').methods(

function __init__(self, node) {
	nodes.NodesWidget.upcall(self, '__init__', node);
},

// ============================================================================
/**
 * Place the widget in the workspace.
 * 
 * @param self
 *            is <"Instance" of undefined.nodes.NodesWidget>
 * @returns a deferred
 */
function ready(self) {
	function cb_widgetready(res) {
		self.hideWidget();
	}
	var uris = collectIMG_src(self.node, null);
	var l_defer = loadImages(uris);
	l_defer.addCallback(cb_widgetready);
	return l_defer;
},
/**
 * Show the self.node widget - nodes.NodesWidget -
 */
function startWidget(self) {
	self.node.style.display = 'block';
	showSelectionButtons(self);
	self.fetchDataFromServer();
},

// ============================================================================
/**
 * This triggers getting the data from the server.
 */
function fetchDataFromServer(self) {
	function cb_fetchDataFromServer(p_json) {
		globals.Computer = JSON.parse(p_json);
		self.buildLcarSelectScreen();
	}
	function eb_fetchDataFromServer(p_result) {
		Divmod.debug('---', 'nodes.eb_fetchDataFromServer() was called. ERROR = ' + p_result);
	}
	var l_defer = self.callRemote("getServerData"); // @ web_rooms.py
	l_defer.addCallback(cb_fetchDataFromServer);
	l_defer.addErrback(eb_fetchDataFromServer);
	return false;
},
/**
 * Build a screen full of buttons - One for each room and some actions.
 */
function buildLcarSelectScreen(self) {
	var l_button_html = buildLcarSelectionButtonsTable(globals.Computer.Nodes, 'handleMenuOnClick');
	var l_html = build_lcars_top('Nodes', 'lcars-salmon-color');
	l_html += build_lcars_middle_menu(15, l_button_html);
	l_html += build_lcars_bottom();
	self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
},
/**
 * Event handler for selection buttons.
 * 
 * The user can click on a selection button, the "Add" button or the "Back"
 * button.
 * 
 * @param self
 *            is <"Instance" of undefined.nodes.NodesWidget>
 * @param p_node
 *            is the node of the button that was clicked.
 */
function handleMenuOnClick(self, p_node) {
	var l_ix = p_node.name;
	var l_name = p_node.value;
	Divmod.debug('---', 'nodes.handleMenuOnClick() was called. ' + l_ix + ' ' + l_name);
	globals.Computer.NodeIx = l_ix;
	globals.Computer.NodeName = l_name;
	console.log("nodes.handleMenuOnClick() - Globals = %O", globals);
	if (l_ix <= 1000) { // One of the nodes buttons.
		var l_obj = globals.Computer.Nodes[l_ix];
		globals.Computer.NodeObj = l_obj;
		showDataEntryScreen(self);
		self.buildDataEntryScreen(l_obj, 'handleDataEntryOnClick');
	} else if (l_ix == 10001) { // The "Add" button
		showDataEntryScreen(self);
		var l_entry = self.createEntry();
		self.buildDataEntryScreen(l_entry, 'handleDataEntryOnClick');
	} else if (l_ix == 10002) { // The "Back" button
		self.showWidget('ComputerMenu');
	}
},

// ============================================================================

function localBuildNodeEntry(self, p_obj, p_html) {
	p_html += buildTextWidget(self, 'Comment', 'Comment', p_obj.Comment);
	p_html += buildTextWidget(self, 'IPv4', 'IPv4 Address', p_obj.ConnectionAddr_IPv4);
	p_html += buildTextWidget(self, 'IPv6', 'IPv6 Address', p_obj.ConnectionAddr_IPv6);
	p_html += buildTextWidget(self, 'Role', 'Node Role', p_obj.NodeRole);
	return p_html;
},

function buildEntry(self, p_obj, p_handler) {
	Divmod.debug('---', 'nodes.buildEntry() was called ');
	console.log("nodes.buildEntry() Obj %O", p_obj);
	var l_html = '';
	l_html = buildBaseEntry(self, p_obj, l_html);
	l_html = localBuildNodeEntry(self, p_obj, l_html);
	l_html = buildLcarEntryButtons(self, p_handler, l_html);
	return l_html;
},

/**
 * Build a screen full of data entry fields.
 */
function buildDataEntryScreen(self, p_entry, p_handler) {
	Divmod.debug('---', 'nodes.buildDataEntryScreen() was called ' + p_entry);
	var l_obj = arguments[1];
	var l_html = build_lcars_top('Node Data', 'lcars-salmon-color');
	l_html += build_lcars_middle_menu(20, self.buildEntry(l_obj, p_handler));
	l_html += build_lcars_bottom();
	self.nodeById('DataEntryDiv').innerHTML = l_html;
},

function localFetchNodeEntry(p_data) {
	p_data.Comment = fetchTextWidget(self, 'Comment');
	p_data.ConnectionAddr_IPv4 = fetchTextWidget(self, 'IPv4');
	p_data.ConnectionAddr_IPv46 = fetchTextWidget(self, 'IPv6');
	p_data.NodeRole = fetchTextWidget(self, 'Role');
},

function fetchEntry(self) {
	var l_data = fetchBaseEntry(self);
	localFetchNodeEntry(l_data);
	return l_data;
},

function localCreateNodeEntry(p_data) {
	p_data.Comment = '';
	p_data.ConnectionAddr_IPv4 = '';
	p_data.ConnectionAddr_IPv6 = '';
	p_data.NodeRoll = 0;
},

function createEntry(self) {
	var l_data = createBaseEntry(self, Object.keys(globals.Computer.Nodes).length);
	localCreateNodeEntry(l_data);
	return l_data;
},

// ============================================================================
/**
 * Event handler for nodes buttons at bottom of entry portion of this widget.
 * Get the possibly changed data and send it to the server.
 * 
 * @param self
 *            is <"Instance" of undefined.nodess.NodesWidget>
 * @param p_node
 *            is the button node that was clicked on
 */
function handleDataEntryOnClick(self, p_node) {
	function cb_handleDataEntryOnClick(p_json) {
		self.startWidget();
	}
	function eb_handleDataEntryOnClick(p_reason) {
		Divmod.debug('---', 'nodes.eb_handleDataEntryOnClick() was called. ERROR =' + p_reason);
	}
	var l_ix = p_node.name;
	var l_defer;
	var l_json;
	switch (l_ix) {
	case '10003':  // Change Button
		l_json = JSON.stringify(self.fetchEntry());
		l_defer = self.callRemote("saveNodeData", l_json); // @ web_nodes
		l_defer.addCallback(cb_handleDataEntryOnClick);
		l_defer.addErrback(eb_handleDataEntryOnClick);
		break;
	case '10002':  // Back button
		showSelectionButtons(self);
		break;
	case '10004':  // Delete button
		var l_obj = self.fetchEntry();
		l_obj.Delete = true;
		l_json = JSON.stringify(l_obj);
		l_defer = self.callRemote("saveNodeData", l_json); // @web_nodes
		l_defer.addCallback(cb_handleDataEntryOnClick);
		l_defer.addErrback(eb_handleDataEntryOnClick);
		break;
	default:
		Divmod.debug('---', 'nodes.handleDataEntryOnClick(Default) was called. l_ix:' + l_ix);
		break;
	}
	// return false stops the resetting of the server.
	return false;
}

);

// Divmod.debug('---', 'nodes.handleMenuOnClick(1) was called. ' + l_ix + ' ' + l_name);
// console.log("nodes.handleMenuOnClick() - l_obj = %O", l_obj);

// ### END DBK
