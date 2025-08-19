function mostrarAba(id) {
    document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
    document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
    document.getElementById(id).classList.add('active');
    event.currentTarget.classList.add('active');
}

function copiarResultado(id, botao) {
    const el = document.getElementById(id);
    let texto = '';

    if (el.tagName === 'DIV' || el.tagName === 'PRE') {
        texto = el.innerText;
    } else {
        texto = el.value;
    }

    navigator.clipboard.writeText(texto).then(() => {
        // muda o botão para verde
        botao.classList.add("copied");
        botao.innerText = "Copiado!";

        // volta ao normal depois de 2s
        setTimeout(() => {
            botao.classList.remove("copied");
            botao.innerText = "Copiar";
        }, 2000);
    });
}
