/**
 * addhouse.js
 * 
 * version 1.00
 * 
 * D. Brian Kimmel
 */

/* 
 * This function creates a new floating window dynamically (Add).
 */
function createNewHouseWindow(p_name) {    
	var divId = createNewWindow(159, 400, 350, 200, 50);  // width, height, start x, start y
	var content = fillNewHouseWindow(divId, p_name);
	document.getElementById('good_windowContent' + divId).innerHTML = content;
	}

/*
 * Generate an empty form with an "add" button.
 */
function fillNewHouseWindow(p_id, p_name) {
	//alert('fill new schedule (add)');
	var ret =	'<br />\n';
	ret = ret + '<form method="post" action="_submit!!post" enctype="multipart/form-data">\n';
	ret = ret + '  Name:      <input type="text" name="Name"      value="Name Required !!" /><br />\n';
	ret = ret + '  Active:    <input type="text" name="Active"    value="True" /><br />\n';
	ret = ret + '  Street:    <input type="text" name="Street"    value="" /><br />\n';
	ret = ret + '  City:      <input type="text" name="Street"    value="" /><br />\n';
	ret = ret + '  State:     <input type="text" name="State"     value="" /><br />\n';
	ret = ret + '  ZipCode:   <input type="text" name="ZipCode"   value="" /><br />\n';
	ret = ret + '  Latitude:  <input type="text" name="Latitude"  value="" /><br />\n';
	ret = ret + '  Longitude: <input type="text" name="Longitude" value="" /><br />\n';
	ret = ret + '  TimeZone:  <input type="text" name="TimeZone"  value="-5.0" /><br />\n';
	ret = ret + '  DST:       <input type="text" name="Type" value="True" /><br />\n';
	ret = ret + '  <input type="submit" name="post_btn" value="Add House" />\n';
	ret = ret + '</form>\n';
	return ret;
}

//### END
