var targetSection = $('.card-menores'); // onde os resultados serão exibidos
var inputBusca = $('input[type="text"]'); // campo de busca
var plantas = []; // array para armazenar os resultados da busca


function renderizarResultados() {
    targetSection = $('.card-menores'); // onde os resultados serão exibidos
    console.log("Renderizando resultados:", plantas); // para debug
        targetSection.empty(); // limpa os resultados anteriores

        if (!plantas || plantas.length === 0) {
            targetSection.append('<p class="text-muted">Nenhuma planta encontrada.</p>');
            return;
        }

        $.each(plantas, function (index, value) {
            console.log("Renderizando planta:", value); // para debug
            var card = `
                <div class="card-menor"  >
                    <img src="${value.imagem_url || '../imgs/margarida_teste.png'}" alt="Planta">
                    <div class="info-card">
                        <h5>${value.nome_popular}</h5>
                        <p>${value.descricao || 'Sem descrição disponível.'}</p>
                        <button class="btn-card" onclick="trocarPaginaPlanta(${value.id})">Mais</button>
                    </div>
                </div>
            `;
            targetSection.append(card);
        });
    }

$(document).ready(function () {





    // ===============================
    // Função: renderizar os resultados na tela
    // ===============================
    
    
    // ===============================
    // Detectar texto digitado
    // ===============================
    // inputBusca.on('input', function () {
    //     var termo = $(this).val().trim();

    //     // só busca se tiver ao menos 2 caracteres
    //     if (termo.length >= 2) {
    //         buscarPlantas(termo);
    //     } else if (termo.length === 0) {
    //         targetSection.empty();
    //     }
    // });

    // ===============================
    // Verificar se há termo na URL ao carregar
    // ===============================
    var params = new URLSearchParams(window.location.search);
    var termoInicial = params.get('termo');
    if (termoInicial) {
        inputBusca.val(termoInicial);
        buscarPlantas(termoInicial);
    }



    
    });



function clickBusca() { 
        console.log("Botão de busca clicado");
        // Pega o valor digitado no campo de pesquisa
        const resBusca = document.getElementById("pesquisaPlanta").value;

        // Exibe o termo no console (para debug)
        console.log("Termo pesquisado:", resBusca);

        // Chama a função que faz a busca
        buscarPlantas(resBusca);
    }
// Reutiliza as funções já existentes no sistema
function trocarPaginaPlanta(id) {
    window.location.href = `tela_planta.html?id=${id}`;
}



// ===============================
    // Função: buscar plantas na API
    // ===============================
    function buscarPlantas(termo) {
        var url = `http://127.0.0.1:5000/busca_planta?termo=${termo}`;

        // Atualiza o link na barra de endereços
        window.history.replaceState({}, '', `?termo=${termo}`);

        $.get(url, function (data) {
            console.log("Resposta da API:", data); // para debug
            if (data.status === "ok") {
                console.log("Passou no IF status ok");
                console.log(data.data);
                plantas = data.data; // atualiza o array de plantas
                renderizarResultados(data.data);
            } else {
                console.log("Erro retornado pela API: ESLE", data.message);
                targetSection.html(`<p class="text-danger">Erro: ${data.message}</p>`);
            }
        }).fail(function () {
            targetSection.html('<p class="text-danger">Erro ao conectar à API.</p>');
        });
    }
