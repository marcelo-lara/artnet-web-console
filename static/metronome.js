export default class Metronome {
    constructor({socket}) {
        this.audioContext = undefined;
        this.buffer = undefined;
        this.isPlaying = false;
        this.audioFile = '/static/Perc_HeadKnock_lo.wav';
        this.socket = socket;

        // bind socket events
        this.socket.on('update', () => {
            this.play();
        });


    }

    _loadSound(file) {
        return fetch(file)
            .then(response => response.arrayBuffer())
            .then(arrayBuffer => this.audioContext.decodeAudioData(arrayBuffer))
            .then(audioBuffer => {
                this.buffer = audioBuffer;
            });
    }

    play() {
        if(!this.buffer){
            this._loadSound(this.audioFile);
        }
        if(!this.audioContext){
            this.audioContext = new AudioContext();
        }

        let source = this.audioContext.createBufferSource();
        source.buffer = this.buffer;
        source.connect(this.audioContext.destination);
        source.start();
    }

    handleMIDIInput(midiInput) {
        midiInput.onmidimessage = (message) => {
            console.log(message);
            // Handle the MIDI message here. For example, you might want to start or stop the metronome
            // based on the message data:
            if (message.data[0] === 144) { // Note on message
                this.play();
            } else if (message.data[0] === 128) { // Note off message
                this.stop();
            }
        };
    }
}