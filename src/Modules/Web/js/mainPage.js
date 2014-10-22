/**
 * @name: PyHouse/src/Modules/Web/js/mainPage.js
 * @author: D. Brian Kimmel
 * @contact: D.BrianKimmel@gmail.com
 * @Copyright (c) 2012-2014 by D. Brian Kimmel
 * @license: MIT License
 * @note: Created about 2012
 * @summary:
 *
 */
// import Divmod
// import Nevow.Athena



// note this is 'PageWidget'
Nevow.Athena.PageWidget.subclass(mainPage, 'mainPage').methods(

	function showDisconnectDialog(self) {
		Divmod.msg("Connection lost, dialog or status display implementation pending");
	}
);
// ### END DBK