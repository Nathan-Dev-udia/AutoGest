from flask import Flask, render_template, request
import sqlite3
import os
import pandas as pd
import json

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

@app.route('/bateria', methods=['GET', 'POST'])
def bateria():
    nome_pesquisa = request.args.get('nome')
    lista_carros = get_carros(nome_pesquisa)
    return render_template('bats.html', carros=lista_carros, pesquisa=nome_pesquisa or '')

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