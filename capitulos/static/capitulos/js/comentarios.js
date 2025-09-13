$(document).ready(function() {
    let comments = [];
    let commentIdCounter = 1;

    // Função para formatar data
    function formatDate(date) {
        const options = { 
            year: 'numeric', 
            month: 'long', 
            day: 'numeric',
            hour: '2-digit',
            minute: '2-digit'
        };
        return date.toLocaleDateString('pt-BR', options);
    }

    
})