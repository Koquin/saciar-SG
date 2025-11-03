# utils/api_utils.py
from pymongo import MongoClient
from bson.objectid import ObjectId
import datetime
import hashlib
import requests

# Conexão com o MongoDB local
client = MongoClient("mongodb://localhost:27017/")
db = client["gerenciamento_clientes"]
collection_clients = db["clientes"]
collection_purchases = db["compras"] 
collection_prizes = db["premios"]
BASE_URL = "http://localhost:8000"  

# ----------------- Funções de AUTENTICAÇÃO (MongoDB) -----------------


# ----------------- Funções CRUD - CLIENTES (MongoDB) -----------------

def get_clients():
    print("No api_utils, metodo get_clients")
    try:
        request = requests.get(f"{BASE_URL}/clientes")
        if request.status_code == 200:
            print("Clientes buscados com sucesso!")
            return request.json()
        else:
            return []
    except Exception as e:
        print("Erro na requisição de clientes:", e)
        return []


def search_clients(query: str):
    print("No api_utils, metodo search_clients, variaveis: ", query)
    try:
        params = {"q": query} if query else {}
        response = requests.get(f"{BASE_URL}/clientes/search", params=params)
        response.raise_for_status()
        clients = response.json()
        print(f"Clientes buscados com sucesso via API! Total: {len(clients)}")
        return clients
    except requests.exceptions.RequestException as e:
        print("Erro ao buscar clientes via API:", e)
        return []


def post_client(client):
    print("No api_utils, metodo post_client, variaveis: ", client)
    try:
        novo_cliente = {
            "nome": client.get("nome", ""),
            "cpf": client.get("cpf", ""),
            "telefone": client.get("telefone", ""),
            "pontos": client.get("pontos", 0)
        }

        cliente = requests.post(f"{BASE_URL}/clientes", json=novo_cliente)
        if cliente.status_code == 201:
            print("Cliente cadastrado com sucesso via API!")
            return cliente.json()
        else:
            return None
    except Exception as e:
        print("Erro na requisição de cadastro de cliente via API:", e)
        return None


def put_client(client):
    """Atualiza dados de um cliente pelo CPF"""
    try:
        cpf = client.get("cpf")
        if not cpf:
            print("CPF é obrigatório para atualizar.")
            return None
        
        update_data = {k: v for k, v in client.items() if k != 'cpf'}
        
        result = collection_clients.update_one({"cpf": cpf}, {"$set": update_data})
        if result.modified_count > 0:
            print("Cliente atualizado com sucesso!")
        
        return client
    except Exception as e:
        print("Erro ao atualizar cliente:", e)
        return None


def delete_client(id):
    print("No api_utils, metodo delete_client, variaveis: ", id)
    try:
        result = requests.delete(f"{BASE_URL}/clientes/{id}")
        print("Resultado da deleção via API:", result.status_code)
        if result.status_code == 204:
            print("Cliente deletado com sucesso via API!")
            return True
        else:
            return False
    except Exception as e:
        print("Erro ao deletar cliente:", e)
        return 0

# ----------------- Funções CRUD - COMPRAS (MongoDB) -----------------

def get_purchases():
    """Busca todos os históricos de compras"""
    try:
        purchases = list(collection_purchases.find({}, {"_id": 0}))
        return purchases
    except Exception as e:
        print("Erro ao buscar compras:", e)
        return []

# --- NOVA FUNÇÃO DE BUSCA PARA COMPRAS ---
def search_purchases(query):
    """Busca compras por nome do cliente, CPF ou data usando regex (insensível a caixa)."""
    if not query:
        return get_purchases()
        
    try:
        regex_pattern = {"$regex": query, "$options": "i"}
        
        filter_query = {
            "$or": [
                {"cliente": regex_pattern},
                {"cpf": regex_pattern},
                {"data": regex_pattern}
            ]
        }
        
        purchases = list(collection_purchases.find(filter_query, {"_id": 0}))
        return purchases
    except Exception as e:
        print("Erro ao buscar compras:", e)
        return []

def post_purchase(purchase):
    """
    Cadastra uma nova compra. Permite compra avulsa, implementa o limite de 10 pontos.
    """
    cpf = purchase.get("cpf", "").strip() 
    valor = purchase.get("valor", 0.0)
    is_delivery = purchase.get("is_delivery", False)
    
    cliente_encontrado = None
    cliente_nome = "Cliente Avulso"
    pontos_ganhos = 0
    MAX_PONTOS_ACUMULADOS = 10
    
    # 1. VERIFICAÇÃO CONDICIONAL DO CLIENTE
    if cpf:
        cliente_encontrado = collection_clients.find_one({"cpf": cpf})
        
        if cliente_encontrado:
            cliente_nome = cliente_encontrado.get("nome", "Desconhecido")
            pontos_atuais = cliente_encontrado.get("pontos", 0)
            
            # --- LÓGICA DE LIMITE DE PONTOS ---
            if pontos_atuais >= MAX_PONTOS_ACUMULADOS:
                pontos_ganhos = 0
                print(f"Cliente {cliente_nome} (CPF: {cpf}) já atingiu {MAX_PONTOS_ACUMULADOS} pontos. Sem novos pontos ganhos.")
            else:
                pontos_a_somar_raw = int(valor // 15)
                espaco_disponivel = MAX_PONTOS_ACUMULADOS - pontos_atuais
                pontos_ganhos = min(pontos_a_somar_raw, espaco_disponivel)
                
            
            # 3. ATUALIZA A PONTUAÇÃO DO CLIENTE NO DB (SOMENTE SE HOUVE GANHO)
            if pontos_ganhos > 0:
                novo_total_pontos = pontos_atuais + pontos_ganhos
                
                try:
                    collection_clients.update_one(
                        {"cpf": cpf},
                        {"$set": {"pontos": novo_total_pontos}}
                    )
                except Exception as e:
                    print("Erro ao atualizar pontos do cliente:", e)
            
        else:
            # CPF fornecido, mas não existe no cadastro.
            cliente_nome = f"CPF NÃO CADASTRADO ({cpf})"
            pontos_ganhos = 0
            
    data_hora_agora = datetime.datetime.now()

    # 4. Prepara e insere o registro da compra (SEMPRE SALVA AQUI)
    nova_compra = {
        "cliente": cliente_nome,
        "cpf": cpf or "AVULSO", 
        "valor": valor,
        "is_delivery": is_delivery,
        "pontos_ganhos": pontos_ganhos,
        "data": data_hora_agora.strftime("%Y-%m-%d %H:%M:%S")            
    }
    
    try:
        collection_purchases.insert_one(nova_compra)
        return nova_compra
    except Exception as e:
        print("Erro ao cadastrar compra:", e)
        return None

def put_purchase(purchase_id, new_data):
    """Atualiza dados de uma compra (não implementado, retorna None)"""
    return None 

def delete_purchase(cpf, data):
    """Remove uma compra específica pelo CPF e Data (para fins didáticos)"""
    try:
        result = collection_purchases.delete_one({"cpf": cpf, "data": data})
        return result.deleted_count
    except Exception as e:
        print("Erro ao deletar compra:", e)
        return 0

# ----------------- Funções CRUD - PRÊMIOS (MongoDB) -----------------

def get_prizes():
    try:
        prizes = list(collection_prizes.find({}, {"_id": 0}))
        
        if not prizes:
             return [
                 {"pontos": 3, "premio": "Desconto de 10%"},
                 {"pontos": 6, "premio": "Desconto de 30%"},
                 {"pontos": 8, "premio": "Desconto de 50%"},
                 {"pontos": 10, "premio": "Açái gratis"}
             ]
        
        return prizes
    except Exception as e:
        print("Erro ao buscar prêmios:", e)
        return []


def update_prizes(prizes_list: list):
    print("NO update_prizes, api_utils")
    try:
        collection_prizes.delete_many({})
        
        if prizes_list:
            print(f"Inserindo {len(prizes_list)} prêmios na coleção.")
            collection_prizes.insert_many(prizes_list)
        
        print(f"Prêmios atualizados com sucesso! Total de {len(prizes_list)} prêmios.")
        
        return True
    
    except Exception as e:
        print("Erro ao atualizar prêmios:", e)
        return False