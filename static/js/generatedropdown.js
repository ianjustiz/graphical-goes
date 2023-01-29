var satellite = "noaa-goes16";
var zoom = "ABI-L2-MCMIPF";
var band = "noir";

function generateDropdownArray(file, element) { // generate the dropdown with a file
    var items = new Array(); // create array
    
    $.get(file, function(data) { // read from file
        items = data.split(/[\n\r]+/); // use regex to split \n and \r from file and then put into array
        createDropdown(items, element); 
    });
}

function createDropdown(items, element) { // actually create the dropdown in html
    $.each(items, function(val, text) {
        $(element).append(
            $('<option></option>').val(val).html(text) // append option elements in html
        );
    });
}

function Center_OLD_(element) { // real codeing frontend developer (real)
    $(element).css({
        'position': 'fixed',
        'left': '50%',
        'top': '50%',
        'margin-left': function() {
            return -$(this).outerWidth()/2;
        },
        'margin-top': function() {
            return -$(this).outerWidth()/2;
        },
        'height': 'auto',
    });
}

function messageOnChange(element, msgBox) {
    $(element).change(function () {
        var selected = $(this).find("option:selected"); // get selected option
        let text = selected.text();

        deleteAllImages(); // delete all current images in html

        if(text == "GOES-16")
            satellite = "noaa-goes16";
        if(text == "GOES-18")
            satellite = "noaa-goes18";
        if(text == "TrueColor Visible")
            band = "noir"
        if(text == "Visible w/ Shortwave IR")
            band = "fc"
        if(text == "Longwave IR")
        band = "ir"
        
        preload(`./static/assets/${satellite}/${zoom}/${band}/images.txt`); // load back in new images

        Center_OLD_(msgBox); // COOL FUNCTION CALL
        $(msgBox).show().delay(1000);
        $(msgBox).fadeOut(500);
        
    });

    
}

$(function() {
    // generate dropdowns for satellites and bands
    generateDropdownArray("./static/assets/satellites.txt", "#satelliteSelect");
    generateDropdownArray("./static/assets/bands.txt", "#bandSelect");
    
    // get current satellite
    var chosenSatellite = $("#satelliteSelect").val();
    var chosenBand = $("#bandSelect").val();
    
    preload(`${satellite}/${zoom}/${band}/images.txt`);
    
    messageOnChange("#satelliteSelect", "#changeSatellite");
    messageOnChange("#bandSelect", "#changeBand");
    
});

