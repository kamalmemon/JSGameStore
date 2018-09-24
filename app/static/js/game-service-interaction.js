var iframeWin = document.getElementById("receiver").contentWindow;
var game_id = $("#receiver").data("game_id");

var send = function (data, url) {
    var request = new XMLHttpRequest();

    request.open("POST", url);
    request.onreadystatechange = function (event) {
        if (request.status !== 200) {
            console.log("Error posting:", request.statusText);
        }
        else if (request.response && request.response !== "OK") {
            if (request.readyState === 4) {
                iframeWin.postMessage(JSON.parse(request.response), "*");
            }
        }

        if (request.response && request.response === "OK" && data.messageType === "SCORE") {
            if (request.readyState === 4) {
                reloadHighScores();
            }
        }
    };
    request.setRequestHeader("Content-Type", "application/json");
    request.setRequestHeader("X-Requested-With", "XMLHttpRequest");
    request.setRequestHeader("X-CSRFToken", getCookie("csrftoken"));

    request.setRequestHeader("message-date", Date.now().toString());
    request.setRequestHeader("game-id", game_id);

    request.send(JSON.stringify(data));
};

var reloadHighScores = function () {
    $.ajax({
        "type": "POST",
        "dataType": "json",
        "url": highscore_retrieval_url,
        "data": {
            game_id: game_id,
            csrfmiddlewaretoken: getCookie("csrftoken")
        },
        "success": function (result) {
            var table_body = document.getElementById("hsTableBody");
            table_body.innerHTML = "";

            var html_str = "";
            for (var i = 0; i < result.length; i++) {
                html_str += "<tr>";
                html_str += "<th>" + result[i].username + "</th>";
                html_str += "<th>" + result[i].points + "</th>";
                html_str += "</tr>";
            }
            table_body.innerHTML = html_str;
        },
        "error": function (error) {
            console.log("g-s-i.js: Ajax error: ", error);
        }
    });
};

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        var cookies = document.cookie.split(";");
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

$(document).ready(function () {
    reloadHighScores();
    $(window).on("message", function (evt) {
        var data = evt.originalEvent.data;
        if (data.messageType === "SETTING") {
            $("#receiver").width(data.options.width);
            $("#receiver").height(data.options.height);
        }
        else {
            send(data, url);
        }
    });
});
