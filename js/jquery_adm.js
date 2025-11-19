$(document).ready(function () {
    var targetTabela = $('targetTabela')// destino onde os cards serão inseridos


    const $acesso = $("#acesso");
    const $painel = $("#painel");
    const $erro = $("#erro");



});

function carregarPlantas() {

    $.get("http://127.0.0.1:5000/plantas", function (data) {

        var targetTabela = $('#targetTabela')
        
        console.log("ttttttttttttttttttttttttttttttttttttttttttttttttttttttttttt",targetTabela)

        var items = data.data; // supondo que o retorno seja uma lista de objetos

        // Limpa tabela já existentes (se necessário)
        targetTabela.empty();
        $("#targetTabela").append("<span>New content at the end</span>");

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
                            <img src="${value.imagem_url || '../imgs/margarida_teste.png'}" alt="Planta" class="img-plant">
                        </td>
                        <td>${value.imagem_url}</td>
                        <td class="actions">
                            <button class="btn-edit" onclick = "EditarPlanta(${value.id})">✏️ Editar </button>
                            <button class="btn-remove" onclick = "RemoverPlanta(${value.id})">🗑️ Remover</button>
                        </td>
                    </tr>
                    `;
            targetTabela.append(elementoTabela);
            console.log(targetTabela)
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
        console.log("Carregando plantas para o administrador.");

        carregarPlantas();
        console.log("Acesso concedido ao painel administrativo.");
    } else {
        erro.style.display = "block";
    }
}

function AdicionarPlanta() {

    if (!confirm("Deseja adicionar uma nova planta?")) {
        return;
    }

    // Remove qualquer formulário anterior
    $("#form-dinamico").remove();

    // Cria formulário dinâmico
    var form =
        `<div id="form-dinamico" class="form-popup">
            <h3>Adicionar Nova Planta</h3>

            <label>Nome Popular:</label>
            <input type="text" id="add_nome_popular">

            <label>Nome Científico:</label>
            <input type="text" id="add_nome_cientifico">

            <label>Descrição:</label>
            <textarea id="add_descricao"></textarea>

            <label>URL da Imagem:</label>
            <input type="text" id="add_imagem_url">

            <button id="btnSalvarAdd">Salvar</button>
        </div>`;

    $("#painel").append(form);

    // Evento salvar
    $("#btnSalvarAdd").on("click", function () {

        const dados = {
            nome_popular: $("#add_nome_popular").val(),
            nome_cientifico: $("#add_nome_cientifico").val(),
            descricao: $("#add_descricao").val(),
            imagem_url: $("#add_imagem_url").val()
        };
        print("Dados a serem enviados:", dados);

        // Envio ao backend
        fetch("http://127.0.0.1:5000/plantas/adm/add", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(dados)
        })
        .then(r => r.json())
        .then(resp => {
            if (resp.status === "success") {
                print()
                alert("Planta adicionada com sucesso!");
                $("#form-dinamico").remove();
                carregarPlantas();
            } else {
                alert("Erro ao adicionar planta.");
            }
        })
        .catch(() => alert("Erro de comunicação com o servidor."));
    });
}
function EditarPlanta(id) {

    if (!confirm(`Deseja editar a planta de ID ${id}?`)) {
        return;
    }

    // Primeiro, buscar dados atuais
    fetch(`http://127.0.0.1:5000/plantas/adm/update/${id}`)
        .then(r => r.json())
        .then(planta => {

            $("#form-dinamico").remove();

            var form =
                `<div id="form-dinamico" class="form-popup">
                    <h3>Editar Planta (ID ${id})</h3>

                    <label>Nome Popular:</label>
                    <input type="text" id="edit_nome_popular" value="${planta.nome_popular}">

                    <label>Nome Científico:</label>
                    <input type="text" id="edit_nome_cientifico" value="${planta.nome_cientifico}">

                    <label>Descrição:</label>
                    <textarea id="edit_descricao">${planta.descricao}</textarea>

                    <label>URL da Imagem:</label>
                    <input type="text" id="edit_imagem_url" value="${planta.imagem_url}">

                    <button id="btnSalvarEdit">Salvar alterações</button>
                </div>`;

            $("#painel").append(form);

            // Botão salvar
            $("#btnSalvarEdit").on("click", function () {

                const dadosEdit = {
                    nome_popular: $("#edit_nome_popular").val(),
                    nome_cientifico: $("#edit_nome_cientifico").val(),
                    descricao: $("#edit_descricao").val(),
                    imagem_url: $("#edit_imagem_url").val()
                };

                fetch(`http://127.0.0.1:5000/plantas/adm/update/${id}`, {
                    method: "PUT",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify(dadosEdit)
                })
                .then(r => r.json())
                .then(resp => {
                    if (resp.status === "success") {
                        alert("Planta atualizada!");
                        $("#form-dinamico").remove();
                        carregarPlantas();
                    } else {
                        alert("Erro ao atualizar planta.");
                    }
                })
                .catch(() => alert("Erro de comunicação com o servidor."));
            });

        });
}


function RemoverPlanta(id) {

    if (!confirm(`Tem certeza que deseja remover a planta ID ${id}?`)) {
        
        return;
    }

    fetch(`http://127.0.0.1:5000//plantas/adm/delete/${id}`, {
        method: "DELETE"
    })
    .then(r => r.json())
    .then(resp => {

        if (resp.status === "success") {
            alert("Planta removida.");
            carregarPlantas(); // atualiza tabela
        } else {
            alert("Erro ao remover planta.");
        }
    })
    .catch(() => alert("Erro de comunicação com o servidor."));
}
