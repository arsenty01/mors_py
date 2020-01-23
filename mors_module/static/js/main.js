$(document).ready(function ($) {
    //Variables
    let socket = io.connect('http://' + document.domain + ':' + location.port + '/');
    let radioStatus = false;
    let radioSound = false;

    //Elements
    let chat = $('#cr-body');
    let form = $('#chat');
    let body = $('body');

    //Buttons
    let play = $('.play');
    let login_btn = $('#login-btn');

    //Fields
    let author = $('.name');
    let message = $('.msg');

    function reset_chat_scroll() {
        chat.scrollTop(chat[0].scrollHeight);
    }

    reset_chat_scroll();

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
        console.log(messages);
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
        console.log(message);
        chat.prepend(
            '<div class="message"><div class="author">'+message['author']+'</div><div class="time">'+message['timestamp']+'</div>'+message['text']+'</div>'
        );
        reset_chat_scroll();
    });

});