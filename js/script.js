function trocarPaginaPesquisa() {
        window.location.href = "tela_pesquisa.html";
    }


function trocarPaginaInicio() {
        window.location.href = "index.html";
    }

function trocarPaginaSobre() {
        window.location.href = "tela_sobre.html";
    }

document.addEventListener("DOMContentLoaded", function () {
  const alerta = document.getElementById("termos-alerta");
  const btnAceitar = document.getElementById("btnAceitarTermos");

  // Mostra o alerta sempre ao carregar a página
  alerta.style.display = "flex";

  // Quando o usuário clica em "Aceitar"
  btnAceitar.addEventListener("click", function () {
    alerta.style.display = "none"; // Oculta o alerta
  });
});