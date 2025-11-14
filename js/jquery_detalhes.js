$(document).ready(function () {


  // ============================
  // 1️⃣ Obter ID da planta pela URL
  // ============================
  const params = new URLSearchParams(window.location.search);
  const plantaId = params.get("id");

  if (!plantaId) {
    console.error("❌ Nenhum ID de planta encontrado na URL.");
    return;
  }

  // ============================
  // 2️⃣ Requisição AJAX à API
  // ============================
  $.get(`http://127.0.0.1:5000/detalhes/${plantaId}`, function (response) {
    if (response.status !== "ok" || !response.data) {
      console.error("❌ Erro ao carregar dados da planta:", response);
      return;
    }

    const planta = response.data;

    // ============================
    // 3️⃣ Preenchendo dados no HTML
    // ============================

    // Título
    $("main h2").text(planta.nome_popular);

    // Imagem
    $("main img.img-fluid").attr("src", planta.imagem_url || "/imgs/margarida_teste.png");

    // Nome científico
    $("main h4").html(`
      <img src="/imgs/icone_folha.png" alt="Ícone folha" width="20" class="me-2">
      ${planta.nome_popular} — <span class="text-muted">${planta.nome_cientifico}</span>
    `);

    // Descrição
    $("main p.mt-3").html(`
      <img src="/imgs/icone_info.png" alt="Ícone info" width="18" class="me-2">
      ${planta.descricao}
    `);

    // Categorias
    const categoria = planta.categorias && planta.categorias.length > 0
      ? planta.categorias.map(c => c.nome).join(", <br>")
      : "Não informado";

    // Métodos de uso (preparos)
    const preparos = planta.preparos && planta.preparos.length > 0
      ? planta.preparos.map(p => p.descricao).join("; ")
      : "Não informado";

    // Locais
    const local = planta.locais && planta.locais.length > 0
      ? `${planta.locais[0].regiao} — ${planta.locais[0].bioma}`
      : "Não informado";

    // Referências
    const referencias = planta.referencias && planta.referencias.length > 0
      ? planta.referencias.map(r => `<a href="${r.url}" target="_blank">${r.nome}</a>`).join("; ")
      : "Sem fontes";

    // Atualiza os textos
    $("main .col-md-6:nth-child(1) p:nth-child(1)").html(`<strong>Métodos de uso:</strong> ${preparos}`);
    $("main .col-md-6:nth-child(1) p:nth-child(2)").html(`<strong>Categoria:</strong> ${categoria}`);
    $("main .col-md-6:nth-child(2) p:nth-child(1)").html(`<strong>Local:</strong> ${local}`);
    $("main .col-md-6:nth-child(2) p:nth-child(2)").html(`<strong>Fonte:</strong> ${referencias}`);
  })
  .fail(function (xhr, status, error) {
    console.error("❌ Erro na requisição AJAX:", error);
  });
  
});


