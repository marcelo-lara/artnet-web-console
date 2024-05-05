var fixtures = [];
$(document).ready(function() {
    $.get("/fixtures", function(data) {
        fixtures = data;
        $.each(fixtures, function(i, fixture) {
            var fixtureDiv = $('<div class="fixture"></div>');
            var fixtureNameDiv = $('<div class="fixture-name"></div>').text(fixture.name);
            fixtureDiv.append(fixtureNameDiv);

            $.each(fixture.channels, function(name, channel) {
                var faderContainerDiv = $('<div class="fader-container"></div>');
                var faderLabelDiv = $('<div class="fader-label"></div>').text(name);
                var faderInput = $('<input type="range" class="fader" min="0" max="255" value="0">').attr('name', name);
                faderInput.on('input', () => {

                    var data = {
                        fixture_name: fixture.name,
                        channels: []
                        };
                    $.each(fixture.channels, function(name, channel) {
                        data.channels.push({
                            name: name,
                            value: $('[name=' + name + ']').val()
                        });
                    });
                    $.ajax({
                        url: "/send_artnet",
                        type: "POST",
                        data: JSON.stringify(data),
                        contentType: "application/json",
                        success: function(response) {
                            console.log(response);
                        }
                    });
                });
                faderContainerDiv.append(faderLabelDiv, faderInput);
                fixtureDiv.append(faderContainerDiv);
            });

            $('#console').append(fixtureDiv);
        });

    });});

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