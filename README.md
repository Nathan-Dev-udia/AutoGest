# ⚙️ AutoGest

**AutoGest** é um sistema completo de apoio à gestão de autocenters, oficinas e lojas de baterias.  
Desenvolvido com **Flask e SQLite**, ele centraliza funcionalidades como:

- 🔋 Consulta de baterias por modelo de carro (com visual aprimorado);
- 📦 Consulta de estoque, preço e produtos em tempo real via **API do Bling**;
- 📊 Dashboard interativo de vendas (leitura de CSV);
- 🧱 Cards de acesso rápido aos sites mais usados;
- 🌙 Interface responsiva com modo escuro e visual limpo.

---

## 🔧 Tecnologias utilizadas

- **Python 3**
- **Flask**
- **SQLite**
- **HTML/CSS/JS**
- **Pandas** (leitura e tratamento de dados CSV)
- **Chart.js** (gráficos dinâmicos e responsivos)
- **Requests** (integração com API do Bling)

---

## 📁 Estrutura do Projeto

```plaintext
AutoGest/
├── static/
│   ├── css/
│   │   └── bat.css, dashh.css, estoque.css, oleo.css, style.css, trelo.css
│   ├── imagens/
│   │   └── logo.png, bling.jpg, mourafacil.png, Fundo-Brutus.png, etc.
│   └── js/
│       └── dashboard.js, sidebar.js
├── templates/
│   └── index.html, dashb.html, bats.html, baterias_amperagem.html, trel.html
├── dados/
│   └── bateria2.db, oleeos.db, kanban.db, vendas maio.csv, produtos.json
├── app.py
└── README.md
```
---
# 🧠 Como funciona
## 🔋 Consulta de Baterias

- O usuário digita o nome do carro e, ao pesquisar, o sistema retorna:
  - Marca do carro;
  - Ano;
  - Amperagem da bateria correspondente;
  - CCA e lado de borne.

Essas informações são consultadas diretamente de um banco de dados SQLite.

## 📊 Dashboard de Vendas

- O sistema lê um arquivo `.csv` com as vendas e exibe:
  - Total vendido;
  - Melhor vendedor;
  - Gráfico de barras (vendas por vendedor);
  - Gráfico de pizza (distribuição proporcional);
  - Gráfico de linha (vendas diárias por vendedor).

Com os gráficos, é possível **selecionar os vendedores** que você deseja visualizar. Assim, dá pra comparar o desempenho entre eles.
Os gráficos são gerados com **Chart.js**, com suporte responsivo e interativo (incluindo uma linha pontilhada que acompanha o cursor no gráfico de linha).
Essa função foi escolhida como uma solução alternativa ao Power BI por oferecer mais liberdade visual, animações modernas, e integração direta com o front-end — sem depender de ferramentas externas ou licenças pagas para apresentações formais.

## 📦 Estoque e Produtos em Tempo Real (via Bling)

- Integração com **API oficial do Bling**.

- Exibe:
  - Nome do produto;
  - Preço de venda;
  - Quantidade atual em estoque.

---
# **🚀 Em breve**

- 📦 API do Bling: exibição de produtos, estoque e preço de venda em tempo real;
- 🔐 Autenticação de usuários (login e permissões);
- 🛢 Consulta de óleo por modelo de carro;
- 🧰 Consulta de filtros (ar, óleo e gasolina) por modelo de carro;
- 📈 Machine Learning para previsões e projeções de vendas (baseado no histórico do CSV);
- 📌 Projeto Kanban embutido para organização interna.

---
# ▶️ Como rodar o projeto

1. Execute o arquivo Flask: `app.py`
2. Acesse no seu navegador o endereço:
   - http://127.0.0.1:5000 *(localhost)*
   - Ou o endereço exibido no terminal (segure `Ctrl` e clique para abrir)

Se quiser acessar em outro dispositivo na mesma rede, utilize o IP local (ex: `http://10.0.0.27:5000`).

*Requisitos:*

Instale os pacotes principais com:
pip install flask pandas

Se for usar recursos futuros, também instale:
pip install requests scikit-learn matplotlib

---
Você também pode acompanhar o andamento do projeto pela aba Projects!

> Feito por Nathan Fernandes Alves — para facilitar os processos dos autocenters e gestão local.

