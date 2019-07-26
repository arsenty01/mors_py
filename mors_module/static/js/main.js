$(document).ready(function ($) {
    $('#cr-body').scrollTop($('#cr-body')[0].scrollHeight)
    let radioStatus = false;
    let radioSound = false;
    let curVolume = 0.5;

    $('.play').click({}, function () {
        if(radioStatus) {
            document.getElementById('radio').pause();
            $('.play').text('Слушать эфир');
            radioStatus = false;
        } else {
            document.getElementById('radio').play();
            document.getElementById('radio').volume = curVolume;
            $('.play').text('Пауза');
            radioStatus = true;
        }
    });


    /*  */
    let socket = io.connect('http://' + document.domain + ':' + location.port + '/');
    socket.on('messages_list', function (messages) {
        console.log(messages);
        $('#cr-body').empty();
        messages = messages.messages;
        for (let i = messages.length-1; i >= 0; i--) {
            $('#cr-body').append(
                '<div class="message"><div class="author">'+messages[i]['author']+'</div><div class="time">'+messages[i]['timestamp']+'</div>'+messages[i]['text']+'</div>'
            )
        }
        $('#cr-body').scrollTop($('#cr-body')[0].scrollHeight)
    });
    socket.on('new_message', function (message) {
        console.log(message);
        $('#cr-body').append(
            '<div class="message"><div class="author">'+message['author']+'</div><div class="time">'+message['timestamp']+'</div>'+message['text']+'</div>'
        )
        $('#cr-body').scrollTop($('#cr-body')[0].scrollHeight)
    });
    $('#chat').submit(function(event) {
        if (($('.msg').val() != '') & ($('.name').val() != '')) {
            socket.emit('sent_message', {text: $('.msg').val(), author: $('.name').val()});
            $('.msg').val('');
        }
        return false;
    });

});