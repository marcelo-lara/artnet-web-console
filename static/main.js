var socket = io.connect(window.location.origin);
(function() {
    document.querySelectorAll('input.slider').forEach(function(x) {
        x.addEventListener('input', (e)=> {
            socket.emit('slider_change', {channel_id: e.target.name, value: e.target.value});
        });
    });
})();