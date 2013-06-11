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

/*
 * Generate an empty form with an "add" button.
 */
function fillNewSchedule(p_id, p_key, p1, p2, p3, p4, p5) {
	//alert('fill new schedule (add)', p6);
	ret =		'';
	ret = ret + '<form method="post" action="_submit!!post" enctype="multipart/form-data">\n';
	ret = ret + '  <input type="text" name="Key" value="8321" />\n';
	ret = ret +	'    <br />\n';
	ret = ret + '  Type:';
	ret = ret +	'    <input type = "radio" name = "Type" value = "Device" checked /> Device &nbsp;';
	ret = ret +	'    <input type = "radio" name = "Type" value = "Scene" /> Scene<br />\n';
	ret = ret +	'  Name:';
	ret = ret +	'    <input type = "text"  name = "Name" value = "" /><br />\n';
	ret = ret +	'  Time:';
	ret = ret +	'    <input type = "text"  name = "Time" value = "00:00" /><br />\n';
	ret = ret +	'  Level:';
	ret = ret +	'    <input type = "range" name = "Level" min="0" max="100" value="0" onchange="showLightValue(this.value)" />\n';
	ret = ret +	'    <span name = slid_02  id="range">0</span>\n';
	ret = ret +	'    <br />\n';
	ret = ret +	'    <br />\n';
	ret = ret +	'  Rate:';
	ret = ret +	'    <input type = "text" name = "Rate" value = "0" /><br />\n';
	ret = ret + '  <input type="hidden" value="' + p_id + '" name="slider_no" />\n';
	ret = ret +	'<br />\n';
	ret = ret + '  <input type="submit" value="AddSlot" name="post_btn" />\n';
	ret = ret + '</form>\n';
	return ret;
}
/*
 * Populate a window to allow changes to be made.
 * Slider for level of light to set 0-100
 */
function fillChangeScheduleWindow(p_divid, p_json) {
	var l_obj = JSON.parse(p_json);
	//alert('Fill Schedule Window (change)' + l_obj.Name);
	// TODO check the correct radio button
	ret = 		'               Schedule A<br />\n';
	ret = ret + '<form method="post" action="_submit!!post" enctype="multipart/form-data">\n';
	ret = ret +	'  Active:<input type = "text"  name = "Active" value = "' + l_obj.Active + '" /><br />\n';
	ret = ret + '  Type:  <input type = "radio" name = "Type" value = "Device /> Device<br />\n';
	ret = ret +	'         <input type = "radio" name = "Type" value = "Scene" /> Scene<br />\n';
	ret = ret +	'  Name:  <input type = "text"  name = "Name" value = "' + l_obj.Name + '" /><br />\n';
	ret = ret +	'  Time:  <input type = "text"  name = "Time" value = "' + l_obj.Time + '" /><br />\n';
	ret = ret +	'  Level: <input type = "range" name = "Level" min="0" max="100" value="' + l_obj.Level + '" onchange="showLightValue(this.value)" />\n';
	ret = ret +	'         <span name = slid_02  id="range">' + l_obj.Level + '</span>\n<br />\n';
	ret = ret +	'  Rate:  <input type = "text" name = "Rate" value = "' + l_obj.Rate + '" /><br />\n';
	ret = ret + '  Room:  <input type = "text" name = "RoomName" value = "' + l_obj.RoomName + '" /><br />\n';
	ret = ret + '  Light: <input type = "text" name = "LightName" value = "' + l_obj.LightName + '" /><br />\n';
	ret = ret + '         <input type="hidden" name="slider_no" value="' + p_divid + '" />\n';
	ret = ret +	'         <input type="hidden" name="Key"      value="' + l_obj.Key  + '" />\n';
	ret = ret +	'         <input type="hidden" name="Type"     value="' + l_obj.Type  + '" />\n';
	ret = ret +	'<br />\n';
	ret = ret + '         <input type="submit" name="post_btn" value="ChangeSchedule" />\n';
	ret = ret + '         <input type="submit" name="post_btn" value="DeleteSchedule" />\n';
	ret = ret + '</form>\n';
	return ret;
}

function showLightValue(newValue) {
	//alert("new value " + newValue + " divId=" + pdivid)
	document.getElementById('range').innerHTML=newValue;
}

/* ### END */
