$(document).ready(function () {
    $('.progress-bar').each(function () {
        const progress = parseFloat($(this).data('progress')); // converte para float
        if (!isNaN(progress)) {
        $(this).find('.progress').css('width', progress + '%');
        }
    });
});