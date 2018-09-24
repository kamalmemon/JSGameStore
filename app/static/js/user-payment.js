$(document).ready(function () {
    $("[id^=Buy]").each(function () {
        var each_game_id = $(this).data("game_id");
        $(this).on("click", function () {
            $.ajax({
                "type": "POST",
                "dataType": "json",
                "url": buy_url,
                "data": {
                    game_id: each_game_id,
                    csrfmiddlewaretoken: getCookie("csrftoken")
                },
                "success": function (result) {
                    $("#checksum" + each_game_id).val(result.checksum);
                    $("#pid" + each_game_id).val(result.pid);
                    $("#sid" + each_game_id).val(result.sid);
                    $("#amount" + each_game_id).val(result.amount);

                    $("#form" + each_game_id).submit();
                },
                "error": function (error) {
                    console.log("Ajax error: ", error);
                }
            });
        });
    });
});

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
