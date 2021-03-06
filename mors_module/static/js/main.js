$(document).ready(function ($) {
    //Variables
    let socket = io.connect('http://' + document.domain + ':' + location.port + '/');
    console.log(document.domain)
    console.log(location.port)
    let radioStatus = false;
    let radioSound = false;

    //Elements
    let chat = $('#cr-body');
    let schedule = $('#tt-body');
    let form = $('#chat');
    let body = $('body');
    let playing = $('#player-on-air');
    let playing_timing = $('#player-timing');

    //Buttons
    let play = $('.play');
    let login_btn = $('#login-btn');

    //Fields
    let author = $('.name');
    let message = $('.msg');
    let broadcast = $('.special-date');

    function reset_chat_scroll() {
        chat.scrollTop(chat[0].scrollHeight);
    }

    function now_playing() {
        socket.emit('cp_request');
    }

    reset_chat_scroll();
    now_playing();
    broadcast.change(function() {
        socket.emit('refresh_schedule', broadcast.find(':selected').text());
    });

    //Actions

    form.submit(function(event) {
        if ((message.val() !== '') && (author.val() !== '')) {
            socket.emit('sent_message', {
                text: message.val(),
                author: author.val()
            });

            message.val('');
        }
        return false;
    });

    play.click({}, function () {
        if(radioStatus) {
            document.getElementById('radio').pause();
            play.text('Слушать эфир');
            radioStatus = false;
        } else {
            document.getElementById('radio').play();
            play.text('Пауза');
            radioStatus = true;
        }
    });

    login_btn.click({}, function () {

    });

    //Listeners
    socket.on('messages_list', function (messages) {
        chat.empty();
        messages = messages.messages;
        for (let i = messages.length-1; i >= 0; i--) {
            chat.append(
                '<div class="message"><div class="author">'+messages[i]['author']+'</div><div class="time">'+messages[i]['timestamp']+'</div>'+messages[i]['text']+'</div>'
            )
        }
        chat.scrollTop(chat[0].scrollHeight)
    });

    socket.on('new_message', function (message) {
        chat.prepend(
            '<div class="message"><div class="author">'+message['author']+'</div><div class="time">'+message['timestamp']+'</div>'+message['text']+'</div>'
        );
        reset_chat_scroll();
    });

    socket.on('cp_response', function (program) {
        playing.empty();
        playing.text(program.title);
        playing_timing.empty();
        playing_timing.text(program.time);
    });

    socket.on('new_schedule', function(new_schedule) {
        schedule.empty();

        if (new_schedule.length > 0) {
            for (let i=0; i < new_schedule.length; i++) {
                schedule.append(
                    '<div class="schedule"><div class="time">'+new_schedule[i].time+'</div><div class="details"><div class="program">'+new_schedule[i].title+'</div><div class="guests">'+new_schedule[i].hosts+'</div></div></div>'
                );
            };
        } else {
            schedule.append(
                '<h3>Расписание отсутствует</h3>'
            );
        };
    });
});
