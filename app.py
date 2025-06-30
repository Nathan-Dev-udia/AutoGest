from flask import Flask, render_template, request
import sqlite3
import os
import pandas as pd
import json
import requests
import base64
import sys

sys.stdout.reconfigure(encoding='utf-8')
app = Flask(__name__)

def get_db_connection():
    caminho_db = os.path.join(os.path.dirname(__file__), 'dados', 'bateria2.db')
    return sqlite3.connect(caminho_db)

def get_carros(nome_pesquisa=None):
    conexao = get_db_connection()
    cursor = conexao.cursor()

    query = """
        SELECT c.nome, c.ano, b.amper, b.lado, b.cca, m.marca
        FROM carro c
        LEFT JOIN bateria b ON c.bateria = b.idbat
        LEFT JOIN modelo m ON c.idmarca = m.idmarca
    """

    params = ()
    if nome_pesquisa:
        query += " WHERE c.nome LIKE ?"
        params = ('%' + nome_pesquisa + '%',)

    cursor.execute(query, params)
    dados = cursor.fetchall()
    conexao.close()
    return dados

import base64

def renovar_token():
    with open('dados/bling_token.json') as f:
        tokens = json.load(f)
    with open('dados/bling_config.json') as f:
        config = json.load(f)

    payload = {
        "grant_type": "refresh_token",
        "refresh_token": tokens["refresh_token"]
    }

    basic = base64.b64encode(
        f"{config['client_id']}:{config['client_secret']}".encode()
    ).decode()
    headers = {
        "Content-Type": "application/x-www-form-urlencoded",
        "Authorization": f"Basic {basic}"
    }

    resp = requests.post("https://www.bling.com.br/Api/v3/oauth/token", data=payload, headers=headers)
    resp.raise_for_status()
    novo = resp.json()

    with open('dados/bling_token.json', 'w') as f:
        json.dump(novo, f, indent=4)

    return novo["access_token"]


@app.route('/bateria', methods=['GET', 'POST'])
def bateria():
    nome_pesquisa = request.args.get('nome')
    lista_carros = get_carros(nome_pesquisa)
    return render_template('bats.html', carros=lista_carros, pesquisa=nome_pesquisa or '')

@app.route('/atualizar_produtos')
def atualizar_produtos():
    try:
        with open('dados/bling_token.json', 'r', encoding='utf-8') as f:
            tokens = json.load(f)

        access_token = tokens.get('access_token')
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }

        marcas = ["Dmark", "Grid", "Moura", "Erbs", "Heliar"]
        todos_produtos = {}

        for marca in marcas:
            url = "https://www.bling.com.br/Api/v3/produtos"
            params = {
                "descricao": marca,
                "limit": 100
            }

            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 401:
                access_token = renovar_token()
                headers["Authorization"] = f"Bearer {access_token}"
                response = requests.get(url, headers=headers, params=params)

            response.raise_for_status()
            dados = response.json()

            produtos = dados.get("data", [])
            for p in produtos:
                produto = p.get("produto") or p
                id_produto = produto.get("id")
                if id_produto and id_produto not in todos_produtos:
                    todos_produtos[id_produto] = produto

        produtos_unicos = list(todos_produtos.values())

        with open('dados/produtos.json', 'w', encoding='utf-8') as f:
            json.dump(produtos_unicos, f, indent=4, ensure_ascii=False)

        print(f"🔢 Total de produtos únicos salvos: {len(produtos_unicos)}")

        return "✅ Produtos atualizados com sucesso!"

    except Exception as e:
        return f"❌ Erro ao atualizar produtos: {e}"
    
def atualizar_estoque_produto(id_produto, headers):
    url = f"https://www.bling.com.br/Api/v3/produtos/{id_produto}"
    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        access_token = renovar_token()
        headers["Authorization"] = f"Bearer {access_token}"
        response = requests.get(url, headers=headers)

    response.raise_for_status()
    dados = response.json()

    # Corrigido: pega do campo "data" → "estoque" → "saldoVirtualTotal"
    estoque = dados.get("data", {}).get("estoque", {}).get("saldoVirtualTotal", 0)
    return estoque


@app.route('/baterias/<amper>')
def listar_baterias_amperagem(amper):
    try:
        with open('dados/produtos.json', 'r', encoding='utf-8') as f:
            produtos = json.load(f)

        with open('dados/bling_token.json', 'r', encoding='utf-8') as f:
            tokens = json.load(f)

        access_token = tokens.get('access_token')
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Accept": "application/json"
        }

        marcas = ["Dmark", "Grid", "Moura", "Erbs", "Heliar"]
        baterias_filtradas = []

        for p in produtos:
            nome = p.get("nome", "").lower()
            preco = float(p.get("preco") or 0)
            id_produto = p.get("id")

            for marca in marcas:
                if marca.lower() in nome and amper.lower() in nome:
                    estoque_atual = atualizar_estoque_produto(id_produto, headers)
                    baterias_filtradas.append((p.get("nome", "Sem nome"), preco, estoque_atual))
                    break

        print(f"🔍 {len(baterias_filtradas)} baterias encontradas com {amper}A")

        return render_template(
            'baterias_amperagem.html',
            amper=amper,
            baterias=baterias_filtradas
        )

    except Exception as e:
        return f"Erro ao buscar baterias localmente: {e}"


# adquirir o Token de acesso
# @app.route('/callback')
# def callback():
#     code = request.args.get('code')

#     if not code:
#         return "❌ Código de autorização não encontrado na URL.", 400

#     try:
#         with open("dados/bling_config.json") as f:
#             config = json.load(f)

#         payload = {
#             "grant_type": "authorization_code",
#             "code": code,
#             "redirect_uri": config["redirect_uri"]
#         }

#         auth_str = f"{config['client_id']}:{config['client_secret']}"
#         auth_b64 = base64.b64encode(auth_str.encode()).decode()

#         headers = {
#             "Authorization": f"Basic {auth_b64}",
#             "Content-Type": "application/x-www-form-urlencoded"
#         }

#         url = "https://www.bling.com.br/Api/v3/oauth/token"
#         response = requests.post(url, data=payload, headers=headers)
#         response.raise_for_status()

#         token_data = response.json()

#         with open("dados/bling_token.json", "w") as f:
#             json.dump(token_data, f, indent=4)

#         return "<h3>✅ Token salvo com sucesso! Pode fechar essa aba.</h3>"

#     except Exception as e:
#         return f"<h3>❌ Erro ao obter token: {e}</h3>", 500

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/trel')
def trel():
    return render_template('trel.html')

@app.route('/dashboard')
def dashboard():
    # Define caminho fixo do CSV
    caminho = os.path.join(os.path.dirname(__file__), 'dados', 'vendas maio.csv')

    if not os.path.exists(caminho):
        return render_template('dashb.html', erro='Arquivo de relatório não encontrado.', vendas_por_vendedor=None)

    try:
        df = pd.read_csv(caminho, sep=';', encoding='latin1')
        df.columns = df.columns.str.strip().str.lower()

        if 'valor' not in df.columns or 'vendedor' not in df.columns:
            return render_template('dashb.html', erro=f'Colunas inválidas no CSV: {list(df.columns)}', vendas_por_vendedor=None)

        df['valor'] = df['valor'].replace('[R$]', '', regex=True)
        df['valor'] = df['valor'].str.replace('.', '', regex=False)
        df['valor'] = df['valor'].str.replace(',', '.', regex=False)
        df['valor'] = df['valor'].astype(float)

        if 'data' not in df.columns:
            return render_template('dashb.html', erro='A coluna "data" não foi encontrada no CSV.', vendas_por_vendedor=None)

        df['data'] = pd.to_datetime(df['data'], dayfirst=True, errors='coerce')
        df = df.dropna(subset=['data'])

        total = df['valor'].sum()
        melhor = df.groupby('vendedor')['valor'].sum().idxmax()
        vendas_por_vendedor = df.groupby('vendedor')['valor'].sum().to_dict()

        vendas_diarias = df.groupby(['data', 'vendedor'])['valor'].sum().unstack(fill_value=0)
        vendas_diarias_json = {
            'datas': vendas_diarias.index.strftime('%d/%m/%Y').tolist(),
            'vendedores': list(vendas_diarias.columns),
            'valores': vendas_diarias.to_dict(orient='list')
        }

        return render_template(
            'dashb.html',
            total=total,
            melhor=melhor,
            vendas_por_vendedor=vendas_por_vendedor,
            vendas_diarias_json=json.dumps(vendas_diarias_json)
        )

    except Exception as e:
        return render_template('dashb.html', erro=f'Erro ao ler CSV: {e}', vendas_por_vendedor=None)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)