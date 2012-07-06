// housepage.js
/*
 * Housepage.js
 * 
 * version 1.00
 * 
 * D. Brian Kimmel
 */

/* 
 * This function creates a new floating window dynamically (Add).
 */
function createNewHouseWindow(p_name) {    
	var divId = createNewWindow(name, 400, 350, 1200, 50); // width, height, start x, start y
	var content = fillNewHouseWindow(divId, p_name);
	document.getElementById('good_windowContent' + divId).innerHTML = content;
	}

/* 
 * This function creates a new floating window dynamically (Change).
 */
function createChangeHouseWindow(p_name, p_active, p_street, p_city, p_state, p_zip, p_latitude, p_longitude, p_timezone, p_dst) {    
	var divId = createNewWindow(p_name, 400, 350, 1200, 50);
	var content = fillChangeHouseWindow(divId, p_name, p_active, p_street, p_city, p_state, p_zip, p_latitude, p_longitude, p_timezone, p_dst);
	document.getElementById('good_windowContent' + divId).innerHTML = content;
	}

/*
 * Generate an empty form with an "add" button.
 */
function fillNewHouseWindow(p_id, p_name) {
	//alert('fill new schedule (add)');
	var ret =	'';
	ret = ret + '<form method="post" action="_submit!!post" enctype="multipart/form-data">\n';
	ret = ret + '  Name: <input type="text" name="Name" value="Name Required !!" /><br />\n';
	ret = ret + '  Active: <input type="text" name="Active" value="True" /><br />\n';
	ret = ret + '  Street: <input type="text" name="Street" value="" /><br />\n';
	ret = ret + '  City: <input type="text" name="Street" value="" /><br />\n';
	ret = ret + '  State: <input type="text" name="State" value="" /><br />\n';
	ret = ret + '  ZipCode: <input type="text" name="ZipCode" value="" /><br />\n';
	ret = ret + '  Latitude: <input type="text" name="Latitude" value="" /><br />\n';
	ret = ret + '  Longitude: <input type="text" name="Longitude" value="" /><br />\n';
	ret = ret + '  TimeZone: <input type="text" name="TimeZone" value="-5.0" /><br />\n';
	ret = ret + '  DST: <input type="text" name="Type" value="True" /><br />\n';
	ret = ret + '  <input type="submit" name="post_btn" value="add" />\n';
	ret = ret + '</form>\n';
	return ret;
}
/*
 * 
 */
function fillChangeHouseWindow(p_divid, p_name, p_active, p_street, p_city, p_state, p_zip, p_latitude, p_longitude, p_timezone, p_dst) {
	var ret = 	'House: ' + p_name + "\n";
	ret = ret + '<form method="post" action="_submit!!post" enctype="multipart/form-data">\n';
	ret = ret + '  Active: <input type="text" name="Active" value="' + p_active + '" /><br />\n';
	ret = ret + '  Street: <input type="text" name="Street" value="' + p_street + '" /><br />\n';
	ret = ret + '  City: <input type="text" name="Street" value="' + p_city + '" /><br />\n';
	ret = ret + '  State: <input type="text" name="State" value="' + p_state + '" /><br />\n';
	ret = ret + '  ZipCode: <input type="text" name="ZipCode" value="' + p_zip + '" /><br />\n';
	ret = ret + '  Latitude: <input type="text" name="Latitude" value="' + p_latitude + '" /><br />\n';
	ret = ret + '  Longitude: <input type="text" name="Longitude" value="' + p_longitude + '" /><br />\n';
	ret = ret + '  TimeZone: <input type="text" name="TimeZone" value="' + p_timezone + '" /><br />\n';
	ret = ret + '  DST: <input type="text" name="Type" value="' + p_dst + '" /><br />\n';
	ret = ret + '  <input type="submit" name="post_btn" value="ChangeHouse" />\n';
	ret = ret + '  <input type="submit" name="post_btn" value="deletehouse" />\n';
	ret = ret + '</form>\n';
	return ret;
}

//### END