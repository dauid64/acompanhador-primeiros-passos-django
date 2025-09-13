$(document).ready(function() {
    let comments = [];
    let commentIdCounter = 1;

    function generateAvatar(name) {
        return name.split(' ').map(word => word[0]).join('').substring(0, 2);
    }

    // Função para atualizar contador de comentários
    function updateCommentsCount() {
        const commentsCountText = $('#commentsCount').text();
        const commentsCount = parseInt(commentsCountText.replace(" comentários", "").replace(" comentário", "")) || 0;
        const totalComments = commentsCount + 1;
        
        $('#commentsCount').text(`${totalComments} ${totalComments === 1 ? 'comentário' : 'comentários'}`);
    }

    // Função para renderizar comentários
    function renderComments() {
        const $commentsList = $('#commentsList');

        let html = '';
        comments.forEach(comment => {
            html += `
                <div class="comment" data-comment-id="${comment.id}">
                    <div class="comment-header">
                        <div class="comment-avatar">${generateAvatar(comment.author)}</div>
                        <div class="comment-info">
                            <h4>${comment.author}</h4>
                            <span class="comment-date">${comment.date}</span>
                        </div>
                    </div>
                    <div class="comment-content">${comment.text}</div>
                    <div class="comment-actions">
                        <button class="btn btn-small btn-reply" data-comment-id="${comment.id}">Responder</button>
                    </div>
                    <div class="reply-form" id="replyForm-${comment.id}">
                        <div class="form-group">
                            <label for="replyAuthor-${comment.id}">Nome:</label>
                            <input type="text" id="replyAuthor-${comment.id}" required placeholder="Digite seu nome">
                        </div>
                        <div class="form-group">
                            <label for="replyText-${comment.id}">Resposta:</label>
                            <textarea id="replyText-${comment.id}" required placeholder="Escreva sua resposta..."></textarea>
                        </div>
                        <button class="btn btn-small btn-reply" onclick="submitReply(${comment.id})">Publicar Resposta</button>
                        <button type="button" class="btn btn-small btn-cancel" onclick="cancelReply(${comment.id})">Cancelar</button>
                    </div>
            `;

            if (comment.replies && comment.replies.length > 0) {
                html += '<div class="replies">';
                comment.replies.forEach(reply => {
                    html += `
                        <div class="reply">
                            <div class="comment-header">
                                <div class="comment-avatar">${generateAvatar(reply.author)}</div>
                                <div class="comment-info">
                                    <h4>${reply.author}</h4>
                                    <span class="comment-date">${reply.date}</span>
                                </div>
                            </div>
                            <div class="comment-content">${reply.text}</div>
                        </div>
                    `;
                });
                html += '</div>';
            }

            html += '</div>';
        });

        $commentsList.html(html);
        updateCommentsCount();
    }

    // Função para adicionar comentário
    function addComment(id, author, text, data) {
        const comment = {
            id: id,
            author: author,
            text: text,
            date: data,
            replies: []
        };
        comments.push(comment);
        renderComments();
    }

    // Função para adicionar resposta
    function addReply(commentId, author, text) {
        const comment = comments.find(c => c.id === commentId);
        if (comment) {
            const reply = {
                id: commentIdCounter++,
                author: author,
                text: text,
                date: new Date()
            };
            comment.replies.push(reply);
            renderComments();
        }
    }

    $('#commentForm').on('submit', async function(e) {
        e.preventDefault();
        const text = $('#id_body').val().trim();

        if (text) {
            try {
                const csrfToken = $("#commentForm input[name='csrfmiddlewaretoken']").val();
                const response = await fetch("/comentarios/create", {
                    method: "POST",
                    headers: {
                        "X-CSRFToken": csrfToken
                    },
                    body: new FormData(this)
                });
                if (response.ok) {
                    const data = await response.json();
                    addComment(data.id, data.nome_usuario, data.body, data.created_at);
                    $('#id_body').val('');
                } else {
                    console.log("Erro ao enviar comentário:", response.statusText);
                    alert("Erro ao enviar comentário. Tente novamente.");
                }
            } catch (error) {
                console.log("Erro ao enviar comentário:", error);
                alert("Erro ao enviar comentário. Tente novamente.");
            }
        }
    });

    // Função para submeter resposta
    window.submitReply = function(commentId) {
        const author = $(`#replyAuthor-${commentId}`).val().trim();
        const text = $(`#replyText-${commentId}`).val().trim();

        if (author && text) {
            addReply(commentId, author, text);
            $(`#replyAuthor-${commentId}`).val('');
            $(`#replyText-${commentId}`).val('');
            $(`#replyForm-${commentId}`).removeClass('active');
        }
    };

    // Função para cancelar resposta
    window.cancelReply = function(commentId) {
        $(`#replyAuthor-${commentId}`).val('');
        $(`#replyText-${commentId}`).val('');
        $(`#replyForm-${commentId}`).removeClass('active');
    };
})