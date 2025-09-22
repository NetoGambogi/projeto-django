const editModal = document.getElementById('editModal');

if (editModal) {
  editModal.addEventListener('show.bs.modal', function (event) {
    const button = event.relatedTarget;
    const url = button.getAttribute('data-url');

    fetch(url)
      .then(response => response.text())
      .then(html => {
        editModal.querySelector('.modal-content').innerHTML = html;
      })
      .catch(err => {
        console.error("Erro ao carregar o formulário de edição:", err);
      });
  });
}
