var socket = io.connect(window.location.origin);
(function() {
    document.querySelectorAll('input.slider').forEach(function(x) {
        x.addEventListener('input', (e)=> {
            socket.emit('slider_change', {channel_id: e.target.name, value: e.target.value});
        });
    });
})();

// Song Chaser
class Chaser {
    constructor(bpm = 120, s_beat = []) {
        this.current = 0;
        this.s_beat = Array.from(s_beat); 
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

    movenext() {
        // show next square beat
        this.s_beat.forEach(x => x.classList.remove('active'));
        this.s_beat[this.current].classList.add('active');

        // set next square beat
        this.current = (this.current + 1) % this.s_beat.length;
        if (this.current > this.s_beat.length) { this.current = 0 };
    }
}

var chaser_timeout = undefined;
const chaser = new Chaser(
    bpm = 120,
    s_beat = document.querySelectorAll('#chaser-plan .beat')
);

document.querySelector('#chaser-start').addEventListener('click', ()=> {
    chaser.start();
});
document.querySelector('#chaser-stop').addEventListener('click', ()=> {
    chaser.stop();
});
document.querySelector('#chaser-reset').addEventListener('click', ()=> {
    chaser.reset();
});
