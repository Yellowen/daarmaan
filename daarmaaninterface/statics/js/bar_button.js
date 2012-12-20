$(function(){
    $("#id_setting_button").hover(function(){
	$("#id_setting_button img").attr("src", "/statics/image/settings-hover.png");
	
    }, function(){
	$("#id_setting_button img").attr("src", "/statics/image/settings.png");
    });

});
