// define variables so it looks nicer?
var earth = $("#content");


// current idea that i think might by going wrong:
// it might be trying to center even though it hasnt loaded in yet, so it centers it incorrectly

$(document).ready(function() {

    earth.css({"display": "none"});
    //$("#0").css({"opacity": "20%"});
    earth.fadeIn(1000, function() {
        //earth.css({'opacity': '100'});
        center("#content");
        
    });

    
    
});

$(window).resize(function() {
    center("#content");
});

