$(function(){
    $("#registerform").hide();
    $("#logintab").click(function(){
	if ($(this).hasClass("selectedtab") == false) {
	    $(this).removeClass("tab unselected").addClass("tab selectedtab");
	    $("#registertab").removeClass("tab selectedtab").addClass("tab unselected");
	    $("#registerform").fadeOut('slow');
	    $("#loginform").delay("slow").fadeIn("slow");
	}
    });
    $("#registertab").click(function(){
	if ($(this).hasClass("selectedtab") == false) {
	    $(this).removeClass("tab unselected").addClass("tab selectedtab");
	    $("#logintab").removeClass("tab selectedtab").addClass("tab unselected");
	    $("#loginform").fadeOut("slow");
	    $("#registerform").delay("slow").fadeIn('slow');
	}

    });
});
