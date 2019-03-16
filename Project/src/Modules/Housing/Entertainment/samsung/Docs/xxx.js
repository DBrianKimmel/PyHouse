/**
 * 
 */
function setTime(){
	var e,
	t=new Date,
	n="";
	(e=t.getMinutes())>=0
	&&e<=9
	&&(e="0"+e);
	var i=t.getHours();
	n=0==i?12+":"+e+" AM":i>=1
			&&i<12?i+":"+e+" AM":12==i?12+":"+e+" PM":i-12+":"+e+" PM",
					$("#first_screen_clock").html(n)
					}
function init(){
	void 0!=window.tizen?(initEventManager(),
			$("#first_screen_launcher_layout_APPS").attr("tabindex","1"),
			$("#first_screen_accelerator").hide(),
			$("#first_screen_shadow_aboveaccelerator").hide(),
			window.tizen.mode.getDebugFlag(),
			window.tizen
			&&window.tizen.appList.getAppList(
			function(e){
				loadAppList(e)?($("#first_screen_accelerator").show(),
					$("#first_screen_shadow_aboveaccelerator").show(),
					!1===$("#overlayBackground",
							window.parent.document).is(":visible")
					&&pFSGridList.Focus()):(!1===$("#overlayBackground",window.parent.document).is(":visible")
							&&$("#first_screen_launcher_layout_APPS").focus(),
							$("#first_screen_accelerator").hide(),
							$("#first_screen_shadow_aboveaccelerator").hide())
							}
			),
							$("#first_screen_launcher_layout_APPS").hover(
					function(){
		$("#first_screen_launcher_layout_APPS").focus()
		},
		function(){}
		),
		setInterval("setTime()",6e4),
		setTime()):timer=setInterval(
				function(){
					void 0!=window.tizen
					&&(clearInterval(timer),
							init()
							)
					},
					100)
					}
function initEventManager(){
	document.addEventListener("tizenhwkey",
						function(e){
					window.tizen.mode.getDebugFlag()}),
					document.body.removeEventListener("keydown",handelKeyEvent,!1),
						document.body.addEventListener("keydown",handelKeyEvent,!1),
						$("body").bind("mouseup",
						function(e){
							0==e.button
							&&handelKeyEvent(
									{keyCode:13}
						)
						}
						)
						}
	function sortApps(e){arrApps.sort(
			function(t,n){
				return 0==e?t.name.localeCompare(n.name.toLowerCase()):1==e?n.name.localeCompare(t.name.toLowerCase()):void 0
						}
			)
			}
	function loadAppList(e){
		if(!e||0===e.length)
			return!1;
		arrApps=e,
		sortApps(window.tizen.appList.getSortIndex());
		t="landscape";
		if(window&&window.tizen)
			var t=window.tizen.appList.getFSALOrientation();
		var n=9,
		i=1;
		return"portrait"==t?(n=5,i=1):(n=9,i=1),
				(pFSGridList=new FSGridList({
					items:arrApps,
					container:$("#"+appsId),
					line:i,
					column:n
					}
				)
				).Init(),!0
				}
	function handelKeyEvent(e){
		switch(window.tizen.mode.getDebugFlag()e.keyCode){
	case TvKeyCode.KEY_RIGHT:
		case TvKeyCode.KEY_LEFT:
			(t=getCurrentElement())===pFSGridList?(pFSGridList.HandleKeyEvent(e.keyCode),
			pFSGridList.Focus()):"first_screen_id"===t
			&&$("#first_screen_launcher_layout_APPS").focus();
	break;
	case TvKeyCode.KEY_UP:
		var t=getCurrentElement();
		"first_screen_launcher_layout_APPS"===t?pFSGridList.Focus():"first_screen_id"===t
			&&$("#first_screen_launcher_layout_APPS").focus();
	break;
	case TvKeyCode.KEY_DOWN:
		$("#first_screen_launcher_layout_APPS").focus();
		break;
	case TvKeyCode.KEY_ENTER:
		getCurrentElement()===pFSGridList
	&&(window.tizen.appList.setPreFrame("firstscreen"),
			pFSGridList.HandleKeyEvent(e.keyCode)),
			"first_screen_launcher_layout_APPS"===document.activeElement.id
			&&window.tizen
			&&document.location.assign(window.tizen.appList.getAppLauncherUrl())
			}
		}
	function getCurrentElement(){
		return appsId===document.activeElement.parentNode.id?pFSGridList:
			document.activeElement.id}$(document).bind("ready",init);
	var arrApps=[],
	pFSGridList,
	appsId="first_screen_accelerator_app_list",
	timer
