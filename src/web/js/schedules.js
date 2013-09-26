/* schedules.js
 * 
 * Displays the schedules
 */

// import Nevow.Athena
// import globals
// import helpers

/**
 * The schedule widget.
 * 
 * This widget has 2 parts:
 *   1. The schedule selection section whhich shows a button for each schedule and allows one to add a new schedule.
 *   2. The schedule data section which allows entering/changing all the detail about the selected schedule.
 *      It also allows the schedule to be deleted.
 */

helpers.Widget.subclass(schedules, 'SchedulesWidget').methods(
		
	function __init__(self, node) {
		schedules.SchedulesWidget.upcall(self, '__init__', node);
		globals.Schedules.Selected = {};
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
			//Divmod.debug('---', 'schedules.cb_widgready() was called.');
			self.hideWidget();
		}
		//Divmod.debug('---', 'scheduless.ready() was called. ' + self);
		var uris = collectIMG_src(self.node, null);
		var l_defer = loadImages(uris);
		l_defer.addCallback(cb_widgetready);
		return l_defer;
	},
	
	function showWidget(self) {
		Divmod.debug('---', 'schedules.showWidget() was called.');
		self.node.style.display = 'block';
		self.showButtons(self);
		self.hideEntry(self);
		self.fetchScheduleData(self, globals.SelectedHouse.Ix);
	},
	function hideButtons(self) {
		Divmod.debug('---', 'schedules.hideButtons() was called. ');
		self.nodeById('ScheduleButtonsDiv').style.display = 'none';		
	},
	function showButtons(self) {
		Divmod.debug('---', 'schedules.showButtons() was called. ');
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
		//console.log('schedules,buildButtonName() using Obj: %O', p_obj);
		var l_html = p_obj['Name']
		l_html += '<br>' + p_obj['RoomName']
		l_html += '<br>' + p_obj['LightName']
		l_html += '<br>' + p_obj['Level'] + '% '
		//Divmod.debug('---', 'schedules.buildButtonName(2) was called. ' + l_html);
		return l_html;
	},

	// ============================================================================
	/**
	 * This triggers getting the schedule data from the server.
	 * The server calls displayScheduleButtons with the schedules info.
	 * 
	 * @param p_houseIndex is the house index that was selected
	 */
	function fetchScheduleData(self, p_houseIndex) {
		function cb_fetchScheduleData(self, p_json, p2) {
			Divmod.debug('---', 'schedules.cb_fetchScheduleData() was called. ' + p_json + ' ' + p2);
		}
		function eb_fetchScheduleData(self, p1, p2) {
			Divmod.debug('---', 'schedules.eb_fetchScheduleData() was called. ' + p1 + ' ' + p2);
		}
        var l_defer = self.callRemote("getScheduleEntries", globals.SelectedHouse.Ix);  // call server @ web_schedules.py
		l_defer.addCallback(cb_fetchScheduleData);
		l_defer.addErrback(eb_fetchScheduleData);
        return false;
	},

	
	/**
	 * Fill in the schedule entry screen with all of the data for this schedule.
	 */
	function fillEntry(self, p_entry) {
		var sched = arguments[2];
		Divmod.debug('---', 'schedules.fillEntry() was called. ' + sched);
		self.nodeById('Name').value = sched.Name;
		self.nodeById('Key').value = sched.Key;
		self.nodeById('Active').value = sched.Active;
		self.nodeById('Type').value = sched.Type;
		self.nodeById('Time').value = sched.Time;
		self.nodeById('Level').value = sched.Level;
		self.nodeById('Rate').value = sched.Rate;
		self.nodeById('RoomName').value = sched.RoomName;
		self.nodeById('LightName').value = sched.LightName;
	},
	
	function fetchEntry(self) {
        var l_scheduleData = {
			Name : self.nodeById('Name').value,
			Key : self.nodeById('Key').value,
			Active : self.nodeById('Active').value,
			Type : self.nodeById('Type').value,
			Time : self.nodeById('Time').value,
			Level : self.nodeById('Level').value,
			Rate : self.nodeById('Rate').value,
			RoomName : self.nodeById('RoomName').value,
			LightName : self.nodeById('LightName').value
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
	function doHandleOnClick(self, p_node) {
		var l_ix = p_node.name;
		var l_name = p_node.value;
		globals.Schedules.Selected.Ix = l_ix;
		globals.Schedules.Selected.Name = l_name;
		if (l_ix <= 1000) {
			// One of the schedule buttons.
			var l_obj = globals.Schedules.Obj[l_ix];
			globals.Schedules.Selected.ScheduleObj = l_obj;
			Divmod.debug('---', 'schedules.doHandleOnClick(1) was called. ' + l_ix + ' ' + l_name);
			console.log("schedules.doHandleOnClick() - l_obj = %O", l_obj);
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
			var l_node = findWidget(self, 'HouseMenu');
			l_node.showWidget(self);
		}
	},
	
	/**
	 * Event handler for submit buttons at bottom of entry portion of this widget.
	 * Get the possibly changed data and send it to the server.
	 */
	function doHandleSubmit(self, p_node) {
		Divmod.debug('---', 'schedules.doHandleSubmit() was called. ');
		console.log("schedules.doHandleSubmit() - self %O", self);
		console.log("schedules.doHandleSubmit() - node %O", p_node);
		
		function cb_doHandleSubmit(p_json) {
			Divmod.debug('---', 'schedule.cb_doHandleSubmit() was called.');
			self.showWidget(self);
		}
		function eb_doHandleSubmit(res){
			Divmod.debug('---', 'login.eb_doHandleSubmit() was called. res=' + res);
		}
    	var l_json = JSON.stringify(self.fetchEntry(self));
		Divmod.debug('---', 'login.doHandleSubmit(1) was called. json:' + l_json);
        var l_defer = self.callRemote("doScheduleSubmit", l_json);  // @ web_schedule
		l_defer.addCallback(cb_doHandleSubmit);
		l_defer.addErrback(eb_doHandleSubmit);
		// return false stops the resetting of the server.
        return false;
	},

	// ============================================================================
	/**
	 * Pushed from the server. fill in the table and wait for an event to happen (doHandleOnClick).
	 */
	function displayScheduleButtons(self, p_json) {
		Divmod.debug('---', 'schedules.displayScheduleButtons(1) was called. ');
		globals.Schedules.Obj = JSON.parse(p_json);
		var l_tab = buildTable(self, globals.Schedules.Obj, self.buildButtonName, '');
		self.nodeById('ScheduleTableDiv').innerHTML = l_tab;
	}
);
