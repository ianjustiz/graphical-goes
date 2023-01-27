function generateDropdownArray(file, element) {
    var items = new Array(); // create array
    
    $.get(file, function(data) { // read from file
        items = data.split(/[\n\r]+/); // use regex to split \n and \r from file and then put into array
        createDropdown(items, element);
    });
}

function createDropdown(items, element) {
    console.log(items);

    $.each(items, function(val, text) {
        $(element).append(
            // create new options in html
            $('<option></option>').val(val).html(text)
        );
    });
}

function messageOnChange(element, msgBox) {
    $(element).change(function () {
        var selected = $(this).find("option:selected");
        //var value = selected.val(); // probably useful for changing image
        var text = selected.text();
        //console.log(value);
        console.log(text);
        $(msgBox).fadeIn(150).delay(1000);
        $(msgBox).fadeOut(500);
    })
}

center(".message");

generateDropdownArray("./static/assets/satellites.txt", "#satelliteSelect");
generateDropdownArray("./static/assets/bands.txt", "#bandSelect");

var chosenSatellite = $(".selection").val();

messageOnChange("#satelliteSelect", "#changeSatellite");
messageOnChange("#bandSelect", "#changeBand");
