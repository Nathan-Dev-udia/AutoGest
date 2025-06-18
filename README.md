***AutoGest***

AutoGest é um sistema de apoio à gestão de autocenters, oficinas e lojas de baterias. Desenvolvido com Flask e SQLite, ele centraliza funcionalidades como:

- Consulta de baterias por modelo de carro;
- Dashboard interativo de vendas (CSV);
- Modo escuro com interface responsiva;
- Integração planejada com API do Bling;
- Projeto Kanban/Trello embutido para organização interna;

---

🔧 Tecnologias utilizadas

- **Python 3**
- **Flask**
- **SQLite**
- **HTML/CSS/JS**
- **Pandas** (leitura e processamento de CSV)
- **API Bling** (em desenvolvimento)

---

📁 Estrutura do Projeto

AutoGest/
├── static/
│ └── css/,
       └──bat.css, dashh.css, oleo.css, style.css, trelo.css
      imagens/,
       └──bling.jpg, Fundo-Brutus.png, hostingerim.png, logo.png, mourafacil.png, rolemar.png
      js/
       └──dashboard.js, sidebar.js
├── templates/
│ └── index.html, dashb.html, bats.html, trel.html
├── dados/
│ └── bateria2.db, oleeos.db, kanban.db, vendas maio.csv
├── app.py
└── README.md

---

**🚀 Em breve**

- 📦 API do Bling: consulta de produtos, estoque e pedidos em tempo real;
- 🔐 Autenticação de usuários (login e permissões);
- 📈 Machine Learning para previsões e projeções de vendas (baseado no histórico do CSV).

---
▶️ Como rodar o projeto

-Execute o arquivo Flask app.py;
-Acesse no seu navegador o endereço: http://127.0.0.1:5000. Para demais dispositivos dentro da mesma rede: http://10.0.0.27:5000.

Requisitos:
flask;
pandas.

Obs: Dependendo das futuras funcionalidades (como API ou Machine Learning), adicione também:
requests;
scikit-learn;
matplotlib.

---
Você também pode acomapanhar o andamento do projeto pela aba Projects!

> Feito por Nathan Fernandes Alves — para facilitar os processos dos autocenters e gestão local.

