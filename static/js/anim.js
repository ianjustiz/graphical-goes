auto = false;

function coolanimation() {
    var images = document.getElementsByTagName("img");
    auto = !auto;
    var time = 0;
    //var max = $("#content").data("images");
    //console.log(max);
    //center("#content");
    var framerate = 100;
    var interval = setInterval(function() { 
        if (auto == true) {
            $("#playpause").text("◼")
            if (time >= $("#content").data("images")) {
                time = 0;
            }
            for (var i = 0; i < images.length; i++) {
                if (images[i].id != time) {
                    images[i].style.display = "none";
                }
                else {
                    images[i].style.display = "block";
                }
            }

            console.log("frame: " + time);
            time++;
        }
        else { 
           clearInterval(interval);
           $("#playpause").text("▶")
        }
     }, framerate);

}

$("#playpause").click(function() {
    coolanimation();
});

// slider
$("#manualslider").on("input", function() {
    var images = document.getElementsByTagName("img");
    
    for (var i = 0; i < images.length; i++) {
        if (images[i].id != this.value) {
            images[i].style.display = "none";
        }
        else {
            images[i].style.display = "block";
        }
    }

});

function deleteAllImages() {
    var images = document.getElementsByTagName("img");
    while (images.length > 0) {
        images[0].parentNode.removeChild(images[0]);
    }
}

function preload(file) {
    $.get(file, function(data) {
        images = data.split(/[\n\r]+/);
        //$("#globe").attr("src", images[num]);
        
        var num = 0;
        $(images).each(function() {
            
            if (num == 0) {
                $("<img />") // if its the first element
                    .attr("src", this)
                    .appendTo("#content")
                    .css("display", "fixed")
                    .attr("id", num)
                    .blowup({
                        background: "#000000",
                        width: 500,
                        height: 500,
                    }); 


            }
            else {
                $("<img />").attr("src", this).appendTo("#content").css("display", "none").attr("id", num); // if its not, then just preload the rest and then set them to not display
            }
            
            num++;
            center("#content");
            saveNumberImages(num);
        });
        
        //console.log("preload"+num);
        //return num;
        //center("#content");
        
    });
}

/*
function getImageFromNumber(file, num) {
    var images = new Array();
    
    $.get(file, function(data) {
        images = data.split(/[\n\r]+/);
        $("#globe").attr("src", images[num]);
        //preload(file);
    });
    
}
*/


function saveNumberImages(num) {
    $("#content").data("images", num);
}

$(function() {
    
    // default preload
    preload("./static/assets/images-cool/images.txt");

});

//center("#content");