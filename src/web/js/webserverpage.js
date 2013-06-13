// webserverpage.js
/*
 * WebServerPage.js
 * 
 * version 1.00
 * 
 * D. Brian Kimmel
 */

/* 
 * This function creates a new floating window dynamically (Add).
 */
function createNewWebWindow(p_name) {    
	var divId = createNewWindow(144, 400, 350, 1200, 50); // width, height, start x, start y
	var content = fillNewWebWindow(divId, p_name);
	document.getElementById('good_windowContent' + divId).innerHTML = content;
	}

/* 
 * This function creates a new floating window dynamically (Change).
 */
function createChangeWebWindow(p_name, p_port) {    
	var divId = createNewWindow(144, 400, 350, 1200, 50);
	var content = fillChangeWebWindow(divId, p_port);
	document.getElementById('good_windowContent' + divId).innerHTML = content;
	}

/*
 * Generate an empty form with an "add" button.
 */
function fillNewWebWindow(p_id, p_name) {
	//alert('fill new schedule (add)');
	var ret =	'';
	ret = ret + '<form method="post" action="_submit!!post" enctype="multipart/form-data">\n';
	ret = ret + '  Name: <input type="text" name="Name" value="Name Required !!" /><br />\n';
	ret = ret + '  Active: <input type="text" name="Active" value="True" /><br />\n';
	ret = ret + '  <input type="submit" name="post_btn" value="add" />\n';
	ret = ret + '</form>\n';
	return ret;
}
/*
 * 
 */
function fillChangeWebWindow(p_divid, p_name, p_port) {
	var ret = 	'House: ' + p_name + "\n";
	ret = ret + '<form method="post" action="_submit!!post" enctype="multipart/form-data">\n';
	ret = ret + '  Active: <input type="text" name="Active" value="' + p_active + '" /><br />\n';
	ret = ret + '  <input type="submit" name="post_btn" value="Change Web Server" />\n';
	//ret = ret + '  <input type="submit" name="post_btn" value="deletehouse" />\n';
	ret = ret + '</form>\n';
	return ret;
}

//### END DBK