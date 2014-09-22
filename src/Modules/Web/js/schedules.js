/**
 * schedules.js
 *
 * The Schedule widget.
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
			Divmod.debug('---', 'schedules.cb_fetchHouseData  was called. ');
			globals.House.HouseObj = JSON.parse(p_json);
			var l_tab = buildTable(globals.House.HouseObj.Schedules, 'handleMenuOnClick', self.buildButtonName);
			self.nodeById('ScheduleTableDiv').innerHTML = l_tab;
		}
		function eb_fetchHouseData(res) {
			Divmod.debug('---', 'schedules.eb_fetchHouseData() was called.  ERROR: ' + res);
		}
		Divmod.debug('---', 'schedules.fetchHouseData  was called. ');
        var l_defer = self.callRemote("getHouseData");  // call server @ web_schedules.py
		l_defer.addCallback(cb_fetchHouseData);
		l_defer.addErrback(eb_fetchHouseData);
        return false;
	},

	/**
	 * Fill in the schedule entry screen with all of the data for this schedule.
	 */
	function fillEntry(self, p_obj) {
		//Divmod.debug('---', 'schedules.fillEntry() was called. ' + p_obj);
        self.nodeById('NameDiv').innerHTML     = buildTextWidget('ScheduleName', p_obj.Name);
        self.nodeById('KeyDiv').innerHTML      = buildTextWidget('ScheduleKey', p_obj.Key, 'disabled');
		self.nodeById('ActiveDiv').innerHTML   = buildTrueFalseWidget('ScheduleActive', p_obj.Active);
		self.nodeById('UUIDDiv').innerHTML     = buildTextWidget('ScheduleUUID', p_obj.UUID, 'disabled');
		self.nodeById('TypeDiv').innerHTML     = buildTextWidget('ScheduleType', p_obj.Type);  // s/b select box of valid types
		self.nodeById('TimeDiv').innerHTML     = buildTextWidget('ScheduleTime', p_obj.Time);
		
		self.nodeById('RoomNameDiv').innerHTML = buildRoomSelectWidget('ScheduleRoomName', p_obj.RoomName, 'disabled');
		self.nodeById('LightNameDiv').innerHTML = buildLightNameSelectWidget('ScheduleLightName', p_obj.LightName, 'disabled');
		self.nodeById('LevelDiv').innerHTML    = buildLevelSliderWidget('ScheduleLevel', p_obj.Level);
		self.nodeById('RateDiv').innerHTML     = buildTextWidget('ScheduleRate', p_obj.Rate, 'disabled');
		self.nodeById('ScheduleEntryButtonsDiv').innerHTML = buildEntryButtons('handleDataOnClick');
	},

	function fetchEntry(self) {
		//Divmod.debug('---', 'schedules.fetchEntry() was called. ');
        var l_data = {
            Name      : fetchTextWidget('ScheduleName'),
            Key       : fetchTextWidget('ScheduleKey'),
			Active    : fetchTrueFalseWidget('ScheduleActive'),
			RoomName  : fetchSelectWidget('ScheduleRoomName'),
			ScheduleType : fetchTextWidget('ScheduleType'),
			UUID      : fetchTextWidget('ScheduleUUID'),

			// be sure to strip any leading or trailing white space and lower case text
			Time      : fetchTextWidget('ScheduleTime'),
			Level     : fetchLevelWidget('ScheduleLevel'),
			Rate      : fetchTextWidget('ScheduleRate'),
			RoomName  : fetchSelectWidget('ScheduleRoomName'),
			LightName : fetchSelectWidget('ScheduleLightName'),
			Delete : false
        }
		return l_data;
	},
	function createEntry(self) {
		//Divmod.debug('---', 'schedules.createEntry() was called.);
        var l_data = {
			Name : 'Change Me',
			Key : Object.keys(globals.House.HouseObj.Schedules).length,
			Active : false,
			UUID : '',
			ScheduleType : '',
			Time : '',
			DOW : 127,
			Mode : 0,
			Level : 0,
			Rate : 0,
			RoomName : '',
			LightName : '',
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
		globals.House.ScheduleIx = l_ix;
		globals.House.ScheduleName = l_name;
		if (l_ix <= 1000) {
			// One of the schedule buttons.
			var l_obj = globals.House.HouseObj.Schedules[l_ix];
			globals.House.ScheduleObj = l_obj;
			self.showEntry();
			self.hideButtons();
			self.fillEntry(l_obj);
		} else if (l_ix == 10001) {
			// The "Add" button
			//Divmod.debug('---', 'schedules.handleMenuOnClick(Add Button) was called. ' + l_ix + ' ' + l_name);
			self.showEntry();
			self.hideButtons();
			var l_ent = self.createEntry();
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
// ### END DBK
