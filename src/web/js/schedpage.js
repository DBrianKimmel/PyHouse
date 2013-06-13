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
	var divId = createNewWindow(139, 350, 300, 200, 250);  // width, height, start x, start y
	var content = fillNewSchedule(divId, 501,1,2,3,4,5);
	document.getElementById('good_windowContent' + divId).innerHTML = content;	
}

/* 
 * Create a new custom window with existing data for changing a slot.
 */
function createChangeScheduleWindow(p_json) {    
	//alert('Create Schedule Window (change)', p_rooms);
	var divId = createNewWindow(139, 350, 300, 200, 250);  // width, height, start x, start y
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
	//alert('Fill Schedule Window (change) JSON = ' + p_json);
	var l_obj = JSON.parse(p_json);
	// TODO check the correct radio button
	ret = 		'               Schedule E<br />\n';
	ret = ret + '<form method="post" action="_submit!!post" enctype="multipart/form-data">\n';
    ret = ret + '  <table width = "100%" >\n';
    ret = ret + '    <tr>\n';
    ret = ret + '      <td>Name:</td>\n';
	ret = ret +	'      <td><input  type = "text"  name = "Name"      value = "' + l_obj.Name + '" /></td>\n';
    ret = ret + '    </tr><tr>\n';
    ret = ret + '      <td>Key:</td>\n';
	ret = ret +	'      <td><input type = "text"  name = "Key"       value = "' + l_obj.Key + '" /></td>\n';
    ret = ret + '    </tr>\n';
    ret = ret + showActive(l_obj.Active);
    ret = ret + '    <tr>\n';
    ret = ret + '     <td>Type:</td>\n';
	ret = ret + '       <td><input  type = "radio" name = "Type"      value = "Device" checked />Device\n';
	ret = ret +	'       <input  type = "radio" name = "Type"      value = "Scene" />Scene</td>\n';
    ret = ret + '    </tr><tr>\n';
    ret = ret + '      <td>Time:</td>\n';
	ret = ret +	'      <td><input  type = "text"  name = "Time"      value = "' + l_obj.Time + '" /></td>\n';
    ret = ret + '    </tr><tr>\n';
    ret = ret + '      <td>Level:</td>\n';
	ret = ret +	'      <td><input  type = "range" name = "Level" min="0" max="100" value="' + l_obj.Level + '" onchange="showLightValue(this.value)" />\n';
	ret = ret +	'             <span name = slid_02  id="range">' + l_obj.Level + '</span>\n</td>\n';
    ret = ret + '    </tr><tr>\n';
    ret = ret + '      <td>Rate:</td>\n';
	ret = ret +	'      <td><input  type = "text"  name = "Rate"      value = "' + l_obj.Rate + '" /></td>\n';
    ret = ret + '    </tr>\n';
    ret = ret + showRoomsList({"0":"Room 0", "1":"Room 1", "2":"Room_2"}, 0);
    ret = ret + showLightsList({"0":"Light-0", "1":"Light 1", "2":"Light_2", "3":"Light # 3"}, 1);
    ret = ret + '  </table>\n';
	ret = ret + '           <input  type="hidden"  name = "slider_no" value = "' + p_divid + '" />\n';
	ret = ret +	'  <br />\n';
	ret = ret + '           <input  type="submit"  name = "post_btn"  value = "ChangeSchedule" />\n';
	ret = ret + '           <input  type="submit"  name = "post_btn"  value = "DeleteSchedule" />\n';
	ret = ret + '</form>\n';
	return ret;
}

function showLightValue(newValue) {
	//alert("new value " + newValue + " divId=" + pdivid)
	document.getElementById('range').innerHTML=newValue;
}

/* Move this to a common js file.
 *
 */
function showActive(p_active){
	//
	var l_t, l_f;
	if (p_active == 'True') {
		l_t = ' checked';
		l_f = ' ';
	} else {
		l_f = ' checked';
		l_t = ' ';
	}
	ret = 		'<tr>\n';
    ret = ret + '  <td>Active:</td>\n';
	ret = ret +	'  <td>\n';
	ret = ret +	'    <input type = "radio" name = "Active" value = "True"  ' + l_t + ' />T\n';
	ret = ret +	'    <input type = "radio" name = "Active" value = "False" ' + l_f + ' />F\n';
	ret = ret + '  </td>\n';
    ret = ret + '</tr>\n';
    return ret;
}

/* Move these to a common js file.
 * 
 */
function showListOptions(p_list, p_index){
	var ret = '';
	var l_len = Object.keys(p_list).length;
	var l_selected = '';
	Object.keys(p_list);
	alert('Show list options - list=' + p_list + '\n index=' + p_index + '\n Length = ' + l_len )
	Object.keys(p_list).forEach(function (key) {
		var l_key = key;
		var l_text = p_list[key];
		if (key == p_index) {
			l_selected = 'selected';
		} else {
			l_selected = '';
		}
		ret = ret + '      <option name = "RoomName"  value = "' + l_key + '" ' + l_selected + '>' + l_text + '</option>\n';
	})
	return ret;
}
function showRoomsList(p_list, p_index){
	//
	var ret = '';
	ret = ret + showListBox("Room:", "RoomName", p_list, p_index)
    return ret;	
}
function showLightsList(p_list, p_index){
	//
	var ret = '';
	ret = ret + showListBox("Light:", "LightName", p_list, p_index)
    return ret;	
}
function showListBox(p_caption, p_name, p_list, p_index){
	//
	var ret =	'<tr>\n';
    ret = ret + '  <td>' + p_caption + '</td>\n';
	ret = ret + '  <td>\n';
	ret = ret + '    <select name = "' + p_name + '" >\n';
	ret = ret + showListOptions(p_list, p_index);
	ret = ret + '    </select>\n';
	ret = ret + '  </td>\n';
    ret = ret + '</tr>\n';
    return ret;	
}


// ### END DBK
