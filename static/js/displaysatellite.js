// define variables so it looks nicer?
var earth       = $("#content");

function center(element) {
    $(element).css({
        'position': 'absolute',
        'left': '50%',
        'top': '50%',
        'margin-left': function() {return -$(this).outerWidth()/2},
        'margin-top': function() {return -$(this).outerHeight()/2},
        'height': 'auto',
    });
}

$(function() {
    earth.css({'display': 'none'});
    center(earth);
    earth.fadeIn(1000);
})

$(window).resize(function() {
    center("#content");
});