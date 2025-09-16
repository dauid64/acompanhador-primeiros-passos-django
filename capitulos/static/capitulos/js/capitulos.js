$(".change-dificuldade").on("click", function () {
    const ratingContainer = $(this).closest(".rating-dificuldade");
    const infoDiv = ratingContainer.find(".info");
    const url = infoDiv.data("url");
    const inputId = $(this).attr("for");
    const dificuldade = parseInt($("#" + inputId).val());
    const csrfToken = $("input[name='csrfmiddlewaretoken']").val();

    // Adicionar estado de loading
    ratingContainer.addClass("loading");
    
    // Atualizar texto imediatamente para feedback visual
    const ratingTexts = ["Muito Fácil", "Fácil", "Médio", "Difícil", "Muito Difícil"];
    const ratingText = ratingContainer.find(".rating-text");
    if (ratingText.length) {
        ratingText.text(ratingTexts[dificuldade] || "Não avaliado");
    }

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
            // Atualizar estrelas (versão legacy)
            ratingContainer.find("label i").each(function (index) {
                if (index <= dificuldade) {
                    $(this).addClass("checked");
                } else {
                    $(this).removeClass("checked");
                }
            });
            
            // Atualizar estrelas (versão moderna)
            ratingContainer.find(".star-icon").each(function (index) {
                if (index <= dificuldade) {
                    $(this).addClass("checked");
                } else {
                    $(this).removeClass("checked");
                }
            });
            
            // Remover loading e adicionar feedback de sucesso
            ratingContainer.removeClass("loading").addClass("success");
            setTimeout(() => {
                ratingContainer.removeClass("success");
            }, 600);
        },
        error: function (xhr, status, error) {
            console.error("Erro ao enviar dificuldade:", error);
            ratingContainer.removeClass("loading");
            
            // Mostrar notificação moderna ao invés de alert
            showNotification("Erro ao salvar dificuldade. Tente novamente.", "error");
        },
    });
});

$(".change-nota").on("click", function () {
    const ratingContainer = $(this).closest(".rating-nota");
    const infoDiv = ratingContainer.find(".info");
    const url = infoDiv.data("url");
    const inputId = $(this).attr("for");
    const nota = parseInt($("#" + inputId).val());
    const csrfToken = $("input[name='csrfmiddlewaretoken']").val();

    // Adicionar estado de loading
    ratingContainer.addClass("loading");
    
    // Atualizar texto imediatamente para feedback visual
    const ratingTexts = ["Não gostei", "Pouco interessante", "Interessante", "Muito bom", "Amei!"];
    const ratingText = ratingContainer.find(".rating-text");
    if (ratingText.length) {
        ratingText.text(ratingTexts[nota] || "Não avaliado");
    }

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
            // Atualizar corações (versão legacy)
            ratingContainer.find("label i").each(function (index) {
                if (index <= nota) {
                    $(this).addClass("checked");
                } else {
                    $(this).removeClass("checked");
                }
            });
            
            // Atualizar corações (versão moderna)
            ratingContainer.find(".heart-icon").each(function (index) {
                if (index <= nota) {
                    $(this).addClass("checked");
                } else {
                    $(this).removeClass("checked");
                }
            });
            
            // Remover loading e adicionar feedback de sucesso
            ratingContainer.removeClass("loading").addClass("success");
            setTimeout(() => {
                ratingContainer.removeClass("success");
            }, 600);
        },
        error: function (xhr, status, error) {
            console.error("Erro ao enviar nota:", error);
            ratingContainer.removeClass("loading");
            
            // Mostrar notificação moderna ao invés de alert
            showNotification("Erro ao salvar avaliação. Tente novamente.", "error");
        },
    });
});

$('.change-feito').on("click", function () {
    const checkbox = $(this);
    const checkboxContainer = checkbox.closest('.container-checkbox, .modern-checkbox');
    const exerciseRow = checkbox.closest('.exercise-row');
    const infoDiv = checkboxContainer.find('.info');
    const url = infoDiv.data("url");
    const feito = this.checked;
    const csrfToken = $("input[name='csrfmiddlewaretoken']").val();

    // Adicionar estado de loading
    checkboxContainer.addClass("loading");
    exerciseRow.addClass("updating");
    
    // Atualizar label do checkbox moderno
    const checkboxLabel = checkboxContainer.find('.checkbox-label');
    if (checkboxLabel.length) {
        checkboxLabel.text(feito ? "Feito" : "Pendente");
    }
    
    // Atualizar atributo data-completed da linha
    exerciseRow.attr('data-completed', feito ? 'true' : 'false');

    const data = new FormData();
    data.append("feito", feito);

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
            // Remover estados de loading
            checkboxContainer.removeClass("loading").addClass("success");
            exerciseRow.removeClass("updating");
            
            // Atualizar badge de conclusão
            const completionBadge = exerciseRow.find('.completion-badge');
            if (feito && completionBadge.length === 0) {
                // Adicionar badge se não existir
                const badgeHtml = `
                    <div class="completion-badge">
                        <svg class="badge-icon" viewBox="0 0 24 24" width="12" height="12">
                            <path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>
                        </svg>
                        Concluído
                    </div>
                `;
                exerciseRow.find('.exercise-details').append(badgeHtml);
            } else if (!feito && completionBadge.length > 0) {
                // Remover badge se existir
                completionBadge.remove();
            }
            
            // Feedback de sucesso
            setTimeout(() => {
                checkboxContainer.removeClass("success");
            }, 600);
            
            // Mostrar notificação de sucesso
            showNotification(
                feito ? "Exercício marcado como concluído!" : "Exercício desmarcado como concluído.",
                "success"
            );
        },
        error: function (xhr, status, error) {
            console.error("Erro ao enviar status de conclusão:", error);
            
            // Reverter o estado do checkbox
            checkbox.prop('checked', !feito);
            exerciseRow.attr('data-completed', feito ? 'false' : 'true');
            
            // Remover loading
            checkboxContainer.removeClass("loading");
            exerciseRow.removeClass("updating");
            
            // Reverter label
            if (checkboxLabel.length) {
                checkboxLabel.text(!feito ? "Feito" : "Pendente");
            }
            
            // Mostrar notificação de erro
            showNotification("Erro ao salvar status. Tente novamente.", "error");
        },
    });
});

// Função para mostrar notificações modernas
function showNotification(message, type = 'info') {
    // Remover notificação existente se houver
    $('.modern-notification').remove();
    
    const iconMap = {
        success: '<path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/>',
        error: '<path d="M19 6.41L17.59 5 12 10.59 6.41 5 5 6.41 10.59 12 5 17.59 6.41 19 12 13.41 17.59 19 19 17.59 13.41 12z"/>',
        info: '<path d="M13,9H11V7H13M13,17H11V11H13M12,2A10,10 0 0,0 2,12A10,10 0 0,0 12,22A10,10 0 0,0 22,12A10,10 0 0,0 12,2Z"/>'
    };
    
    const colorMap = {
        success: '#27ae60',
        error: '#e74c3c',
        info: '#3498db'
    };
    
    const notification = $(`
        <div class="modern-notification modern-notification-${type}" style="
            position: fixed;
            top: 20px;
            right: 20px;
            background: white;
            color: ${colorMap[type]};
            padding: 1rem 1.5rem;
            border-radius: 12px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.15);
            border-left: 4px solid ${colorMap[type]};
            display: flex;
            align-items: center;
            gap: 0.8rem;
            z-index: 10000;
            transform: translateX(100%);
            transition: transform 0.3s ease;
            max-width: 350px;
            font-weight: 500;
        ">
            <svg width="20" height="20" viewBox="0 0 24 24" fill="${colorMap[type]}">
                ${iconMap[type]}
            </svg>
            <span>${message}</span>
        </div>
    `);
    
    $('body').append(notification);
    
    // Animar entrada
    setTimeout(() => {
        notification.css('transform', 'translateX(0)');
    }, 100);
    
    // Auto remover
    setTimeout(() => {
        notification.css('transform', 'translateX(100%)');
        setTimeout(() => {
            notification.remove();
        }, 300);
    }, 3000);
}

// Inicialização quando o documento estiver pronto
$(document).ready(function() {
    // Adicionar tooltips aos elementos de rating
    $('.star-label, .heart-label').each(function() {
        const title = $(this).attr('title');
        if (title) {
            $(this).attr('data-tooltip', title);
        }
    });
    
    // Melhorar acessibilidade
    $('.star-label, .heart-label').on('keydown', function(e) {
        if (e.key === 'Enter' || e.key === ' ') {
            e.preventDefault();
            $(this).click();
        }
    });
    
    // Adicionar indicadores de carregamento para AJAX
    $(document).ajaxStart(function() {
        $('body').addClass('ajax-loading');
    }).ajaxStop(function() {
        $('body').removeClass('ajax-loading');
    });
    
    console.log('Sistema de capítulos modernizado inicializado com sucesso! 🚀');
});