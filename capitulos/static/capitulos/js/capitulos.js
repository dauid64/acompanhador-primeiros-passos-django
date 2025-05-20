$(".change-dificuldade").on("click", function () {
    const ratingTd = $(this).closest(".rating-dificuldade");
    const infoDiv = ratingTd.find(".info");

    const url = infoDiv.data("url");

    const inputId = $(this).attr("for");
    const dificuldade = parseInt($("#" + inputId).val());
    const csrfToken = $("input[name='csrfmiddlewaretoken']").val();

    const data = new FormData();
    data.append("dificuldade", dificuldade);

    $.ajax({
        type: "POST",
        url: url,
        data: data,
        processData: false,
        contentType: false,
        dataType: "json",
        headers: {
            "X-CSRFToken": csrfToken,
        },
        success: function (response) {
            ratingTd.find("label i").each(function (index) {
                if (index <= dificuldade) {
                    $(this).addClass("checked");
                } else {
                    $(this).removeClass("checked");
                }
            });
        },
        error: function (xhr, status, error) {
            alert("Erro ao enviar a dificuldade. Tente novamente mais tarde.");
        },
    });
});

$(".change-nota").on("click", function () {
    const ratingTd = $(this).closest(".rating-nota");
    const infoDiv = ratingTd.find(".info");

    const url = infoDiv.data("url");

    const inputId = $(this).attr("for");
    const nota = parseInt($("#" + inputId).val());
    const csrfToken = $("input[name='csrfmiddlewaretoken']").val();

    const data = new FormData();
    data.append("nota", nota);

    $.ajax({
        type: "POST",
        url: url,
        data: data,
        processData: false,
        contentType: false,
        dataType: "json",
        headers: {
            "X-CSRFToken": csrfToken,
        },
        success: function (response) {
            ratingTd.find("label i").each(function (index) {
                if (index <= nota) {
                    $(this).addClass("checked");
                } else {
                    $(this).removeClass("checked");
                }
            });
        },
        error: function (xhr, status, error) {
            alert("Erro ao enviar a dificuldade. Tente novamente mais tarde.");
        },
    });
});

