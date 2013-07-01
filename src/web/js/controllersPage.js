/*
 * controllerspage.js
 *
 * version 1.00
 * 
 * D. Brian Kimmel
 */

/* 
 * This function creates a new floating window dynamically (Add).
 */
function createNewControllerWindow(p_name) {    
	var divId = createNewWindow(117, 300, 250, 200, 250);  // width, height, start x, start y
	var content = fillNewControllerWindow(divId, p_name);
	document.getElementById('good_windowContent' + divId).innerHTML = content;
	}

/* 
 * This function creates a new floating window dynamically (Change).
 */
function createChangeControllerWindow(p_json) {    
	var divId = createNewWindow(117, 300, 220, 100, 250);  // width, height, start x, start y
	var content = fillChangeControllerWindow(divId, p_json);
	document.getElementById('good_windowContent' + divId).innerHTML = content;
	}

/*
 * Generate an empty form with an "add" button.
 */
function fillNewControllerWindow(p_id, p_name) {
	//alert('fill new controllerpage (add)');
	var ret =	'';
	ret = ret + '<form method="post" action="_submit!!post" enctype="multipart/form-data">\n';
	ret = ret + '  Name: <input type="text" name="Name" value="test_light2" />\n';
	ret = ret + '  Address: <input type="text" name="Address" value="CC:11:22" /><br />\n';
	ret = ret + '  Family: <input type="text" name="Family" value="Insteon" /><br />\n';
	ret = ret + '  Type: <input type="text" name="Type" value="WSLD" /><br />\n';
	ret = ret + '  <input type="hidden" name="Controller" value="False" />\n';
	ret = ret + '  <input type="hidden" name="Dimmable" value="False" />\n';
	ret = ret + '  <input type="hidden" name="Coords" value="0,0" />\n';
	ret = ret + '  <input type="hidden" name="Master" value="False" />\n';
	ret = ret + '  <input type="hidden" name="CurLevel" value="0" />\n';
	ret = ret + '  <input type="submit" name="post_btn" value="AddLight" />\n';
	ret = ret + '</form>\n';
	return ret;
}
/*
 * Slider for level of light to set 0-100
 */
function fillChangeControllerWindow(p_divid, p_json) {
	alert('fill new lightpage (change) JSON=' + p_json);
	var l_obj = JSON.parse(p_json);
	var ret =	'';
	ret = ret +	'Controller: ' + l_obj.Name + ' - ' + p_divid + " - Test 2\n";
	ret = ret +	'<br />\n';
	ret = ret + '<form method="post" action="_submit!!post" enctype="multipart/form-data">\n';
	ret = ret +	'  Name:   <input type = "text"  name = "Name" value = "' + l_obj.Name + '" /><br />\n';
	ret = ret +	'  Key:    <input type = "text"  name = "Key" value = "' + l_obj.Key + '" /><br />\n';
	ret = ret +	'  Active: <input type = "radio" name = "Active" value = "' + l_obj.Active + '" />\n';
	ret = ret +	'          <input type = "radio" name = "Active" value = "' + l_obj.Active + '" /><br />\n';
	ret = ret + '  Family: <input type = "text"  name = "Family" value="' + l_obj.Family + '" /><br />\n';
	ret = ret + '  <input type="hidden" value="' + p_divid + '" name="slider_no" />\n';
	ret = ret +	'  <input type="hidden" value="' + l_obj.Name + '" name="Name" />\n';
	ret = ret +	'  <input type="hidden" value="' + l_obj.Family + '" name="Family" />\n';
	ret = ret + '  <input type="submit" name="post_btn" value="changelight" />\n';
	ret = ret + '  <input type="submit" name="post_btn" value="DeleteLight" />\n';
	ret = ret + '</form>\n';
	return ret;
}

//### END DBK