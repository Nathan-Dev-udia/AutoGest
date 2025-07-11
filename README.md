# ⚙️ AutoGest
![Python](https://img.shields.io/badge/Python-3776AB?style=flat&logo=python&logoColor=white)
![Flask](https://img.shields.io/badge/Flask-000000?style=flat&logo=flask&logoColor=white)
![MySQL](https://img.shields.io/badge/MySQL-4479A1?style=flat&logo=mysql&logoColor=white)
![HTML5](https://img.shields.io/badge/HTML5-E34F26?style=flat&logo=html5&logoColor=white)
![CSS3](https://img.shields.io/badge/CSS3-1572B6?style=flat&logo=css3&logoColor=white)
![JavaScript](https://img.shields.io/badge/JavaScript-F7DF1E?style=flat&logo=javascript&logoColor=black)
![Chart.js](https://img.shields.io/badge/Chart.js-FF6384?style=flat&logo=chartdotjs&logoColor=white)

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
# 🔗 Integração com API do Bling

O Bling é um sistema ERP brasileiro muito usado por pequenas e médias empresas para gestão financeira, estoque, vendas, emissão de notas fiscais, entre outras funções.

No AutoGest, o vendedor pesquisa o modelo do carro desejado. O sistema exibe o nome do carro junto com a amperagem da bateria recomendada. Ao clicar na amperagem, o vendedor é levado a uma tela que mostra o estoque disponível e as opções de baterias daquela amperagem, consultadas em tempo real via integração com a API do Bling.

Isso facilita o processo de venda, pois permite consultar rapidamente a disponibilidade e preços das baterias, sem precisar sair do sistema, economizando tempo e evitando erros de informação.

Para detalhes técnicos da integração (autenticação OAuth, renovação de token, segurança e chamadas à API), consulte o arquivo [`bling_integration.md`](./bling_integration.md).

![Demonstração da integração com o Bling](static/imagens/01-AutoCar-Brave-2025-06-30-17-44-15.gif)
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

- Integração com a **API oficial do Bling**.
- Exibe:
  - Nome do produto;
  - Preço de venda;
  - Quantidade atual em estoque (saldo virtual total).

> A consulta ao estoque é feita em tempo real na API, mas só para os produtos filtrados (ex: baterias de 60A), garantindo mais performance.

---
# **🚀 Em breve**

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
## 📄 Documentação adicional

- [bling_integration.md](./bling_integration.md): Explicação detalhada sobre a integração com a API do Bling, incluindo autenticação OAuth, fluxo de atualização de produtos e boas práticas de segurança.
---
Você também pode acompanhar o andamento do projeto pela aba Projects!

> Desenvolvido com 💡, no meio de lançamentos, NFes, ligações de cliente e um caixa que nunca fecha — por Nathan Fernandes Alves.
