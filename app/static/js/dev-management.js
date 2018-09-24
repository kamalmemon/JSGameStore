$(document).ready(function () {
    $(".remove-game-button").each(function () {
        $(this).on("click", function () {
            var r = confirm("Are you sure?");
            if (r === true) {
                window.location.href = delete_urls[$(this).attr("id")];
            }
        });
    });
});
