auto = false;
var time = 0;

function convertEpochToTime(epoch) {
    var date = new Date(epoch * 1000); // js uses millisecond unix time, so we convert
    return date.toUTCString();
}

function coolanimation() {
    $("#playpause").css("background-image", "url('./static/assets/icons/pause.png')")
    var images = document.getElementsByTagName("img");
    auto = !auto;
    
    var framerate = $("#frametime").val();
    var interval = setInterval(function() { 
        $("#stop").click(function() {
            time = 0;
        });

        $("#frametime").on("change", function() {
            clearInterval(interval);
            $("#playpause").css("background-image", "url('./static/assets/icons/play.png')")
        });

        if (auto) {
            if (time >= getNumberImages()) {
                time = 0;
            }
            for (var i = 0; i < images.length; i++) {
                if (images[i].id != time) {
                    images[i].style.display = "none";
                }
                else {
                    images[i].style.display = "block";
                    $("#epochtime").text(convertEpochToTime($("#" + i).data("unix")));
                    $("#manualslider").val(i);

                }
            }
            time++;

        }

        else { 
           clearInterval(interval);
           $("#playpause").css("background-image", "url('./static/assets/icons/play.png')")
        }
     }, framerate);

}

$("#playpause").click(function() {
    coolanimation();
});

$("#stop").click(function() {
    var images = document.getElementsByTagName("img");
    auto = false;
    time = 0;

    for (var i = 0; i < images.length; i++) {
        if (images[i].id != 0) {
            images[i].style.display = "none";
        }
        else {
            images[i].style.display = "block";
            $("#epochtime").text(convertEpochToTime($("#" + i).data("unix")));
        }
    }
});

// slider
$("#manualslider").on("input", function() {
    var images = document.getElementsByTagName("img");
    translatedStep = Math.round(this.value * 1);
    for (var i = 0; i < images.length; i++) {
        if (images[i].id != translatedStep) {
            images[i].style.display = "none";
        }
        else {
            $("#epochtime").text(convertEpochToTime($("#" + i).data("unix")));
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
        
        var num = 0;
        $(images).each(function() {
            
            if (num == 0) {
                $("<img />") // if its the first element
                    .attr("src", this)
                    .appendTo("#content")
                    .css("display", "fixed")
                    .attr("id", num);
                saveUnixTime($("#" + num), this);
                $("#epochtime").text(convertEpochToTime($("#0").data("unix")));
            }
            else {
                $("<img />")
                    .attr("src", this)
                    .appendTo("#content")
                    .css("display", "none")
                    .attr("id", num); // if its not, then just preload the rest and then set them to not display
                saveUnixTime($("#" + num), this);
            }
            
            num++;

        });
        center("#content");
        $("img").attr("draggable", "false");
    });
}

function saveNumberImages() {
    var numImages = $("#content").find("img").length
    $("#content").data("images", numImages);
}

function getNumberImages() {
    var numImages = $("#content").find("img").length
    return numImages;
}

function saveUnixTime(element, url) {
    timestamp = url.replace(/\D/g, '');
    timestamp = timestamp.substr(timestamp.length - 10);

    $(element).data("unix", timestamp);
}

$(function() {
    preload(`./static/assets/${satellite}/${zoom}/${band}/images.txt`);
});
