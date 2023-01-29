$(function() {
    $("#content").click(function(e) {
        var offset = $(this).offset();
        x = e.pageX - offset.left
        y = e.pageY - offset.top

        console.log("(%d, %d)", x, y)
        //center("#content");

        //$(this).animate({height:'150%', width:'150%'}, 500);
        //$("#0").width("102%");
        //center("#0")
        
    });

    $("#content").hover(function(e) {
        //center("#content");

        //$(this).animate({height:'150%', width:'150%'}, 500);
        //$("#0").width("102%");
        //center("#0")
        
    });
});