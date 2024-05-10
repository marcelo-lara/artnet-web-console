// Beats Chaser
export default class Chaser {
    constructor({
        bpm, 
        s_beat,
        socket
    }) {
        this.current = 0;
        this.s_beat = s_beat;
        this.bpm = bpm;
        this.chase_timer = null;
        this.socket = socket;
        
        this.socket.on('update', (data) => {
            // Handle the 'update' event here
            this.current = data.current;
            this.showBeat(this.current);
        });
    }

    //// Backend control functions
    start() {
        this.socket.emit('chaser_start', { bpm: this.bpm, s_beat: this.s_beat });
    }

    stop() {
        this.socket.emit('chaser_stop');
    }

    reset() {
        this.socket.emit('chaser_reset');
    }

    // set the tempo in bpm
    setBpm(newBpm) {
        this.bpm = newBpm;
        this.socket.emit('chaser_set_bpm', { bpm: this.bpm });
    }

    //// Frontend display functions
    showBeat(beat) {
        this.current = beat
        this.s_beat.forEach(x => x.classList.remove('active'));
        this.s_beat[beat].classList.add('active');
    }

}
