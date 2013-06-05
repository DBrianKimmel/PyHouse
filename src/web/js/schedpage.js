/*
 * schedpage.js
 * 
 * version 1.03
 * 
 * D. Brian Kimmel
 */

/*
 * Create a new window with all data blank for adding a slot
 */
function createNewSchedule(p_schedule) {
	//alert('Create New Schedule (add)');
	var divId = createNewWindow(127, 250, 300, 1200, 50);
	var content = fillNewSchedule(divId, 501,1,2,3,4,5);
	document.getElementById('good_windowContent' + divId).innerHTML = content;	
}

/* 
 * Create a new custom window with existing data for changing a slot.
 */
function createChangeScheduleWindow(p_slot, p_type, p_name, p_time, p_level, p_rate) {    
	//alert('Create Schedule Window (change)');
	var divId = createNewWindow(p_slot, 250, 300, 1200, 50);
	var content = fillChangeScheduleWindow(divId, p_slot, p_type, p_name, p_time, p_level, p_rate);
	document.getElementById('good_windowContent' + divId).innerHTML = content;
}

/*
 * Generate an empty form with an "add" button.
 */
function fillNewSchedule(p_id, p_slot, p1, p2, p3, p4, p5) {
	//alert('fill new schedule (add)');
	ret =		'';
	ret = ret + '<form method="post" action="_submit!!post" enctype="multipart/form-data">\n';
	ret = ret + '  <input type="text" name="Slot" value="8321" />\n' +
				'    <br />\n';
	ret = ret + '  Type:' +
				'    <input type = "radio" name = "Type" value = "Device" checked /> Device &nbsp;' +
				'    <input type = "radio" name = "Type" value = "Scene" /> Scene<br />\n' +
				'  Name:' +
				'    <input type = "text"  name = "Name" value = "" /><br />\n' +
				'  Time:' +
				'    <input type = "text"  name = "Time" value = "00:00" /><br />\n' +
				'  Level:' +
				'    <input type = "range" name = "Level" min="0" max="100" value="0" onchange="showLightValue(this.value)" />\n' +
				'    <span name = slid_02  id="range">0</span>\n' +
				'    <br />\n' +
				'    <br />\n' +
				'  Rate:' +
				'    <input type = "text" name = "Rate" value = "0" /><br />' +
				'\n';
	ret = ret + '  <input type="hidden" value="' + p_id + '" name="slider_no" />\n' +
				'<br />' +
				'\n'; 
	ret = ret + '  <input type="submit" value="AddSlot" name="post_btn" />\n';
	ret = ret + '</form>\n';
	return ret;
}
/*
 * Populate a window to allow changes to be made.
 * Slider for level of light to set 0-100
 */
function fillChangeScheduleWindow(p_divid, p_slot, p_type, p_name, p_time, p_level, p_rate) {
	//alert('Fill Schedule Window (change)');
	// TODO check the correct radio button
	ret = 		'Schedule: ' + p_slot + "<br />\n";
	ret = ret + '<form method="post" action="_submit!!post" enctype="multipart/form-data">\n';
	ret = ret + '  Type:' +
				'    <input type = "radio" name = "Type" value = "Device /> Device &nbsp;' +
				'    <input type = "radio" name = "Type" value = "Scene" /> Scene<br />\n' +
				'  Name:' +
				'    <input type = "text" name = "Name" value = "' + p_name + '" /><br />\n' +
				'  Time:' +
				'    <input type = "text" name = "Time" value = "' + p_time + '" /><br />\n' +
				'  Level:' +
				'    <input type="range" name = "Level" min="0" max="100" value="' + p_level + '" onchange="showLightValue(this.value)" />\n' +
				'    <span name = slid_02  id="range">' + p_level + '</span>\n' +
				'    <br />\n' +
				'    <br />\n' +
				'  Rate:' +
				'    <input type = "text" name = "Rate" value = "' + p_rate + '" /><br />' +
				'\n';
	ret = ret + '  <input type="hidden" name="slider_no" value="' + p_divid + '" />\n' +
				'  <input type="hidden" name="Slot"      value="' + p_slot  + '" />\n' +
				'  <input type="hidden" name="Type"      value="' + p_type  + '" />\n' +
				'<br />' +
				'\n';
	ret = ret + '  <input type="submit" name="post_btn" value="ChangeSchedule" />\n';
	ret = ret + '  <input type="submit" name="post_btn" value="DeleteSchedule" />\n';
	ret = ret + '</form>\n';
	return ret;
}

function showLightValue(newValue) {
	//alert("new value " + newValue + " divId=" + pdivid)
	document.getElementById('range').innerHTML=newValue;
}

/* ### END */
