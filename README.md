# 🌿 Herbology

Website educacional sobre plantas medicinais brasileiras
Versão 1.0 • Desenvolvido por Pedro Henrique Roncatto Mueller – IFPR Campus Quedas do Iguaçu

---

## 📌 Sobre o Projeto

O **Herbology** é um website informacional desenvolvido para organizar e disponibilizar dados confiáveis sobre **plantas medicinais brasileiras**.
O sistema utiliza tecnologias web modernas e integra um banco de dados próprio, alimentado manualmente 

O objetivo principal é promover o uso consciente e educacional de plantas medicinais, oferecendo informações categorizadas, referências científicas e uma interface simples e intuitiva.

---

## 🛠️ Tecnologias Utilizadas

**Frontend:**

* HTML5
* CSS3
* JavaScript
* jQuery
* Bootstrap

**Backend:**

* Python
* Flask

**Banco de Dados:**

* MySQL

**Outros:**
* Figma (protótipos)

---

## 📂 Estrutura do Projeto

```
PFI_Herbology/
├── css/               # Estilos gerais do site
├── html/              # Páginas HTML (início, busca, planta, termos, admin, etc.)
├── imgs/              # Imagens complementares
├── js/                # Scripts JavaScript e jquery (busca, renderização, admin, alerts...)
├── python/            # Scripts Python (API, coneção com o banco de dados, controller)
├── svg/               # Ícones e elementos gráficos em SVG
├── .gitignore
└── README.md
```

---

## ⚙️ Instalação

### 1. Clone o repositório

```bash
git clone https://github.com/PedroMueller/PFI_Herbology.git
cd Herbology
```

### 2. Crie o ambiente virtual

```bash
python -m venv venv
```

Ative-o:

Windows:

```bash
venv\Scripts\activate
```

Linux/Mac:

```bash
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

### 4. Configure o banco de dados

1. Crie o banco:

```
CREATE DATABASE herbology;
```

2. Importe o arquivo `https://drive.google.com/drive/folders/1sF6c9bBu48WX0x8sipNRhxWHFD0hVvlM?usp=sharing` e realize a importação da base de dados
3. Ajuste as credenciais no arquivo `MySQLCRUD.py`:

```python
db = HerbologyDB(user="root", password="SUA_SENHA", database="herbology")
```

### 5. Execute o backend

```bash
python app.py
```

A aplicação estará disponível em:
**[http://127.0.0.1:5000/](http://127.0.0.1:5000/)**

---

## 🌱 Funcionalidades Principais

### 🔍 Busca de Plantas

* Busca por nome popular ou científico
* Filtros por categorias
* Resultados em tempo real

### 🌿 Página Individual da Planta

* Nome científico e popular
* Imagens
* Propriedades e usos medicinais
* Riscos e contraindicações
* Referências

### ⚙️ Modo Administrador

Como o sistema não possui login, o acesso administrativo é feito por uma rota interna protegida por senha.
Funções disponíveis:

* Cadastrar plantas
* Editar plantas
* Remover plantas


## ❗ Solução de Problemas

**Erro ao iniciar o servidor**
→ Verifique se todas as dependências foram instaladas.

**Banco não conecta**
→ Verifique usuário, senha e porta no MySQLCRUD.py.

**Imagens não carregam**
→ Confirme os caminhos na pasta `/imgs`.

---

## 📄 Licença

Projeto de caráter educacional desenvolvido no IFPR.
Licença: **MIT License** .

---

## 👤 Autor

**Pedro Henrique Roncatto Mueller**
IFPR – Campus Quedas do Iguaçu
Contato: [pedromuellerifpr@gmail.com](mailto:pedromuellerifpr@gmail.com)

---


# PFI_Herbology
Esse Projeto consiste em um Projeto Final Interdisciplinar do IFPR para finalização de curso 
Link para acesso do ducumento https://docs.google.com/document/d/1tB2rK7kYM2dZdBbX1WlCrDJ1694XJciWxAS6_52EsKc/edit?usp=sharing
