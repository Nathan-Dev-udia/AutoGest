# Integração com API do Bling
Este documento explica o funcionamento da integração da aplicação AutoGest com a API do Bling para consulta e atualização de produtos, estoque e token de acesso.
---
## Visão geral da integração
A aplicação usa a API REST do Bling para obter informações de produtos, preços e estoque em tempo real.

O acesso é autenticado via OAuth 2.0, utilizando um access_token que deve ser renovado periodicamente via refresh_token.

Os dados são armazenados localmente em arquivos JSON (produtos.json e bling_token.json) para uso rápido e evitar chamadas desnecessárias.
---
## Como funciona a autenticação
Inicialmente, o token é obtido manualmente (pode ser via rota /callback comentada no código).

O bling_token.json guarda:

**access_token:** token temporário usado nas requisições.

**refresh_token:** usado para renovar o access_token sem nova autenticação do usuário.

Outras informações do token (expiração, escopo, etc.).

A função renovar_token() lê os tokens atuais e as configurações (client_id, client_secret e redirect_uri no arquivo bling_config.json), e faz a requisição para renovar o access_token automaticamente quando o token expira (erro 401 na API).
---
## Fluxo de atualização dos produtos

A rota `/atualizar_produtos` busca produtos de marcas específicas na API do Bling e salva os dados básicos (como nome e preço) de todos esses produtos no arquivo `produtos.json`. Essa atualização é feita em lote e não inclui a atualização do estoque.

Já a atualização do **estoque** dos produtos é feita sob demanda, ou seja, somente para os produtos que o usuário pesquisa.

Por exemplo, ao acessar `/baterias/<amper>`, o sistema filtra os produtos no `produtos.json` pela amperagem desejada e, **apenas para esses produtos filtrados**, faz chamadas à API para obter o estoque atualizado em tempo real.

Dessa forma, o sistema evita fazer muitas chamadas à API, economiza recursos e mantém a resposta rápida, consultando o estoque somente quando necessário.
---
## Consulta e filtro de baterias
A rota /baterias/<amper> filtra os produtos carregados em produtos.json pela amperagem e marcas pré-definidas.

Para cada produto filtrado, é feita uma chamada à API para obter o estoque atualizado usando a função atualizar_estoque_produto().

Essa função também renova o token caso necessário, garantindo que a consulta seja sempre válida.
---
## Considerações sobre segurança
Arquivos JSON:
Os arquivos bling_token.json e bling_config.json contêm informações sensíveis (tokens, client_id, client_secret).

Nunca envie esses arquivos para repositórios públicos sem removê-los ou protegê-los.

Para colaborar ou publicar, use .gitignore para ignorá-los ou utilize variáveis de ambiente.

Uso do sys.stdout.reconfigure(encoding='utf-8'):
No início do código, essa linha força o padrão de saída do terminal para UTF-8, garantindo que caracteres especiais sejam exibidos corretamente, especialmente no Windows.

Isso evita erros ou problemas ao imprimir logs que contenham caracteres acentuados ou emojis.
---
## Recomendações para uso e manutenção
Manter tokens atualizados: Sempre rode o processo de autenticação inicial (rota /callback) para gerar o primeiro token. Depois, o sistema renova automaticamente.

Backup dos arquivos JSON: Como os dados são armazenados localmente, faça backups regulares para evitar perda de dados.

Limitar chamadas à API: Sempre que possível, utilize os dados armazenados localmente (produtos.json) para melhorar a performance e diminuir chamadas à API.

Configurar corretamente o bling_config.json: Esse arquivo deve conter os dados corretos da aplicação no Bling (client_id, client_secret, redirect_uri).

Evitar exposição pública dos tokens: Tokens podem dar acesso aos dados da sua conta Bling. Trate-os com cuidado.
---
## Código relevante e trechos úteis
### Renovação automática do token:
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
### Chamada à API para obter produtos e atualizar estoque:
def atualizar_estoque_produto(id_produto, headers):
    url = f"https://www.bling.com.br/Api/v3/produtos/{id_produto}"
    response = requests.get(url, headers=headers)

    if response.status_code == 401:
        access_token = renovar_token()
        headers["Authorization"] = f"Bearer {access_token}"
        response = requests.get(url, headers=headers)

    response.raise_for_status()
    dados = response.json()
    estoque = dados.get("data", {}).get("estoque", {}).get("saldoVirtualTotal", 0)
    return estoque
