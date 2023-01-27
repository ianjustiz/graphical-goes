$(function() {
    $("#globe").click(function(e) {
        var offset = $(this).offset();
        x = e.pageX - offset.left
        y = e.pageY - offset.top

        console.log("(%d, %d)", x, y)
    })
});