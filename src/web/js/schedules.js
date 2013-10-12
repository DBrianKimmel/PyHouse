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
			// do whatever initialization needs here, 'show' for the widget is handled in superclass
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
		//Divmod.debug('---', 'schedules.showWidget() was called.');
		self.node.style.display = 'block';
		self.showButtons(self);
		self.hideEntry(self);
		self.fetchScheduleData(self, globals.SelectedHouse.Ix);
	},
	function hideButtons(self) {
		//Divmod.debug('---', 'schedules.hideButtons() was called. ');
		self.nodeById('ScheduleButtonsDiv').style.display = 'none';		
	},
	function showButtons(self) {
		//Divmod.debug('---', 'schedules.showButtons() was called. ');
		self.nodeById('ScheduleButtonsDiv').style.display = 'block';	
	},
	function hideEntry(self) {
		//Divmod.debug('---', 'schedules.hideEntry() was called. ');
		self.nodeById('ScheduleEntryDiv').style.display = 'none';		
	},
	function showEntry(self) {
		//Divmod.debug('---', 'schedules.showEntry() was called. ');
		self.nodeById('ScheduleEntryDiv').style.display = 'block';		
	},

	function buildButtonName(self, p_obj) {
		//Divmod.debug('---', 'schedules.buildButtonName(1) was called. ');
		var l_html = p_obj['Name']
		l_html += '<br>' + p_obj['RoomName']
		l_html += '<br>' + p_obj['LightName']
		l_html += '<br>' + p_obj['Level'] + '% '
		return l_html;
	},

	// ============================================================================
	/**
	 * This triggers getting the schedule data from the server.
	 * 
	 * @param p_houseIndex is the house index that was selected
	 */
	function fetchScheduleData(self, p_houseIndex) {
		function cb_fetchScheduleData(p_json) {
			//Divmod.debug('---', 'schedules.cb_fetchScheduleData() was called. ');
			globals.Schedules.Obj = JSON.parse(p_json);
			var l_tab = buildTable(globals.Schedules.Obj, 'handleMenuOnClick', self.buildButtonName);
			self.nodeById('ScheduleTableDiv').innerHTML = l_tab;
		}
		function eb_fetchScheduleData(res) {
			//Divmod.debug('---', 'schedules.eb_fetchScheduleData() was called. ' + res);
		}
		//Divmod.debug('---', 'schedules.fetchScheduleData() was called. ');
        var l_defer = self.callRemote("getScheduleData", globals.SelectedHouse.Ix);  // call server @ web_schedules.py
		l_defer.addCallback(cb_fetchScheduleData);
		l_defer.addErrback(eb_fetchScheduleData);
        return false;
	},

	/**
	 * Fill in the schedule entry screen with all of the data for this schedule.
	 */
	function fillEntry(self, p_entry) {
		var sched = arguments[2];
		//Divmod.debug('---', 'schedules.fillEntry() was called. ' + sched);
		self.nodeById('Name').value = sched.Name;
		self.nodeById('Key').value = sched.Key;
		self.nodeById('Active').innerHTML = buildActiveWidget(sched.Active);
		self.nodeById('Type').value = sched.Type;  // s/b select box of valid types
		self.nodeById('Time').value = sched.Time;
		self.nodeById('Level').innerHTML = buildLevelSlider(sched.Level);
		self.nodeById('Rate').value = sched.Rate;
		self.nodeById('RoomName').innerHTML = buildRoomSelectWidget(sched.RoomName);
		self.nodeById('LightName').innerHTML = buildLightSelectWidget(sched.LightName);
		self.nodeById('UUID').value = sched.UUID;
		self.nodeById('ScheduleEntryButtonsDiv').innerHTML = buildEntryButtons('handleDataOnClick');
	},
	
	function fetchEntry(self) {
        var l_scheduleData = {
			Name : self.nodeById('Name').value,
			Key : self.nodeById('Key').value,
			Active : fetchActive('Active'),
			Type : self.nodeById('Type').value,
			Time : self.nodeById('Time').value,
			Level : fetchLevel('Level'),
			Rate : self.nodeById('Rate').value,
			RoomName : fetchSelectWidget('RoomName'),
			LightName : fetchSelectWidget('LightName'),
			UUID : self.nodeById('UUID').value,
			HouseIx : globals.SelectedHouse.Ix,
			Delete : false
            }
		return l_scheduleData;
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
		globals.Schedules.Ix = l_ix;
		globals.Schedules.Name = l_name;
		if (l_ix <= 1000) {
			// One of the schedule buttons.
			var l_obj = globals.Schedules.Obj[l_ix];
			globals.Schedules.ScheduleObj = l_obj;
			//Divmod.debug('---', 'schedules.doHandleOnClick(1) was called. ' + l_ix + ' ' + l_name);
			//console.log("schedules.doHandleOnClick() - l_obj = %O", l_obj);
			self.showEntry(self);
			self.hideButtons(self);
			self.fillEntry(self, l_obj);
		} else if (l_ix == 10001) {
			// The "Add" button
			self.showEntry(self);
			self.hideButtons(self);
		} else if (l_ix == 10002) {
			// The "Back" button
			self.hideWidget();
			var l_node = findWidgetByClass('HouseMenu');
			l_node.showWidget(self);
		}
	},
	
	/**
	 * Event handler for submit buttons at bottom of entry portion of this widget.
	 * Get the possibly changed data and send it to the server.
	 */
	function handleDataOnClick(self, p_node) {
		function cb_doHandleSubmit(p_json) {
			//Divmod.debug('---', 'schedule.cb_handleDataOnClick() was called.');
			self.showWidget(self);
		}
		function eb_doHandleSubmit(res){
			Divmod.debug('---', 'schedule.eb_handleDataOnClick() was called. ERROR =' + res);
		}
		var l_ix = p_node.name;
		switch(l_ix) {
		case '10003':  // Change Button
	    	var l_json = JSON.stringify(self.fetchEntry(self));
			Divmod.debug('---', 'schedules.handleDataOnClick(Change) was called. JSON:' + l_json);
	        var l_defer = self.callRemote("saveScheduleData", l_json);  // @ web_schedule
			l_defer.addCallback(cb_doHandleSubmit);
			l_defer.addErrback(eb_doHandleSubmit);
			break;
		case '10002':  // Back button
			Divmod.debug('---', 'schedules.handleDataOnClick(Back) was called.  ');
			self.hideEntry(self);
			self.showButtons(self);
			break;
		case '10004':  // Delete button
			var l_obj = self.fetchEntry(self);
			l_obj['Delete'] = true;
	    	var l_json = JSON.stringify(l_obj);
			Divmod.debug('---', 'schedules.handleDataOnClick(Delete) was called. JSON:' + l_json);
	        var l_defer = self.callRemote("saveScheduleData", l_json);  // @ web_rooms
			l_defer.addCallback(cb_doHandleSubmit);
			l_defer.addErrback(eb_doHandleSubmit);
			break;
		default:
			Divmod.debug('---', 'schedules.handleDataOnClick(Default) was called. l_ix:' + l_ix);
		break;			
		}
		// return false stops the resetting of the server.
        return false;
	}
);
