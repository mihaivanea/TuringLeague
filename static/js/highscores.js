var usersUrl = "/leaderboards/users"
var botsUrl = "/leaderboards/bots"

$(document).ready(function() {
    if ($("#bot-leaderboards").length) {
        fetchDatabase(botsUrl);
    }

    if ($("#user-leaderboards").length) {
        fetchDatabase(usersUrl);
    }
});

function fetchDatabase(url) {
    var res = httpGet(url);
    var db = JSON.parse(res);
    var bot = url === botsUrl;

    var num = db['score'].length;
    if (num > 10) {
        num = 10;
    }

    for (var i = 0; i < num; i++) {
        if (bot) {
            addRecord(i+1, db['bot_name'][i], db['score'][i], bot);
        } else {
            addRecord(i+1, db['user_name'][i], db['score'][i], bot);
        }
    }
}

function addRecord(rank, name, points, bot) {
    var id = "";
    if (rank === 1) {
        id = 'id = "score-first"';
    } else if (rank === 2) {
        id = 'id = "score-second"';
    } else if (rank === 3) {
        id = 'id = "score-third"';
    } 

    var template = ' <div class="row score-row"' + id + '> <div class="col-xs-1 score-rank text-center"> ' + rank + ' </div> <div class="col-xs-10 score-name"> ' + name + ' </div> <div class="col-xs-1 score-points"> ' + points + ' </div> </div> '
    if (bot) {
        $("#bot-leaderboards").append(template);
    } else {
        $("#user-leaderboards").append(template);
    }
}

function httpGet(url)
{
    var xmlHttp = new XMLHttpRequest();
    xmlHttp.open( "GET", url, false );
    xmlHttp.send( null );
    return xmlHttp.responseText;
}
