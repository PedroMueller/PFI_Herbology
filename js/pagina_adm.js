document.addEventListener("DOMContentLoaded", () => {
  const senhaCorreta = "123"; // pode ser movida para o backend
  const acesso = document.getElementById("acesso");
  const painel = document.getElementById("painel");
  const erro = document.getElementById("erro");

  document.getElementById("entrar").addEventListener("click", () => {
    const senha = document.getElementById("senha").value;
    if (senha === senhaCorreta) {
      acesso.style.display = "none";
      painel.style.display = "block";
      carregarPlantas();
    } else {
      erro.style.display = "block";
    }
  });

  // Função para carregar plantas no select
  async function carregarPlantas() {
    const resp = await fetch("/api/plantas");
    const plantas = await resp.json();
    const selectEditar = document.getElementById("selectEditar");
    const selectRemover = document.getElementById("selectRemover");

    selectEditar.innerHTML = "";
    selectRemover.innerHTML = "";
    plantas.forEach(p => {
      const opt = new Option(p.nome_popular, p.id);
      selectEditar.add(opt.cloneNode(true));
      selectRemover.add(opt);
    });
  }

  // Adicionar planta
  document.getElementById("formAdd").addEventListener("submit", async (e) => {
    e.preventDefault();
    const dados = Object.fromEntries(new FormData(e.target).entries());
    const resp = await fetch("/api/add_planta", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(dados)
    });
    const msg = await resp.text();
    document.getElementById("mensagem").textContent = msg;
    carregarPlantas();
  });

  // Editar planta
  document.getElementById("formEdit").addEventListener("submit", async (e) => {
    e.preventDefault();
    const id = document.getElementById("selectEditar").value;
    const dados = Object.fromEntries(new FormData(e.target).entries());
    const resp = await fetch(`/api/update_planta/${id}`, {
      method: "PUT",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(dados)
    });
    const msg = await resp.text();
    document.getElementById("mensagem").textContent = msg;
    carregarPlantas();
  });

  // Remover planta
  document.getElementById("btnRemover").addEventListener("click", async () => {
    const id = document.getElementById("selectRemover").value;
    if (!id) return;
    if (!confirm("Tem certeza que deseja remover esta planta?")) return;

    const resp = await fetch(`/api/delete_planta/${id}`, { method: "DELETE" });
    const msg = await resp.text();
    document.getElementById("mensagem").textContent = msg;
    carregarPlantas();
  });
});
