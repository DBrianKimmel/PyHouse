/*
 * roompage.js
 * 
 * version 1.00
 * 
 * D. Brian Kimmel
 */
/*
 * Create a new window with all data blank for adding a slot
 */
function createNewRoomWindow(p_name, p_key) {
	var divId = createNewWindow(133, 250, 300, 1200, 50);
	var content = fillNewRoomWindow(divId, p_name, p_key, 2,3,4,5);
	document.getElementById('good_windowContent' + divId).innerHTML = content;	
}

/* 
 * Create a new custom window with existing data for changing a slot.
 */
function createChangeRoomWindow(p_name, p_key, p_active, p_size, p_corner, p_comment) {    
	var divId = createNewWindow(133, 250, 300, 1200, 50);
	var content = fillChangeRoomWindow(divId, p_name, p_key, p_active, p_size, p_corner, p_comment);
	document.getElementById('good_windowContent' + divId).innerHTML = content;
}

/*
 * Generate an empty form with an "add" button.
 */
function fillNewRoomWindow(p_id, p_name, p_key, p_active, p_size, p_corner, p_comment) {
	ret =		'';
	ret = ret + '<form method="post" action="_submit!!post" enctype="multipart/form-data">\n';
	ret = ret + '  <input type="text" name="Key" value="" />\n';
	ret = ret + '    <br />\n';
	ret = ret +	'  Name:';
	ret = ret +	'    <input type = "text"  name = "Name" value = "" /><br />\n';
	ret = ret +	'  Key:';
	ret = ret +	'    <input type = "text" name = "Key" value = "' + p_key + '" /><br />\n';
	ret = ret +	'  Level:';
	ret = ret +	'    <input type = "range" name = "Level" min="0" max="100" value="0" onchange="showLightValue(this.value)" />\n';
	ret = ret +	'    <span name = slid_02  id="range">0</span>\n';
	ret = ret + '    <br />\n';
	ret = ret + '    <br />\n';
	ret = ret +	'  Rate:';
	ret = ret +	'    <input type = "text" name = "Rate" value = "0" /><br />\n';
	ret = ret + '  <input type="hidden" value="' + p_id + '" name="slider_no" />\n';
	ret = ret +			'<br />\n';
	ret = ret + '  <input type="submit" value="AddSlot" name="post_btn" />\n';
	ret = ret + '</form>\n';
	return ret;
}
/*
 * Populate a window to allow changes to be made.
 * Slider for level of light to set 0-100
 */
function fillChangeRoomWindow(p_divid, p_name, p_key, p_active, p_size, p_corner, p_comment) {
	// TODO check the correct radio button
	ret = 		'Room: ' + p_name + "<br />\n";
	ret = ret + '<form method="post" action="_submit!!post" enctype="multipart/form-data">\n';
	ret = ret +	'  Name:';
	ret = ret +	'    <input type = "text" name = "Name" value = "' + p_name + '" /><br />\n';
	ret = ret +	'  Key:';
	ret = ret +	'    <input type = "text" name = "Key" value = "' + p_key + '" /><br />\n';
	ret = ret +	'  Active:';
	ret = ret +	'    <input type = "text" name = "Active" value = "' + p_active + '" /><br />\n';
	ret = ret +	'  Size:';
	ret = ret +	'    <input type = "text" name = "Size" value = "' + p_size + '" /><br />\n';
	ret = ret +	'  Corner:';
	ret = ret +	'    <input type = "text" name = "Corner" value = "' + p_corner + '" /><br />\n';
	ret = ret +	'  Comment:';
	ret = ret +	'    <input type = "text" name = "Comment" value = "' + p_comment + '" /><br />\n';
	ret = ret +	'<br />\n';
	ret = ret + '  <input type="submit" name="post_btn" value="Change Room" />\n';
	ret = ret + '  <input type="submit" name="post_btn" value="Delete Room" />\n';
	ret = ret + '</form>\n';
	return ret;
}

function showLightValue(newValue) {
	//alert("new value " + newValue + " divId=" + pdivid)
	document.getElementById('range').innerHTML=newValue;
}

/* ### END */
