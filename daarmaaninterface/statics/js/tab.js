function hashchange (){
    hash = window.location.hash;
    console.log(hash);
    if (hash == "#register") {
	$("#loginform").hide();
	$("#registerform").show();
	$("#logintab").removeClass("tab selectedtab").addClass("tab unselected");
	$("#registertab").removeClass("tab unselected").addClass("tab selectedtab");
    }
    else {
	$("#registerform").hide();
	$("#loginform").show();
	$("#registertab").removeClass("tab selectedtab").addClass("tab unselected");
	$("#logintab").removeClass("tab unselected").addClass("tab selectedtab");
    }

};
$(function(){
    window.onhashchange = hashchange;


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
