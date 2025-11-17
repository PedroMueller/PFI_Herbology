$(document).ready(function () {
    var targetTabela = $('targetTabela')// destino onde os cards serão inseridos


    const $acesso = $("#acesso");
    const $painel = $("#painel");
    const $erro = $("#erro");



});

function carregarPlantas() {

    $.get("http://127.0.0.1:5000/plantas", function (data) {

        var targetTabela = $('targetTabela')
        console.log

        var items = data.data; // supondo que o retorno seja uma lista de objetos

        // Limpa tabela já existentes (se necessário)
        targetTabela.empty();

        console.log("Carregando plantas na tabela administrativa", items);

        // Para cada planta recebida
        $.each(items, function (index, value) {
            console.log(value);
                var elementoTabela = 
                `<tr>
                        <td>${value.id}</td>
                        <td>${value.nome_popular}</td>
                        <td>${value.nome_cientifico}</td>
                        <td>${value.descricao}</td>
                        <td>
                            <img src="${value.imagem_url || '../imgs/margarida_teste.png'}" alt="Planta">
                        </td>
                        <td>${value.imagem_url}</td>
                        <td class="actions">
                            <button class="btn-edit" onclick = "EditarPlanta(${value.id})">✏️ Editar </button>
                            <button class="btn-remove" onclick = "RemoverPlanta(${value.id})">🗑️ Remover</button>
                        </td>
                    </tr>
                    `;
            targetTabela.append(elementoTabela);
        });

    });
}



var senhaCorreta ="123"; 

function EntrarAdm() {
    const senha = document.getElementById("senha").value;
    console.log("Senha digitada:", senha); // para debug

    if (senha === senhaCorreta) {
        acesso.style.display = "none";
        painel.style.display = "block";
        carregarPlantas();
    } else {
        erro.style.display = "block";
    }
}

