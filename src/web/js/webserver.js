/**
 * webserver.js
 * 
 * version 1.00
 * 
 * D. Brian Kimmel
 */

/* 
 * Create a new custom window with existing data for changing a slot.
 */
function createChangeWebServerWindow(p_port) {    
	var divId = createNewWindow('WebServer', 250, 300, 200, 250);  // width, height, start x, start y
	var content = fillChangeWebServerWindow(divId, p_port);
	document.getElementById('good_windowContent' + divId).innerHTML = content;
}

/*
 * Populate a window to allow changes to be made.
 * Slider for level of light to set 0-100
 */
function fillChangeWebServerWindow(p_divid, p_port) {
	// TODO check the correct radio button
	ret = 		'<br />\n';
	ret = ret + '<form method="post" action="_submit!!post" enctype="multipart/form-data">\n';
	ret = ret +	'  Web Port:';
	ret = ret +	'    <input type = "text" name = "WebPort" value = "' + p_port + '" /><br />\n';
	ret = ret +	'  <br />\n';
	ret = ret + '  <input type="submit" name="post_btn" value="Change_Web Port" />\n';
	ret = ret + '</form>\n';
	return ret;
}

/* ### END */
