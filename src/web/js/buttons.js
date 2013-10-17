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
			self.hideWidget();
		}
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},

	/**
	 * routines for showing and hiding parts of the screen.
	 */
	function showWidget(self) {
		//Divmod.debug('---', 'buttons.showWidget() was called.');
		self.node.style.display = 'block';
		self.showButtons(self);
		self.hideEntry(self);
		self.fetchButtonData(self, globals.House.HouseIx);
	},
	function hideButtons(self) {
		self.nodeById('ButtonButtonsDiv').style.display = 'none';		
	},
	function showButtons(self) {
		self.nodeById('ButtonButtonsDiv').style.display = 'block';	
	},
	function hideEntry(self) {
		self.nodeById('ButtonEntryDiv').style.display = 'none';		
	},
	function showEntry(self) {
		self.nodeById('ButtonEntryDiv').style.display = 'block';		
	},

	// ============================================================================
	/**
	 * This triggers getting the button data from the server.
	 * The server calls displayButtonButtons with the buttons info.
	 * 
	 * @param p_houseIndex is the house index that was selected
	 */
	function fetchButtonData(self, p_houseIndex) {
		function cb_fetchButtonData(p_json) {
			//Divmod.debug('---', 'buttons.cb_fetchButtonData() was called. ' + p_json);
			globals.House.HouseObj = JSON.parse(p_json);
			var l_tab = buildTable(globals.House.HouseObj.Buttons, 'handleMenuOnClick');
			self.nodeById('ButtonTableDiv').innerHTML = l_tab;
		}
		function eb_fetchButtonData(res) {
			Divmod.debug('---', 'buttons.eb_fetchButtonData() was called.  ERROR - ' + res);
		}
        var l_defer = self.callRemote("getButtonData", globals.House.HouseIx);  // call server @ web_buttons.py
		l_defer.addCallback(cb_fetchButtonData);
		l_defer.addErrback(eb_fetchButtonData);
        return false;
	},

	
	/**
	 * Fill in the button entry screen with all of the data for this button.
	 */
	function fillEntry(self, p_obj) {
		//Divmod.debug('---', 'buttons.fillEntry() was called. ' + p_obj);
		self.nodeById('NameDiv').innerHTML = buildTextWidget('ButtonName', p_obj.Name);
		self.nodeById('KeyDiv').innerHTML = buildTextWidget('ButtonKey', p_obj.Key, 'disabled');
		self.nodeById('ActiveDiv').innerHTML = buildTrueFalseWidget('ButtonActive', p_obj.Active);
		self.nodeById('CommentDiv').innerHTML = buildTextWidget('ButtonComment', p_obj.Comment);
		self.nodeById('CoordsDiv').innerHTML = buildTextWidget('ButtonCoords', p_obj.Coords);
		self.nodeById('FamilyDiv').innerHTML = buildTextWidget('ButtonFamily', p_obj.Family);
		self.nodeById('RoomNameDiv').innerHTML = buildRoomSelectWidget('ButtonRoomName', p_obj.RoomName);
		self.nodeById('TypeDiv').innerHTML = buildTextWidget('ButtonType', p_obj.Type);  // s/b select box of valid types
		self.nodeById('UUIDDiv').innerHTML = buildTextWidget('ButtonUUID', p_obj.UUID, 'disabled');
		self.nodeById('ButtonEntryButtonsDiv').innerHTML = buildEntryButtons('handleDataOnClick');
	},
	function fetchEntry(self) {
        var l_data = {
			Name : fetchTextWidget('ButtonName'),
			Key : fetchTextWidget('ButtonKey'),
			Active : fetchTrueFalse('ButtonActive'),
			Comment : fetchTextWidget('ButtonComment'),
			Coords : fetchTextWidget('ButtonCoords'),
			Family : fetchTextWidget('ButtonFamily'),
			RoomName : fetchSelectWidget('ButtonRoomName'),
			Type : fetchTextWidget('ButtonType'),
			UUID : fetchTextWidget('ButtonUUID'),
			HouseIx : globals.House.HouseIx,
			Delete : false
            }
		return l_data;
	},

	/**
	 * Event handler for button selection buttons.
	 * 
	 * The user can click on a button button, the "Add" button or the "Back" button.
	 * 
	 * @param self is    <"Instance" of undefined.buttons.ButtonsWidget>
	 * @param p_node is  the node of the button that was clicked.
	 */
	function handleMenuOnClick(self, p_node) {
		var l_ix = p_node.name;
		var l_name = p_node.value;
		globals.House.ButtonIx = l_ix;
		globals.House.ButtonName = l_name;
		if (l_ix <= 1000) {
			// One of the button buttons.
			var l_obj = globals.House.HouseObj.Buttons[l_ix];
			//Divmod.debug('---', 'buttons.handleMenuOnClick(1) was called. ' + l_ix + ' ' + l_name);
			//console.log("buttons.handleMenuOnClick() - l_obj = %O", l_obj);
			self.showEntry();
			self.hideButtons();
			self.fillEntry(l_obj);
		} else if (l_ix == 10001) {
			// The "Add" button
			self.showEntry();
			self.hideButtons();
		} else if (l_ix == 10002) {
			// The "Back" button
			self.hideWidget();
			var l_node = findWidgetByClass('HouseMenu');
			l_node.showWidget();
		}
	},
	
	/**
	 * Event handler for submit buttons at bottom of entry portion of this widget.
	 * Get the possibly changed data and send it to the server.
	 */
	function handleDataOnClick(self, p_node) {
		//Divmod.debug('---', 'buttons.handleDataOnClick() was called. ');
		//console.log("buttons.handleDataOnClick() - self %O", self);
		//console.log("buttons.handleDataOnClick() - node %O", p_node);
		
		function cb_handleDataOnClick(p_json) {
			//Divmod.debug('---', 'button.cb_handleDataOnClick() was called.');
			self.showWidget(self);
		}
		function eb_handleDataOnClick(res){
			//Divmod.debug('---', 'button.eb_handleDataOnClick() was called. res=' + res);
		}
		var l_ix = p_node.name;
		switch(l_ix) {
		case '10003':  // Change Button
	    	var l_json = JSON.stringify(self.fetchEntry(self));
			//Divmod.debug('---', 'buttons.handleDataOnClick(1) was called. json:' + l_json);
	        var l_defer = self.callRemote("saveButtonData", l_json);  // @ web_button
			l_defer.addCallback(cb_handleDataOnClick);
			l_defer.addErrback(eb_handleDataOnClick);
			break;
		case '10002':  // Back button
			//Divmod.debug('---', 'buttonss.handleDataOnClick(Back) was called.  ');
			self.hideEntry();
			self.showButtons();
			break;
		case '10004':  // Delete button
			var l_obj = self.fetchEntry();
			l_obj['Delete'] = true;
	    	var l_json = JSON.stringify(l_obj);
			//Divmod.debug('---', 'buttons.handleDataOnClick(Delete) was called. JSON:' + l_json);
	        var l_defer = self.callRemote("saveButtonData", l_json);  // @ web_rooms
			l_defer.addCallback(cb_handleDataOnClick);
			l_defer.addErrback(eb_handleDataOnClick);
			break;
		default:
			Divmod.debug('---', 'buttons.handleDataOnClick(Default) was called. l_ix:' + l_ix);
			break;			
		}
        return false;  // false stops the chain.
	}
);
