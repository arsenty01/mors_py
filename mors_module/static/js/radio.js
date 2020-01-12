var mountpoint = "/RH20499";
var mountpoint2 = "/nonstop";//нонстоп
var nac = true;
var counter=0;
var url = "http://s0.radioheart.ru:8000/json_new.xsl?"; //наш url к json в папке Web
var url2 = url;
url+= "mount=" + mountpoint + "&callback=";
url2+="mount=" + mountpoint2 + "&callback=";

function parseMusic(results)
{
    for  (var n in results){
        var nm = results[n];
        if(nm["title"] && nac){
            nac = false;
            $('#stream_name').text('Название станции: '+nm["name"]);
            $('#stream_description').text('Описание станции: '+nm["description"]);
            $('#stream_song').text('Сейчас в эфире: '+nm["title"]);
            $('#stream_listenters').text('Слушателей: '+nm["listeners"]);
        }
    }
}
var span;
var script;
$.ajaxSetup({ scriptCharset: "utf-8" , contentType: "application/json; charset=utf-8"});
function initMusic()
{
    span = document.createElement("span");
    span.id="getscript";
    document.body.appendChild(span);
    script  = document.createElement("script");
    script.type="text/javascript";
    script.charset="UTF-8";
}
function addMusic()
{
    nac = true;
    $('#getscript').empty();
    script.src = url + counter;
    $('#getscript').append(script);
    script.src = url2 + counter;
    $('#getscript').append(script);
}
function updateMusic()
{
    counter=counter+1;
    addMusic();
}

$(document).ready(
        function () {
            initMusic();
            addMusic();
            setInterval('updateMusic()', 30000 );
        });