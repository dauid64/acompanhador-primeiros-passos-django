// static/capitulos/js/comentarios.js
$(document).ready(function () {
  // Mantém sua leitura dos comentários iniciais (se houver)
  let comments = JSON.parse(document.getElementById('comentarios-data')?.textContent || '[]');

  // Util para avatar com iniciais (usa o nome do usuário)
  function generateAvatar(name) {
    if (!name) return '??';
    return name.split(' ').map(w => w[0]).join('').slice(0, 2).toUpperCase();
  }

  // Atualiza o contador (use só para COMENTÁRIOS raiz, não para respostas)
  function incrementCommentsCount() {
    const $el = $('#commentsCount');
    const txt = $el.text();
    const n = parseInt(txt.replace(' comentários','').replace(' comentário','')) || 0;
    const total = n + 1;
    $el.text(`${total} ${total === 1 ? 'comentário' : 'comentários'}`);
  }

  // ----- Envio de COMENTÁRIO raiz (já existia) -----
  $('#commentForm').on('submit', async function (e) {
    e.preventDefault();
    const btn = $('#commentForm button[type="submit"]');
    btn.prop('disabled', true);
    try {
      const text = $('#id_body').val().trim();
      if (!text) return;

      const csrfToken = $("#commentForm input[name='csrfmiddlewaretoken']").val();
      const resp = await fetch("/comentarios/create", {
        method: "POST",
        headers: { "X-CSRFToken": csrfToken },
        body: new FormData(this)
      });

      if (!resp.ok) throw new Error(resp.statusText);
      const data = await resp.json();

      // Renderiza no topo da lista
      const $list = $('#commentsList');
      const html = `
        <div class="comment" data-comment-id="${data.id}">
          <div class="comment-header">
            <div class="comment-avatar">${generateAvatar(data.nome_usuario)}</div>
            <div class="comment-info">
              <h4>${data.nome_usuario}</h4>
              <span class="comment-date">${data.created_at}</span>
            </div>
          </div>
          <div class="comment-content">${data.body}</div>
          <div class="comment-actions">
            <button type="button" class="btn btn-small btn-reply-toggle btn-secondary" data-comment-id="${data.id}">Responder</button>
          </div>
          <form class="reply-form" id="replyForm-${data.id}" style="display:none;">
            <input type="hidden" name="csrfmiddlewaretoken" value="${csrfToken}">
            <input type="hidden" name="exercicio" value="${$('#commentForm [name=exercicio]').val()}">
            <input type="hidden" name="parent" value="${data.id}">
            <div class="form-group">
              <label for="replyText-${data.id}">Resposta:</label>
              <textarea id="replyText-${data.id}" name="body" required placeholder="Escreva sua resposta..."></textarea>
            </div>
            <div class="buttons">
              <button type="submit" class="btn btn-small btn-primary">Publicar Resposta</button>
              <button type="button" class="btn btn-small btn-cancel-reply btn-secondary" data-comment-id="${data.id}">Cancelar</button>
            </div>
          </form>
          <div class="replies" id="replies-${data.id}"></div>
        </div>`;
      $list.prepend(html);

      $('#id_body').val('');
      incrementCommentsCount();
    } catch (err) {
      console.error("Erro ao enviar comentário:", err);
      alert("Erro ao enviar comentário. Tente novamente.");
    } finally {
      btn.prop('disabled', false);
    }
  });

  // ----- Mostrar/ocultar o formulário de resposta -----
  $(document).on('click', '.btn-reply-toggle', function () {
    const id = $(this).data('comment-id');
    const $form = $(`#replyForm-${id}`);
    $form.toggle(); // alterna mostrar/ocultar
    if ($form.is(':visible')) $form.find('textarea').focus();
  });

  $(document).on('click', '.btn-cancel-reply', function () {
    const id = $(this).data('comment-id');
    const $form = $(`#replyForm-${id}`);
    $form.find('textarea').val('');
    $form.hide();
  });

  // ----- Envio de RESPOSTA (delegação em cada form .reply-form) -----
  $(document).on('submit', '.reply-form', async function (e) {
    e.preventDefault();
    const $form = $(this);
    const btn = $form.find('button[type="submit"]');
    btn.prop('disabled', true);
    try {
      const body = $form.find('textarea[name="body"]').val().trim();
      if (!body) return;

      const resp = await fetch("/comentarios/create", {
        method: "POST",
        headers: { "X-CSRFToken": $form.find('input[name="csrfmiddlewaretoken"]').val() },
        body: new FormData(this)
      });
      if (!resp.ok) throw new Error(resp.statusText);
      const data = await resp.json();

      // Adiciona a resposta no container do pai
      const $replies = $(`#replies-${data.parent_id}`);
      const replyHtml = `
        <div class="reply">
          <div class="comment-header">
            <div class="comment-avatar">${generateAvatar(data.nome_usuario)}</div>
            <div class="comment-info">
              <h4>${data.nome_usuario}</h4>
              <span class="comment-date">${data.created_at}</span>
            </div>
          </div>
          <div class="comment-content">${data.body}</div>
        </div>`;
      $replies.append(replyHtml);

      // limpa/fecha o form
      $form.find('textarea[name="body"]').val('');
      $form.hide();
    } catch (err) {
      console.error("Erro ao enviar resposta:", err);
      alert("Erro ao enviar resposta. Tente novamente.");
    } finally {
      btn.prop('disabled', false);
    }
  });
});
