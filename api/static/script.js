function copiarResultado(id) {
    const box = document.getElementById(id);
    const btn = box.previousElementSibling;

    navigator.clipboard.writeText(box.textContent).then(() => {
        btn.classList.add("copied");
        btn.textContent = "Copiado!";
        setTimeout(() => {
            btn.classList.remove("copied");
            btn.textContent = "Copiar";
        }, 2000);
    });
}

function copiarJSON() {
    try {
        const texto = JSON.stringify(editor.get(), null, 2);
        navigator.clipboard.writeText(texto).then(() => {
            const btn = document.querySelector(".btn-copiar-json");
            btn.classList.add("copied");
            btn.textContent = "Copiado!";
            setTimeout(() => {
                btn.classList.remove("copied");
                btn.textContent = "Copiar";
            }, 2000);
        });
    } catch (e) {
        document.getElementById("json-error").textContent = "Erro ao copiar: " + e.message;
    }
}
