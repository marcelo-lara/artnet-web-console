// Beats Chaser
export default class Chaser {
    constructor({
        bpm, 
        s_beat,
        socket,
        s_channels
    }) {
        this.current = 0;
        this.s_beat = s_beat;
        this.bpm = bpm;
        this.chase_timer = null;
        this.socket = socket;
        this.channels = new Object();

        for (const ch of s_channels) {
            this.channels[ch.name] = ch;
        }
        
        // Setup event listeners
        this.s_beat.forEach((x, i) => {
            x.addEventListener('click', () => {
                this.showBeat(i);
            });
        });

        // Setup the initial sceme
        this.s_beat[0]['channels'] = this._get_channels_status();

        this.div_bpm = document.getElementById('bpm');

        // Handle server evemts
        this.socket.on('update', (data) => {
            this.current = data.current;
            this.showBeat(this.current);
        });

        this.socket.on('update_bpm', (data) => {
            this.bpm = data.bpm;
            this.div_bpm.innerHTML = data.bpm;
        });

        //BPM setter
        let isDragging = false;
        let isOverBpmDiv = false;
        let lastBpm = this.bpm;
        let startY;

        this.div_bpm.addEventListener('mousedown', (event) => {
            isDragging = true;
            startY = event.clientY;
            event.preventDefault();
        });

        this.div_bpm.addEventListener('mouseenter', (event) => {
            isOverBpmDiv = true;
            event.preventDefault();
        });

        window.addEventListener('mousemove', (event) => {
            if (isDragging && isOverBpmDiv) {
                const deltaY = startY - event.clientY;
                let newBpm = this.bpm += parseInt(deltaY * 0.5); // Adjust the multiplier as needed
                if(newBpm != lastBpm){
                    this.setBpm(newBpm);
                    this.socket.emit('chaser_set_bpm', { bpm: this.bpm });
                    lastBpm = newBpm;
                }
                startY = event.clientY;
            }
            event.preventDefault();
        });

        window.addEventListener('mouseup', (event) => {
            isOverBpmDiv = false;
            isDragging = false;
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
        this.div_bpm.innerHTML = this.bpm.toFixed(0);
    }

    //// Frontend display functions
    showBeat(beat) {
        // activate the current beat
        this.current = beat
        this.s_beat.forEach(x => x.classList.remove('active'));
        this.s_beat[beat].classList.add('active');

        // update the sliders
        if (this.s_beat[beat]['channels']) {
            this.s_beat[beat]['channels'].forEach(x => {
                this.channels[x.name].value = x.value;
            });
        };

    }

    //// Scene control functions
    _get_channels_status() {
        const _channels = [];
        Object.entries(this.channels).forEach(x => {
            _channels.push({name: x[0], value: x[1].value});
        });
        return _channels;
    }

    set_scene() {
        // retrieve scene object or create a new one
        const new_channel_values = this._get_channels_status();
        this.s_beat[this.current]['channels'] = new_channel_values;
        this.s_beat[this.current].classList.add('has_scene');
    }

    clear_scene() {   
        // remove the current scene from the scenes array
        this.s_beat[this.current]['channels'] = undefined;
        this.s_beat[this.current].classList.remove('has_scene');

        // send the updated scene to the server
    }
}