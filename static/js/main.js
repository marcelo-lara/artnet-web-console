import Chaser from './chaser.js';
import Metronome from './metronome.js';

var socket = io.connect(window.location.origin);
(function() {
    // setup sliders
    const channels = document.querySelectorAll('input.slider');
    channels.forEach(function(x) {
        // x.addEventListener('input', (e)=> {
        //     socket.emit('slider_change', {channel_id: e.target.name, value: e.target.value});
        // });
    });

    // setup metronome
    const metronome = new Metronome({socket:socket});

    // setup chaser blocks and controls
    const chaser_beats = document.querySelectorAll('#song .beat')
    const chaser = new Chaser( {bpm:120, s_beat:chaser_beats, socket:socket, s_channels:channels});

    document.querySelector('#start').addEventListener('click', ()=> {
        chaser.start();
    });
    document.querySelector('#stop').addEventListener('click', ()=> {
        chaser.stop();
    });
    document.querySelector('#reset').addEventListener('click', ()=> {
        chaser.reset();
    });
    document.querySelector('#save').addEventListener('click', ()=> {
        chaser.set_scene();
    });
    document.querySelector('#del').addEventListener('click', ()=> {
        chaser.clear_scene();
    });


})();

/// setup midi input /////////////////////////////////////////////////
if (navigator.requestMIDIAccess) {
    navigator.requestMIDIAccess({ sysex: true })
        .then(onMIDISuccess, onMIDIFailure);
} else {
    console.log("WebMIDI is not supported in this browser.");
}

function onMIDISuccess(midiAccess) {
    console.log('MIDI Access Object', midiAccess);
    var inputs = midiAccess.inputs;
    var outputs = midiAccess.outputs;
    for (var input of inputs.values()) {
        input.onmidimessage = getMIDIMessage;
    }
}

function onMIDIFailure() {
    console.log('Could not access your MIDI devices.');
}

function getMIDIMessage(midiMessage) {
    console.log(midiMessage);
}    
