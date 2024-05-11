import Chaser from './chaser.js';

var socket = io.connect(window.location.origin);
(function() {
    // setup sliders
    const channels = document.querySelectorAll('input.slider');
    channels.forEach(function(x) {
        // x.addEventListener('input', (e)=> {
        //     socket.emit('slider_change', {channel_id: e.target.name, value: e.target.value});
        // });
    });

    // setup chaser blocks and controls
    const chaser_beats = document.querySelectorAll('#chaser-plan .beat')
    const chaser = new Chaser( {bpm:100, s_beat:chaser_beats, socket:socket, channels:channels});

    document.querySelector('#chaser-start').addEventListener('click', ()=> {
        chaser.start();
    });
    document.querySelector('#chaser-stop').addEventListener('click', ()=> {
        chaser.stop();
    });
    document.querySelector('#chaser-reset').addEventListener('click', ()=> {
        chaser.reset();
    });
    document.querySelector('#chaser-save').addEventListener('click', ()=> {
        chaser.save_scene();
    });
    document.querySelector('#chaser-del').addEventListener('click', ()=> {
        chaser.delete_scene();
    });


})();