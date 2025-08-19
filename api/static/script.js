function mostrarAba(id) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
    document.getElementById(id).classList.add('active');
    event.currentTarget.classList.add('active');
}

function copiarResultado(id) {
    const el = document.getElementById(id);
    let texto = '';
    if (el.tagName === 'DIV' || el.tagName === 'PRE') {
        texto = el.innerText;
    } else {
        texto = el.value;
    }
    navigator.clipboard.writeText(texto);
}
