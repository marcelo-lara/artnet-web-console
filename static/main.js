var socket = io.connect('http://s1.local:5000');
(function() {
    document.querySelectorAll('input.slider').forEach(function(x) {
        x.addEventListener('input', (e)=> {
            socket.emit('slider_change', {channel_id: e.target.name, value: e.target.value});
        });
    });
})();