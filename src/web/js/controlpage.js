// controlpage.js
/*
 * version 1.00
 * 
 * D. Brian Kimmel
 */

/*
 * Create a new window with all data blank for adding a slot
 */
function createNewControl(p_schedule) {
	//alert('Create New Schedule (add)');
	var divId = createNewWindow(127, 250, 300, 200, 250);  // width, height, start x, start y
	var content = fillNewSchedule(divId, 501,1,2,3,4,5);
	document.getElementById('good_windowContent' + divId).innerHTML = content;	
}

/* 
 * Create a new custom window with existing data for changing a slot.
 */
function createChangeScheduleWindow(p_json) {    
	//alert('Create Schedule Window (change)', p_rooms);
	var divId = createNewWindow(127, 250, 300, 200, 250);  // width, height, start x, start y
	var content = fillChangeScheduleWindow(divId, p_json);
	document.getElementById('good_windowContent' + divId).innerHTML = content;
}

