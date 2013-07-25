// lightpage.js
/*
 * version 1.05
 * 
 * D. Brian Kimmel
 */

/* 
 * This function creates a new floating window dynamically (Add).
 */
function createNewLightWindow(p_name) {    
	var divId = createNewWindow(135, 300, 250, 200, 250);  // width, height, start x, start y
	var content = fillNewLightWindow(divId, p_name);
	document.getElementById('good_windowContent' + divId).innerHTML = content;
	}

/* 
 * This function creates a new floating window dynamically (Change).
 */
function createChangeLightWindow(p_name, p_json) {    
	alert('changeChangeLightWindow (change) ' + p_json);
	var divId = createNewWindow(135, 250, 120, 200, 250);  // width, height, start x, start y
	var content = fillChangeLightWindow(divId, p_json);
	document.getElementById('good_windowContent' + divId).innerHTML = content;
	}

/*
 * Generate an empty form with an "add" button.
 */
function fillNewLightWindow(p_id, p_name) {
	alert('fill new lightpage (add)');
	var ret =	'';
	ret = ret + '<form method="post" action="_submit!!post" enctype="multipart/form-data">\n';
	ret = ret + '  Name: <input type="text" name="Name" value="test_light2" />\n';
	ret = ret + '    <br />\n';
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
function fillChangeLightWindow(p_divid, p_json) {
	alert('fill new lightpage (change) ' + p_json);
	var l_obj = JSON.parse(p_json);
	var ret = 	'Light: ' + l_obj.Name + ' - ' + p_divid + " - Test 10\n";
	ret = ret + '<form method="post" action="_submit!!post" enctype="multipart/form-data">\n';
	ret = ret + '  <input name = slider_val type="range" min="0" max="100" value="' + p_level + '" onchange="showLightValue(this.value)" />\n';
	ret = ret +	'  <span name = slid_02  id="range">' + l_obj.Level + '</span><br />\n';
	ret = ret + '  <input type="hidden" value="' + p_divid + '" name="slider_no" />\n';
	ret = ret +	'  <input type="hidden" value="' + l_obj.Name + '" name="Name" />\n';
	ret = ret +	'  <input type="hidden" value="' + l_obj.Family + '" name="Family" />\n';
	ret = ret + '  <input type="submit" name="post_btn" value="changelight" />\n';
	ret = ret + '  <input type="submit" name="post_btn" value="DeleteLight" />\n';
	ret = ret + '</form>\n';
	return ret;
}

function showLightValue(newValue) {
	//alert("new value " + newValue + " divId=" + pdivid)
	document.getElementById('range').innerHTML=newValue;
}

//### END DBK