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
		self.fetchScheduleData(self, globals.selectedHouse);
	},
	

	/**
	 * This gets the schedule data from the server.
	 * 
	 * @param p_houseIndex is the house index that was selected
	 */
	function fetchScheduleData(self, p_houseIndex) {
		function cb_fetchScheduleData(self, p_json, p2) {
			Divmod.debug('---', 'schedules.cb_fetchScheduleData() was called.');
			console.log("schedules.cb_fetchScheduleData() - self: %O ", self);
			console.log("schedules.cb_fetchScheduleData() - Json: %O ", p_json);
			var l_obj = JSON.parse(p_json);
			var l_tab = buildTable(self, l_obj);
			self.nodeById('ScheduleTableDiv').innerHTML = l_tab;
			
		}
		function eb_fetchScheduleData(self, p1, p2) {
			Divmod.debug('---', 'schedules.eb_fetchScheduleData() was called.');
		}
		
        var l_defer = self.callRemote("getScheduleEntries", globals.selectedHouse);  // call server @ web_schedules.py
		l_defer.addCallback(cb_fetchScheduleData);
		l_defer.addErrback(eb_fetchScheduleData);
        return false;
	},

	function hideButtons(self) {
		self.nodeById('ScheduleButtonsDiv').style.display = 'none';		
	},
	function showButtons(self) {
		Divmod.debug('---', 'schedules.showButtons() was called. ');
		self.nodeById('ScheduleButtonsDiv').style.display = 'block';	
	},

	function hideEntry(self) {
		Divmod.debug('---', 'schedules.hideEntry() was called. ');
		self.nodeById('ScheduleEntryDiv').style.display = 'none';		
	},
	function showEntry(self) {
		Divmod.debug('---', 'schedules.showEntry() was called. ');
		self.nodeById('ScheduleEntryDiv').style.display = 'block';		
	}
);
