/*
 * controlpage.js
 * 
 * version 1.01
 * 
 * D. Brian Kimmel
 */

/* 
 * Create a new custom window with existing data for changing a slot.
 */
function createChangeControlWindow(p_json) {    
	//alert('Create Control Window (change) ' + p_json);
	var divId = createNewWindow(127, 300, 250, 200, 250);  // id, width, height, start x, start y
	var content = fillChangeControlWindow(divId, p_json);
	document.getElementById('good_windowContent' + divId).innerHTML = content;
}

/*
 * Populate a window to allow changes to be made.
 * Slider for level of light to set 0-100
 */
function fillChangeControlWindow(p_divid, p_json) {
	//alert('Fill Control Window (change) JSON = ' + p_json);
	var l_obj = JSON.parse(p_json);
	// TODO check the correct radio button
	ret = 		'          Control Light A<br />\n';
	ret = ret + '<form method="post" action="_submit!!post" enctype="multipart/form-data">\n';
    ret = ret + '  <table width = "100%" >\n';
    ret = ret + '    <tr>\n';
    ret = ret + '      <td>Name:</td>\n';
	ret = ret +	'      <td><input  type = "text"  name = "Name"      value = "' + l_obj.Name + '" /></td>\n';
    ret = ret + '    </tr>\n';
    ret = ret + '    <tr>\n';
    ret = ret + '      <td>Level:</td>\n';
	ret = ret +	'      <td><input  type = "range" name = "Level" min="0" max="100" value="' + l_obj.CurLevel + '" onchange="showLightValue(this.value)" />\n';
	ret = ret +	'             <span name = slid_02  id="range">' + l_obj.CurLevel + '</span>\n</td>\n';
    ret = ret + '    </tr>\n';
    ret = ret + '  </table>\n';
	ret = ret + '           <input  type="hidden"  name = "slider_no" value = "' + p_divid + '" />\n';
	ret = ret +	'  <br />\n';
	ret = ret + '           <input  type="submit"  name = "post_btn"  value = "ChangeLight" />\n';
	ret = ret + '</form>\n';
	return ret;
}

function showLightValue(newValue) {
	//alert("new value " + newValue + " divId=" + pdivid)
	document.getElementById('range').innerHTML=newValue;
}

//### END DBK
