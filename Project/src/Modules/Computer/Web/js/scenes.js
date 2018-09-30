/*
 * Scenepage.js
 * 
 * version 1.01
 * 
 * D. Brian Kimmel
 */

/* 
 * This function creates a new floating window dynamically (Add).
 */
function createNewSceneWindow() {    
	var divId = createNewWindow(137, 300, 250, 1200, 50);
	var content = fillNewSceneWindow(divId);
	document.getElementById('good_windowContent' + divId).innerHTML = content;
	}

/* 
 * This function creates a new floating window dynamically (Change).
 */
function createChangeSceneWindow(p_name, p_level, p_rate) {    
	var divId = createNewWindow(137, 250, 120, 1200, 50);
	var content = fillChangeSceneWindow(divId, p_name, p_level, p_rate);
	document.getElementById('good_windowContent' + divId).innerHTML = content;
	}

/*
 * Generate an empty form with an "add" button.
 */
function fillNewSceneWindow(p_id) {
	var ret =	'';
	ret = ret + '<form method="post" action="_submit!!post" enctype="multipart/form-data">\n';
	ret = ret + '  Name: <input type="text" name="Name" value="" /><br />\n';
	ret = ret + '  Controller: <input type="text" name="Controller" value="PLM" /><br />\n';
	ret = ret + '  Responder: <input type="text" name="Responder" value="list" /><br />\n';
	ret = ret + '  Level: <input type="text" name="Level" value="100" /><br />\n';
	ret = ret + '  Ramp: <input type="text" name="Ramp" value="2s" /><br />\n';
	ret = ret + '  <input type="submit" name="post_btn" value="AddScene" />\n';
	ret = ret + '</form>\n';
	return ret;
}
/*
 * Slider for level of light to set 0-100
 */
function fillChangeSceneWindow(p_divid, p_name, p_level, p_rate) {
	var ret = 	'Scene: ' + p_name + ' - ' + p_divid + "\n";
	ret = ret + '<form method="post" action="_submit!!post" enctype="multipart/form-data">\n';
	ret = ret + '  <input name = slider_val type="range" min="0" max="100" value="' + p_level + '" onchange="showSceneValue(this.value)" />\n' +
				'  <span name = slid_02  id="range">' + p_level + '</span><br />\n';
	ret = ret + '  <input type="hidden" value="' + p_divid + '" name="slider_no" />\n' +
				'  <input type="hidden" value="' + p_name + '" name="Name" />\n';
	ret = ret + '  <input type="submit" name="post_btn" value="ChangeScene" />\n';
	ret = ret + '  <input type="submit" name="post_btn" value="DeleteScene" />\n';
	ret = ret + '</form>\n';
	return ret;
}

function showSceneValue(newValue) {
	//alert("new value " + newValue + " divId=" + pdivid)
	document.getElementById('range').innerHTML=newValue;
}

//### END