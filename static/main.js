var socket = io.connect('http://localhost:5000');

// slider.onchange = function() {
//     socket.emit('slider_change', {channel_id: 'myChannel', value: this.value});
// };

(function() {
    document.querySelectorAll('input.fader').forEach(function(x) {
        x.onchange = function() {
            console.log(x.value)
            // socket.emit('button_click', {channel_id: 'myChannel', value: this.value});
        };
    });

})();