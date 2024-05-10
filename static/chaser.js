// Beats Chaser
export default class Chaser {
    constructor({
        bpm, 
        s_beat
    }) {
        this.current = 0;
        this.s_beat = s_beat;
        this.bpm = bpm;
        this.chase_timer = null;
    }

    start() {
        this.chase_timer = setInterval(() => this.movenext(), 60000 / this.bpm);
    }

    stop() {
        clearInterval(this.chase_timer);
    }

    reset() {
        this.s_beat.forEach((x) => {
            x.classList.remove('active');
        });
        this.current = 0;
    }

    // set the tempo in bpm
    setBpm(newBpm) {
        this.bpm = newBpm;
        if (this.chase_timer) {
            clearInterval(this.chase_timer);
            this.start();
        }
    }

    stopAndSelectBeat(beat) {
        clearInterval(this.chase_timer);
        this.current = beat;
        this.movenext();
    }

    movenext() {
        // show next square beat
        this.s_beat.forEach(x => x.classList.remove('active'));
        this.s_beat[this.current].classList.add('active');

        // set next square beat
        this.current = (this.current + 1) % this.s_beat.length;
        if (this.current > this.s_beat.length) { this.current = 0; };
    }
}
