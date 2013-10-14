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
			self.hideWidget();
		}
	
		//Divmod.debug('---', 'buttons.ready() was called. ' + self);
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
		//Divmod.debug('---', 'buttons.hideButtons() was called. ');
		self.nodeById('ButtonButtonsDiv').style.display = 'none';		
	},
	function showButtons(self) {
		//Divmod.debug('---', 'buttons.showButtons() was called. ');
		self.nodeById('ButtonButtonsDiv').style.display = 'block';	
	},
	function hideEntry(self) {
		//Divmod.debug('---', 'buttons.hideEntry() was called. ');
		self.nodeById('ButtonEntryDiv').style.display = 'none';		
	},
	function showEntry(self) {
		//Divmod.debug('---', 'buttons.showEntry() was called. ');
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
		function cb_fetchButtonData(self, p_json, p2) {
			//Divmod.debug('---', 'buttons.cb_fetchButtonData() was called. ' + p_json + ' ' + p2);
		}
		function eb_fetchButtonData(self, p1, p2) {
			//Divmod.debug('---', 'buttons.eb_fetchButtonData() was called. ' + p1 + ' ' + p2);
		}
        var l_defer = self.callRemote("getButtonData", globals.House.HouseIx);  // call server @ web_buttons.py
		l_defer.addCallback(cb_fetchButtonData);
		l_defer.addErrback(eb_fetchButtonData);
        return false;
	},

	
	/**
	 * Fill in the button entry screen with all of the data for this button.
	 */
	function fillEntry(self, p_entry) {
		var sched = arguments[1];
		//Divmod.debug('---', 'buttons.fillEntry() was called. ' + sched);
		self.nodeById('Name').value = sched.Name;
		self.nodeById('Key').value = sched.Key;
		self.nodeById('Active').value = sched.Active;  // s/b radio buttons
		self.nodeById('Type').value = sched.Type;  // s/b select box of valid types
		self.nodeById('Time').value = sched.Time;
		self.nodeById('Level').value = sched.Level;  // s/b a slider with value box
		self.nodeById('Rate').value = sched.Rate;
		self.nodeById('RoomName').value = sched.RoomName;  // s/b a select box
		self.nodeById('LightName').value = sched.LightName;  // s/b a select box
	},
	
	function fetchEntry(self) {
        var l_buttonData = {
			Name : self.nodeById('Name').value,
			Key : self.nodeById('Key').value,
			Active : self.nodeById('Active').value,
			Type : self.nodeById('Type').value,
			Time : self.nodeById('Time').value,
			Level : self.nodeById('Level').value,
			Rate : self.nodeById('Rate').value,
			RoomName : self.nodeById('RoomName').value,
			LightName : self.nodeById('LightName').value,
			HouseIx : globals.House.HouseIx
            }
		return l_buttonData;
	},

	/**
	 * Event handler for button selection buttons.
	 * 
	 * The user can click on a button button, the "Add" button or the "Back" button.
	 * 
	 * @param self is    <"Instance" of undefined.buttons.ButtonsWidget>
	 * @param p_node is  the node of the button that was clicked.
	 */
	function doHandleOnClick(self, p_node) {
		var l_ix = p_node.name;
		var l_name = p_node.value;
		globals.House.ButtonIx = l_ix;
		globals.House.ButtonName = l_name;
		if (l_ix <= 1000) {
			// One of the button buttons.
			var l_obj = globals.House.HouseObj.Buttons[l_ix];
			//Divmod.debug('---', 'buttons.doHandleOnClick(1) was called. ' + l_ix + ' ' + l_name);
			console.log("buttons.doHandleOnClick() - l_obj = %O", l_obj);
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
	function doHandleSubmit(self, p_node) {
		//Divmod.debug('---', 'buttons.doHandleSubmit() was called. ');
		//console.log("buttons.doHandleSubmit() - self %O", self);
		//console.log("buttons.doHandleSubmit() - node %O", p_node);
		
		function cb_doHandleSubmit(p_json) {
			//Divmod.debug('---', 'button.cb_doHandleSubmit() was called.');
			self.showWidget(self);
		}
		function eb_doHandleSubmit(res){
			//Divmod.debug('---', 'button.eb_doHandleSubmit() was called. res=' + res);
		}
    	var l_json = JSON.stringify(self.fetchEntry(self));
		//Divmod.debug('---', 'scedule.doHandleSubmit(1) was called. json:' + l_json);
        var l_defer = self.callRemote("doButtonSubmit", l_json);  // @ web_button
		l_defer.addCallback(cb_doHandleSubmit);
		l_defer.addErrback(eb_doHandleSubmit);
		// return false stops the resetting of the server.
        return false;
	},

	// ============================================================================
	/**
	 * Pushed from the server. fill in the table and wait for an event to happen (doHandleOnClick).
	 */
	function displayButtonButtons(self, p_json) {
		//Divmod.debug('---', 'buttons.displayButtonButtons(1) was called. ');
		globals.House.HouseObj.Buttons = JSON.parse(p_json);
		var l_tab = buildTable(self, globals.House.HouseObj.Buttons, '');
		self.nodeById('ButtonTableDiv').innerHTML = l_tab;
	}
);
