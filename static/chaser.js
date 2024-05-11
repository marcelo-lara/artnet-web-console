// Beats Chaser
export default class Chaser {
    constructor({
        bpm, 
        s_beat,
        socket,
        channels
    }) {
        this.current = 0;
        this.s_beat = s_beat;
        this.bpm = bpm;
        this.chase_timer = null;
        this.socket = socket;
        this.scenes = [];
        this.channels = channels;
        
        // Setup the initial sceme
        let _channels = [];
        channels.forEach(x => {
            _channels.push({name: x.name, value: x.value});
        });
        this.scenes.push({beat: 0, channels: _channels});

        // Setup event listeners
        this.s_beat.forEach((x, i) => {
            x.addEventListener('click', () => {
                this.select_beat(i);
            });
        });

        // Handle server evemts
        this.socket.on('update', (data) => {
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

    select_beat(beat) {
        this.showBeat(beat)
    }

    save_scene() {
        // find the channels that has changed from previous beat
        const previousScene = this.scenes[this.scenes.length - 1];
        
        //FIXME: check if scene beat already exists 
        const currentScene = { beat: this.current, channels: [] };

        //FIXME: channel names are not stored properly
        this.channels.forEach((channel, index) => {
            if (previousScene.channels[index] && channel.value !== (previousScene.channels[index].value) ) {
                currentScene.channels.push({ name: channel.name, value: channel.value });
            }
        });

        // add/update the scenes array
        this.scenes.push(currentScene);
        console.log(this.scenes);

        // send the updated scene to the server

    }

    delete_scene() {   
        // remove the current scene from the scenes array

        // send the updated scene to the server
    }
}