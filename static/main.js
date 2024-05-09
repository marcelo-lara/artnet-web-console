var socket = io.connect(window.location.origin);
(function() {
    document.querySelectorAll('input.slider').forEach(function(x) {
        x.addEventListener('input', (e)=> {
            socket.emit('slider_change', {channel_id: e.target.name, value: e.target.value});
        });
    });
})();

// Song Chaser
var squares = document.querySelectorAll('#chaser-plan .beat');
var chaser_timeout = undefined;
var chaser = {
    bpm: 120,
    current: 0,
    _timeout: undefined,
    start: function() {
        this.movenext();
        var interval = (60000 / this.bpm); // Convert BPM to ms
        chaser_timeout = setInterval(() =>{
            this.movenext();
        }, interval);
    },
    stop: function() {
        clearInterval(chaser_timeout);
    },
    reset: function() {
        squares.forEach((x)=> {
            x.classList.remove('active');
        });
        this.current = 0;
    },
    movenext: function() {
        
        // show next square
        squares.forEach(x=>x.classList.remove('active'));
        squares[chaser.current].classList.add('active');

        // set next square
        this.current = (this.current + 1) % squares.length;
        if (this.current > squares.length) {this.current=0};

    }
}

var chaser_start_button = document.querySelector('#chaser-start');
var chaser_stop_button = document.querySelector('#chaser-stop');
var chaser_reset_button = document.querySelector('#chaser-reset');
chaser_start_button.addEventListener('click', ()=> {
    chaser.start();
});
chaser_stop_button.addEventListener('click', ()=> {
    chaser.stop();
});
chaser_reset_button.addEventListener('click', ()=> {
    chaser.reset();
});
