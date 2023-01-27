// todo : make this not bad

function toggleMenu(element) {

}

var toggled = false;


$("#closeBar").click(function() {
    toggled = !toggled;
    //console.log(toggled);
    if (toggled == true) {
        
        $("#closeBar").addClass("closeEnabled");
        $("#menuOverlay").slideDown(250);
    }
    else {
        $("#closeBar").removeClass("closeEnabled");
        $("#menuOverlay").slideUp(250);
    }
});