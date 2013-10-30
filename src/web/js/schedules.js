/* schedules.js
 * 
 * The schedule widget.
 * 
 * This widget has 2 parts:
 *   1. The schedule selection section which shows a button for each schedule and allows one to add a new schedule.
 *   2. The schedule data section which allows entering/changing all the detail about the selected schedule.
 *      It also allows the schedule to be deleted.
 */

// import Nevow.Athena
// import globals
// import helpers

helpers.Widget.subclass(schedules, 'SchedulesWidget').methods(
		
	function __init__(self, node) {
		//Divmod.debug('---', 'schedules.__init__() was called. - self=' + self + "  node=" + node);
		schedules.SchedulesWidget.upcall(self, '__init__', node);
	},

	/**
     * Place the widget in the workspace.
	 * 
	 * @param self is    <"Instance" of undefined.schedules.SchedulesWidget>
	 * @returns a deferred
	 */
	function ready(self) {
		function cb_widgetready(res) {
			//Divmod.debug('---', 'schedules.cb_widgready() was called. - res='  + res);
			self.hideWidget();
		}
		//Divmod.debug('---', 'scheduless.ready() was called. ');
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},
	
	/**
	 * routines for showing and hiding parts of the screen.
	 */
	function showWidget(self) {
		self.node.style.display = 'block';
		self.showButtons();
		self.hideEntry();
		self.fetchHouseData();
	},
	function hideButtons(self) {
		self.nodeById('ScheduleButtonsDiv').style.display = 'none';		
	},
	function showButtons(self) {
		self.nodeById('ScheduleButtonsDiv').style.display = 'block';	
	},
	function hideEntry(self) {
		self.nodeById('ScheduleEntryDiv').style.display = 'none';		
	},
	function showEntry(self) {
		self.nodeById('ScheduleEntryDiv').style.display = 'block';		
	},

	function buildButtonName(self, p_obj) {
		//Divmod.debug('---', 'schedules.buildButtonName(1) was called. ');
		var l_html = p_obj['Name'];
		l_html += '<br>' + p_obj['RoomName'];
		l_html += '<br>' + p_obj['LightName'];
		l_html += '<br>' + p_obj['Level'] + '% ';
		return l_html;
	},

	// ============================================================================
	/**
	 * This triggers getting the schedule data from the server.
	 */
	function fetchHouseData(self) {
		function cb_fetchHouseData(p_json) {
			//Divmod.debug('---', 'schedules.cb_fetchHouseData() was called. ');
			globals.House.HouseObj = JSON.parse(p_json);
			var l_tab = buildTable(globals.House.HouseObj.Schedules, 'handleMenuOnClick', self.buildButtonName);
			self.nodeById('ScheduleTableDiv').innerHTML = l_tab;
		}
		function eb_fetchHouseData(res) {
			Divmod.debug('---', 'schedules.eb_fetchHouseData() was called.  ERROR: ' + res);
		}
		//Divmod.debug('---', 'schedules.fetchHouseData() was called. Ix: ' + p_houseIndex);
        var l_defer = self.callRemote("getHouseData", globals.House.HouseIx);  // call server @ web_schedules.py
		l_defer.addCallback(cb_fetchHouseData);
		l_defer.addErrback(eb_fetchHouseData);
        return false;
	},

	/**
	 * Fill in the schedule entry screen with all of the data for this schedule.
	 */
	function fillEntry(self, p_obj) {
		//Divmod.debug('---', 'schedules.fillEntry() was called. ' + p_obj);
		self.nodeById('Name').value = p_obj.Name;
		self.nodeById('Key').value = p_obj.Key;
		self.nodeById('ActiveDiv').innerHTML = buildTrueFalseWidget('SchedActive', p_obj.Active);
		self.nodeById('Type').value = p_obj.Type;  // s/b select box of valid types
		self.nodeById('Time').value = p_obj.Time;
		self.nodeById('LevelDiv').innerHTML = buildLevelSlider(p_obj.Level);
		self.nodeById('Rate').value = p_obj.Rate;
		self.nodeById('RoomNameDiv').innerHTML = buildRoomSelectWidget('SchedRoomName', p_obj.RoomName);
		self.nodeById('LightNameDiv').innerHTML = buildLightSelectWidget('SchedLightName', p_obj.LightName);
		self.nodeById('UUID').value = p_obj.UUID;
		self.nodeById('ScheduleEntryButtonsDiv').innerHTML = buildEntryButtons('handleDataOnClick');
	},
	
	function fetchEntry(self) {
		//Divmod.debug('---', 'schedules.fetchEntry() was called. ');
        var l_data = {
			Name : self.nodeById('Name').value,
			Key : self.nodeById('Key').value,
			Active : fetchTrueFalseWidget('SchedActive'),
			Type : self.nodeById('Type').value,
			Time : self.nodeById('Time').value,
			Level : fetchLevel('Level'),
			Rate : self.nodeById('Rate').value,
			RoomName : fetchSelectWidget('SchedRoomName'),
			LightName : fetchSelectWidget('SchedLightName'),
			UUID : self.nodeById('UUID').value,
			HouseIx : globals.House.HouseIx,
			Delete : false
        }
		return l_data;
	},
	function createEntry(self, p_ix) {
		//Divmod.debug('---', 'schedules.createEntry() was called.  Ix: ' + p_ix);
        var l_data = {
			Name : 'Change Me',
			Key : Object.keys(globals.House.HouseObj.Schedules).length,
			Active : false,
			Type : '',
			Time : '',
			Level : 0,
			Rate : 0,
			RoomName : '',
			LightName : '',
			UUID : '',
			HouseIx : p_ix,
			Delete : false
        }
		return l_data;
	},

	/**
	 * Event handler for schedule selection buttons.
	 * 
	 * The user can click on a schedule button, the "Add" button or the "Back" button.
	 * 
	 * @param self is    <"Instance" of undefined.schedules.SchedulesWidget>
	 * @param p_node is  the node of the button that was clicked.
	 */
	function handleMenuOnClick(self, p_node) {
		var l_ix = p_node.name;
		var l_name = p_node.value;
		//Divmod.debug('---', 'schedules.handleMenuOnClick() was called. ' + l_ix + ' ' + l_name);
		globals.House.ScheduleIx = l_ix;
		globals.House.ScheduleName = l_name;
		if (l_ix <= 1000) {
			// One of the schedule buttons.
			var l_obj = globals.House.HouseObj.Schedules[l_ix];
			globals.House.ScheduleObj = l_obj;
			//Divmod.debug('---', 'schedules.handleMenuOnClick("Schedule" Button) was called. ' + l_ix + ' ' + l_name);
			//console.log("schedules.doHandleOnClick() - l_obj = %O", l_obj);
			self.showEntry();
			self.hideButtons();
			self.fillEntry(l_obj);
		} else if (l_ix == 10001) {
			// The "Add" button
			//Divmod.debug('---', 'schedules.handleMenuOnClick(Add Button) was called. ' + l_ix + ' ' + l_name);
			self.showEntry();
			self.hideButtons();
			var l_ent = self.createEntry(globals.House.HouseIx);
			self.fillEntry(l_ent);
		} else if (l_ix == 10002) {
			// The "Back" button
			//Divmod.debug('---', 'schedules.handleMenuOnClick(Back Button) was called. ' + l_ix + ' ' + l_name);
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
		function cb_handleDataOnClick(p_json) {
			//Divmod.debug('---', 'schedules.cb_handleDataOnClick() was called.');
			self.showWidget();
		}
		function eb_handleDataOnClick(res){
			Divmod.debug('---', 'schedules.eb_handleDataOnClick() was called. ERROR =' + res);
		}
		var l_ix = p_node.name;
		//Divmod.debug('---', 'schedules.handleDataOnClick() was called. Node:' + l_ix);
		switch(l_ix) {
		case '10003':  // Change Button
	    	var l_json = JSON.stringify(self.fetchEntry());
			//Divmod.debug('---', 'schedules.handleDataOnClick(Change) was called. JSON:' + l_json);
	        var l_defer = self.callRemote("saveScheduleData", l_json);  // @ web_schedule
			l_defer.addCallback(cb_handleDataOnClick);
			l_defer.addErrback(eb_handleDataOnClick);
			break;
		case '10002':  // Back button
			//Divmod.debug('---', 'schedules.handleDataOnClick(Back) was called.  ');
			self.hideEntry();
			self.showButtons();
			break;
		case '10004':  // Delete button
			var l_obj = self.fetchEntry();
			l_obj['Delete'] = true;
	    	var l_json = JSON.stringify(l_obj);
			//Divmod.debug('---', 'schedules.handleDataOnClick(Delete) was called. JSON:' + l_json);
	        var l_defer = self.callRemote("saveScheduleData", l_json);  // @ web_rooms
			l_defer.addCallback(cb_handleDataOnClick);
			l_defer.addErrback(eb_handleDataOnClick);
			break;
		default:
			Divmod.debug('---', 'schedules.handleDataOnClick(Default) was called. l_ix:' + l_ix);
			break;			
		}
		// return false stops the resetting of the server.
        return false;
	}
);
