var toggled = false;
var showUI = true;

$("#hideui").change(function() {
    console.log('hai');
    $(".controls").toggle();
});

function center(element) {
    $(element).css({
        'position': 'fixed',
        'left': '50%',
        'top': '50%',
        'margin-left': function() {
            $.getJSON(`./static/assets/${satellite}/${zoom}/info.json`, function(data){
                return  data.width * 2;
            });

        },
        'margin-top': function() {
            return $.getJSON(`./static/assets/${satellite}/${zoom}/info.json`, function(data){
                return data.height / 2;
            });
        },
        'height': 'auto',
    });

    $.getJSON(`./static/assets/${satellite}/${zoom}/info.json`, function(data){
        $(element).css({
            'margin-left': function() {return -(data.width / 2)},
            'margin-top': function() {return -(data.height / 2)}
        })
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
