import Chaser from './chaser.js';

var socket = io.connect(window.location.origin);
(function() {
    document.querySelectorAll('input.slider').forEach(function(x) {
        x.addEventListener('input', (e)=> {
            socket.emit('slider_change', {channel_id: e.target.name, value: e.target.value});
        });
    });

    // setup chaser blocks and controls
    const chaser_beats = document.querySelectorAll('#chaser-plan .beat')
    const chaser = new Chaser( {bpm:100, s_beat:chaser_beats });

    document.querySelector('#chaser-start').addEventListener('click', ()=> {
        chaser.start();
    });
    document.querySelector('#chaser-stop').addEventListener('click', ()=> {
        chaser.stop();
    });
    document.querySelector('#chaser-reset').addEventListener('click', ()=> {
        chaser.reset();
    });

})();