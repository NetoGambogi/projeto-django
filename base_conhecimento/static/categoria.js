const createModal = document.getElementById('createModal');

if (createModal) {
    createModal.addEventListener('show.bs.modal', function (event) {
        const button = event.relatedTarget;
        const url = button.getAttribute('data-url');

        fetch(url)
            .then(response => response.text())
            .then(html => {
                createModal.querySelector('.modal-content').innerHTML = html;
            })
            .catch(err => {
                console.error("Erro ao carregar o formulário de criação:", err);
            });
    });
}