// todo : make this not bad
var toggled = false;

function center(element) {
    $(element).css({
        'position': 'fixed',
        'left': '50%',
        'top': '50%',
        'margin-left': function() {
            //$(element).waitForImages(function() {
            return -$(this).outerWidth()/2;
            //});

            
            //return -1000
        },
        'margin-top': function() {
            //$(element).waitForImages(function() {
            return -$(this).outerWidth()/2;
            //});
            //return -1000
        },
        'height': 'auto',
    });
}


$("#closeBar").click(function() {
    toggled = !toggled;

    if (toggled == true) {
        $("#closeBar").addClass("closeEnabled");
        $("#menuOverlay").slideDown(250);
    }
    else {
        $("#closeBar").removeClass("closeEnabled");
        $("#menuOverlay").slideUp(250);
    }
});