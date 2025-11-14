$(document).ready(function () {
    var targetSection = $('.card-menores'); // destino onde os cards serão inseridos
    var principalPlanta = $('.cardMaior'); // destino onde os cards serão inseridos

    // Requisição ao backend Flask
    $.get("http://127.0.0.1:5000/plantas", function (data) {

        //const array = [1, 2, 3, 4, 5];
        //const lastElement = array[array.length - 1];


        var items = data.data; // supondo que o retorno seja uma lista de objetos
        var ultimo = items[items.length - 1];
        items.pop(); // remove o último elemento do array     
        
        
        
        // console.log(items); se precisar printar no console

        // Limpa cards já existentes (se necessário)
        targetSection.empty();
        principalPlanta.empty();

        // Adiciona o card maior
        var cardMaior = `
            <div class="row g-0 align-items-center">
                <div class="col-md-2 text-center">
            <img src= "${ultimo.imagem_url || '../imgs/margarida_teste.png'}" class="img-fluid rounded" alt="Imagem da planta principal">
            </div>
            <div class="col-md-10">
            <div class="card-body">
                <h3 class="card-title">${ultimo.nome_popular}</h3>
                <p class="card-text">${ultimo.descricao}</p>
                <button class="btn-card" onclick="trocarPaginaPlanta(${ultimo.id})" >Mais</button>
            </div>
            </div>
        </div>`;
        principalPlanta.append(cardMaior);
        
        
        

        // Para cada planta recebida
        $.each(items, function (index, value) {
            console.log(value);
            // Aqui assumo que cada "value" é um objeto {nome, resumo, imagem}
            var card = `
                <div class="card-menor">
                    <img src="${value.imagem_url || '../imgs/margarida_teste.png'}" alt="Planta">
                    <div class="info-card">
                        <h5>${value.nome_popular}</h5>
                        <p>${value.descricao}</p>                     
                        <button class="btn-card" onclick="trocarPaginaPlanta(${value.id})" >Mais</button>
                    </div>
                </div>
            `;
            targetSection.append(card);
        });
    });


});

    function trocarPaginaPlanta(id) {
        window.location.href = `tela_planta.html?id=${id}`;
    }

    
    // ===============================

    // FAZER UM JS QUE VAI CARREGAR OS DADOS DA PLANTA NA PÁGINA DE DETALHES
    //PARA CARREGAR OS DETALHES DA PLANTA TEM QUE PERGA O ID DA URL E BUSCAR OS DADOS EM UMA NOOOOOOOVVVVVVVVAAA API (/DETALHES?id=1)
    // no python fazer um /datelhes que vai na base de dados e faz as parad tudo




