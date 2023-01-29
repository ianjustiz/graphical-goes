var earth = $("#content");

$(document).ready(function() {

    earth.css({"display": "none"});
    earth.fadeIn(1000);
    center("#content");  

});

$(window).resize(function() {
    center("#content");
});

