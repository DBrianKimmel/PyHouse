/* ***************************************************************************
Javascript file for LCARS Framework
By :: Josh Messer
Free to use, please give source credit.
*****************************************************************************/

$(
	function(){
		// --------------------------------------------------------- Detect page width & height
		var DOCwidth = $(document).width();
		var DOCheight = $(document).height();
		if (DOCwidth <= 900){
		$('body').html('<font color="red" size="+6">ERROR 104 PAGE WIDTH TO LOW</font><br>The width of the page is ' + DOCwidth + ' it needs to be higher than 900.');}
		if (DOCheight <= 450){
		$('body').html('<font color="red" size="+6">ERROR 105 PAGE HEIGHT TO LOW</font><br>The height of the page is ' + DOCheight + ' it needs to be higher than 450.');}
		// -------------------------------------------------------------------------
		var LI = $('ul#left_content li').size();
		// Random Number
		function getRandom(min, max) {
			var randomNum = Math.random() * (max-min);
		// Round to the closest integer and return it
			return(Math.round(randomNum) + min);
		}
		if(LI > 8){
			$('body').html('<font color="red" size="+6">ERROR 106 LINKS TO MANY</font><br>You can not have anymore then 8 links under ul#right_content');
		}
		if (LI <= 8){
			var u = 8 - LI;
			var i = 1;
			for (i=1;i<=u;i++){
				var ran = getRandom(100,999);
				$('ul#left_content').append('<li>' + ran + '</li>');  // Create list items with random number as title
			}
			var DOCheight = $(document).height() - 60;
			var NLI = LI + u;
			var number = DOCheight / NLI;
			var numberPX = number + 'px';
			$('ul#left_content li').height(numberPX);  //---------------sets height of links
		}
	}
);

function LCARS_init(style,color1,color2) {
	//-----------------------------------------------------------------Style Colors
	$('ul#left_content li:even').css('background-color',color1);
	$('ul#left_content li:odd').css('background-color',color2);
	// style parameters ------------------------------------------------------------
	if(style == 'full') {  // ----------------------------------------------Full Style
		$('div.top_line').css('background-color',color1);
		$('div.bottom_line').css('background-color',color2);
		$('div#right_content').css('width','90%');
		$('div.bottom_line, div.top_line').text('');
	}
	else if(style == 'panel'){  // ---------------------------------------Panel Style
		$('ul#left_content').hide();
		$('div#right_content').css({'margin-left' : '-9%', 'margin-top' : '45px', 'height' : '85%'});
		$('div.top_line').removeClass('top_line').addClass('top_bar').css('background-color',color1);
		$('div.bottom_line').removeClass('bottom_line').addClass('bottom_bar').css('background-color',color2);
	}
	else if(style == 'split'){  // ---------------------------------------Split Style
		$('ul#left_content').css('padding','0px');  // -- Content padding = zero
		$('div.top_line').removeClass('top_line').addClass('top_split').css('background-color',color2);  // -- change classes & set BG color
		$('div.top_split').append().html('<div class="bottom_split"></div>');// -- add bottom beam
		var TSheight = $('div.top_split').height() + 15;  // -- height var
		var LIheight = $('ul#left_content li').height() * 2;  // -- height var
		$('div#right_content').css('margin-top', LIheight + TSheight + 'px').height(LIheight * 3 + 'px');  // -- link margin = zero
		$('div.bottom_split').css('background-color',color1);  // -- set background color
		$('div.bottom_line').hide();  // -- remove bottom line
		$('ul#left_content li:eq(1)').css('margin-bottom', TSheight + 'px');  // -- set link margins
		$('div.top_split').offset({ top: LIheight, left: 0 });  // -- offest of beams
	}
	// -----------------------------------------------------------------Error Codes
	else if(style == ''){
		$('body').html('<font color="red" size="+6">ERROR 100 STYLE CALLED BLANK</font><br>LCARS_init(); paramiter &quot;style&quot; = &quot; &quot;');
	}
	else if(style == 'version'){
		$('body').html('<font color="red" size="+6">LCARS WEBSITE SYSTEM</font><br>By Josh Messer<br>Version 1.0<br><a href=\"http://www.prolenet.org/LCARS\">Homepage</a>');
		}
	else if(style == 'help'){$('body').html('<font color="red" size="+6">LCARS FRAMEWORK :: HELP</font><br>Call options include.<br>1) colors = view LCARS color list.<br>2) panel - panel screen<br>3) split - split screen<br>4)full - full screen<br>5)help - view this<br>--HIDDEN--<br>NC1701<br>starfleet<br>vulcan<br>bones<br>picard<br>kirk<br>data<br>riker<br>spock<br>scotty<br>You can view the help documentation <a href=\'help.html\'>here</a>');}
	else if(style == 'fuck you'){$('body').html('<font color="red" size="+6">ERROR 201 CALL IN POOR TASTE</font><br>Fuck you too');}
	else if(style == 'colors'){$('body').html('<font color="red" size="+6">COLORS CALL</font><br>Here is a list of the LCARS FRAMEWORK colors.<hr><pre><div class="colors" style="font-family:monospace;font-size:12px;"></div></pre><br><a href="colors.txt">view the .txt file</a>');$('div.colors').load('colors.txt');}
	else if(style == 'NC1701'){$('body').html('<h1>Galaxy Class (USS Enterprise NCC-1701-D)</h1><a href=\"txt/galaxy.txt\">view file</a><pre><div class="ascii" style=\"font-family:monospace;font-size:12px;\"></div></pre>');$('div.ascii').load('txt/galaxy.txt');}
	else if(style == 'starfleet'){$('body').html('<h1>Starfleet Symbol</h1><a href=\"txt/starfleet.txt\">view file</a><pre><div class="ascii" style=\"font-family:monospace;font-size:12px;\"></div></pre>');$('div.ascii').load('txt/starfleet.txt');}
	else if(style == 'vulcan'){$('body').html('<h1>Vulcan IDIC Symbol</h1><a href=\"txt/vulcan.txt\">view file</a><pre><div class="ascii" style=\"font-family:monospace;font-size:12px;\"></div></pre>');$('div.ascii').load('txt/vulcan.txt');}
	else if(style == 'bones'){$('body').html('<h1>BONES</h1><a href=\"txt/bones.txt\">view file</a><pre><div class="ascii" style=\"font-family:monospace;font-size:12px;\"></div></pre>');$('div.ascii').load('txt/bones.txt');}
	else if(style == 'picard'){$('body').html('<h1>PICARD</h1><a href=\"txt/picard.txt\">view file</a><pre><div class="ascii" style=\"font-family:monospace;font-size:12px;\"></div></pre>');$('div.ascii').load('txt/picard.txt');}
	else if(style == 'kirk'){$('body').html('<h1>KIRK</h1><a href=\"txt/kirk.txt\">view file</a><pre><div class="ascii" style=\"font-family:monospace;font-size:12px;\"></div></pre>');$('div.ascii').load('txt/kirk.txt');}
	else if(style == 'riker'){$('body').html('<h1>RIKER</h1><a href=\"txt/riker.txt\">view file</a><pre><div class="ascii" style=\"font-family:monospace;font-size:12px;\"></div></pre>');$('div.ascii').load('txt/riker.txt');}
	else if(style == 'data'){$('body').html('<h1>DATA</h1><a href=\"txt/data.txt\">view file</a><pre><div class="ascii" style=\"font-family:monospace;font-size:12px;\"></div></pre>');$('div.ascii').load('txt/data.txt');}
	else if(style == 'spock'){
		$('body').html('<h1>SPOCK</h1><a href=\"txt/spock.txt\">view file</a><br><iframe style=\"font-family: Courier;font-size:12px;background:white;color:black;\" width=\"600\" height=\"500\" src=\"txt/spock.txt\"></iframe>');
	}
	else if(style == 'scotty'){
		$('body').html('<h1>SCOTTY</h1><a href=\"txt/scotty.txt\">view file</a><pre><div class="ascii" style=\"font-family:monospace;font-size:12px;\"></div></pre>');
		$('div.ascii').load('txt/scotty.txt');
	}
	else{
		$('body').html('<font color="red" size="+6">ERROR 101 UNKNOWN PAGE STYLE</font><br>LCARS_init(); paramiter &quot;style&quot; is unknown or blank');
	}
	// ----------------------------------------------------------------------------
	// color ERRORS----------------------------------------------------------------
	if(color1 == null){
		$('body').html('<font color="red" size="+6">ERROR 102 COLOR1 CALLED BLANK</font><br>page_init(); paramiter &quot;color1&quot; = &quot; &quot;');
	}
	if(color2 == null){
		$('body').html('<font color="red" size="+6">ERROR 103 COLOR2 CALLED BLANK</font><br>page_init(); paramiter &quot;color2&quot; = &quot; &quot;');
	}
	// ----------------------------------------------------------------------------
};
//----------------------------------- useful functions
function replace(source, dest){
	var html = $(source).html();
	$(dest).html(html);
}

