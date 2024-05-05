$(document).ready(function() {
    $(".fader").on("input", function() {
        var data = {
            fixture_name: $("#fixture_name").val(),
            fader: $("#fader").val(),
            red: $("#red").val(),
            green: $("#green").val(),
            blue: $("#blue").val(),
            strobe: $("#strobe").val(),
            colors: $("#colors").val()
        };
        $.post("/send_artnet", data, function(response) {
            
        });
    });
});