/*
 * @name:      PyHouse/src/Modules/Web/js/buttons.js
 * @author:    D. Brian Kimmel
 * @contact:   D.BrianKimmel@gmail.com
 * @copyright: (c) 2014-2016 by D. Brian Kimmel
 * @license:   MIT License
 * @note:      Created on Mar 11, 2014
 * @summary:   Displays the buttons element
 *
 */

helpers.Widget.subclass(buttons, 'ButtonsWidget').methods(

	function __init__(self, node) {
		buttons.ButtonsWidget.upcall(self, '__init__', node);
	},


// ============================================================================
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
	function startWidget(self) {
		self.node.style.display = 'block';
		showSelectionButtons(self);
		self.fetchDataFromServer();
	},


// ============================================================================
	/**
	 * This triggers getting the button data from the server.
	 * The server calls displayButtonButtons with the buttons info.
	 */
	function fetchDataFromServer(self) {
		function cb_fetchDataFromServer(p_json) {
			globals.House = JSON.parse(p_json);
			self.buildLcarSelectScreen();
		}
		function eb_fetchDataFromServer(p_reason) {
			Divmod.debug('---', 'buttons.eb_fetchDataFromServer() was called.  ERROR - ' + p_reason);
		}
        var l_defer = self.callRemote("getHouseData");  // call server @ web_buttons.py
		l_defer.addCallback(cb_fetchDataFromServer);
		l_defer.addErrback(eb_fetchDataFromServer);
        return false;
	},
	/**
	 * Build a screen full of buttons - One for each Button and some actions.
	 */
	function buildLcarSelectScreen(self){
		var l_button_html = buildLcarSelectionButtonsTable(globals.House.Lighting.Buttons, 'handleMenuOnClick');
		var l_html = build_lcars_top('Buttons', 'lcars-salmon-color');
		l_html += build_lcars_middle_menu(10, l_button_html);
		l_html += build_lcars_bottom();
		self.nodeById('SelectionButtonsDiv').innerHTML = l_html;
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
        var l_obj;
		globals.House.ButtonIx = l_ix;
		globals.House.ButtonName = l_name;
		globals.Add = false;
		if (l_ix <= 1000) {  // One of the button buttons.
			l_obj = globals.House.Lighting.Buttons[l_ix];
			showDataEntryScreen(self);
			self.buildLcarSelectScreen(l_obj);
		} else if (l_ix == 10001) {  // The "Add" button
			globals.Add = true;
			showDataEntryScreen(self);
		} else if (l_ix == 10002) {  // The "Back" button
			self.showWidget('HouseMenu');
		}
	},
	// ============================================================================
	function fetchEntry(self) {
        var l_data = {
			Name : fetchTextWidget(self, 'ButtonName'),
			Key : fetchTextWidget(self, 'ButtonKey'),
			Active : fetchTrueFalseWidget(self,'ButtonActive'),
			Comment : fetchTextWidget(self, 'ButtonComment'),
			RoomCoords : fetchTextWidget(self, 'ButtonCoords'),
			Family : fetchTextWidget(self, 'ButtonFamily'),
			RoomName : fetchSelectWidget(self, 'ButtonRoomName'),
			Type : fetchTextWidget(self, 'ButtonType'),
			UUID : fetchTextWidget(self, 'ButtonUUID'),
			Delete : false
            };
		return l_data;
	},

	
	/**
	 * Event handler for submit buttons at bottom of entry portion of this widget.
	 * Get the possibly changed data and send it to the server.
	 */
	function handleDataOnClick(self, p_node) {
		function cb_handleDataOnClick(p_json) {
			Divmod.debug('---', 'button.cb_handleDataOnClick() was called.');
		}
		function eb_handleDataOnClick(res){
			//Divmod.debug('---', 'button.eb_handleDataOnClick() was called. res=' + res);
		}
		var l_defer;
		var l_ix = p_node.name;
		var l_json;
		var l_obj = self.fetchEntry();
		l_obj.Add = globals.Add;
		switch(l_ix) {
		case '10003':  // Change Button
	    	l_json = JSON.stringify(self.fetchEntry(self));
	        l_defer = self.callRemote("saveButtonData", l_json);  // @ web_button
			l_defer.addCallback(cb_handleDataOnClick);
			l_defer.addErrback(eb_handleDataOnClick);
			break;
		case '10002':  // Back button
			showSelectionButtons(self);
			break;
		case '10004':  // Delete button
			l_obj.Delete = true;
	    	l_json = JSON.stringify(l_obj);
			//Divmod.debug('---', 'buttons.handleDataOnClick(Delete) was called. JSON:' + l_json);
	        l_defer = self.callRemote("saveButtonData", l_json);  // @ web_rooms
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
// Divmod.debug('---', 'buttons.handleMenuOnClick(1) was called. ' + l_ix + ' ' + l_name);
// console.log("buttons.handleMenuOnClick() - l_obj = %O", l_obj);
// ### END DBK