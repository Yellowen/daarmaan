$(function(){
    $("#id_setting_button").hover(function(){
	$("#id_setting_button img").attr("src", "/statics/image/settings-hover.png");
	
    }, function(){
	$("#id_setting_button img").attr("src", "/statics/image/settings.png");
    });
    $(".bar_button").click(function(){
	var menu = $(".submenu[belongs_to='" + $(this).attr("id") + "']");
	$(".submenu").not(menu).hide();
	menu.fadeToggle("slow");
    });

});
