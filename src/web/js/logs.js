/**
 * logs.js
 * 
 * version 1.00
 * 
 * D. Brian Kimmel
 */

/* 
 * Create a new custom window with existing data for changing a slot.
 */
function createChangeLogsWindow(p_debug, p_error) {    
	var divId = createNewWindow('Logs', 250, 300, 200, 250);  // width, height, start x, start y
	var content = fillChangeLogsWindow(divId, p_debug, p_error);
	document.getElementById('good_windowContent' + divId).innerHTML = content;
}

/*
 * Populate a window to allow changes to be made.
 * Slider for level of light to set 0-100
 */
function fillChangeLogsWindow(p_divid, p_debug, p_error) {
	// TODO check the correct radio button
	ret = 		'<br />\n';
	ret = ret + '<form method="post" action="_submit!!post" enctype="multipart/form-data">\n';
	ret = ret +	'  Debug:';
	ret = ret +	'    <input type = "text" name = "Debug" value = "' + p_debug + '" /><br />\n';
	ret = ret +	'  Error:';
	ret = ret +	'    <input type = "text" name = "Error" value = "' + p_error + '" /><br />\n';
	ret = ret +	'  <br />\n';
	ret = ret + '  <input type="submit" name="post_btn" value="Change_Logs" />\n';
	ret = ret + '</form>\n';
	return ret;
}

/* ### END */
